"""Read sensor states from status bodies and webhook contexts."""

from __future__ import annotations

from collections.abc import Mapping  # noqa: TC003 - runtime type hints
from typing import Any

from switchbot_api.common.models import DetectionState, DoorState
from switchbot_api.sensor.models import WaterLeakState


def sensor_detection_state(payload: Mapping[str, Any]) -> DetectionState | None:
    """Read a status body or webhook context for a motion/presence sensor.

    Presence status uses Detected or detected; motion/contact status uses
    moveDetected. Use water_leak_state for the Water Detector's integer
    detectionState field.
    """
    if "detectionState" in payload:
        value = payload["detectionState"]
        if not isinstance(value, str):
            msg = "motion detectionState must be a string; use WaterLeakState for water"
            raise TypeError(msg)
        return DetectionState(value)
    for key in ("moveDetected", "Detected", "detected"):
        if key in payload:
            value = payload[key]
            if not isinstance(value, bool):
                msg = f"{key} must be a boolean"
                raise TypeError(msg)
            return DetectionState.DETECTED if value else DetectionState.NOT_DETECTED
    return None


def water_leak_state(payload: Mapping[str, Any]) -> WaterLeakState | None:
    """Read the webhook detectionState or the REST status as a water leak state.

    When both fields are present, use detectionState even when it is unknown.
    """
    value = payload.get("detectionState", payload.get("status"))
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    try:
        return WaterLeakState(value)
    except ValueError:
        return None


def contact_door_state(payload: Mapping[str, Any]) -> DoorState | None:
    """Read openState, preserving the timeout state and unknown readings."""
    try:
        return DoorState(payload.get("openState"))
    except ValueError:
        return None
