"""Build model-specific vacuum command parameters without Enum JSON values."""

from __future__ import annotations

from typing import Any

from switchbot_api.common.utils import integer_in_range
from switchbot_api.vacuum.models import (
    FLOOR_CLEANING_ROBOT_S10,
    K10_PRO_COMBO,
    K20_PRO,
    ROBOT_VACUUM_K11,
    ROBOT_VACUUM_K11_PRO,
    S10_S20_DEVICE_TYPES,
    VacuumCleanMode,
    VacuumFanLevel,
    VacuumFanSpeed,
    VacuumWaterLevel,
)

_S20_DEVICE_TYPES = S10_S20_DEVICE_TYPES - {FLOOR_CLEANING_ROBOT_S10}
_MODERN_ROBOTS = S10_S20_DEVICE_TYPES | {
    K10_PRO_COMBO,
    K20_PRO,
    ROBOT_VACUUM_K11,
    ROBOT_VACUUM_K11_PRO,
}


def _fan_level(value: VacuumFanLevel | int) -> int:
    """Build a modern JSON fanLevel."""
    if isinstance(value, VacuumFanLevel):
        return int(value.value)
    return integer_in_range(value, 1, 4, "fan_level")


def _fan_level_for_preset(preset: str | None) -> VacuumFanLevel | None:
    """Resolve a preset name to its modern numeric fan level."""
    if preset is None:
        return None
    if not isinstance(preset, str):
        msg = "fan speed preset must be a string"
        raise TypeError(msg)
    return VacuumFanLevel.__members__.get(preset.upper())


def _water_level(value: VacuumWaterLevel | int) -> int:
    """Build a JSON waterLevel."""
    if isinstance(value, VacuumWaterLevel):
        return int(value.value)
    return integer_in_range(value, 1, 2, "water_level")


def _validate_modern_robot(device_type: str) -> None:
    """Require a documented startClean deviceType rather than a legacy robot."""
    if device_type not in _MODERN_ROBOTS:
        msg = "device_type must identify a documented startClean vacuum"
        raise ValueError(msg)


def vacuum_fan_speed_parameter(speed: VacuumFanSpeed | int) -> str:
    """Build legacy PowLevel (0-3), distinct from modern fanLevel (1-4)."""
    if isinstance(speed, VacuumFanSpeed):
        return str(speed.value)
    return str(integer_in_range(speed, 0, 3, "speed"))


def vacuum_volume_parameter(volume: int) -> str:
    """Build setVolume, following the command tables' inclusive 0-100 range."""
    return str(integer_in_range(volume, 0, 100, "volume"))


def vacuum_start_clean_parameters(
    device_type: str,
    mode: VacuumCleanMode,
    fan_level: VacuumFanLevel | int,
    times: int = 1,
    *,
    water_level: VacuumWaterLevel | int | None = None,
) -> dict[str, Any]:
    """Build startClean with model-specific action and nested param fields.

    S10/S20 accept sweep/sweep_mop and require waterLevel. S20 also accepts
    first_sweep_then_mop. K10 Pro Combo, K20 Pro, and K11/K11 Pro accept
    sweep/mop with fanLevel and times only.
    """
    _validate_modern_robot(device_type)
    if not isinstance(mode, VacuumCleanMode):
        msg = "mode must be a VacuumCleanMode member"
        raise TypeError(msg)
    allowed_modes = (
        {VacuumCleanMode.SWEEP, VacuumCleanMode.SWEEP_MOP}
        if device_type in S10_S20_DEVICE_TYPES
        else {VacuumCleanMode.SWEEP, VacuumCleanMode.MOP}
    )
    if device_type in _S20_DEVICE_TYPES:
        allowed_modes.add(VacuumCleanMode.FIRST_SWEEP_THEN_MOP)
    if mode not in allowed_modes:
        msg = "clean mode is not documented for this device_type"
        raise ValueError(msg)
    parameters = {
        "fanLevel": _fan_level(fan_level),
        "times": integer_in_range(times, 1, 2639999, "times"),
    }
    if device_type in S10_S20_DEVICE_TYPES:
        if water_level is None:
            msg = "water_level is required for S10/S20 startClean"
            raise ValueError(msg)
        parameters["waterLevel"] = _water_level(water_level)
    elif water_level is not None:
        msg = "water_level is not documented for this device's startClean"
        raise ValueError(msg)
    return {"action": mode.value, "param": parameters}


def vacuum_start_clean_parameters_from_preset(
    device_type: str, fan_speed: str | None = None
) -> dict[str, Any]:
    """Build the HA sweep request with a quiet fallback and 1-4 fan levels."""
    fan_level = _fan_level_for_preset(fan_speed) or VacuumFanLevel.QUIET
    water_level = VacuumWaterLevel.LOW if device_type in S10_S20_DEVICE_TYPES else None
    return vacuum_start_clean_parameters(
        device_type, VacuumCleanMode.SWEEP, fan_level, water_level=water_level
    )


def vacuum_change_parameters(
    device_type: str,
    *,
    fan_level: VacuumFanLevel | int | None = None,
    water_level: VacuumWaterLevel | int | None = None,
    times: int | None = None,
) -> dict[str, int]:
    """Build a changeParam update containing at least one supported setting."""
    _validate_modern_robot(device_type)
    parameters = {}
    if fan_level is not None:
        parameters["fanLevel"] = _fan_level(fan_level)
    if times is not None:
        parameters["times"] = integer_in_range(times, 1, 2639999, "times")
    if water_level is not None:
        if device_type == K10_PRO_COMBO:
            msg = "water_level is not documented for K10 Pro Combo changeParam"
            raise ValueError(msg)
        parameters["waterLevel"] = _water_level(water_level)
    if not parameters:
        msg = "at least one cleaning parameter is required"
        raise ValueError(msg)
    return parameters


def vacuum_change_fan_speed_parameters(
    device_type: str, fan_speed: str
) -> dict[str, int]:
    """Build the HA fan speed update with one cycle and the model's water field."""
    fan_level = _fan_level_for_preset(fan_speed)
    if fan_level is None:
        msg = f"unknown fan speed preset: {fan_speed!r}"
        raise ValueError(msg)
    water_level = None if device_type == K10_PRO_COMBO else VacuumWaterLevel.LOW
    return vacuum_change_parameters(
        device_type, fan_level=fan_level, water_level=water_level, times=1
    )


def s30_start_clean_parameters(
    action: VacuumCleanMode | str,
    fan_level: VacuumFanLevel | int,
    times: Any = 1,
    *,
    water_level: VacuumWaterLevel | int,
) -> dict[str, Any]:
    """Build S30 startClean with validated levels and a caller-supplied action.

    The documented examples use sweep and sweep_mop. The API does not define
    an action allowlist or a type and range for the JSON value of times.
    """
    if isinstance(action, VacuumCleanMode):
        action = str(action.value)
    if not isinstance(action, str):
        msg = "action must be a string or VacuumCleanMode member"
        raise TypeError(msg)
    return {
        "action": action,
        "param": {
            "fanLevel": _fan_level(fan_level),
            "waterLevel": _water_level(water_level),
            "times": times,
        },
    }


def s30_change_parameters(
    *,
    fan_level: VacuumFanLevel | int | None = None,
    water_level: VacuumWaterLevel | int | None = None,
    times: Any = None,
) -> dict[str, Any]:
    """Build a nonempty S30 changeParam update, passing supplied times through."""
    parameters: dict[str, Any] = {}
    if fan_level is not None:
        parameters["fanLevel"] = _fan_level(fan_level)
    if water_level is not None:
        parameters["waterLevel"] = _water_level(water_level)
    if times is not None:
        parameters["times"] = times
    if not parameters:
        msg = "at least one cleaning parameter is required"
        raise ValueError(msg)
    return parameters


def s30_volume_parameter(volume: int) -> int:
    """Build S30 setVolume as an integer from 0 to 100."""
    return integer_in_range(volume, 0, 100, "volume")


def s30_self_clean_parameter(code: int) -> int:
    """Build an S30 selfClean code without assuming the action for each code."""
    return integer_in_range(code, 1, 4, "code")
