"""constant for  SwitchBot API."""

from __future__ import annotations

from enum import Enum, StrEnum


class PowerState(Enum):
    """Power state."""

    ON = "on"
    OFF = "off"


class BatteryCirculatorFanMode(StrEnum):
    """Fan mode types [Battery Circulator Fan] API."""

    DIRECT = "direct"
    NATURAL = "natural"
    SLEEP = "sleep"
    BABY = "baby"


class BatteryCirculatorFan2ProMode(StrEnum):
    """Fan mode types [Battery Circulator Fan2 Pro] API."""

    DIRECT = "direct"
    NATURAL = "natural"
    SLEEP = "sleep"
    BABY = "baby"
    HURRICANE = "hurricane"


class AirPurifierMode(Enum):
    """mode types [Air Purifier] API."""

    LEVEL = 1
    AUTO = 2
    SLEEP = 3
    PET = 4


class AirPurifierModeV2(Enum):
    """Air Purifier Modes."""

    NORMAL = 1
    AUTO = 2
    SLEEP = 3
    PET = 4

    @classmethod
    def get_modes(cls) -> list[str]:
        """Return a list of available air purifier modes as lowercase strings."""
        return [mode.name.lower() for mode in cls]


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


class Switch(Enum):
    """Switch parameter."""

    ON = "on"
    OFF = "off"


class KataFriendsMode(Enum):
    """Kata Friends Mode."""

    NORMAL = "Normal"
    STANDBY = "Standby"
    SLEEP = "Sleep"


class KataFriendsWorkStatus(Enum):
    """Kata Friends Work Status."""

    STROLLING = "Strolling"
    WELCOMING_HOME = "Welcoming Home"
    WAKE_UP_CALL = "Wake-up Call"
    SLEEPING = "Sleeping"
    PLAYING = "Playing"
    RETURNING = "Returning"


class KataFriendsHospitalizedStatus(Enum):
    """Kata Friends Hospitalized Status."""

    NORMAL = 0
    REPAIR = 1
    MAINTAIN = 2
    CLEAN = 3


class Humidifier2Mode(Enum):
    """Enumerates the available modes for a SwitchBot humidifier2."""

    HIGH = 1
    MEDIUM = 2
    LOW = 3
    QUIET = 4
    TARGET_HUMIDITY = 5
    SLEEP = 6
    AUTO = 7
    DRYING_FILTER = 8

    @classmethod
    def get_modes(cls) -> list[str]:
        """Return a list of available humidifier2 modes as lowercase strings."""
        return [mode.name.lower() for mode in cls]


class SwitchbotCloudDeviceLockState(Enum):
    """Lock State."""

    LOCKED = "locked"
    UNLOCKED = "unlocked"
    LOCKING = "locking"
    UNLOCKING = "unlocking"
    JAMMED = "jammed"
    LATCH_BOLT_LOCKED = "latchBoltLocked"
    HALF_LOCKED = "halfLocked"

    @classmethod
    def get_states(cls) -> list[SwitchbotCloudDeviceLockState]:
        """Get lock states."""
        return list(cls)

    @classmethod
    def get_values(cls) -> list[str]:
        """Get lock value."""
        return [mode.value for mode in cls]
