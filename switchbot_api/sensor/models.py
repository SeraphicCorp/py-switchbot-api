"""Sensor constants and ordinary status enums from SwitchBot API v1.1.

Constants contain the actual deviceType values, including MeterPlus,
MeterPro(CO2), WoIOSensor, and Water Detector. Status payloads stay dictionaries.
Motion detection and brightness use common.DetectionState and BrightnessLevel;
contact position uses common.DoorState, including its timeout state.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/sensors
"""

from enum import Enum
from typing import Final

CONTACT_SENSOR: Final = "Contact Sensor"
METER: Final = "Meter"
METER_PLUS: Final = "MeterPlus"
METER_PRO: Final = "MeterPro"
METER_PRO_CO2: Final = "MeterPro(CO2)"
MOTION_SENSOR: Final = "Motion Sensor"
OUTDOOR_METER: Final = "WoIOSensor"
PRESENCE_SENSOR: Final = "Presence Sensor"
WATER_LEAK_DETECTOR: Final = "Water Detector"

SENSOR_DEVICE_TYPES: Final[list[str]] = [
    CONTACT_SENSOR,
    METER,
    METER_PLUS,
    METER_PRO,
    METER_PRO_CO2,
    MOTION_SENSOR,
    OUTDOOR_METER,
    PRESENCE_SENSOR,
    WATER_LEAK_DETECTOR,
]


class ContactDoorMode(Enum):
    """Contact sensor webhook entry/exit indication."""

    IN_DOOR = "IN_DOOR"
    OUT_DOOR = "OUT_DOOR"


class WaterLeakState(Enum):
    """Water Detector status and detectionState; separate from motion strings."""

    DRY = 0
    LEAK_DETECTED = 1
