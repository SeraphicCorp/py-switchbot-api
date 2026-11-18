"""Curtain and blind constants and enums for SwitchBot API v1.1.

Curtain 3/4 discovery and status tables use Curtain3/Curtain4, while their
command tables use Curtain 3/Curtain 4. Both spellings are collected below.
Webhook types such as WoCurtain3 are separate from discovery device types.

Status and webhook payloads remain ordinary dictionaries. Calibration,
grouping, and moving fields are booleans. Battery values are retained as
reported; no conversion to the documented battery buckets is performed.
Blind Tilt has no documented webhook. Curtain and Roller Shade positions
use 0 for open and 100 for closed; Blind Tilt uses the opposite convention.

Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/curtains-blinds
"""

from enum import Enum
from typing import Final

CURTAIN: Final = "Curtain"
CURTAIN_3: Final = "Curtain3"
CURTAIN_3_SPACED: Final = "Curtain 3"
CURTAIN_4: Final = "Curtain4"
CURTAIN_4_SPACED: Final = "Curtain 4"
BLIND_TILT: Final = "Blind Tilt"
ROLLER_SHADE: Final = "Roller Shade"

CURTAIN_DEVICE_TYPES: Final[list[str]] = [
    CURTAIN,
    CURTAIN_3,
    CURTAIN_3_SPACED,
    CURTAIN_4,
    CURTAIN_4_SPACED,
    BLIND_TILT,
    ROLLER_SHADE,
]


class CurtainMode(Enum):
    """Curtain setPosition modes, encoded in the index,mode,position string."""

    NORMAL = "0"
    SILENT = "1"
    DEFAULT = "ff"


class BlindTiltDirection(Enum):
    """Blind Tilt setPosition directions, encoded as direction;position."""

    UP = "up"
    DOWN = "down"
