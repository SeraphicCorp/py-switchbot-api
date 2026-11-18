"""Build fan parameters with device-specific validation."""

from __future__ import annotations

from switchbot_api.common.models import PowerState
from switchbot_api.common.utils import integer_in_range, rgb_component
from switchbot_api.fan.models import (
    BatteryCirculatorFan2ProMode,
    CirculatorFanMode,
    ModernCeilingFanMode,
)


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


def modern_ceiling_fan_wind_mode_parameter(mode: ModernCeilingFanMode) -> str:
    """Build a writable mode without sending the webhook-only custom state."""
    if not isinstance(mode, ModernCeilingFanMode):
        msg = "mode must be a ModernCeilingFanMode member"
        raise TypeError(msg)
    if mode is ModernCeilingFanMode.CUSTOM:
        msg = "custom is a webhook-only mode and cannot be sent as a wind command"
        raise ValueError(msg)
    return str(mode.value)


def modern_ceiling_fan_wind_speed_parameter(speed: int) -> int:
    """Build a numeric setWindSpeed value from 1 to 100."""
    return integer_in_range(speed, 1, 100, "speed")


def modern_ceiling_fan_close_delay_parameter(minutes: int) -> int:
    """Build closeDelay as a positive integer number of minutes."""
    if isinstance(minutes, bool) or not isinstance(minutes, int):
        msg = "minutes must be an integer"
        raise TypeError(msg)
    if minutes <= 0:
        msg = "minutes must be positive"
        raise ValueError(msg)
    return minutes


def modern_ceiling_fan_brightness_parameter(brightness: int) -> int:
    """Build main light or backlight brightness as an integer from 0 to 100."""
    return integer_in_range(brightness, 0, 100, "brightness")


def modern_ceiling_fan_color_temperature_parameter(kelvin: int) -> int:
    """Build the numeric main light color temperature in Kelvin."""
    return integer_in_range(kelvin, 2700, 6500, "kelvin")


def modern_ceiling_fan_color_parameter(red: int, green: int, blue: int) -> str:
    """Build the backlight's R:G:B string."""
    red = rgb_component(red, "red")
    green = rgb_component(green, "green")
    blue = rgb_component(blue, "blue")
    return f"{red}:{green}:{blue}"
