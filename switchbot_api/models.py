"""Models for SwitchBot API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Annotated, Any

from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.types import Discriminator

from switchbot_api.const import Model


class OpenDirection(StrEnum):
    """Open direction."""

    LEFT = "left"
    RIGHT = "right"


@dataclass
class DeviceList(DataClassJSONMixin):
    """Device list."""

    devices: list[
        Annotated[Device, Discriminator(field="deviceType", include_subtypes=True)]
    ] = field(metadata=field_options(alias="deviceList"))
    remotes: list[Remote] = field(metadata=field_options(alias="infraredRemoteList"))


@dataclass
class Device:
    """Device."""

    deviceType: Model  # noqa: N815
    device_id: str = field(metadata=field_options(alias="deviceId"))
    name: str = field(metadata=field_options(alias="deviceName"))
    type: Model = field(metadata=field_options(alias="deviceType"))
    hub_device_id: str | None = field(metadata=field_options(alias="hubDeviceId"))

    @classmethod
    def __pre_deserialize__(cls, d: dict[str, Any]) -> dict[str, Any]:
        """Pre deserialize hook."""
        if d["hubDeviceId"] == "":
            d["hubDeviceId"] = None
        return d


@dataclass
class Hub2(Device):
    """Hub2 device."""

    deviceType = Model.HUB_2  # noqa: N815


@dataclass
class Curtain3(Device):
    """Curtain3 device."""

    deviceType = Model.CURTAIN3  # noqa: N815
    calibrate: bool
    open_direction: OpenDirection = field(metadata=field_options(alias="openDirection"))
    main: bool = field(metadata=field_options(alias="master"))


@dataclass
class Curtain(Device):
    """Curtain device."""

    deviceType = Model.CURTAIN  # noqa: N815
    calibrate: bool
    group: bool
    curtain_devices_ids: list[str] = field(
        metadata=field_options(alias="curtainDevicesIds")
    )


@dataclass
class Remote:
    """Remote device."""

    device_id: str = field(metadata=field_options(alias="deviceId"))
    name: str = field(metadata=field_options(alias="deviceName"))
    type: str = field(metadata=field_options(alias="remoteType"))
    hub_device_id: str = field(metadata=field_options(alias="hubDeviceId"))


@dataclass
class DeviceStatus(DataClassJSONMixin):
    """Device status."""

    class Config:
        """Config."""

        discriminator = Discriminator(field="deviceType", include_subtypes=True)

    deviceType: Model  # noqa: N815
    version: str
    device_id: str = field(metadata=field_options(alias="deviceId"))
    type: Model = field(metadata=field_options(alias="deviceType"))
    hub_device_id: str | None = field(metadata=field_options(alias="hubDeviceId"))

    @classmethod
    def __pre_deserialize__(cls, d: dict[str, Any]) -> dict[str, Any]:
        """Pre deserialize hook."""
        if d["hubDeviceId"] in ["000000000000", d["deviceId"]]:
            d["hubDeviceId"] = None
        return d


@dataclass
class Hub2Status(DeviceStatus):
    """Hub2 status."""

    deviceType = Model.HUB_2  # noqa: N815
    temperature: float
    humidity: float


@dataclass
class CurtainStatus(DeviceStatus):
    """Curtain status."""

    deviceType = Model.CURTAIN  # noqa: N815
    calibrate: bool
    group: bool
    moving: bool
    battery: int
    slide_position: int = field(metadata=field_options(alias="slidePosition"))


@dataclass
class Curtain3Status(CurtainStatus):
    """Hub2 status."""

    deviceType = Model.CURTAIN3  # noqa: N815
