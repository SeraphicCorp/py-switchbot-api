"""Fan constants and ordinary enums from SwitchBot API v1.1.

Standing Circulator Fan is reported as Standing Fan; both names are listed.
Battery Circulator Fan 2 Pro has different nightlight command codes and no
documented closeDelay command. Its custom mode is status-only, and nightStatus
reports on/off rather than the numeric command codes. Shared power and
charging states live in common.models. Status payloads remain dictionaries.
Modern Ceiling Fan reports an integer mode in REST status and a string mode
in webhooks. The numeric mapping is undocumented. REST mainLightBrightness
and backLightBrightness are mainBrightness and backBrightness in webhooks.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/climate-control
"""

from enum import Enum
from typing import Final

BATTERY_CIRCULATOR_FAN: Final = "Battery Circulator Fan"
CIRCULATOR_FAN: Final = "Circulator Fan"
BATTERY_CIRCULATOR_FAN_2_PRO: Final = "Battery Circulator Fan 2 Pro"
MODERN_CEILING_FAN: Final = "Modern Ceiling Fan"
STANDING_FAN: Final = "Standing Fan"
STANDING_CIRCULATOR_FAN: Final = "Standing Circulator Fan"

FAN_DEVICE_TYPES: Final[list[str]] = [
    BATTERY_CIRCULATOR_FAN,
    CIRCULATOR_FAN,
    BATTERY_CIRCULATOR_FAN_2_PRO,
    MODERN_CEILING_FAN,
    STANDING_FAN,
    STANDING_CIRCULATOR_FAN,
]


class CirculatorFanMode(Enum):
    """Command/status modes for Battery, Circulator, and Standing Fan."""

    DIRECT = "direct"
    NATURAL = "natural"
    SLEEP = "sleep"
    BABY = "baby"


class BatteryCirculatorFan2ProMode(Enum):
    """Fan 2 Pro modes; CUSTOM is reported by status, not accepted as a command."""

    DIRECT = "direct"
    NATURAL = "natural"
    SLEEP = "sleep"
    HURRICANE = "hurricane"
    CUSTOM = "custom"


class CirculatorFanNightLightMode(Enum):
    """Nightlight command codes for Battery, Circulator, and Standing Fan."""

    ON = "on"
    OFF = "off"
    BRIGHT = "1"
    DIM = "2"


class ModernCeilingFanMode(Enum):
    """String modes used by ceiling fan commands and webhooks."""

    DIRECT = "direct"
    NATURAL = "natural"
    SLEEP = "sleep"
    HURRICANE = "hurricane"
    REVERSE = "reverse"
    CUSTOM = "custom"  # Webhook only.


class BatteryCirculatorFan2ProNightLightMode(Enum):
    """Fan 2 Pro nightlight command codes, distinct from nightStatus on/off."""

    ON = "on"
    OFF = "off"
    BRIGHT = "0"
    SOFT = "1"
