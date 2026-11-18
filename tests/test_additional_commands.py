"""Verify additional device commands using mocked HTTP responses."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.climate import (
    AirPurifierCommands,
    AirPurifierLightSensorMode,
    EvaporativeHumidifierCommands,
    air_purifier_brightness_parameter,
    air_purifier_light_color_parameters,
    air_purifier_light_sensor_parameter,
    evaporative_humidifier_auto_add_time_parameters,
)
from switchbot_api.common import PowerState
from switchbot_api.curtain import RollerShadeCommands
from switchbot_api.fan import (
    BatteryCirculatorFan2ProCommands,
    BatteryCirculatorFanCommands,
    CirculatorFanCommands,
    StandingCirculatorFanCommands,
    fan_oscillation_parameter,
)
from switchbot_api.light import (
    PermanentOutdoorLightsCommands,
    RGBICNeonWireRopeLightCommands,
    RGBICWWCeilingLightCommands,
)
from switchbot_api.others import (
    ArtFrame2Commands,
    ArtFrameCommands,
    ArtFrameDeleteImageMode,
    WeatherStationCommands,
    art_frame_delete_image_parameter,
    weather_station_component_parameters,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api.common import Commands
    from tests import CommandSender


@pytest.mark.parametrize(
    ("command", "parameters", "expected_command", "expected_parameter"),
    [
        (
            BatteryCirculatorFan2ProCommands.SET_OSCILLATION,
            fan_oscillation_parameter(PowerState.ON),
            "setOscillation",
            "on",
        ),
        (
            BatteryCirculatorFan2ProCommands.SET_VERTICAL_OSCILLATION,
            fan_oscillation_parameter(PowerState.OFF),
            "setVerticalOscillation",
            "off",
        ),
        (
            AirPurifierCommands.SET_LIGHT_COLOR,
            air_purifier_light_color_parameters(0, 128, 255),
            "setLightColor",
            {"red": 0, "green": 128, "blue": 255},
        ),
        (
            AirPurifierCommands.SET_BRIGHTNESS,
            air_purifier_brightness_parameter(0),
            "setBrightness",
            0,
        ),
        (
            AirPurifierCommands.SET_LIGHT_SENSOR,
            air_purifier_light_sensor_parameter(AirPurifierLightSensorMode.STEADY),
            "setLightSensor",
            "steadyMode",
        ),
        (
            EvaporativeHumidifierCommands.SET_AUTO_ADD_TIME,
            evaporative_humidifier_auto_add_time_parameters(
                [{"weekDay": [1, 5], "start": "04:12", "end": "07:12"}],
            ),
            "setAutoAddTime",
            [{"weekDay": [1, 5], "start": "04:12", "end": "07:12"}],
        ),
        (
            EvaporativeHumidifierCommands.SET_AUTO_ADD_TIME,
            evaporative_humidifier_auto_add_time_parameters([]),
            "setAutoAddTime",
            [],
        ),
        (
            WeatherStationCommands.CUSTOM_PUT_COMPONENT,
            weather_station_component_parameters(123, 66666, "Hello"),
            "customPutComponent",
            {"templateID": 123, "componentID": 66666, "text": "Hello"},
        ),
        (
            ArtFrameCommands.DELETE_IMAGE,
            art_frame_delete_image_parameter(ArtFrameDeleteImageMode.NEWEST),
            "deleteImage",
            "newest",
        ),
        (
            ArtFrame2Commands.DELETE_IMAGE,
            art_frame_delete_image_parameter(ArtFrameDeleteImageMode.OLDEST),
            "deleteImage",
            "oldest",
        ),
        (RollerShadeCommands.PAUSE, "default", "pause", "default"),
        (
            RGBICNeonWireRopeLightCommands.SET_LIGHT_EFFECT,
            {"effectId": 1},
            "setLightEffect",
            {"effectId": 1},
        ),
        (
            PermanentOutdoorLightsCommands.SET_LIGHT_EFFECT,
            {"effectId": 1},
            "setLightEffect",
            {"effectId": 1},
        ),
        (
            RGBICWWCeilingLightCommands.SET_LIGHT_EFFECT,
            {"effectId": 1},
            "setLightEffect",
            {"effectId": 1},
        ),
    ],
)
async def test_additional_command_wire_payloads(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands,
    parameters: dict[str, Any] | list[dict[str, Any]] | str | int,
    expected_command: str,
    expected_parameter: dict[str, Any] | list[dict[str, Any]] | str | int,
) -> None:
    """Keep integers, arrays, key casing, and distinct scalar formats on the wire."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Serialize the actual client payload without executing device actions."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/additional-id/commands", callback=capture)
    await send_command("additional-id", command, parameters=parameters)
    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": expected_parameter,
        },
    ]


def test_oscillation_stays_specific_to_fan_2_pro() -> None:
    """A documented status field alone does not imply a control command."""
    for commands in (
        BatteryCirculatorFanCommands,
        CirculatorFanCommands,
        StandingCirculatorFanCommands,
    ):
        assert not hasattr(commands, "SET_OSCILLATION")
        assert not hasattr(commands, "SET_VERTICAL_OSCILLATION")


@pytest.mark.parametrize(
    ("state", "expected"), [(PowerState.ON, "on"), (PowerState.OFF, "off")]
)
def test_oscillation_power_state(state: PowerState, expected: str) -> None:
    """Reuse the shared state while encoding the command's lowercase value."""
    assert fan_oscillation_parameter(state) == expected


def test_oscillation_rejects_partial() -> None:
    """Aggregate light power is not a valid binary fan setting."""
    with pytest.raises(ValueError, match="ON or OFF"):
        fan_oscillation_parameter(PowerState.PARTIAL)


@pytest.mark.parametrize("state", ["on", True, None])
def test_oscillation_rejects_untyped_state(state: Any) -> None:
    """Require an explicit common power enum rather than coercing values."""
    with pytest.raises(TypeError, match="PowerState"):
        fan_oscillation_parameter(state)


@pytest.mark.parametrize("value", [0, 255])
def test_purifier_color_endpoints(value: int) -> None:
    """Use object-shaped integer RGB endpoints for purifier lights."""
    assert air_purifier_light_color_parameters(value, value, value) == {
        "red": value,
        "green": value,
        "blue": value,
    }


@pytest.mark.parametrize("channel", ["red", "green", "blue"])
@pytest.mark.parametrize("value", [-1, 256])
def test_purifier_color_ranges(channel: str, value: int) -> None:
    """Check each individual color channel rather than validating just one."""
    values = {"red": 0, "green": 0, "blue": 0, channel: value}
    with pytest.raises(ValueError, match=f"{channel} must be between"):
        air_purifier_light_color_parameters(**values)


@pytest.mark.parametrize("value", [True, 0.5, "0"])
def test_purifier_color_types(value: Any) -> None:
    """Do not let JSON booleans or strings stand in for color components."""
    with pytest.raises(TypeError, match="integer"):
        air_purifier_light_color_parameters(value, 0, 0)


@pytest.mark.parametrize("brightness", [0, 100])
def test_purifier_brightness_endpoints(brightness: int) -> None:
    """The new command returns a JSON number, including zero brightness."""
    result = air_purifier_brightness_parameter(brightness)
    assert result == brightness
    assert isinstance(result, int)


@pytest.mark.parametrize("brightness", [-1, 101])
def test_purifier_brightness_range(brightness: int) -> None:
    """Reject out-of-range brightness before sending."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        air_purifier_brightness_parameter(brightness)


@pytest.mark.parametrize("brightness", [True, 50.5, "50"])
def test_purifier_brightness_type(brightness: Any) -> None:
    """Preserve exact integer semantics for the new numeric parameter."""
    with pytest.raises(TypeError, match="integer"):
        air_purifier_brightness_parameter(brightness)


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        (AirPurifierLightSensorMode.ON, "on"),
        (AirPurifierLightSensorMode.OFF, "off"),
        (AirPurifierLightSensorMode.STEADY, "steadyMode"),
    ],
)
def test_purifier_light_sensor_modes(
    mode: AirPurifierLightSensorMode, expected: str
) -> None:
    """Keep steadyMode capitalization distinct from generic ON/OFF."""
    assert air_purifier_light_sensor_parameter(mode) == expected


def test_purifier_light_sensor_requires_enum() -> None:
    """Do not accept arbitrary raw mode strings."""
    with pytest.raises(TypeError, match="AirPurifierLightSensorMode"):
        air_purifier_light_sensor_parameter("on")  # type: ignore[arg-type]


def test_refill_schedule_limits_and_independent_data() -> None:
    """Allow ten periods, preserve cross-midnight times, and copy weekday lists."""
    period = {"weekDay": [1, 7], "start": "23:59", "end": "00:00"}
    periods = [period] * 10
    result = evaporative_humidifier_auto_add_time_parameters(periods)
    assert result == periods
    result[0]["weekDay"].append(3)
    assert period["weekDay"] == [1, 7]
    assert result[1]["weekDay"] == [1, 7]
    with pytest.raises(ValueError, match="at most ten"):
        evaporative_humidifier_auto_add_time_parameters([period] * 11)


@pytest.mark.parametrize("periods", [None, {}, ()])
def test_refill_schedule_requires_list(periods: Any) -> None:
    """Only an explicit JSON array can express the schedule or its clearing."""
    with pytest.raises(TypeError, match="periods must be a list"):
        evaporative_humidifier_auto_add_time_parameters(periods)


@pytest.mark.parametrize(
    "period",
    [
        {},
        {"weekDay": [1], "start": "04:12"},
        {"weekDay": [1], "start": "04:12", "end": "07:12", "extra": 1},
        {"weekDay": [], "start": "04:12", "end": "07:12"},
        {"weekDay": [0], "start": "04:12", "end": "07:12"},
        {"weekDay": [8], "start": "04:12", "end": "07:12"},
        {"weekDay": [1], "start": "4:12", "end": "07:12"},
        {"weekDay": [1], "start": "24:00", "end": "07:12"},
        {"weekDay": [1], "start": "04:12", "end": "07:60"},
    ],
)
def test_refill_schedule_invalid_values(period: dict[str, Any]) -> None:
    """Validate required keys, weekdays, and strict clock-time syntax."""
    with pytest.raises(ValueError, match="period|weekDay|weekday|HH:mm"):
        evaporative_humidifier_auto_add_time_parameters([period])


@pytest.mark.parametrize(
    "period",
    [
        "not an object",
        {"weekDay": "1", "start": "04:12", "end": "07:12"},
        {"weekDay": [True], "start": "04:12", "end": "07:12"},
        {"weekDay": [1], "start": 412, "end": "07:12"},
        {"weekDay": [1], "start": "04:12", "end": None},
    ],
)
def test_refill_schedule_invalid_types(period: Any) -> None:
    """Avoid coercing external schedule data into valid-looking requests."""
    with pytest.raises(TypeError, match="dictionary|list|integer|string"):
        evaporative_humidifier_auto_add_time_parameters([period])


@pytest.mark.parametrize("mode", list(ArtFrameDeleteImageMode))
def test_frame_delete_mode(mode: ArtFrameDeleteImageMode) -> None:
    """All three single-image selection modes preserve their exact value."""
    assert art_frame_delete_image_parameter(mode) == mode.value


@pytest.mark.parametrize("mode", ["random", 1, None])
def test_frame_delete_mode_type(mode: Any) -> None:
    """Reject arbitrary selection strings before issuing destructive requests."""
    with pytest.raises(TypeError, match="ArtFrameDeleteImageMode"):
        art_frame_delete_image_parameter(mode)


@pytest.mark.parametrize("text", ["", "text", "\u4e2d" * 100])
def test_weather_component_text(text: str) -> None:
    """Allow clearing text and count Unicode characters rather than bytes."""
    assert weather_station_component_parameters(123, 66666, text) == {
        "templateID": 123,
        "componentID": 66666,
        "text": text,
    }


def test_weather_component_text_limit() -> None:
    """Reject only text exceeding the component's documented length."""
    with pytest.raises(ValueError, match="at most 100"):
        weather_station_component_parameters(123, 66666, "x" * 101)


@pytest.mark.parametrize(
    ("template_id", "component_id", "text"),
    [(True, 1, "text"), (1, "2", "text"), (1, 2, None)],
)
def test_weather_component_argument_types(
    template_id: Any, component_id: Any, text: Any
) -> None:
    """Keep numeric IDs and text types without inventing undocumented ID ranges."""
    with pytest.raises(TypeError, match="integer|string"):
        weather_station_component_parameters(template_id, component_id, text)
