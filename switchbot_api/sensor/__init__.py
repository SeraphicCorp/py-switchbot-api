"""Sensor device support."""

from switchbot_api.sensor.models import (
    CONTACT_SENSOR,
    METER,
    METER_PLUS,
    METER_PRO,
    METER_PRO_CO2,
    MOTION_SENSOR,
    OUTDOOR_METER,
    PRESENCE_SENSOR,
    SENSOR_DEVICE_TYPES,
    WATER_LEAK_DETECTOR,
    ContactDoorMode,
    WaterLeakState,
)
from switchbot_api.sensor.utils import sensor_detection_state

__all__ = [
    "CONTACT_SENSOR",
    "METER",
    "METER_PLUS",
    "METER_PRO",
    "METER_PRO_CO2",
    "MOTION_SENSOR",
    "OUTDOOR_METER",
    "PRESENCE_SENSOR",
    "SENSOR_DEVICE_TYPES",
    "WATER_LEAK_DETECTOR",
    "ContactDoorMode",
    "WaterLeakState",
    "sensor_detection_state",
]
