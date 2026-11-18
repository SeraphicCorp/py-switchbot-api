"""Verify lighting command compatibility with the existing HTTP client."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

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
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands


@pytest.mark.parametrize(
    ("command", "parameters", "expected_command", "expected_parameter"),
    [
        (CandleWarmerLampCommands.SET_BRIGHTNESS, "0", "setBrightness", "0"),
        (
            CeilingLightCommands.SET_COLOR_TEMPERATURE,
            "2700",
            "setColorTemperature",
            "2700",
        ),
        (CeilingLightProCommands.ON, "default", "turnOn", "default"),
        (ColorBulbCommands.SET_COLOR, "255:0:1", "setColor", "255:0:1"),
        (FloorLampCommands.SET_BRIGHTNESS, "0", "setBrightness", "0"),
        (
            RGBICNeonRopeLightCommands.SET_LIGHT_EFFECT,
            {"effectId": LightEffect.CHERRY_BLOSSOM.value},
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
        (StripLightCommands.SET_BRIGHTNESS, "1", "setBrightness", "1"),
        (
            StripLight3Commands.SET_COLOR_TEMPERATURE,
            "6500",
            "setColorTemperature",
            "6500",
        ),
        (
            RGBICWWLightBarsCommands.SET_MUSIC_PARAM_MODE,
            {
                "musicMode": RGBICWWLightBarsMusicMode.ENERGY.value,
                "musicLevel": 50,
                "sensitivity": 100,
                "controllerMode": RGBICWWLightBarsControlMode.PHONE.value,
            },
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
            {"brightness": 1, "temperature": 2700},
            "setBrightnessAndTemperature",
            {"brightness": 1, "temperature": 2700},
        ),
        (
            RGBICWWLightBarsCommands.SET_MUSIC_COLOR_MODE,
            {"colorList": ["255:0:0", "0:0:255"]},
            "setMusicColorMode",
            {"colorList": ["255:0:0", "0:0:255"]},
        ),
        (
            RGBICWWLightBarsCommands.SET_EFFECT_COLOR_MODE,
            {"style": 7, "colorList": ["0:255:0"]},
            "setEffectColorMode",
            {"style": 7, "colorList": ["0:255:0"]},
        ),
        (
            RGBICWWLightBarsCommands.SET_EFFECT_SPEED_MODE,
            {"speed": 255},
            "setEffectSpeedMode",
            {"speed": 255},
        ),
        (
            RGBICWWLightBarsCommands.SET_SEGMENT_COLOR_MODE,
            {"color": "0:255:128", "lightIndex": 11},
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
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    parameters: dict[str, Any] | str,
    expected_command: str,
    expected_parameter: dict[str, Any] | str,
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

    await client.send_command(
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
