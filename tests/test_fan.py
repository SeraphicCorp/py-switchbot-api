"""Test fan command parameter differences and client integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.fan import (
    BatteryCirculatorFan2ProCommands,
    BatteryCirculatorFan2ProMode,
    BatteryCirculatorFan2ProNightLightMode,
    BatteryCirculatorFanCommands,
    CirculatorFanCommands,
    CirculatorFanMode,
    CirculatorFanNightLightMode,
    StandingCirculatorFanCommands,
    fan_close_delay_parameter,
    fan_wind_mode_parameter,
    fan_wind_speed_parameter,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from collections.abc import Callable

    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands


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
    ],
)
async def test_send_fan_command(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    parameter: str,
    expected_command: str,
    expected_parameter: str,
) -> None:
    """Preserve family-specific modes and nightlight codes in the HTTP body."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Record mock request JSON."""
        captured.append(kwargs["json"])
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/fan-id/commands", callback=capture)
    # The existing client's TypeVar is narrower than its runtime Commands check.
    await client.send_command(
        "fan-id",
        command,  # type: ignore[arg-type]
        parameters=parameter,
    )
    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": expected_parameter,
        }
    ]
