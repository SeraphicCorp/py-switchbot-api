"""Tools to query the SwitchBot API."""

import base64
from dataclasses import dataclass
from enum import Enum
import hashlib
import hmac
import logging
import socket
import time
from typing import Any, TypeVar
import uuid

from aiohttp import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST

from switchbot_api.exceptions import (
    SwitchBotAuthenticationError,
    SwitchBotConnectionError,
    SwitchBotDeviceOfflineError,
)

_API_HOST = "https://api.switch-bot.com"

_LOGGER = logging.getLogger(__name__)
NON_OBSERVED_REMOTE_TYPES = ["Others"]


@dataclass
class Device:
    """Device."""

    device_id: str
    device_name: str
    device_type: str
    hub_device_id: str

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""
        self.device_id = kwargs["deviceId"]
        self.device_name = kwargs["deviceName"]
        self.device_type = kwargs.get("deviceType", "-")
        self.hub_device_id = kwargs["hubDeviceId"]


@dataclass
class Remote:
    """Remote device."""

    device_id: str
    device_name: str
    device_type: str
    hub_device_id: str

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""
        self.device_id = kwargs["deviceId"]
        self.device_name = kwargs["deviceName"]
        self.device_type = kwargs.get("remoteType", "-")
        self.hub_device_id = kwargs["hubDeviceId"]


class PowerState(Enum):
    """Power state."""

    ON = "on"
    OFF = "off"


class Commands(Enum):
    """Base command class."""


class CommonCommands(Commands):
    """Common commands."""

    ON = "turnOn"
    OFF = "turnOff"


class OthersCommands(Commands):
    """Others commands."""

    CUSTOMIZE = "customize"  # Command {user-defined button name}


class AirConditionerCommands(Commands):
    """Air conditioner commands."""

    SET_ALL = "setAll"  # parameter: {temperature},{mode},{fan speed},{power state}


class HumidifierCommands(Commands):
    """Humidifier commands."""

    SET_MODE = "setMode"  # parameter: auto, set to Auto Mode, 101, set atomization efficiency to 34%,102, set atomization efficiency to 67%, 103, set atomization efficiency to 100%


class TVCommands(Commands):
    """TV commands."""

    SET_CHANNEL = "SetChannel"
    VOLUME_ADD = "volumeAdd"
    VOLUME_SUB = "volumeSub"
    CHANNEL_ADD = "channelAdd"
    CHANNEL_SUB = "channelSub"


class DVDCommands(Commands):
    """DVD commands."""

    SET_MUTE = "setMute"
    FAST_FORWARD = "FastForward"
    REWIND = "Rewind"
    NEXT = "Next"
    PREVIOUS = "Previous"
    PAUSE = "Pause"
    PLAY = "Play"
    STOP = "Stop"


class SpeakerCommands(Commands):
    """Speaker commands."""

    VOLUME_ADD = "volumeAdd"
    VOLUME_SUB = "volumeSub"


class FanCommands(Commands):
    """Fan commands."""

    SWING = "swing"
    TIMER = "timer"
    LOW_SPEED = "lowSpeed"
    MIDDLE_SPEED = "middleSpeed"
    HIGH_SPEED = "highSpeed"


class LightCommands(Commands):
    """Light commands."""

    BRIGHTNESS_UP = "brightnessUp"
    BRIGHTNESS_DOWN = "brightnessDown"


class LockCommands(Commands):
    """Lock commands."""

    LOCK = "lock"
    UNLOCK = "unlock"


class CeilingLightCommands(Commands):
    """Ceiling light commands."""

    # 1-100
    SET_BRIGHTNESS = "setBrightness"
    # 2700-6500
    SET_COLOR_TEMPERATURE = "setColorTemperature"


class VacuumCommands(Commands):
    """Vacuum commands."""

    START = "start"
    STOP = "stop"
    DOCK = "dock"
    POW_LEVEL = "PowLevel"


class BotCommands(Commands):
    """Bot commands."""

    PRESS = "press"


T = TypeVar("T", bound=CommonCommands)


class SwitchBotAPI:
    """SwitchBot API."""

    def __init__(self, token: str, secret: str) -> None:
        """Initialize."""
        self.token = token
        self.secret = secret

    def make_headers(self, token: str, secret: str) -> dict[str, Any]:
        """Make headers."""
        nonce = uuid.uuid4()
        timestamp = int(round(time.time() * 1000))
        string_to_sign = bytes(f"{token}{timestamp}{nonce}", "utf-8")
        secret_bytes = bytes(secret, "utf-8")

        sign = base64.b64encode(
            hmac.new(
                secret_bytes, msg=string_to_sign, digestmod=hashlib.sha256
            ).digest()
        )

        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "charset": "utf8",
            "t": str(timestamp),
            "sign": str(sign, "utf-8"),
            "nonce": str(nonce),
        }

    async def _request(
        self, method: str, path: str, json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        async with ClientSession() as session:
            try:
                response = await session.request(
                    method,
                    f"{_API_HOST}/v1.1/{path}",
                    headers=self.make_headers(self.token, self.secret),
                    json=json,
                )
            except (
                ClientError,
                ClientResponseError,
                socket.gaierror,
            ) as exception:
                msg = "Error occurred while communicating with the SwitchBot API"
                raise SwitchBotConnectionError(msg) from exception
            if response.status == 403:
                raise SwitchBotAuthenticationError()

            body = await response.json()

            if response.status >= 400:
                _LOGGER.error("Error %d: %s", response.status, body)
                raise SwitchBotConnectionError()

            match body.get("statusCode"):
                case 100:
                    return body["body"]  # type: ignore
                case 161 | 171:
                    # SwitchBot docs claim that 161 is the code for device
                    # being offline, and 171 for a _hub_ being offline.
                    # In testing, the Plug Mini (JP) return 171 when not
                    # online too.
                    raise SwitchBotDeviceOfflineError()
                case _:
                    _LOGGER.error("Error %d: %s", response.status, body)
                    raise SwitchBotConnectionError()

    async def list_devices(self) -> list[Device | Remote]:
        """List devices."""
        body = await self._request(METH_GET, "devices")
        _LOGGER.debug("Devices: %s", body)
        devices = [Device(**device) for device in body.get("deviceList")]  # type: ignore
        remotes = [
            Remote(**remote)
            for remote in body.get("infraredRemoteList")  # type: ignore
            if remote.get("remoteType") not in NON_OBSERVED_REMOTE_TYPES
        ]
        return [*devices, *remotes]

    async def get_status(self, device_id: str) -> dict[str, Any]:
        """No status for IR devices."""
        body = await self._request(METH_GET, f"devices/{device_id}/status")
        return body

    async def get_webook_configuration(self) -> dict[str, Any]:
        """List webhooks."""
        json = {"action": "queryUrl"}
        return await self._request(METH_POST, "webhook/queryWebhook", json=json)

    async def setup_webhook(self, url: str) -> None:
        """Set up webhook to receive device status updates."""
        json = {"deviceList": "ALL", "action": "setupWebhook", "url": url}
        await self._request(METH_POST, "webhook/setupWebhook", json=json)

    async def delete_webhook(self, url: str) -> None:
        """Delete webhook."""
        json = {"action": "deleteWebhook", "url": url}
        await self._request(METH_POST, "webhook/deleteWebhook", json=json)

    async def send_command(
        self,
        device_id: str,
        command: T | str,
        command_type: str = "command",
        parameters: dict | str = "default",  # type: ignore
    ) -> None:
        """Send command to device.

        Args:
            device_id (str): The ID of the device.
            command (string | extends CommonCommands): The command to be sent.
            command_type (str, optional): The type of the command. Defaults to "command".
            parameters (dict | str, optional): The parameters for the command. Defaults to "default".

        Example JSON:
            {
                "commandType": "customize",
                "command": "ボタン", // the name of the customized button
                "parameter": "default"
            }

        """
        json = {
            "commandType": command_type,
            "command": command.value if isinstance(command, Commands) else command,
            "parameter": parameters,
        }
        await self._request(METH_POST, f"devices/{device_id}/commands", json=json)
