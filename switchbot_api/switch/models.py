"""Plug, relay, and garage constants and ordinary protocol enums.

Garage doorStatus uses 0=on and 1=off, opposite to relay switchStatus.
Power measured in Watts is a number, not common.PowerState.
Plug Mini (IT) and Outdoor Plug (EU) use numeric switchStatus in both status
and webhooks. Status reports onlineStatus (online/offline), voltage (V),
power (W), electricCurrent (mA), and usedElectricity (W min). Their webhook
types match discovery and use boolean online, overTemperature, and overload.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/plugs-switches
"""

from enum import Enum
from typing import Final

GARAGE_DOOR_OPENER: Final = "Garage Door Opener"
OUTDOOR_PLUG_EU: Final = "Outdoor Plug (EU)"
PLUG: Final = "Plug"
PLUG_MINI_EU: Final = "Plug Mini (EU)"
PLUG_MINI_IT: Final = "Plug Mini (IT)"
PLUG_MINI_JP: Final = "Plug Mini (JP)"
PLUG_MINI_US: Final = "Plug Mini (US)"
RELAY_SWITCH_1: Final = "Relay Switch 1"
RELAY_SWITCH_1PM: Final = "Relay Switch 1PM"
RELAY_SWITCH_2PM: Final = "Relay Switch 2PM"

SWITCH_DEVICE_TYPES: Final[list[str]] = [
    GARAGE_DOOR_OPENER,
    OUTDOOR_PLUG_EU,
    PLUG,
    PLUG_MINI_EU,
    PLUG_MINI_IT,
    PLUG_MINI_JP,
    PLUG_MINI_US,
    RELAY_SWITCH_1,
    RELAY_SWITCH_1PM,
    RELAY_SWITCH_2PM,
]


class RelaySwitchMode(Enum):
    """Relay setMode codes shared by the three relay families."""

    TOGGLE = 0
    EDGE = 1
    DETACHED = 2
    MOMENTARY = 3


class RelayChannel(Enum):
    """Relay 2PM command channels; no combined-channel code is documented."""

    CHANNEL_1 = "1"
    CHANNEL_2 = "2"


class SwitchStatus(Enum):
    """Integer switchStatus for compatible plugs and relays."""

    OFF = 0
    ON = 1


class GarageDoorStatus(Enum):
    """Garage doorStatus codes, without assuming physical door position."""

    ON = 0
    OFF = 1
