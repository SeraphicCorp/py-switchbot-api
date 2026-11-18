"""Build fan parameter strings with device-specific validation."""

from __future__ import annotations

from .models import BatteryCirculatorFan2ProMode, CirculatorFanMode


def _integer_parameter(value: int, minimum: int, maximum: int, name: str) -> str:
    """Validate an integer range, excluding boolean coercion."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{name} must be an integer"
        raise TypeError(msg)
    if not minimum <= value <= maximum:
        msg = f"{name} must be between {minimum} and {maximum}"
        raise ValueError(msg)
    return str(value)


def fan_wind_speed_parameter(speed: int) -> str:
    """Build a setWindSpeed string from 1 to 100."""
    return _integer_parameter(speed, 1, 100, "speed")


def fan_close_delay_parameter(delay: int) -> str:
    """Build closeDelay from 1 to 36000 for the three supported fan families."""
    return _integer_parameter(delay, 1, 36000, "delay")


def fan_wind_mode_parameter(
    mode: CirculatorFanMode | BatteryCirculatorFan2ProMode,
) -> str:
    """Build a command mode while rejecting Fan 2 Pro's status-only CUSTOM."""
    if not isinstance(mode, (CirculatorFanMode, BatteryCirculatorFan2ProMode)):
        msg = "mode must be a fan mode enum member"
        raise TypeError(msg)
    if mode is BatteryCirculatorFan2ProMode.CUSTOM:
        msg = "custom is a status-only mode and cannot be sent as a wind command"
        raise ValueError(msg)
    return str(mode.value)
