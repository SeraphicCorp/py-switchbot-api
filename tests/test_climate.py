"""Test climate payload encodings, validation, and device categorization."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.climate import (
    CLIMATE_DEVICE_TYPES,
    AirPurifierCommands,
    AirPurifierFanGear,
    AirPurifierMode,
    EvaporativeHumidifierCommands,
    EvaporativeHumidifierMode,
    HumidifierCommands,
    HumidifierMode,
    SmartRadiatorThermostatCommands,
    SmartRadiatorThermostatMode,
    air_purifier_child_lock_parameter,
    air_purifier_mode_parameters,
    evaporative_humidifier_child_lock_parameter,
    evaporative_humidifier_mode_parameters,
    humidifier_mode_parameter,
    thermostat_mode_parameter,
    thermostat_temperature_parameter,
)
from switchbot_api.fan import FAN_DEVICE_TYPES
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from collections.abc import Callable

    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands


def test_device_categories_do_not_overlap() -> None:
    """Fans and the other climate devices belong to separate type lists."""
    assert set(FAN_DEVICE_TYPES).isdisjoint(CLIMATE_DEVICE_TYPES)


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        (HumidifierMode.AUTO, "auto"),
        (HumidifierMode.LOW, "101"),
        (0, "0"),
        (100, "100"),
        (101, "101"),
        (102, "102"),
        (103, "103"),
    ],
)
def test_humidifier_modes(mode: HumidifierMode | int, expected: str) -> None:
    """Support percentage endpoints, auto, and the three special preset codes."""
    assert humidifier_mode_parameter(mode) == expected


@pytest.mark.parametrize("value", [-1, 104])
def test_humidifier_rejects_invalid_mode_code(value: int) -> None:
    """Reject integers that are neither percentages nor documented presets."""
    with pytest.raises(ValueError, match="must be between"):
        humidifier_mode_parameter(value)


@pytest.mark.parametrize("value", [True, 1.5, "auto", None])
def test_humidifier_rejects_untyped_mode(value: Any) -> None:
    """Do not silently coerce invalid preset or percentage types."""
    with pytest.raises(TypeError, match="must be an integer"):
        humidifier_mode_parameter(value)


@pytest.mark.parametrize("humidity", [0, 100])
def test_evaporative_humidifier_payload(humidity: int) -> None:
    """Use targetHumidify, including the API spelling and integer value types."""
    assert evaporative_humidifier_mode_parameters(
        EvaporativeHumidifierMode.TARGET_HUMIDITY,
        humidity,
    ) == {"mode": 5, "targetHumidify": humidity}


@pytest.mark.parametrize("humidity", [-1, 101])
def test_evaporative_humidifier_rejects_invalid_humidity(humidity: int) -> None:
    """Enforce the documented inclusive target humidity range."""
    with pytest.raises(ValueError, match="target_humidity must be between"):
        evaporative_humidifier_mode_parameters(EvaporativeHumidifierMode.AUTO, humidity)


@pytest.mark.parametrize("humidity", [True, 50.5, "50"])
def test_evaporative_humidifier_rejects_humidity_types(humidity: Any) -> None:
    """Keep humidity a JSON integer rather than coercing external values."""
    with pytest.raises(TypeError, match="target_humidity must be an integer"):
        evaporative_humidifier_mode_parameters(EvaporativeHumidifierMode.AUTO, humidity)


def test_evaporative_humidifier_omits_none_humidity() -> None:
    """An unset target stays absent from the request object."""
    assert evaporative_humidifier_mode_parameters(
        EvaporativeHumidifierMode.SLEEP, target_humidity=None
    ) == {"mode": 6}


def test_evaporative_humidifier_requires_mode_enum() -> None:
    """Require an explicit mode enum for the structured parameter."""
    with pytest.raises(TypeError, match="EvaporativeHumidifierMode member"):
        evaporative_humidifier_mode_parameters(5, 50)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("mode", "gear", "expected"),
    [
        (AirPurifierMode.NORMAL, AirPurifierFanGear.LOW, {"mode": 1, "fanGear": 1}),
        (AirPurifierMode.NORMAL, AirPurifierFanGear.HIGH, {"mode": 1, "fanGear": 3}),
        (AirPurifierMode.AUTO, None, {"mode": 2}),
        (AirPurifierMode.SLEEP, None, {"mode": 3}),
        (AirPurifierMode.PET, None, {"mode": 4}),
    ],
)
def test_air_purifier_mode_payload(
    mode: AirPurifierMode,
    gear: AirPurifierFanGear | None,
    expected: dict[str, int],
) -> None:
    """Send fanGear in NORMAL mode and omit it for automatic modes."""
    assert air_purifier_mode_parameters(mode, gear) == expected


def test_air_purifier_normal_requires_gear() -> None:
    """The NORMAL parameter builder requires an explicit fan level."""
    with pytest.raises(ValueError, match="fan_gear is required"):
        air_purifier_mode_parameters(AirPurifierMode.NORMAL)


def test_air_purifier_auto_rejects_gear() -> None:
    """Do not send a fanGear override in a mode that forbids it."""
    with pytest.raises(ValueError, match="only be set in NORMAL"):
        air_purifier_mode_parameters(AirPurifierMode.AUTO, AirPurifierFanGear.LOW)


def test_air_purifier_rejects_raw_mode() -> None:
    """Require a mode enum instead of an unchecked raw integer."""
    with pytest.raises(TypeError, match="AirPurifierMode member"):
        air_purifier_mode_parameters(1)  # type: ignore[arg-type]


def test_air_purifier_rejects_raw_gear() -> None:
    """Require an explicitly selected gear enum."""
    with pytest.raises(TypeError, match="AirPurifierFanGear member"):
        air_purifier_mode_parameters(AirPurifierMode.NORMAL, 2)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("builder", "enabled", "expected"),
    [
        (evaporative_humidifier_child_lock_parameter, True, "true"),
        (evaporative_humidifier_child_lock_parameter, False, "false"),
        (air_purifier_child_lock_parameter, True, "1"),
        (air_purifier_child_lock_parameter, False, "0"),
    ],
)
def test_child_lock_encodings(
    builder: Callable[..., str],
    *,
    enabled: bool,
    expected: str,
) -> None:
    """Retain each device family's distinct boolean or numeric encoding."""
    assert builder(enabled=enabled) == expected


@pytest.mark.parametrize(
    "builder",
    [evaporative_humidifier_child_lock_parameter, air_purifier_child_lock_parameter],
)
@pytest.mark.parametrize("value", [0, 1, "false", None])
def test_child_lock_rejects_non_boolean(
    builder: Callable[..., str], value: Any
) -> None:
    """Avoid interpreting nonempty strings or integers as enabled booleans."""
    with pytest.raises(TypeError, match="enabled must be a boolean"):
        builder(enabled=value)


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        (SmartRadiatorThermostatMode.SCHEDULE, "0"),
        (SmartRadiatorThermostatMode.FAST_HEATING, "5"),
    ],
)
def test_thermostat_mode(mode: SmartRadiatorThermostatMode, expected: str) -> None:
    """Convert ordinary numeric enums into scalar strings."""
    assert thermostat_mode_parameter(mode) == expected


def test_thermostat_rejects_untyped_mode() -> None:
    """Require the thermostat mode enum."""
    with pytest.raises(TypeError, match="SmartRadiatorThermostatMode member"):
        thermostat_mode_parameter(1)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("value", "expected"),
    [(4, "4"), (35, "35"), (20.5, "20.5"), (20.123456789, "20.123456789")],
)
def test_thermostat_temperature(value: float, expected: str) -> None:
    """Accept range endpoints and preserve precision without inventing a step."""
    assert thermostat_temperature_parameter(value) == expected


@pytest.mark.parametrize(
    "value", [3.9, 35.1, float("nan"), float("inf"), -float("inf")]
)
def test_thermostat_rejects_invalid_temperature(value: float) -> None:
    """Reject out-of-range and non-finite targets."""
    with pytest.raises(ValueError, match="between 4 and 35"):
        thermostat_temperature_parameter(value)


@pytest.mark.parametrize("value", [True, "20", None])
def test_thermostat_rejects_temperature_types(value: Any) -> None:
    """Do not coerce boolean or text values into heating targets."""
    with pytest.raises(TypeError, match="temperature must be a number"):
        thermostat_temperature_parameter(value)


@pytest.mark.parametrize(
    ("command", "parameter", "expected_command", "expected_parameter"),
    [
        (HumidifierCommands.ON, "default", "turnOn", "default"),
        (HumidifierCommands.SET_MODE, humidifier_mode_parameter(33), "setMode", "33"),
        (
            EvaporativeHumidifierCommands.SET_MODE,
            evaporative_humidifier_mode_parameters(EvaporativeHumidifierMode.AUTO),
            "setMode",
            {"mode": 7},
        ),
        (
            EvaporativeHumidifierCommands.SET_MODE,
            evaporative_humidifier_mode_parameters(
                EvaporativeHumidifierMode.TARGET_HUMIDITY, 0
            ),
            "setMode",
            {"mode": 5, "targetHumidify": 0},
        ),
        (
            EvaporativeHumidifierCommands.SET_CHILD_LOCK,
            evaporative_humidifier_child_lock_parameter(enabled=True),
            "setChildLock",
            "true",
        ),
        (
            AirPurifierCommands.SET_MODE,
            air_purifier_mode_parameters(
                AirPurifierMode.NORMAL, AirPurifierFanGear.MEDIUM
            ),
            "setMode",
            {"mode": 1, "fanGear": 2},
        ),
        (
            AirPurifierCommands.SET_MODE,
            air_purifier_mode_parameters(AirPurifierMode.AUTO),
            "setMode",
            {"mode": 2},
        ),
        (
            AirPurifierCommands.SET_CHILD_LOCK,
            air_purifier_child_lock_parameter(enabled=False),
            "setChildLock",
            "0",
        ),
        (
            SmartRadiatorThermostatCommands.SET_MODE,
            thermostat_mode_parameter(SmartRadiatorThermostatMode.MANUAL),
            "setMode",
            "1",
        ),
        (
            SmartRadiatorThermostatCommands.SET_MANUAL_MODE_TEMPERATURE,
            thermostat_temperature_parameter(20.5),
            "setManualModeTemperature",
            "20.5",
        ),
    ],
)
async def test_send_climate_command(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    parameter: dict[str, int] | str,
    expected_command: str,
    expected_parameter: dict[str, int] | str,
) -> None:
    """Encode nested JSON integers and distinct scalar parameter formats."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Ensure ordinary Enum objects never leak into JSON parameters."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/climate-id/commands", callback=capture)
    await client.send_command(
        "climate-id",
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
