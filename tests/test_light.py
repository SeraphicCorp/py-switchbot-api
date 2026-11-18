"""Verify lighting command compatibility with the existing HTTP client."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, get_type_hints

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.common import Commands
from switchbot_api.light import (
    CandleWarmerLampCommands,
    CeilingLightCommands,
    CeilingLightProCommands,
    ColorBulbCommands,
    FloorLampCommands,
    LightEffect,
    PermanentOutdoorLightsCommands,
    RGBICNeonRopeLightCommands,
    RGBICNeonWireRopeLightCommands,
    RGBICWWCeilingLightCommands,
    RGBICWWFloorLampCommands,
    RGBICWWLightBarsCommands,
    RGBICWWLightBarsControlMode,
    RGBICWWLightBarsMusicMode,
    RGBICWWStripLightCommands,
    StripLight3Commands,
    StripLightCommands,
    light_bars_brightness_temperature_parameters,
    light_bars_effect_color_parameters,
    light_bars_effect_speed_parameters,
    light_bars_music_color_parameters,
    light_bars_music_parameters,
    light_bars_segment_color_parameters,
    light_brightness_parameter,
    light_color_parameter,
    light_color_temperature_parameter,
    light_effect_parameters,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from collections.abc import Callable

    from tests import CommandSender


@pytest.mark.parametrize(
    "builder",
    [
        light_brightness_parameter,
        light_color_temperature_parameter,
        light_effect_parameters,
    ],
)
def test_light_command_annotations_resolve_at_runtime(
    builder: Callable[..., object],
) -> None:
    """Resolve command annotations to the canonical V2 command base."""
    assert get_type_hints(builder)["command"] is Commands


@pytest.mark.parametrize(
    "command",
    [
        CeilingLightCommands.SET_BRIGHTNESS,
        StripLightCommands.SET_BRIGHTNESS,
        RGBICWWCeilingLightCommands.SET_COLOR_LIGHT_BRIGHTNESS,
    ],
)
def test_light_brightness_rejects_zero_for_one_based_commands(
    command: Commands,
) -> None:
    """Avoid using the zero-based brightness range for other commands."""
    with pytest.raises(ValueError, match="brightness must be between 1 and 100"):
        light_brightness_parameter(command, 0)


def test_combined_brightness_range_is_distinct() -> None:
    """Standalone Light Bars brightness accepts zero; the combined command does not."""
    assert light_brightness_parameter(RGBICWWLightBarsCommands.SET_BRIGHTNESS, 0) == 0
    with pytest.raises(ValueError, match="brightness must be between 1 and 100"):
        light_bars_brightness_temperature_parameters(0, 3000)


@pytest.mark.parametrize(
    ("builder", "value", "message"),
    [
        (light_bars_effect_speed_parameters, 0, "speed must be between 1 and 255"),
        (light_bars_effect_speed_parameters, 256, "speed must be between 1 and 255"),
        (
            lambda index: light_bars_segment_color_parameters(index, "0:0:0"),
            12,
            "light_index must be between 0 and 11",
        ),
    ],
)
def test_light_bars_command_bounds(
    builder: Callable[[int], dict[str, int] | dict[str, int | str]],
    value: int,
    message: str,
) -> None:
    """Maintain the independent limits for speed and segment indexes."""
    with pytest.raises(ValueError, match=message):
        builder(value)


def test_rgb_parameter_validation() -> None:
    """Apply RGB limits to scalar commands and arrays alike."""
    with pytest.raises(TypeError, match="red must be an integer"):
        light_color_parameter(red=True, green=0, blue=0)
    with pytest.raises(ValueError, match="green must be between 0 and 255"):
        light_bars_music_color_parameters(["0:256:0"])
    with pytest.raises(ValueError, match="R:G:B"):
        light_bars_music_color_parameters(["#aabbcc"])
    with pytest.raises(TypeError, match="color_list must be a sequence"):
        light_bars_music_color_parameters("0:0:0")


def test_light_bars_style_uses_an_independent_code() -> None:
    """The same named preset and its algorithm style have distinct wire codes."""
    with pytest.raises(TypeError, match="style must be an integer"):
        light_bars_effect_color_parameters(
            LightEffect.ROMANCE,  # type: ignore[arg-type]
            ["0:255:0"],
        )
    assert light_bars_effect_color_parameters(0, ["0:255:0"])["style"] == 0
    assert light_bars_effect_color_parameters(63, ["0:255:0"])["style"] == 63
    with pytest.raises(ValueError, match="effect_id must be between 0 and 25"):
        light_effect_parameters(RGBICWWLightBarsCommands.SET_LIGHT_EFFECT, 53)


def test_unlisted_effect_ids_are_not_limited_to_shared_presets() -> None:
    """A documented integer effectId does not establish a shared preset table."""
    command = RGBICNeonWireRopeLightCommands.SET_LIGHT_EFFECT
    assert light_effect_parameters(command, 53) == {"effectId": 53}
    with pytest.raises(TypeError, match="effect_id must be an integer"):
        light_effect_parameters(command, LightEffect.ROMANCE)


@pytest.mark.parametrize(
    ("command", "parameters", "expected_command", "expected_parameter"),
    [
        (
            CandleWarmerLampCommands.SET_BRIGHTNESS,
            light_brightness_parameter(CandleWarmerLampCommands.SET_BRIGHTNESS, 0),
            "setBrightness",
            0,
        ),
        (
            CeilingLightCommands.SET_COLOR_TEMPERATURE,
            light_color_temperature_parameter(
                CeilingLightCommands.SET_COLOR_TEMPERATURE, 2700
            ),
            "setColorTemperature",
            2700,
        ),
        (CeilingLightProCommands.ON, "default", "turnOn", "default"),
        (
            ColorBulbCommands.SET_COLOR,
            light_color_parameter(255, 0, 1),
            "setColor",
            "255:0:1",
        ),
        (FloorLampCommands.SET_BRIGHTNESS, "0", "setBrightness", "0"),
        (
            RGBICNeonRopeLightCommands.SET_LIGHT_EFFECT,
            light_effect_parameters(
                RGBICNeonRopeLightCommands.SET_LIGHT_EFFECT, LightEffect.CHERRY_BLOSSOM
            ),
            "setLightEffect",
            {"effectId": 25},
        ),
        (
            RGBICNeonWireRopeLightCommands.SET_COLOR,
            "0:0:255",
            "setColor",
            "0:0:255",
        ),
        (
            RGBICWWFloorLampCommands.SET_LIGHT_EFFECT,
            {"effectId": LightEffect.VITALITY.value},
            "setLightEffect",
            {"effectId": 1},
        ),
        (
            RGBICWWStripLightCommands.SET_LIGHT_EFFECT,
            {"effectId": LightEffect.RAINBOW.value},
            "setLightEffect",
            {"effectId": 15},
        ),
        (
            StripLightCommands.SET_BRIGHTNESS,
            light_brightness_parameter(StripLightCommands.SET_BRIGHTNESS, 1),
            "setBrightness",
            "1",
        ),
        (
            StripLight3Commands.SET_COLOR_TEMPERATURE,
            "6500",
            "setColorTemperature",
            "6500",
        ),
        (
            RGBICWWLightBarsCommands.SET_MUSIC_PARAM_MODE,
            light_bars_music_parameters(
                RGBICWWLightBarsMusicMode.ENERGY,
                50,
                100,
                RGBICWWLightBarsControlMode.PHONE,
            ),
            "setMusicParamMode",
            {
                "musicMode": 5,
                "musicLevel": 50,
                "sensitivity": 100,
                "controllerMode": 1,
            },
        ),
        (PermanentOutdoorLightsCommands.TOGGLE, "default", "toggle", "default"),
        (
            RGBICWWCeilingLightCommands.SET_COLOR_LIGHT_RGB,
            "2:3:4",
            "setColorLightRGB",
            "2:3:4",
        ),
        (
            RGBICWWLightBarsCommands.SET_BRIGHTNESS_AND_TEMPERATURE,
            light_bars_brightness_temperature_parameters(1, 2700),
            "setBrightnessAndTemperature",
            {"brightness": 1, "temperature": 2700},
        ),
        (
            RGBICWWLightBarsCommands.SET_MUSIC_COLOR_MODE,
            light_bars_music_color_parameters(("255:0:0", "0:0:255")),
            "setMusicColorMode",
            {"colorList": ["255:0:0", "0:0:255"]},
        ),
        (
            RGBICWWLightBarsCommands.SET_LIGHT_EFFECT,
            light_effect_parameters(
                RGBICWWLightBarsCommands.SET_LIGHT_EFFECT, LightEffect.ROMANCE
            ),
            "setLightEffect",
            {"effectId": 0},
        ),
        (
            RGBICWWLightBarsCommands.SET_EFFECT_COLOR_MODE,
            light_bars_effect_color_parameters(53, ["0:255:0"]),
            "setEffectColorMode",
            {"style": 53, "colorList": ["0:255:0"]},
        ),
        (
            RGBICWWLightBarsCommands.SET_EFFECT_SPEED_MODE,
            light_bars_effect_speed_parameters(255),
            "setEffectSpeedMode",
            {"speed": 255},
        ),
        (
            RGBICWWLightBarsCommands.SET_SEGMENT_COLOR_MODE,
            light_bars_segment_color_parameters(11, "0:255:128"),
            "setSegmentColorMode",
            {"color": "0:255:128", "lightIndex": 11},
        ),
        (
            RGBICWWCeilingLightCommands.ON,
            "default",
            "turnOn",
            "default",
        ),
        (
            RGBICWWCeilingLightCommands.TURN_OFF_MAIN_LIGHT,
            "default",
            "turnOffMainLight",
            "default",
        ),
    ],
)
async def test_send_lighting_command(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands,
    parameters: dict[str, Any] | str | int,
    expected_command: str,
    expected_parameter: dict[str, Any] | str | int,
) -> None:
    """New enum members and structured parameters produce the documented JSON."""
    captured: list[dict[str, Any]] = []

    def capture_request(_: str, **kwargs: Any) -> CallbackResult:
        """Capture JSON after enum parameter values are explicitly extracted."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(
            status=200,
            payload={"statusCode": 100, "body": {}, "message": "success"},
        )

    responses.post(
        f"{MOCK_URL}/devices/light-id/commands",
        callback=capture_request,
    )

    await send_command(
        "light-id",
        command,
        parameters=parameters,
    )

    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": expected_parameter,
        },
    ]
