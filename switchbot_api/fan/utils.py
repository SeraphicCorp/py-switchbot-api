"""Build fan parameter strings with device-specific validation."""

from __future__ import annotations

from switchbot_api.common import PowerState
from switchbot_api.common.utils import integer_in_range

from .models import BatteryCirculatorFan2ProMode, CirculatorFanMode


def fan_wind_speed_parameter(speed: int) -> str:
    """Build a setWindSpeed string from 1 to 100."""
    return str(integer_in_range(speed, 1, 100, "speed"))


def fan_close_delay_parameter(delay: int) -> str:
    """Build closeDelay from 1 to 36000 for the three supported fan families."""
    return str(integer_in_range(delay, 1, 36000, "delay"))


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


def fan_oscillation_parameter(state: PowerState) -> str:
    """Build Fan 2 Pro horizontal/vertical oscillation as lowercase on/off."""
    if not isinstance(state, PowerState):
        msg = "state must be a common.PowerState member"
        raise TypeError(msg)
    if state is PowerState.PARTIAL:
        msg = "oscillation state must be ON or OFF"
        raise ValueError(msg)
    return str(state.value).lower()
