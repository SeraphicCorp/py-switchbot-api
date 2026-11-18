"""Build documented climate command strings and ordinary parameter dictionaries."""

from __future__ import annotations

import re
from typing import Any

from .models import (
    AirPurifierFanGear,
    AirPurifierLightSensorMode,
    AirPurifierMode,
    EvaporativeHumidifierMode,
    HumidifierMode,
    SmartRadiatorThermostatMode,
)


def _integer_value(value: int, minimum: int, maximum: int, name: str) -> int:
    """Validate a JSON integer range without coercing floats or booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{name} must be an integer"
        raise TypeError(msg)
    if not minimum <= value <= maximum:
        msg = f"{name} must be between {minimum} and {maximum}"
        raise ValueError(msg)
    return value


def humidifier_mode_parameter(mode: HumidifierMode | int) -> str:
    """Build auto, a percentage 0-100, or a preset code 101-103."""
    if isinstance(mode, HumidifierMode):
        return str(mode.value)
    return str(_integer_value(mode, 0, 103, "mode"))


def evaporative_humidifier_mode_parameters(
    mode: EvaporativeHumidifierMode,
    target_humidity: int,
) -> dict[str, int]:
    """Build mode and targetHumidify, preserving the API's exact key spelling."""
    if not isinstance(mode, EvaporativeHumidifierMode):
        msg = "mode must be an EvaporativeHumidifierMode member"
        raise TypeError(msg)
    humidity = _integer_value(target_humidity, 0, 100, "target_humidity")
    return {"mode": mode.value, "targetHumidify": humidity}


def air_purifier_mode_parameters(
    mode: AirPurifierMode,
    fan_gear: AirPurifierFanGear | None = None,
) -> dict[str, int]:
    """Build a purifier mode; NORMAL requires a gear, other modes forbid it."""
    if not isinstance(mode, AirPurifierMode):
        msg = "mode must be an AirPurifierMode member"
        raise TypeError(msg)
    if mode is AirPurifierMode.NORMAL:
        if fan_gear is None:
            msg = "fan_gear is required for NORMAL mode"
            raise ValueError(msg)
        if not isinstance(fan_gear, AirPurifierFanGear):
            msg = "fan_gear must be an AirPurifierFanGear member"
            raise TypeError(msg)
        return {"mode": mode.value, "fanGear": fan_gear.value}
    if fan_gear is not None:
        msg = "fan_gear can only be set in NORMAL mode"
        raise ValueError(msg)
    return {"mode": mode.value}


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


def thermostat_mode_parameter(mode: SmartRadiatorThermostatMode) -> str:
    """Encode the radiator mode enum as a scalar string 0-5."""
    if not isinstance(mode, SmartRadiatorThermostatMode):
        msg = "mode must be a SmartRadiatorThermostatMode member"
        raise TypeError(msg)
    return str(mode.value)


def thermostat_temperature_parameter(temperature: float) -> str:
    """Build a finite 4-35 celsius target without imposing an undocumented step."""
    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
        msg = "temperature must be a number"
        raise TypeError(msg)
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
        "red": _integer_value(red, 0, 255, "red"),
        "green": _integer_value(green, 0, 255, "green"),
        "blue": _integer_value(blue, 0, 255, "blue"),
    }


def air_purifier_brightness_parameter(brightness: int) -> int:
    """Build the numeric purifier setBrightness parameter, including zero."""
    return _integer_value(brightness, 0, 100, "brightness")


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
        _integer_value(day, 1, 7, "weekday")
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
