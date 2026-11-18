"""Test sensor status/webhook differences without inventing control actions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, get_type_hints

import pytest

from switchbot_api.common import DetectionState, DoorState
from switchbot_api.sensor import (
    METER_PLUS,
    METER_PRO_CO2,
    OUTDOOR_METER,
    WATER_LEAK_DETECTOR,
    ContactDoorMode,
    WaterLeakState,
    contact_door_state,
    sensor_detection_state,
    water_leak_state,
)


def test_sensor_detection_annotations_resolve_at_runtime() -> None:
    """Keep the Mapping annotation available to runtime consumers."""
    assert get_type_hints(sensor_detection_state)["payload"] == Mapping[str, Any]


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
        ({"detected": True}, DetectionState.DETECTED),
        ({"detected": False}, DetectionState.NOT_DETECTED),
        ({}, None),
    ],
)
def test_detection_status_and_webhook(
    payload: dict[str, Any],
    expected: DetectionState | None,
) -> None:
    """Accept documented presence field spellings and keep missing readings unknown."""
    assert sensor_detection_state(payload) is expected


@pytest.mark.parametrize(
    "payload",
    [
        {"Detected": 1},
        {"detected": 1},
        {"detected": "false"},
        {"detected": None},
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


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        (
            {"detectionState": "NOT_DETECTED", "detected": True},
            DetectionState.NOT_DETECTED,
        ),
        ({"moveDetected": False, "detected": True}, DetectionState.NOT_DETECTED),
        ({"Detected": False, "detected": True}, DetectionState.NOT_DETECTED),
    ],
)
def test_detection_field_precedence(
    payload: dict[str, Any],
    expected: DetectionState,
) -> None:
    """The new alias must not override previously supported fields."""
    assert sensor_detection_state(payload) is expected


def test_unknown_motion_state() -> None:
    """Do not convert an unknown webhook value into absence of motion."""
    with pytest.raises(ValueError, match="DetectionState"):
        sensor_detection_state({"detectionState": "unknown"})


@pytest.mark.parametrize("field", ["status", "detectionState"])
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, WaterLeakState.DRY),
        (1, WaterLeakState.LEAK_DETECTED),
        (None, None),
        ("0", None),
        ("1", None),
        (False, None),
        (True, None),
        (1.0, None),
        (2, None),
    ],
)
def test_water_leak_state_accepts_only_documented_integer_codes(
    field: str, value: object, expected: WaterLeakState | None
) -> None:
    """Resolve both payload fields without coercing unknown codes into alarms."""
    assert water_leak_state({field: value}) is expected


def test_water_leak_state_prefers_webhook_field() -> None:
    """Let a dry webhook reading replace an older leak status."""
    assert water_leak_state({"status": 1, "detectionState": 0}) is WaterLeakState.DRY
    assert water_leak_state({"status": 1, "detectionState": None}) is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("open", DoorState.OPEN),
        ("OPENED", DoorState.OPEN),
        ("close", DoorState.CLOSED),
        ("timeOutNotClose", DoorState.TIMEOUT_NOT_CLOSED),
        (None, None),
        ("unknown", None),
    ],
)
def test_contact_door_state(value: object, expected: DoorState | None) -> None:
    """Resolve contact position while preserving a door-open timeout."""
    assert contact_door_state({"openState": value}) is expected


def test_sensor_payload_without_readings_is_unknown() -> None:
    """Keep missing contact and water readings unknown in partial events."""
    payload = {"battery": 50}
    assert contact_door_state(payload) is None
    assert water_leak_state(payload) is None


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
