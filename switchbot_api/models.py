"""constant for  SwitchBot API."""

from __future__ import annotations

from enum import Enum, StrEnum


class PowerState(Enum):
    """Power state."""

    ON = "on"
    OFF = "off"


class EntityType(Enum):
    """Entity Type."""

    BINARY_SENSOR = "binary_sensor"
    BUTTON = "button"
    CLIMATE = "climate"
    COVER = "cover"
    FAN = "fan"
    HUMIDIFIER="humidifier"
    IMAGE = "image"
    LIGHT = "light"
    LOCK ="lock"
    SENSOR = "sensor"
    SWITCH= "switch"
    VACUUM = "vacuum"



class BatteryCirculatorFanMode(StrEnum):
    """Fan mode types [Battery Circulator Fan] API."""

    DIRECT = "direct"
    NATURAL = "natural"
    SLEEP = "sleep"
    BABY = "baby"


class AirPurifierMode(Enum):
    """mode types [Air Purifier] API."""

    LEVEL = 1
    AUTO = 2
    SLEEP = 3
    PET = 4


class AirPurifierFanGear(Enum):
    """Air Purifier Fan Gear."""

    High = 3
    Medium = 2
    Low = 1


class VacuumFanSpeed(StrEnum):
    """Fan options for VacuumCommands supported devices."""

    VACUUM_FAN_SPEED_QUIET = "0"
    VACUUM_FAN_SPEED_STANDARD = "1"
    VACUUM_FAN_SPEED_STRONG = "2"
    VACUUM_FAN_SPEED_MAX = "3"


class VacuumFanSpeedV2(StrEnum):
    """Fan options for VacuumV2Commands & VacuumV3Commands supported devices."""

    VACUUM_FAN_SPEED_QUIET = "1"
    VACUUM_FAN_SPEED_STANDARD = "2"
    VACUUM_FAN_SPEED_STRONG = "3"
    VACUUM_FAN_SPEED_MAX = "4"


class VacuumCleanMode(StrEnum):
    """Clean mode for Vacuum."""

    SWEEP = "sweep"
    MOP = "mop"
    SWEEP_MOP = "sweep_mop"


class SmartRadiatorThermostatMode(Enum):
    """mode for Smart Radiator Thermostat ."""

    SCHEDULE = 0
    MANUAL = 1
    OFF = 2
    ENERGY_SAVING = 3
    COMFORT = 4
    FAST_HEATING = 5

    @classmethod
    def get_all_modes(cls) -> list[SmartRadiatorThermostatMode]:
        """Get all modes as a list."""
        return [
            cls.SCHEDULE,
            cls.MANUAL,
            cls.OFF,
            cls.ENERGY_SAVING,
            cls.COMFORT,
            cls.FAST_HEATING,
        ]


class BatteryLevel(Enum):
    """Battery Level modes."""

    High = "high"
    Medium = "medium"
    Low = "low"
    Critical = "critical"
    Unknown = "unknown"

    @classmethod
    def get_battery_level(cls, value: int) -> BatteryLevel:
        """Return a battery level."""
        if 100 >= value >= 60:
            return cls.High
        if 60 > value >= 20:
            return cls.Medium
        if 20 > value >= 10:
            return cls.Low
        if 10 > value >= 0:
            return cls.Critical
        return cls.Unknown
