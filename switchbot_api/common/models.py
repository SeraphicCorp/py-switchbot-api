"""Shared device models."""

from __future__ import annotations

from enum import Enum


class DetectionState(Enum):
    """Motion states reported by device detectionState webhook fields.

    Some devices report only DETECTED. A missing field, such as in a Solar
    camera battery-only event, does not imply NOT_DETECTED.
    """

    DETECTED = "DETECTED"
    NOT_DETECTED = "NOT_DETECTED"


class PowerState(Enum):
    """Power states shared by device status responses and webhook events.

    Accept either case when parsing API values. Canonical values are
    uppercase. PARTIAL represents devices with independently powered parts.
    """

    ON = "ON"
    OFF = "OFF"
    PARTIAL = "PARTIAL"

    @classmethod
    def _missing_(cls, value: object) -> PowerState | None:
        """Resolve lowercase or mixed-case API states to their enum member."""
        if isinstance(value, str):
            return cls.__members__.get(value.upper())
        return None
