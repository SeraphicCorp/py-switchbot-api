"""Build documented climate command strings and ordinary parameter dictionaries."""

from __future__ import annotations

import re
from typing import Any

from switchbot_api.climate.models import (
    AirPurifierFanGear,
    AirPurifierLightSensorMode,
    AirPurifierMode,
    EvaporativeHumidifierMode,
    HumidifierMode,
    SmartRadiatorThermostatMode,
)
from switchbot_api.common.utils import finite_number, integer_in_range, rgb_component


def humidifier_mode_parameter(mode: HumidifierMode | int) -> str:
    """Build auto, a percentage 0-100, or a preset code 101-103."""
    if isinstance(mode, HumidifierMode):
        return str(mode.value)
    return str(integer_in_range(mode, 0, 103, "mode"))


def evaporative_humidifier_mode_parameters(
    mode: EvaporativeHumidifierMode,
    target_humidity: int | None = None,
) -> dict[str, int]:
    """Build setMode with an optional targetHumidify value from 0 to 100."""
    if not isinstance(mode, EvaporativeHumidifierMode):
        msg = "mode must be an EvaporativeHumidifierMode member"
        raise TypeError(msg)
    parameters: dict[str, int] = {"mode": mode.value}
    if target_humidity is not None:
        parameters["humidity"] = integer_in_range(
            target_humidity, 0, 100, "target_humidity"
        )
    return parameters


def air_purifier_mode_parameters(
    mode: AirPurifierMode,
    fan_gear: AirPurifierFanGear | None = None,
) -> dict[str, int]:
    """Build a purifier mode with an optional gear for NORMAL mode."""
    if not isinstance(mode, AirPurifierMode):
        msg = "mode must be an AirPurifierMode member"
        raise TypeError(msg)
    if fan_gear is None:
        return {"mode": mode.value}
    if mode is not AirPurifierMode.NORMAL:
        msg = "fan_gear can only be set in NORMAL mode"
        raise ValueError(msg)
    if not isinstance(fan_gear, AirPurifierFanGear):
        msg = "fan_gear must be an AirPurifierFanGear member"
        raise TypeError(msg)
    return {"mode": mode.value, "fanGear": fan_gear.value}


def evaporative_humidifier_child_lock_parameter(*, enabled: bool) -> str:
    """Encode the Humidifier2 child lock as true/false."""
    if not isinstance(enabled, bool):
        msg = "enabled must be a boolean"
        raise TypeError(msg)
    return "true" if enabled else "false"


def air_purifier_child_lock_parameter(*, enabled: bool) -> str:
    """Encode the purifier child lock as 1/0 rather than true/false."""
    if not isinstance(enabled, bool):
        msg = "enabled must be a boolean"
        raise TypeError(msg)
    return "1" if enabled else "0"


def thermostat_mode_parameter(mode: SmartRadiatorThermostatMode) -> int:
    """Encode the radiator mode as the integer used by Home Assistant."""
    if not isinstance(mode, SmartRadiatorThermostatMode):
        msg = "mode must be a SmartRadiatorThermostatMode member"
        raise TypeError(msg)
    return mode.value


def thermostat_temperature_parameter(temperature: float) -> str:
    """Build a finite 4-35 celsius target without imposing an undocumented step."""
    temperature = finite_number(temperature, "temperature")
    if not 4 <= temperature <= 35:
        msg = "temperature must be between 4 and 35 celsius"
        raise ValueError(msg)
    return str(temperature)


def air_purifier_light_color_parameters(
    red: int,
    green: int,
    blue: int,
) -> dict[str, int]:
    """Build purifier light color as JSON RGB integers, not an R:G:B string."""
    return {
        "red": rgb_component(red, "red"),
        "green": rgb_component(green, "green"),
        "blue": rgb_component(blue, "blue"),
    }


def air_purifier_brightness_parameter(brightness: int) -> int:
    """Build the numeric purifier setBrightness parameter, including zero."""
    return integer_in_range(brightness, 0, 100, "brightness")


def air_purifier_light_sensor_parameter(mode: AirPurifierLightSensorMode) -> str:
    """Build the purifier's on/off/steadyMode light-sensor setting."""
    if not isinstance(mode, AirPurifierLightSensorMode):
        msg = "mode must be an AirPurifierLightSensorMode member"
        raise TypeError(msg)
    return str(mode.value)


def _auto_add_time_period(period: dict[str, Any]) -> dict[str, Any]:
    """Validate one schedule without inventing overlap or cross-midnight rules."""
    if not isinstance(period, dict):
        msg = "each period must be a dictionary"
        raise TypeError(msg)
    if set(period) != {"weekDay", "start", "end"}:
        msg = "each period must contain exactly weekDay, start, and end"
        raise ValueError(msg)
    weekdays = period["weekDay"]
    if not isinstance(weekdays, list):
        msg = "weekDay must be a list of integer weekdays"
        raise TypeError(msg)
    if not weekdays:
        msg = "weekDay must contain at least one weekday"
        raise ValueError(msg)
    for day in weekdays:
        integer_in_range(day, 1, 7, "weekday")
    for field in ("start", "end"):
        value = period[field]
        if not isinstance(value, str):
            msg = f"{field} must be a string in HH:mm format"
            raise TypeError(msg)
        if re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", value) is None:
            msg = f"{field} must be a valid time in HH:mm format"
            raise ValueError(msg)
    return {"weekDay": weekdays.copy(), "start": period["start"], "end": period["end"]}


def evaporative_humidifier_auto_add_time_parameters(
    periods: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build up to ten automatic refill periods; an empty list clears all.

    Weekdays use 1 (Monday) through 7 (Sunday), and times use HH:mm.
    Preserve supplied ordering and allow cross-midnight or overlapping periods
    because the specification does not define restrictions on those cases.
    """
    if not isinstance(periods, list):
        msg = "periods must be a list"
        raise TypeError(msg)
    if len(periods) > 10:
        msg = "periods must contain at most ten entries"
        raise ValueError(msg)
    return [_auto_add_time_period(period) for period in periods]
