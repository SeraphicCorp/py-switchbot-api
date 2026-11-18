"""Shared device support."""

from switchbot_api import Commands
from switchbot_api.common.models import (
    BrightnessLevel,
    ChargingStatus,
    DetectionState,
    PowerState,
)

__all__ = [
    "BrightnessLevel",
    "ChargingStatus",
    "Commands",
    "DetectionState",
    "PowerState",
]
