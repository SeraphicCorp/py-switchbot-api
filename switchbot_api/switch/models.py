"""Plug, relay, and garage constants and ordinary protocol enums.

Garage doorStatus uses 0=on and 1=off, opposite to relay switchStatus.
Power measured in Watts is a number, not common.PowerState.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/plugs-switches
"""

from enum import Enum
from typing import Final

GARAGE_DOOR_OPENER: Final = "Garage Door Opener"
PLUG: Final = "Plug"
PLUG_MINI_EU: Final = "Plug Mini (EU)"
PLUG_MINI_JP: Final = "Plug Mini (JP)"
PLUG_MINI_US: Final = "Plug Mini (US)"
RELAY_SWITCH_1: Final = "Relay Switch 1"
RELAY_SWITCH_1PM: Final = "Relay Switch 1PM"
RELAY_SWITCH_2PM: Final = "Relay Switch 2PM"

SWITCH_DEVICE_TYPES: Final[list[str]] = [
    GARAGE_DOOR_OPENER,
    PLUG,
    PLUG_MINI_EU,
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
    """Integer switchStatus for EU Plug Mini and relays."""

    OFF = 0
    ON = 1


class GarageDoorStatus(Enum):
    """Garage doorStatus codes, without assuming physical door position."""

    ON = 0
    OFF = 1
