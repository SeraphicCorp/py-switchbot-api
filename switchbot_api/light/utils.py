"""Build lighting command parameters with device-specific bounds and types."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Final

from switchbot_api.common.utils import integer_in_range, rgb_component

from .commands import (
    CandleWarmerLampCommands,
    CeilingLightCommands,
    CeilingLightProCommands,
    ColorBulbCommands,
    FloorLampCommands,
    PermanentOutdoorLightsCommands,
    RGBICNeonRopeLightCommands,
    RGBICNeonWireRopeLightCommands,
    RGBICWWCeilingLightCommands,
    RGBICWWFloorLampCommands,
    RGBICWWLightBarsCommands,
    RGBICWWStripLightCommands,
    StripLight3Commands,
    StripLightCommands,
)
from .models import LightEffect, RGBICWWLightBarsControlMode, RGBICWWLightBarsMusicMode

if TYPE_CHECKING:
    from switchbot_api.common import Commands

# Brightness bounds follow the public command tables.
_BRIGHTNESS_MINIMUMS: Final[dict[Commands, int]] = {
    CandleWarmerLampCommands.SET_BRIGHTNESS: 0,
    CeilingLightCommands.SET_BRIGHTNESS: 1,
    CeilingLightProCommands.SET_BRIGHTNESS: 1,
    ColorBulbCommands.SET_BRIGHTNESS: 1,
    FloorLampCommands.SET_BRIGHTNESS: 0,
    PermanentOutdoorLightsCommands.SET_BRIGHTNESS: 0,
    RGBICNeonRopeLightCommands.SET_BRIGHTNESS: 0,
    RGBICNeonWireRopeLightCommands.SET_BRIGHTNESS: 0,
    RGBICWWCeilingLightCommands.SET_MAIN_LIGHT_BRIGHTNESS: 1,
    RGBICWWCeilingLightCommands.SET_COLOR_LIGHT_BRIGHTNESS: 1,
    RGBICWWFloorLampCommands.SET_BRIGHTNESS: 0,
    RGBICWWLightBarsCommands.SET_BRIGHTNESS: 0,
    RGBICWWStripLightCommands.SET_BRIGHTNESS: 0,
    StripLight3Commands.SET_BRIGHTNESS: 0,
    StripLightCommands.SET_BRIGHTNESS: 1,
}
_TEMPERATURE_COMMANDS: Final[frozenset[Commands]] = frozenset(
    {
        CeilingLightCommands.SET_COLOR_TEMPERATURE,
        CeilingLightProCommands.SET_COLOR_TEMPERATURE,
        ColorBulbCommands.SET_COLOR_TEMPERATURE,
        FloorLampCommands.SET_COLOR_TEMPERATURE,
        PermanentOutdoorLightsCommands.SET_COLOR_TEMPERATURE,
        RGBICWWCeilingLightCommands.SET_MAIN_LIGHT_COLOR_TEMP,
        RGBICWWFloorLampCommands.SET_COLOR_TEMPERATURE,
        RGBICWWLightBarsCommands.SET_COLOR_TEMPERATURE,
        RGBICWWStripLightCommands.SET_COLOR_TEMPERATURE,
        StripLight3Commands.SET_COLOR_TEMPERATURE,
    }
)
_STRING_SCALAR_COMMANDS: Final[frozenset[Commands]] = frozenset(
    {
        ColorBulbCommands.SET_BRIGHTNESS,
        ColorBulbCommands.SET_COLOR_TEMPERATURE,
        StripLightCommands.SET_BRIGHTNESS,
    }
)
_PRESET_EFFECT_COMMANDS: Final[frozenset[Commands]] = frozenset(
    {
        RGBICNeonRopeLightCommands.SET_LIGHT_EFFECT,
        RGBICWWFloorLampCommands.SET_LIGHT_EFFECT,
        RGBICWWLightBarsCommands.SET_LIGHT_EFFECT,
        RGBICWWStripLightCommands.SET_LIGHT_EFFECT,
    }
)
_UNLISTED_EFFECT_COMMANDS: Final[frozenset[Commands]] = frozenset(
    {
        PermanentOutdoorLightsCommands.SET_LIGHT_EFFECT,
        RGBICNeonWireRopeLightCommands.SET_LIGHT_EFFECT,
        RGBICWWCeilingLightCommands.SET_LIGHT_EFFECT,
    }
)


def light_brightness_parameter(command: Commands, brightness: int) -> int | str:
    """Build a scalar brightness parameter using the command's lower bound."""
    minimum = _BRIGHTNESS_MINIMUMS.get(command)
    if minimum is None:
        msg = "command must be a scalar lighting brightness command"
        raise ValueError(msg)
    value = integer_in_range(brightness, minimum, 100, "brightness")
    return str(value) if command in _STRING_SCALAR_COMMANDS else value


def light_color_temperature_parameter(command: Commands, temperature: int) -> int | str:
    """Build a scalar 2700-6500 Kelvin parameter for a lighting command."""
    if command not in _TEMPERATURE_COMMANDS:
        msg = "command must be a scalar lighting color temperature command"
        raise ValueError(msg)
    value = integer_in_range(temperature, 2700, 6500, "temperature")
    return str(value) if command in _STRING_SCALAR_COMMANDS else value


def light_color_parameter(red: int, green: int, blue: int) -> str:
    """Build the R:G:B string used by lighting color commands."""
    red = rgb_component(red, "red")
    green = rgb_component(green, "green")
    blue = rgb_component(blue, "blue")
    return f"{red}:{green}:{blue}"


def _integer_code(value: int, name: str) -> int:
    """Validate a wire code whose range is unspecified."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{name} must be an integer"
        raise TypeError(msg)
    return value


def light_effect_parameters(
    command: Commands, effect_id: LightEffect | int
) -> dict[str, int]:
    """Build setLightEffect; only apply preset bounds where documented."""
    if command in _PRESET_EFFECT_COMMANDS:
        if isinstance(effect_id, LightEffect):
            return {"effectId": int(effect_id.value)}
        return {"effectId": integer_in_range(effect_id, 0, 25, "effect_id")}
    if command in _UNLISTED_EFFECT_COMMANDS:
        if isinstance(effect_id, LightEffect):
            msg = "effect_id must be an integer for this device's undocumented presets"
            raise TypeError(msg)
        return {"effectId": _integer_code(effect_id, "effect_id")}
    msg = "command must be a lighting setLightEffect command"
    raise ValueError(msg)


def _validate_color(color: str) -> str:
    """Validate an existing R:G:B string while preserving its spelling."""
    if not isinstance(color, str):
        msg = "color must be a string in R:G:B format"
        raise TypeError(msg)
    components = color.split(":")
    if len(components) != 3 or any(
        not (1 <= len(component) <= 3 and component.isascii() and component.isdecimal())
        for component in components
    ):
        msg = "color must contain three ASCII decimal channels in R:G:B format"
        raise ValueError(msg)
    red, green, blue = components
    light_color_parameter(int(red), int(green), int(blue))
    return color


def _color_list(colors: Sequence[str]) -> list[str]:
    """Validate the RGB strings and return a JSON array."""
    if not isinstance(colors, Sequence) or isinstance(colors, (str, bytes, bytearray)):
        msg = "color_list must be a sequence of R:G:B strings"
        raise TypeError(msg)
    return [_validate_color(color) for color in colors]


def light_bars_brightness_temperature_parameters(
    brightness: int, temperature: int
) -> dict[str, int]:
    """Build setBrightnessAndTemperature using its documented 1-100 range."""
    return {
        "brightness": integer_in_range(brightness, 1, 100, "brightness"),
        "temperature": integer_in_range(temperature, 2700, 6500, "temperature"),
    }


def light_bars_music_color_parameters(
    color_list: Sequence[str],
) -> dict[str, list[str]]:
    """Build setMusicColorMode with a colorList of RGB strings."""
    return {"colorList": _color_list(color_list)}


def light_bars_music_parameters(
    music_mode: RGBICWWLightBarsMusicMode | int,
    music_level: int,
    sensitivity: int,
    controller_mode: RGBICWWLightBarsControlMode | int,
) -> dict[str, int]:
    """Build setMusicParamMode using numeric codes and validated percentages."""
    if isinstance(music_mode, RGBICWWLightBarsMusicMode):
        music_mode = int(music_mode.value)
    if isinstance(controller_mode, RGBICWWLightBarsControlMode):
        controller_mode = int(controller_mode.value)
    return {
        "musicMode": integer_in_range(music_mode, 0, 5, "music_mode"),
        "musicLevel": integer_in_range(music_level, 1, 100, "music_level"),
        "sensitivity": integer_in_range(sensitivity, 1, 100, "sensitivity"),
        "controllerMode": integer_in_range(controller_mode, 0, 2, "controller_mode"),
    }


def light_bars_effect_color_parameters(
    style: int, color_list: Sequence[str]
) -> dict[str, int | list[str]]:
    """Build setEffectColorMode using an integer algorithm style code.

    Style is independent from LightEffect, whose members identify presets.
    The referenced protocol assigns more than one preset to some style codes.
    """
    return {
        "style": _integer_code(style, "style"),
        "colorList": _color_list(color_list),
    }


def light_bars_effect_speed_parameters(speed: int) -> dict[str, int]:
    """Build setEffectSpeedMode with an integer speed from 1 to 255."""
    return {"speed": integer_in_range(speed, 1, 255, "speed")}


def light_bars_segment_color_parameters(
    light_index: int, color: str
) -> dict[str, int | str]:
    """Build setSegmentColorMode for a Light Bars segment indexed from 0 to 11."""
    return {
        "lightIndex": integer_in_range(light_index, 0, 11, "light_index"),
        "color": _validate_color(color),
    }
