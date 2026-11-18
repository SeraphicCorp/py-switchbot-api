"""Test sensor status/webhook differences without inventing control actions."""

from __future__ import annotations

from typing import Any

import pytest

from switchbot_api.common import DetectionState, DoorState
from switchbot_api.sensor import (
    METER_PLUS,
    METER_PRO_CO2,
    OUTDOOR_METER,
    WATER_LEAK_DETECTOR,
    ContactDoorMode,
    WaterLeakState,
    sensor_detection_state,
)


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"moveDetected": True}, DetectionState.DETECTED),
        ({"moveDetected": False}, DetectionState.NOT_DETECTED),
        ({"Detected": True, "lightLevel": 20}, DetectionState.DETECTED),
        ({"Detected": False}, DetectionState.NOT_DETECTED),
        ({"detectionState": "DETECTED"}, DetectionState.DETECTED),
        ({"detectionState": "NOT_DETECTED"}, DetectionState.NOT_DETECTED),
        ({"battery": 100}, None),
        ({"detected": True}, None),
    ],
)
def test_detection_status_and_webhook(
    payload: dict[str, Any],
    expected: DetectionState | None,
) -> None:
    """Respect case-sensitive presence fields and unknown missing readings."""
    assert sensor_detection_state(payload) is expected


@pytest.mark.parametrize(
    "payload",
    [
        {"Detected": 1},
        {"moveDetected": "false"},
        {"moveDetected": None},
        {"detectionState": 1},
        {"detectionState": 0},
    ],
)
def test_reject_confused_motion_and_water_codes(payload: dict[str, Any]) -> None:
    """Water Detector numeric detectionState must never be treated as motion."""
    with pytest.raises(TypeError, match="must be"):
        sensor_detection_state(payload)


def test_unknown_motion_state() -> None:
    """Do not convert an unknown webhook value into absence of motion."""
    with pytest.raises(ValueError, match="DetectionState"):
        sensor_detection_state({"detectionState": "unknown"})


def test_sensor_protocol_values() -> None:
    """Discovery identifiers and contact/water states keep exact API spellings."""
    assert (METER_PLUS, METER_PRO_CO2, OUTDOOR_METER, WATER_LEAK_DETECTOR) == (
        "MeterPlus",
        "MeterPro(CO2)",
        "WoIOSensor",
        "Water Detector",
    )
    assert DoorState("timeOutNotClose") is DoorState.TIMEOUT_NOT_CLOSED
    assert ContactDoorMode("IN_DOOR") is ContactDoorMode.IN_DOOR
    assert WaterLeakState(0) is WaterLeakState.DRY
    assert WaterLeakState(1) is WaterLeakState.LEAK_DETECTED
