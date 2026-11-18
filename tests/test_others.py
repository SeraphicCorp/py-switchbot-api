"""Test other device payloads and case-sensitive infrared commands."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.common import PowerState
from switchbot_api.others import (
    AI_ART_FRAME_2,
    AI_ART_FRAME_LUMA,
    OTHERS_DEVICE_TYPES,
    WEATHER_STATION,
    ArtFrame2Commands,
    ArtFrameCommands,
    BotCommands,
    InfraredAirConditionerCommands,
    InfraredAirConditionerFanSpeed,
    InfraredAirConditionerMode,
    InfraredDVDCommands,
    InfraredFanCommands,
    InfraredIPTVStreamerCommands,
    InfraredLightCommands,
    InfraredSetTopBoxCommands,
    InfraredSpeakerCommands,
    InfraredTVCommands,
    KataFriendsCommands,
    KataFriendsMode,
    WeatherStationCommands,
    art_frame_upload_image_parameters,
    infrared_air_conditioner_parameter,
    infrared_channel_parameter,
    kata_friends_mode_parameter,
    on_off_parameter,
    weather_station_quote_parameter,
    weather_station_text_parameter,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api.common import Commands
    from tests import CommandSender


def test_device_protocol_names() -> None:
    """Use deviceType values rather than product headings."""
    assert AI_ART_FRAME_2 == "AI Art Frame 2"
    assert AI_ART_FRAME_LUMA == "AI Art Frame Luma"
    assert {AI_ART_FRAME_2, AI_ART_FRAME_LUMA}.issubset(OTHERS_DEVICE_TYPES)
    assert WEATHER_STATION == "WeatherStation"


@pytest.mark.parametrize(
    "encoded",
    ["aW1hZ2U=", "data:image/jpeg;base64,aW1hZ2U="],
)
def test_upload_base64_representation(encoded: str) -> None:
    """Preserve both forms documented for AI Art Frame 2."""
    assert art_frame_upload_image_parameters(image_base64=encoded) == {
        "imageBase64": encoded,
    }


@pytest.mark.parametrize(
    "sources",
    [
        {},
        {"image_url": "https://example.com/a.jpg", "image_base64": "aW1hZ2U="},
        {"image_url": ""},
        {"image_url": "/a.jpg"},
        {"image_url": "ftp://example.com/a.jpg"},
        {"image_base64": ""},
        {"image_base64": "%%%"},
        {"image_base64": "data:text/plain;base64,aW1hZ2U="},
        {"image_base64": "data:image/jpeg,aW1hZ2U="},
        {"image_base64": "data:image/jpeg;base64,"},
        {"image_base64": "non-ascii-\u4e2d"},
    ],
)
def test_reject_invalid_image_sources(sources: dict[str, str]) -> None:
    """Choose one valid source and reject invalid content before sending."""
    with pytest.raises(ValueError, match="image_|Base64"):
        art_frame_upload_image_parameters(**sources)


@pytest.mark.parametrize("sources", [{"image_url": 1}, {"image_base64": False}])
def test_image_source_types(sources: dict[str, Any]) -> None:
    """Avoid coercing external values into URL or Base64 fields."""
    with pytest.raises(TypeError, match="must be a string"):
        art_frame_upload_image_parameters(**sources)


@pytest.mark.parametrize(
    "mode", [InfraredAirConditionerMode.AUTO_LEGACY, InfraredAirConditionerMode.AUTO]
)
def test_air_conditioner_auto_codes(mode: InfraredAirConditionerMode) -> None:
    """Both documented auto codes retain their distinct numeric spelling."""
    assert (
        infrared_air_conditioner_parameter(
            26,
            mode,
            InfraredAirConditionerFanSpeed.MEDIUM,
            PowerState("on"),
        )
        == f"26,{mode.value},3,on"
    )


@pytest.mark.parametrize("temperature", [float("nan"), float("inf"), -float("inf")])
def test_air_conditioner_rejects_nonfinite_temperature(temperature: float) -> None:
    """NaN and infinity cannot become a valid infrared temperature string."""
    with pytest.raises(ValueError, match="finite"):
        infrared_air_conditioner_parameter(
            temperature,
            InfraredAirConditionerMode.COOL,
            InfraredAirConditionerFanSpeed.AUTO,
            PowerState.ON,
        )


@pytest.mark.parametrize(
    ("temperature", "mode", "fan", "power", "message"),
    [
        (
            True,
            InfraredAirConditionerMode.COOL,
            InfraredAirConditionerFanSpeed.AUTO,
            PowerState.ON,
            "number",
        ),
        (26, 2, InfraredAirConditionerFanSpeed.AUTO, PowerState.ON, "Mode"),
        (26, InfraredAirConditionerMode.COOL, 1, PowerState.ON, "FanSpeed"),
        (
            26,
            InfraredAirConditionerMode.COOL,
            InfraredAirConditionerFanSpeed.AUTO,
            "on",
            "PowerState",
        ),
    ],
)
def test_air_conditioner_argument_types(
    temperature: Any,
    mode: Any,
    fan: Any,
    power: Any,
    message: str,
) -> None:
    """Reject raw mode codes and booleans while using ordinary Enum members."""
    with pytest.raises(TypeError, match=message):
        infrared_air_conditioner_parameter(temperature, mode, fan, power)


@pytest.mark.parametrize("state", [PowerState.ON, PowerState.OFF])
def test_feature_switch_state(state: PowerState) -> None:
    """Shared uppercase power enums serialize as lowercase command parameters."""
    assert on_off_parameter(state) == state.name.lower()


def test_feature_switch_rejects_partial() -> None:
    """PARTIAL cannot be used for a binary Kata or infrared feature."""
    with pytest.raises(ValueError, match="ON or OFF"):
        on_off_parameter(PowerState.PARTIAL)


def test_kata_mode_requires_enum() -> None:
    """Kata modes remain case-sensitive and explicit."""
    with pytest.raises(TypeError, match="KataFriendsMode"):
        kata_friends_mode_parameter("Sleep")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("channel", "expected"), [(15, "15"), ("0015", "0015"), (0, "0")]
)
def test_channel_parameter(channel: str | int, expected: str) -> None:
    """Preserve leading zeros in a numeric channel name."""
    assert infrared_channel_parameter(channel) == expected


@pytest.mark.parametrize("channel", [-1, "", "1,2", "\uff11"])
def test_channel_digits(channel: str | int) -> None:
    """Reject non-ASCII numbers and delimiter injection."""
    with pytest.raises(ValueError, match="ASCII digits"):
        infrared_channel_parameter(channel)


@pytest.mark.parametrize("channel", [True, 1.5, None])
def test_channel_types(channel: Any) -> None:
    """Do not convert booleans or fractional numbers into channel strings."""
    with pytest.raises(TypeError, match="integer"):
        infrared_channel_parameter(channel)


@pytest.mark.parametrize("text", ["", "  "])
def test_weather_text_blank(text: str) -> None:
    """Custom display text must be nonblank."""
    with pytest.raises(ValueError, match="blank"):
        weather_station_text_parameter(text)


def test_weather_text_type() -> None:
    """Do not stringify objects as display text."""
    with pytest.raises(TypeError, match="string"):
        weather_station_text_parameter(42)  # type: ignore[arg-type]


def test_weather_station_quote_length() -> None:
    """Measure the quote limit in characters and leave customPage unrestricted."""
    text = "\u6d77" * 100
    assert weather_station_quote_parameter(text) == text
    with pytest.raises(ValueError, match="at most 100 characters"):
        weather_station_quote_parameter(text + "\u6d77")
    assert weather_station_text_parameter(text + "\u6d77") == text + "\u6d77"


@pytest.mark.parametrize(
    ("command", "parameter", "expected", "command_type"),
    [
        (BotCommands.PRESS, "default", "press", "command"),
        (BotCommands.ON, "default", "turnOn", "command"),
        (
            ArtFrameCommands.UPLOAD_IMAGE,
            art_frame_upload_image_parameters(image_url="https://example.com/a.jpg"),
            "uploadImage",
            "command",
        ),
        (
            ArtFrame2Commands.UPLOAD_IMAGE,
            art_frame_upload_image_parameters(image_base64="aW1hZ2U="),
            "uploadImage",
            "command",
        ),
        (
            WeatherStationCommands.CUSTOM_QUOTE,
            weather_station_quote_parameter("\u6d77" * 100),
            "customQuote",
            "command",
        ),
        (
            WeatherStationCommands.CUSTOM_PAGE,
            weather_station_text_parameter("  Hello, world!  "),
            "customPage",
            "command",
        ),
        (
            KataFriendsCommands.SET_MODE,
            kata_friends_mode_parameter(KataFriendsMode.SLEEP),
            "mode",
            "command",
        ),
        (
            KataFriendsCommands.SET_CHILD_LOCK,
            on_off_parameter(PowerState.OFF),
            "childLock",
            "command",
        ),
        (
            InfraredAirConditionerCommands.SET_ALL,
            infrared_air_conditioner_parameter(
                26.5,
                InfraredAirConditionerMode.COOL,
                InfraredAirConditionerFanSpeed.HIGH,
                PowerState.OFF,
            ),
            "setAll",
            "command",
        ),
        (
            InfraredTVCommands.SET_CHANNEL,
            infrared_channel_parameter("0015"),
            "SetChannel",
            "command",
        ),
        (InfraredIPTVStreamerCommands.CHANNEL_UP, "default", "channelAdd", "command"),
        (InfraredSetTopBoxCommands.VOLUME_DOWN, "default", "volumeSub", "command"),
        (InfraredDVDCommands.NEXT, "default", "Next", "command"),
        (InfraredSpeakerCommands.MUTE, "default", "setMute", "command"),
        (InfraredFanCommands.MIDDLE_SPEED, "default", "middleSpeed", "command"),
        (InfraredLightCommands.BRIGHTNESS_DOWN, "default", "brightnessDown", "command"),
        ("My custom button", "default", "My custom button", "customize"),
    ],
)
async def test_other_device_commands(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands | str,
    parameter: dict[str, str] | str,
    expected: str,
    command_type: str,
) -> None:
    """Verify wire casing, custom button type, and structured image parameters."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Exercise real JSON serialization to detect leaked Enum instances."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/other-id/commands", callback=capture)
    await send_command(
        "other-id",
        command,
        command_type=command_type,
        parameters=parameter,
    )
    assert captured == [
        {"command": expected, "commandType": command_type, "parameter": parameter},
    ]
