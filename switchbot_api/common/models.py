"""Shared device models."""

from __future__ import annotations

from enum import Enum


class OnlineStatus(Enum):
    """String connectivity states shared by vacuums and other devices."""

    ONLINE = "online"
    OFFLINE = "offline"


class DoorState(Enum):
    """Door position shared by lock and sensor state payloads."""

    OPEN = "open"
    CLOSED = "close"
    TIMEOUT_NOT_CLOSED = "timeOutNotClose"

    @classmethod
    def _missing_(cls, value: object) -> DoorState | None:
        """Accept uppercase values and the equivalent closed spelling."""
        if not isinstance(value, str):
            return None
        normalized = value.casefold()
        if normalized == "open":
            return cls.OPEN
        if normalized in {"close", "closed"}:
            return cls.CLOSED
        if normalized == "timeoutnotclose":
            return cls.TIMEOUT_NOT_CLOSED
        return None


class ChargingStatus(Enum):
    """Battery charging states shared by rechargeable devices."""

    CHARGING = "charging"
    UNCHARGED = "uncharged"


class BrightnessLevel(Enum):
    """Qualitative webhook brightness, distinct from numeric light readings."""

    BRIGHT = "bright"
    DIM = "dim"


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
