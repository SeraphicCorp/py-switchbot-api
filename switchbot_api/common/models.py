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
        """Accept case differences and the equivalent opened/closed spellings."""
        if not isinstance(value, str):
            return None
        normalized = value.casefold()
        if normalized in {"open", "opened"}:
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

    Parsing accepts different letter cases and returns an enum with an
    uppercase value. PARTIAL describes a device with independently powered
    parts. A command that takes only on or off needs a binary state.
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
