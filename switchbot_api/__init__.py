"""Tools to query the SwitchBot API."""
import base64
from dataclasses import dataclass
from enum import Enum
import hashlib
import hmac
import logging
import time
from typing import TypeVar
import uuid

from aiohttp import ClientSession

_API_HOST = "https://api.switch-bot.com"

_LOGGER = logging.getLogger(__name__)
NON_OBSERVED_REMOTE_TYPES = ["Others"]


class CannotConnect(Exception):
    """Cannot connect to the SwitchBot API."""


class InvalidAuth(Exception):
    """Invalid auth for the SwitchBot API."""


class DeviceOffline(Exception):
    """Device currently offline."""
    

@dataclass
class Device:
    """Device."""

    device_id: str
    device_name: str
    device_type: str
    hub_device_id: str

    def __init__(self, **kwargs) -> None:
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

    def __init__(self, **kwargs) -> None:
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
    pass


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


T = TypeVar("T", bound=CommonCommands)


class SwitchBotAPI:
    """SwitchBot API."""

    def __init__(self, token: str, secret: str) -> None:
        """Initialize."""
        self.token = token
        self.secret = secret

    def make_headers(self, token: str, secret: str):
        """Make headers."""
        nonce = uuid.uuid4()
        timestamp = int(round(time.time() * 1000))
        string_to_sign = bytes(f"{token}{timestamp}{nonce}", "utf-8")
        secret_bytes = bytes(secret, "utf-8")

        sign = base64.b64encode(hmac.new(secret_bytes, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "charset": "utf8",
            "t": str(timestamp),
            "sign": str(sign, "utf-8"),
            "nonce": str(nonce),
        }

    async def _request(self, path: str = "", callback: str = "get", json=None):
        async with ClientSession() as session:
            async with getattr(session, callback)(
                f"{_API_HOST}/v1.1/{path}",
                headers=self.make_headers(self.token, self.secret),
                json=json,
            ) as response:
                if response.status == 403:
                    raise InvalidAuth()

                body = await response.json()

                if response.status >= 400:
                    raise CannotConnect() 
                    
                match body.get("statusCode"):
                    case 100:
                        return body.get("body")
                    case 171:
                        raise DeviceOffline()
                    case _:
                        _LOGGER.error("Error %s: %s", response.status, body)
                        raise CannotConnect()
                

    async def list_devices(self):
        """List devices."""
        body = await self._request("devices")
        _LOGGER.debug("Devices: %s", body)
        devices = [Device(**device) for device in body.get("deviceList")]
        remotes = [
            Remote(**remote)
            for remote in body.get("infraredRemoteList")
            if remote.get("remoteType") not in NON_OBSERVED_REMOTE_TYPES
        ]
        return [*devices, *remotes]

    async def get_status(self, device_id: str):
        """No status for IR devices."""
        body = await self._request(f"devices/{device_id}/status")
        return body

    async def get_webook_configuration(self):
        """List webhooks."""
        json = {"action": "queryUrl"}
        return await self._request("webhook/queryWebhook", callback="post", json=json)

    async def setup_webhook(self, url: str):
        """Setup webhook to receive device status updates."""
        json = {"deviceList": "ALL", "action": "setupWebhook", "url": url}
        await self._request("webhook/setupWebhook", callback="post", json=json)

    async def delete_webhook(self, url: str):
        """Delete webhook."""
        json = {"action": "deleteWebhook", "url": url}
        await self._request("webhook/deleteWebhook", callback="post", json=json)

    async def send_command(
        self,
        device_id: str,
        command: T,
        command_type: str = "command",
        parameters: dict | str = "default",
    ):
        """Send command to device.

        Args:
            device_id (str): The ID of the device.
            command (extends CommonCommands): The command to be sent.
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
            "command": command.value,
            "parameter": parameters,
        }
        await self._request(f"devices/{device_id}/commands", callback="post", json=json)
