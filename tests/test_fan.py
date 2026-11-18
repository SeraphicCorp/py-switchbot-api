"""Test fan command parameter differences and client integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.fan import (
    FAN_DEVICE_TYPES,
    MODERN_CEILING_FAN,
    BatteryCirculatorFan2ProCommands,
    BatteryCirculatorFan2ProMode,
    BatteryCirculatorFan2ProNightLightMode,
    BatteryCirculatorFanCommands,
    CirculatorFanCommands,
    CirculatorFanMode,
    CirculatorFanNightLightMode,
    ModernCeilingFanCommands,
    ModernCeilingFanMode,
    StandingCirculatorFanCommands,
    fan_close_delay_parameter,
    fan_wind_mode_parameter,
    fan_wind_speed_parameter,
    modern_ceiling_fan_brightness_parameter,
    modern_ceiling_fan_close_delay_parameter,
    modern_ceiling_fan_color_parameter,
    modern_ceiling_fan_color_temperature_parameter,
    modern_ceiling_fan_wind_mode_parameter,
    modern_ceiling_fan_wind_speed_parameter,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from collections.abc import Callable

    from switchbot_api.common import Commands
    from tests import CommandSender


@pytest.mark.parametrize(
    ("builder", "value", "expected"),
    [
        (fan_wind_speed_parameter, 1, "1"),
        (fan_wind_speed_parameter, 100, "100"),
        (fan_close_delay_parameter, 1, "1"),
        (fan_close_delay_parameter, 36000, "36000"),
    ],
)
def test_fan_numeric_parameters(
    builder: Callable[[int], str],
    value: int,
    expected: str,
) -> None:
    """Encode both endpoints without scaling or imposing undocumented units."""
    assert builder(value) == expected


@pytest.mark.parametrize(
    ("builder", "value"),
    [
        (fan_wind_speed_parameter, 0),
        (fan_wind_speed_parameter, 101),
        (fan_close_delay_parameter, 0),
        (fan_close_delay_parameter, 36001),
    ],
)
def test_fan_rejects_out_of_range(builder: Callable[[int], str], value: int) -> None:
    """Reject invalid speed and delay values before sending a command."""
    with pytest.raises(ValueError, match="must be between"):
        builder(value)


@pytest.mark.parametrize(
    "builder", [fan_wind_speed_parameter, fan_close_delay_parameter]
)
@pytest.mark.parametrize("value", [True, False, 1.5, "10", None])
def test_fan_rejects_non_integer_values(
    builder: Callable[[int], str],
    value: Any,
) -> None:
    """Do not coerce booleans, fractions, or strings into numeric commands."""
    with pytest.raises(TypeError, match="must be an integer"):
        builder(value)


def test_fan_2_pro_custom_is_status_only() -> None:
    """CUSTOM can be parsed from a status but must not become a wind command."""
    mode = BatteryCirculatorFan2ProMode("custom")
    with pytest.raises(ValueError, match="status-only"):
        fan_wind_mode_parameter(mode)


def test_fan_rejects_untyped_mode() -> None:
    """Use a family-specific enum instead of an unchecked string."""
    with pytest.raises(TypeError, match="fan mode enum member"):
        fan_wind_mode_parameter("direct")  # type: ignore[arg-type]


def test_ceiling_fan_discovery_and_mode() -> None:
    """Recognize the discovery type and keep webhook mode strings separate."""
    assert MODERN_CEILING_FAN == "Modern Ceiling Fan"
    assert MODERN_CEILING_FAN in FAN_DEVICE_TYPES
    assert ModernCeilingFanMode("reverse") is ModernCeilingFanMode.REVERSE
    with pytest.raises(ValueError, match="ModernCeilingFanMode"):
        ModernCeilingFanMode(1)
    with pytest.raises(ValueError, match="webhook-only"):
        modern_ceiling_fan_wind_mode_parameter(ModernCeilingFanMode("custom"))
    with pytest.raises(TypeError, match="ModernCeilingFanMode member"):
        modern_ceiling_fan_wind_mode_parameter(1)  # type: ignore[arg-type]


def test_ceiling_fan_delay_uses_positive_integer_minutes() -> None:
    """Keep the integer value without scaling or copying the older fan limit."""
    assert modern_ceiling_fan_close_delay_parameter(36_001) == 36_001
    with pytest.raises(ValueError, match="minutes must be positive"):
        modern_ceiling_fan_close_delay_parameter(0)
    with pytest.raises(TypeError, match="minutes must be an integer"):
        modern_ceiling_fan_close_delay_parameter(minutes=True)


@pytest.mark.parametrize(
    ("command", "parameter", "expected_command", "expected_parameter"),
    [
        (BatteryCirculatorFanCommands.OFF, "default", "turnOff", "default"),
        (
            BatteryCirculatorFanCommands.SET_WIND_MODE,
            fan_wind_mode_parameter(CirculatorFanMode.BABY),
            "setWindMode",
            "baby",
        ),
        (
            CirculatorFanCommands.SET_WIND_SPEED,
            fan_wind_speed_parameter(100),
            "setWindSpeed",
            "100",
        ),
        (
            StandingCirculatorFanCommands.CLOSE_DELAY,
            fan_close_delay_parameter(36000),
            "closeDelay",
            "36000",
        ),
        (
            CirculatorFanCommands.SET_NIGHT_LIGHT_MODE,
            CirculatorFanNightLightMode.BRIGHT.value,
            "setNightLightMode",
            "1",
        ),
        (
            StandingCirculatorFanCommands.SET_NIGHT_LIGHT_MODE,
            CirculatorFanNightLightMode.DIM.value,
            "setNightLightMode",
            "2",
        ),
        (BatteryCirculatorFan2ProCommands.ON, "default", "turnOn", "default"),
        (
            BatteryCirculatorFan2ProCommands.SET_WIND_MODE,
            fan_wind_mode_parameter(BatteryCirculatorFan2ProMode.HURRICANE),
            "setWindMode",
            "hurricane",
        ),
        (
            BatteryCirculatorFan2ProCommands.SET_NIGHT_LIGHT_MODE,
            BatteryCirculatorFan2ProNightLightMode.BRIGHT.value,
            "setNightLightMode",
            "0",
        ),
        (
            BatteryCirculatorFan2ProCommands.SET_NIGHT_LIGHT_MODE,
            BatteryCirculatorFan2ProNightLightMode.SOFT.value,
            "setNightLightMode",
            "1",
        ),
        (ModernCeilingFanCommands.ON, "default", "turnOn", "default"),
        (ModernCeilingFanCommands.OFF, "default", "turnOff", "default"),
        (ModernCeilingFanCommands.TOGGLE, "default", "toggle", "default"),
        (ModernCeilingFanCommands.FAN_ON, "default", "turnOnFan", "default"),
        (ModernCeilingFanCommands.FAN_OFF, "default", "turnOffFan", "default"),
        (
            ModernCeilingFanCommands.SET_WIND_MODE,
            modern_ceiling_fan_wind_mode_parameter(ModernCeilingFanMode.REVERSE),
            "setWindMode",
            "reverse",
        ),
        (
            ModernCeilingFanCommands.SET_WIND_SPEED,
            modern_ceiling_fan_wind_speed_parameter(100),
            "setWindSpeed",
            100,
        ),
        (
            ModernCeilingFanCommands.CLOSE_DELAY,
            modern_ceiling_fan_close_delay_parameter(30),
            "closeDelay",
            30,
        ),
        (
            ModernCeilingFanCommands.MAIN_LIGHT_ON,
            "default",
            "turnOnMainLight",
            "default",
        ),
        (
            ModernCeilingFanCommands.MAIN_LIGHT_OFF,
            "default",
            "turnOffMainLight",
            "default",
        ),
        (
            ModernCeilingFanCommands.SET_MAIN_BRIGHTNESS,
            modern_ceiling_fan_brightness_parameter(0),
            "setMainBrightness",
            0,
        ),
        (
            ModernCeilingFanCommands.BACK_LIGHT_ON,
            "default",
            "turnOnBackLight",
            "default",
        ),
        (
            ModernCeilingFanCommands.BACK_LIGHT_OFF,
            "default",
            "turnOffBackLight",
            "default",
        ),
        (
            ModernCeilingFanCommands.SET_BACK_BRIGHTNESS,
            modern_ceiling_fan_brightness_parameter(100),
            "setBackBrightness",
            100,
        ),
        (
            ModernCeilingFanCommands.SET_COLOR_TEMPERATURE,
            modern_ceiling_fan_color_temperature_parameter(4000),
            "setColorTemperature",
            4000,
        ),
        (
            ModernCeilingFanCommands.SET_COLOR,
            modern_ceiling_fan_color_parameter(255, 0, 80),
            "setColor",
            "255:0:80",
        ),
    ],
)
async def test_send_fan_command(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands,
    parameter: str | int,
    expected_command: str,
    expected_parameter: str | int,
) -> None:
    """Preserve the distinct circulator and ceiling fan request formats."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Record mock request JSON."""
        captured.append(kwargs["json"])
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/fan-id/commands", callback=capture)
    await send_command(
        "fan-id",
        command,
        parameters=parameter,
    )
    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": expected_parameter,
        }
    ]
