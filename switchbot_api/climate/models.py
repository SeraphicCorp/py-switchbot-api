"""Climate device constants and enums from SwitchBot API v1.1.

Air purifiers, humidifiers, the radiator thermostat, and Home Climate Panel
belong here; circulator fans belong in fan. Both evaporative humidifiers use
the API device type Humidifier2. The existing Humidifier 2 spelling is kept
as an alias.

Status/webhook payloads remain ordinary dictionaries. Home Climate Panel has
no documented control commands. Its numeric status brightness differs from
the bright/dim webhook field (common.models.BrightnessLevel). Shared power
and motion states are also in common.models. hubDeviceId may be null.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/climate-control
"""

from enum import Enum
from typing import Final

AIR_PURIFIER_VOC: Final = "Air Purifier VOC"
AIR_PURIFIER_TABLE_VOC: Final = "Air Purifier Table VOC"
AIR_PURIFIER_PM25: Final = "Air Purifier PM2.5"
AIR_PURIFIER_TABLE_PM25: Final = "Air Purifier Table PM2.5"
HUMIDIFIER: Final = "Humidifier"
HUMIDIFIER_2: Final = "Humidifier2"
HUMIDIFIER_2_SPACED: Final = "Humidifier 2"
SMART_RADIATOR_THERMOSTAT: Final = "Smart Radiator Thermostat"
HOME_CLIMATE_PANEL: Final = "Home Climate Panel"

CLIMATE_DEVICE_TYPES: Final[list[str]] = [
    AIR_PURIFIER_VOC,
    AIR_PURIFIER_TABLE_VOC,
    AIR_PURIFIER_PM25,
    AIR_PURIFIER_TABLE_PM25,
    HUMIDIFIER,
    HUMIDIFIER_2,
    HUMIDIFIER_2_SPACED,
    SMART_RADIATOR_THERMOSTAT,
    HOME_CLIMATE_PANEL,
]


class HumidifierMode(Enum):
    """Original Humidifier presets; percentages 0-100 are also accepted."""

    AUTO = "auto"
    LOW = "101"
    MEDIUM = "102"
    HIGH = "103"


class EvaporativeHumidifierMode(Enum):
    """Humidifier2 modes used by both evaporative humidifier variants."""

    HIGH = 1
    MEDIUM = 2
    LOW = 3
    QUIET = 4
    TARGET_HUMIDITY = 5
    SLEEP = 6
    AUTO = 7
    DRYING_FILTER = 8

    LEVEL_4 = HIGH
    LEVEL_3 = MEDIUM
    LEVEL_2 = LOW
    LEVEL_1 = QUIET

    @classmethod
    def get_modes(cls) -> list[str]:
        """Return lowercase preset names, omitting aliases for the same mode."""
        return [mode.name.lower() for mode in cls]


class AirPurifierMode(Enum):
    """Modes shared by the four VOC and PM2.5 purifier variants."""

    NORMAL = 1
    AUTO = 2
    SLEEP = 3
    PET = 4

    @classmethod
    def get_modes(cls) -> list[str]:
        """Return lowercase mode names for display or preset selection."""
        return [mode.name.lower() for mode in cls]


class AirPurifierFanGear(Enum):
    """Fan levels available only in the purifier's NORMAL mode."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class AirPurifierLightSensorMode(Enum):
    """Purifier light settings; ON enables sensor-based light shutdown."""

    ON = "on"
    OFF = "off"
    STEADY = "steadyMode"


class SmartRadiatorThermostatMode(Enum):
    """Radiator thermostat modes encoded as 0-5 in command parameters."""

    SCHEDULE = 0
    MANUAL = 1
    OFF = 2
    ENERGY_SAVING = 3
    COMFORT = 4
    FAST_HEATING = 5
