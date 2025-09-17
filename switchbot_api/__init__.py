"""Tools to query the SwitchBot API."""

from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import hmac
import logging
import socket
import time
from typing import Any, Self
import uuid

from aiohttp import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST

from switchbot_api.commands import (
    AirConditionerCommands,
    AirPurifierCommands,
    BatteryCirculatorFanCommands,
    BlindTiltCommands,
    BotCommands,
    CeilingLightCommands,
    Commands,
    CommonCommands,
    CurtainCommands,
    DoorBellCommands,
    DVDCommands,
    FanCommands,
    HumidifierCommands,
    HumidifierV2Commands,
    LightCommands,
    LockCommands,
    LockV2Commands,
    OthersCommands,
    RGBWLightCommands,
    RGBWWLightCommands,
    RollerShadeCommands,
    SmartRadiatorThermostatCommands,
    SpeakerCommands,
    Switch2PMCommands,
    SwitchCommands,
    T,
    TVCommands,
    VacuumCleanerV2Commands,
    VacuumCleanerV3Commands,
    VacuumCommands,
)
from switchbot_api.exceptions import (
    SwitchBotAuthenticationError,
    SwitchBotConnectionError,
    SwitchBotDeviceOfflineError,
)
from switchbot_api.models import (
    BatteryCirculatorFanMode,
    PowerState,
    SmartRadiatorThermostatMode,
    VacuumCleanMode,
    VacuumFanSpeed,
    VacuumFanSpeedV2,
)

__all__ = [
    "AirConditionerCommands",
    "AirPurifierCommands",
    "BatteryCirculatorFanCommands",
    "BatteryCirculatorFanMode",
    "BlindTiltCommands",
    "BotCommands",
    "CeilingLightCommands",
    "Commands",
    "CommonCommands",
    "CurtainCommands",
    "DVDCommands",
    "Device",
    "DoorBellCommands",
    "FanCommands",
    "HumidifierCommands",
    "HumidifierV2Commands",
    "LightCommands",
    "LockCommands",
    "LockV2Commands",
    "OthersCommands",
    "PowerState",
    "RGBWLightCommands",
    "RGBWWLightCommands",
    "Remote",
    "RollerShadeCommands",
    "SmartRadiatorThermostatCommands",
    "SmartRadiatorThermostatMode",
    "SpeakerCommands",
    "Switch2PMCommands",
    "SwitchBotAPI",
    "SwitchCommands",
    "T",
    "TVCommands",
    "VacuumCleanMode",
    "VacuumCleanerV2Commands",
    "VacuumCleanerV3Commands",
    "VacuumCommands",
    "VacuumFanSpeed",
    "VacuumFanSpeedV2",
]

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
    group: bool
    master: bool | None

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""
        self.device_id = kwargs["deviceId"]
        self.device_name = kwargs["deviceName"]
        self.device_type = kwargs.get("deviceType", "-")
        self.hub_device_id = kwargs["hubDeviceId"]
        self.group = kwargs.get("group", False)
        self.master = kwargs.get("master")


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


class SwitchBotAPI:
    """SwitchBot API."""

    _close_session: bool = False

    def __init__(
        self, token: str, secret: str, session: ClientSession | None = None
    ) -> None:
        """Initialize."""
        self.token = token
        self.secret = secret
        self.session = session

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
        if not self.session:
            self.session = ClientSession()
            self._close_session = True
        try:
            response = await self.session.request(
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
            raise SwitchBotAuthenticationError

        body = await response.json()

        if response.status >= 400:
            _LOGGER.error("Error %d: %s", response.status, body)
            raise SwitchBotConnectionError

        match body.get("statusCode"):
            case 100:
                return body["body"]  # type: ignore[no-any-return]
            case 161 | 171:
                # SwitchBot docs claim that 161 is the code for device
                # being offline, and 171 for a _hub_ being offline.
                # In testing, the Plug Mini (JP) return 171 when not
                # online too.
                raise SwitchBotDeviceOfflineError
            case _:
                _LOGGER.error("Error %d: %s", response.status, body)
                raise SwitchBotConnectionError

    async def list_devices(self) -> list[Device | Remote]:
        """List devices."""
        body = await self._request(METH_GET, "devices")
        _LOGGER.debug("Devices: %s", body)
        devices = [Device(**device) for device in body.get("deviceList")]  # type: ignore[union-attr]
        remotes = [
            Remote(**remote)
            for remote in body.get("infraredRemoteList")  # type: ignore[union-attr]
            if remote.get("remoteType") not in NON_OBSERVED_REMOTE_TYPES
        ]
        return [*devices, *remotes]

    async def get_status(self, device_id: str) -> dict[str, Any]:
        """No status for IR devices."""
        return await self._request(METH_GET, f"devices/{device_id}/status")

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
        parameters: dict | str = "default",  # type: ignore[type-arg]
    ) -> None:
        """Send command to device.

        Args:
            device_id (str): The ID of the device.
            command (string | extends CommonCommands): The command to be sent.
            command_type (str, optional): The type of the command.
            Defaults to "command".
            parameters (dict | str, optional): The parameters for the command.
            Defaults to "default".

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

    async def close(self) -> None:
        """Close the client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The SwitchBotAPI object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
