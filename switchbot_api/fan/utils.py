"""Build fan parameters with device-specific validation."""

from __future__ import annotations

from typing import Final

from switchbot_api.common.models import PowerState
from switchbot_api.common.utils import integer_in_range, rgb_component
from switchbot_api.fan.models import (
    BATTERY_CIRCULATOR_FAN,
    BATTERY_CIRCULATOR_FAN_2_PRO,
    CIRCULATOR_FAN,
    STANDING_CIRCULATOR_FAN,
    STANDING_FAN,
    BatteryCirculatorFan2ProMode,
    BatteryCirculatorFan2ProNightLightMode,
    CirculatorFanMode,
    CirculatorFanNightLightMode,
    ModernCeilingFanMode,
)

_STANDARD_CIRCULATOR_FAN_TYPES: Final = (
    BATTERY_CIRCULATOR_FAN,
    CIRCULATOR_FAN,
    STANDING_FAN,
    STANDING_CIRCULATOR_FAN,
)
# The same brightness option has a different command code on Fan 2 Pro.
_STANDARD_NIGHT_LIGHT_PARAMETERS: Final = {
    "off": CirculatorFanNightLightMode.OFF.value,
    "bright": CirculatorFanNightLightMode.BRIGHT.value,
    "soft": CirculatorFanNightLightMode.DIM.value,
}
_FAN_2_PRO_NIGHT_LIGHT_PARAMETERS: Final = {
    "off": BatteryCirculatorFan2ProNightLightMode.OFF.value,
    "bright": BatteryCirculatorFan2ProNightLightMode.BRIGHT.value,
    "soft": BatteryCirculatorFan2ProNightLightMode.SOFT.value,
}


def fan_wind_speed_parameter(speed: int) -> str:
    """Build a setWindSpeed string from 1 to 100."""
    return str(integer_in_range(speed, 1, 100, "speed"))


def fan_close_delay_parameter(delay: int) -> str:
    """Build closeDelay from 1 to 36000 for the three supported fan families."""
    return str(integer_in_range(delay, 1, 36000, "delay"))


def fan_wind_mode_parameter(
    mode: CirculatorFanMode | BatteryCirculatorFan2ProMode,
) -> str:
    """Build a command parameter from a circulator fan mode."""
    if not isinstance(mode, (CirculatorFanMode, BatteryCirculatorFan2ProMode)):
        msg = "mode must be a fan mode enum member"
        raise TypeError(msg)
    return str(mode.value)


def fan_writable_wind_modes(device_type: str) -> list[str]:
    """Return writable presets for a supported circulator fan's device type.

    Fan 2 Pro accepts custom as a command. The ceiling fan's custom state
    is webhook-only and belongs to a separate mode enum.
    """
    if device_type == BATTERY_CIRCULATOR_FAN_2_PRO:
        return [mode.value for mode in BatteryCirculatorFan2ProMode]
    if device_type in _STANDARD_CIRCULATOR_FAN_TYPES:
        return [mode.value for mode in CirculatorFanMode]
    return []


def fan_restore_wind_mode_parameter(device_type: str, mode: str | None) -> str | None:
    """Return a reported mode only when it can be sent back to that fan."""
    return mode if mode in fan_writable_wind_modes(device_type) else None


def fan_night_light_parameter(device_type: str, option: str) -> str:
    """Encode an on, off, bright, or soft option for the fan's night light.

    A generic on request uses the model's bright command code.
    """
    if device_type == BATTERY_CIRCULATOR_FAN_2_PRO:
        parameters = _FAN_2_PRO_NIGHT_LIGHT_PARAMETERS
    elif device_type in _STANDARD_CIRCULATOR_FAN_TYPES:
        parameters = _STANDARD_NIGHT_LIGHT_PARAMETERS
    else:
        msg = f"unsupported fan device type for night light: {device_type!r}"
        raise ValueError(msg)

    parameter = parameters.get("bright" if option == "on" else option)
    if parameter is None:
        msg = f"unsupported fan night light option: {option!r}"
        raise ValueError(msg)
    return parameter


def fan_night_light_option(
    device_type: str, night_status: str | int | None
) -> str | None:
    """Decode nightStatus to a select option when the payload identifies one.

    Standard circulators can report both on/off and brightness codes. The
    Fan 2 Pro branch accepts the on/off report and leaves brightness unknown.
    """
    if device_type == BATTERY_CIRCULATOR_FAN_2_PRO:
        if isinstance(night_status, str) and night_status in ("on", "off"):
            return night_status
        return None
    if device_type not in _STANDARD_CIRCULATOR_FAN_TYPES:
        return None
    status = str(night_status)
    if status == CirculatorFanNightLightMode.ON.value:
        return "on"
    return next(
        (
            option
            for option, code in _STANDARD_NIGHT_LIGHT_PARAMETERS.items()
            if code == status
        ),
        None,
    )


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
