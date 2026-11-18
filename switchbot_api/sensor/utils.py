"""Normalize motion fields while keeping missing readings unknown."""

from __future__ import annotations

from collections.abc import Mapping  # noqa: TC003 - runtime type hints
from typing import Any

from switchbot_api.common import DetectionState


def sensor_detection_state(payload: Mapping[str, Any]) -> DetectionState | None:
    """Read a status body or webhook context for a motion/presence sensor.

    Presence status uses Detected or detected; motion/contact status uses
    moveDetected. Water Detector uses integer detectionState and must instead
    be parsed with WaterLeakState. Existing field precedence is preserved.
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
