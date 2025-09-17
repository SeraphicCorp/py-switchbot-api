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
    FAST_HEARTING = 5

    @classmethod
    def get_all_modes(cls) -> list[SmartRadiatorThermostatMode]:
        """Get all modes as a list."""
        return [
            cls.SCHEDULE,
            cls.MANUEL,
            cls.OFF,
            cls.ENERGY_SAVING,
            cls.COMFORT,
            cls.FAST_HEARTING,
        ]
