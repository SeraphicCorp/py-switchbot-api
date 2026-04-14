"""constant for  SwitchBot API."""

from __future__ import annotations

from enum import Enum, StrEnum


class PowerState(Enum):
    """Power state."""

    ON = "on"
    OFF = "off"


class EntityType(Enum):
    """Entity Type."""

    BINARY_SENSOR = "binary_sensors"
    BUTTON = "buttons"
    CLIMATE = "climates"
    COVER = "covers"
    FAN = "fans"
    HUMIDIFIER = "humidifiers"
    IMAGE = "images"
    LIGHT = "lights"
    LOCK = "locks"
    SENSOR = "sensors"
    SWITCH = "switches"
    VACUUM = "vacuums"


DeviceSupportMap: dict[str, dict[str, bool | list[EntityType]]] = {
    "Smart Radiator Thermostat": {
        "webhook": False,
        "entity_list": [EntityType.CLIMATE, EntityType.SENSOR],
    },
    "Relay Switch 1PM": {
        "webhook": False,
        "entity_list": [EntityType.SWITCH, EntityType.SENSOR],
    },
    "Relay Switch 1": {"webhook": False, "entity_list": [EntityType.SWITCH]},
    "Relay Switch 2PM": {
        "webhook": False,
        "entity_list": [EntityType.SWITCH, EntityType.SENSOR],
    },
    "K10+": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "K10+ Pro": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "Robot Vacuum Cleaner S1": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "Robot Vacuum Cleaner S1 Plus": {
        "webhook": True,
        "entity_list": [EntityType.VACUUM],
    },
    "K20+ Pro": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "Robot Vacuum Cleaner K10+ Pro Combo": {
        "webhook": True,
        "entity_list": [EntityType.VACUUM],
    },
    "Robot Vacuum Cleaner S10": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "Robot Vacuum Cleaner S20": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "S20": {"webhook": True, "entity_list": [EntityType.VACUUM]},
    "Robot Vacuum Cleaner K11 Plus": {
        "webhook": True,
        "entity_list": [EntityType.VACUUM],
    },
    "Smart Lock": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Smart Lock Lite": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Smart Lock Pro": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Smart Lock Ultra": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Smart Lock Vision": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Smart Lock Vision Pro": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Smart Lock Pro Wifi": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Lock Vision": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Lock Vision Pro": {
        "webhook": False,
        "entity_list": [EntityType.LOCK, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Motion Sensor": {
        "webhook": True,
        "entity_list": [EntityType.BINARY_SENSOR, EntityType.SENSOR],
    },
    "Contact Sensor": {
        "webhook": True,
        "entity_list": [EntityType.BINARY_SENSOR, EntityType.SENSOR],
    },
    "Presence Sensor": {
        "webhook": True,
        "entity_list": [EntityType.BINARY_SENSOR, EntityType.SENSOR],
    },
    "Hub 3": {
        "webhook": True,
        "entity_list": [EntityType.BINARY_SENSOR, EntityType.SENSOR],
    },
    "Water Detector": {
        "webhook": True,
        "entity_list": [EntityType.BINARY_SENSOR, EntityType.SENSOR],
    },
    "Battery Circulator Fan": {
        "webhook": False,
        "entity_list": [EntityType.FAN, EntityType.SENSOR],
    },
    "Standing Fan": {
        "webhook": False,
        "entity_list": [EntityType.FAN, EntityType.SENSOR],
    },
    "Circulator Fan": {"webhook": False, "entity_list": [EntityType.FAN]},
    "Curtain": {
        "webhook": False,
        "entity_list": [EntityType.COVER, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Curtain3": {
        "webhook": False,
        "entity_list": [EntityType.COVER, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Roller Shade": {
        "webhook": False,
        "entity_list": [EntityType.COVER, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Blind Tilt": {
        "webhook": False,
        "entity_list": [EntityType.COVER, EntityType.SENSOR, EntityType.BINARY_SENSOR],
    },
    "Strip Light": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Strip Light 3": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Floor Lamp": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Color Bulb": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "RGBICWW Floor Lamp": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "RGBICWW Strip Light": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Ceiling Light": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Ceiling Light Pro": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "RGBIC Neon Rope Light": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "RGBIC Neon Wire Rope Light": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Candle Warmer Lamp": {"webhook": False, "entity_list": [EntityType.LIGHT]},
    "Humidifier2": {"webhook": False, "entity_list": [EntityType.HUMIDIFIER]},
    "Humidifier": {
        "webhook": False,
        "entity_list": [EntityType.HUMIDIFIER, EntityType.SENSOR],
    },
    "Home Climate Panel": {
        "webhook": False,
        "entity_list": [EntityType.BINARY_SENSOR, EntityType.SENSOR],
    },
    "AI Art Frame": {
        "webhook": False,
        "entity_list": [EntityType.BUTTON, EntityType.SENSOR, EntityType.IMAGE],
    },
    "WeatherStation": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "Meter": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "MeterPlus": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "WoIOSensor": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "Hub 2": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "MeterPro": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "MeterPro(CO2)": {"webhook": False, "entity_list": [EntityType.SENSOR]},
    "Plug": {"webhook": False, "entity_list": [EntityType.SWITCH]},
    "Plug Mini (US)": {
        "webhook": False,
        "entity_list": [EntityType.SENSOR, EntityType.SWITCH],
    },
    "Plug Mini (JP)": {
        "webhook": False,
        "entity_list": [EntityType.SENSOR, EntityType.SWITCH],
    },
    "Plug Mini (EU)": {
        "webhook": False,
        "entity_list": [EntityType.SENSOR, EntityType.SWITCH],
    },
}


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


class DoorState(Enum):
    """Door State."""

    OPEN = "open"
    CLOSED = "close"


class LockState(Enum):
    """Lock State."""

    LOCKED = "locked"
    UNLOCKED = "unlocked"
    LOCKING = "locking"
    UNLOCKING = "unlocking"
    JAMMED = "jammed"
    LATCH_BOLT_LOCKED = "latchBoltLocked"
    HALF_LOCKED = "halfLocked"
