"""Test vacuum family differences and serialized nested cleaning parameters."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.vacuum import (
    FLOOR_CLEANING_ROBOT_S10,
    FLOOR_CLEANING_ROBOT_S20,
    FLOOR_CLEANING_ROBOT_S30,
    K10_PRO_COMBO,
    K20_PRO,
    ROBOT_VACUUM_K11,
    ROBOT_VACUUM_K11_PRO,
    VACUUM_DEVICE_TYPES,
    FloorCleaningRobotS10Commands,
    FloorCleaningRobotS20Commands,
    FloorCleaningRobotS30Commands,
    K10ProComboCommands,
    K20ProCommands,
    MiniRobotVacuumK10Commands,
    MiniRobotVacuumK10ProCommands,
    RobotVacuumCleanerS1Commands,
    RobotVacuumCleanerS1PlusCommands,
    RobotVacuumK11Commands,
    RobotVacuumK11ProCommands,
    VacuumCleanMode,
    VacuumFanLevel,
    VacuumFanSpeed,
    VacuumSelfCleanMode,
    VacuumWaterLevel,
    VacuumWorkingStatus,
    s30_change_parameters,
    s30_self_clean_parameter,
    s30_start_clean_parameters,
    s30_volume_parameter,
    vacuum_change_parameters,
    vacuum_fan_speed_parameter,
    vacuum_start_clean_parameters,
    vacuum_volume_parameter,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands


@pytest.mark.parametrize(
    "device_type",
    [FLOOR_CLEANING_ROBOT_S10, FLOOR_CLEANING_ROBOT_S20],
)
def test_water_robot_clean_payload(device_type: str) -> None:
    """S10/S20 use sweep_mop and include numeric waterLevel inside param."""
    assert vacuum_start_clean_parameters(
        device_type,
        VacuumCleanMode.SWEEP_MOP,
        VacuumFanLevel.MAX,
        2639999,
        water_level=VacuumWaterLevel.HIGH,
    ) == {
        "action": "sweep_mop",
        "param": {"fanLevel": 4, "waterLevel": 2, "times": 2639999},
    }


@pytest.mark.parametrize(
    "device_type",
    [K10_PRO_COMBO, K20_PRO, ROBOT_VACUUM_K11, ROBOT_VACUUM_K11_PRO],
)
def test_modern_k_robot_clean_payload(device_type: str) -> None:
    """K-family startClean documents mop instead of sweep_mop, without water."""
    assert vacuum_start_clean_parameters(
        device_type,
        VacuumCleanMode.MOP,
        1,
    ) == {"action": "mop", "param": {"fanLevel": 1, "times": 1}}
    with pytest.raises(ValueError, match="clean mode"):
        vacuum_start_clean_parameters(device_type, VacuumCleanMode.SWEEP_MOP, 1)
    with pytest.raises(ValueError, match="water_level is not documented"):
        vacuum_start_clean_parameters(
            device_type,
            VacuumCleanMode.MOP,
            1,
            water_level=1,
        )


def test_s20_first_sweep_then_mop() -> None:
    """Accept the extra S20 action and keep the same nested water settings."""
    mode = VacuumCleanMode.FIRST_SWEEP_THEN_MOP
    assert vacuum_start_clean_parameters(
        FLOOR_CLEANING_ROBOT_S20, mode, 2, water_level=1
    ) == {
        "action": "first_sweep_then_mop",
        "param": {"fanLevel": 2, "waterLevel": 1, "times": 1},
    }


@pytest.mark.parametrize(
    "device_type",
    [
        FLOOR_CLEANING_ROBOT_S10,
        K10_PRO_COMBO,
        K20_PRO,
        ROBOT_VACUUM_K11,
        ROBOT_VACUUM_K11_PRO,
    ],
)
def test_first_sweep_then_mop_is_s20_only(device_type: str) -> None:
    """Limit the action to S20 in the modeled startClean family."""
    with pytest.raises(ValueError, match="clean mode"):
        vacuum_start_clean_parameters(
            device_type, VacuumCleanMode.FIRST_SWEEP_THEN_MOP, 1
        )


def test_water_robot_requires_valid_mode_and_water() -> None:
    """Do not accept the K-family mop code or omit S10 waterLevel."""
    with pytest.raises(ValueError, match="clean mode"):
        vacuum_start_clean_parameters(FLOOR_CLEANING_ROBOT_S10, VacuumCleanMode.MOP, 1)
    with pytest.raises(ValueError, match="water_level is required"):
        vacuum_start_clean_parameters(
            FLOOR_CLEANING_ROBOT_S10, VacuumCleanMode.SWEEP, 1
        )


@pytest.mark.parametrize(
    "settings",
    [
        {"fan_level": 0},
        {"fan_level": 5},
        {"times": 0},
        {"times": 2640000},
        {"water_level": 0},
        {"water_level": 3},
    ],
)
def test_clean_setting_ranges(settings: dict[str, int]) -> None:
    """Enforce modern levels and the documented cycle maximum."""
    values = {"fan_level": 1, "times": 1, "water_level": 1, **settings}
    with pytest.raises(ValueError, match="must be between"):
        vacuum_start_clean_parameters(
            FLOOR_CLEANING_ROBOT_S10,
            VacuumCleanMode.SWEEP,
            **values,
        )


@pytest.mark.parametrize(
    "settings",
    [{"fan_level": True}, {"times": 1.5}, {"water_level": "1"}],
)
def test_clean_setting_types(settings: dict[str, Any]) -> None:
    """Nested JSON settings require integers rather than coerced strings."""
    values = {"fan_level": 1, "times": 1, "water_level": 1, **settings}
    with pytest.raises(TypeError, match="must be an integer"):
        vacuum_start_clean_parameters(
            FLOOR_CLEANING_ROBOT_S10,
            VacuumCleanMode.SWEEP,
            **values,
        )


def test_reject_legacy_device_and_raw_mode() -> None:
    """Model checks prevent sending modern command payloads to old robots."""
    with pytest.raises(ValueError, match="startClean vacuum"):
        vacuum_start_clean_parameters("K10+", VacuumCleanMode.SWEEP, 1)
    with pytest.raises(TypeError, match="VacuumCleanMode"):
        vacuum_start_clean_parameters(K10_PRO_COMBO, "sweep", 1)  # type: ignore[arg-type]


def test_change_parameter_profiles() -> None:
    """Preserve supported full updates and reject unavailable settings or devices."""
    assert vacuum_change_parameters(
        K10_PRO_COMBO,
        fan_level=2,
        times=1,
    ) == {"fanLevel": 2, "times": 1}
    assert vacuum_change_parameters(
        K20_PRO,
        fan_level=VacuumFanLevel.STRONG,
        water_level=2,
        times=1,
    ) == {"fanLevel": 3, "waterLevel": 2, "times": 1}
    with pytest.raises(ValueError, match="not documented"):
        vacuum_change_parameters(K10_PRO_COMBO, fan_level=1, water_level=1, times=1)
    with pytest.raises(ValueError, match="startClean vacuum"):
        vacuum_change_parameters("Robot Vacuum Cleaner S1", times=1)


@pytest.mark.parametrize(
    ("device_type", "settings", "expected"),
    [
        (FLOOR_CLEANING_ROBOT_S10, {"fan_level": 2}, {"fanLevel": 2}),
        (FLOOR_CLEANING_ROBOT_S20, {"times": 1}, {"times": 1}),
        (K10_PRO_COMBO, {"fan_level": VacuumFanLevel.STRONG}, {"fanLevel": 3}),
        (K20_PRO, {"water_level": 2}, {"waterLevel": 2}),
        (ROBOT_VACUUM_K11, {"times": 2639999}, {"times": 2639999}),
        (
            ROBOT_VACUUM_K11_PRO,
            {"water_level": VacuumWaterLevel.LOW},
            {"waterLevel": 1},
        ),
    ],
)
def test_single_setting_change(
    device_type: str,
    settings: dict[str, Any],
    expected: dict[str, int],
) -> None:
    """Build a changeParam object without resending other settings."""
    assert vacuum_change_parameters(device_type, **settings) == expected


@pytest.mark.parametrize(
    "device_type", [FLOOR_CLEANING_ROBOT_S10, ROBOT_VACUUM_K11_PRO]
)
def test_empty_setting_change(device_type: str) -> None:
    """Require at least one parameter for a changeParam update."""
    with pytest.raises(ValueError, match="at least one"):
        vacuum_change_parameters(device_type)


@pytest.mark.parametrize(
    "settings",
    [{"fan_level": 0}, {"water_level": 3}, {"times": 2640000}],
)
def test_partial_change_still_validates(settings: dict[str, int]) -> None:
    """Partial updates obey the same numeric bounds as full updates."""
    with pytest.raises(ValueError, match="must be between"):
        vacuum_change_parameters(FLOOR_CLEANING_ROBOT_S10, **settings)


@pytest.mark.parametrize(
    "settings",
    [{"fan_level": True}, {"water_level": "1"}, {"times": 1.5}],
)
def test_partial_change_rejects_invalid_types(settings: dict[str, Any]) -> None:
    """Reject invalid supplied values even when only one field is sent."""
    with pytest.raises(TypeError, match="must be an integer"):
        vacuum_change_parameters(FLOOR_CLEANING_ROBOT_S10, **settings)


def test_s30_clean_parameters() -> None:
    """Preserve S30-specific pass-through fields and numeric cleaning levels."""
    assert FLOOR_CLEANING_ROBOT_S30 == "Robot Vacuum Cleaner S30"
    assert FLOOR_CLEANING_ROBOT_S30 in VACUUM_DEVICE_TYPES
    assert s30_start_clean_parameters(
        VacuumCleanMode.SWEEP_MOP, VacuumFanLevel.STANDARD, water_level=1
    ) == {"action": "sweep_mop", "param": {"fanLevel": 2, "waterLevel": 1, "times": 1}}
    assert s30_start_clean_parameters("customAction", 1, "2", water_level=2) == {
        "action": "customAction",
        "param": {"fanLevel": 1, "waterLevel": 2, "times": "2"},
    }
    assert s30_change_parameters(water_level=VacuumWaterLevel.HIGH) == {"waterLevel": 2}
    assert s30_change_parameters(times=3_000_000) == {"times": 3_000_000}


def test_s30_change_parameter_validation() -> None:
    """Reject empty changes and invalid levels without imposing legacy times bounds."""
    with pytest.raises(ValueError, match="at least one"):
        s30_change_parameters()
    with pytest.raises(TypeError, match="fan_level must be an integer"):
        s30_change_parameters(fan_level=True)
    with pytest.raises(ValueError, match="water_level must be between 1 and 2"):
        s30_change_parameters(water_level=3)


def test_s30_rejects_nonstring_action() -> None:
    """The action remains a wire string even though its values are open."""
    with pytest.raises(TypeError, match="action must be a string"):
        s30_start_clean_parameters(1, 2, water_level=1)  # type: ignore[arg-type]


@pytest.mark.parametrize("code", [1, 2, 3, 4])
def test_s30_self_clean_codes(code: int) -> None:
    """Send documented code numbers while leaving their semantics unspecified."""
    assert s30_self_clean_parameter(code) == code


@pytest.mark.parametrize("code", [True, "1", 1.0])
def test_s30_self_clean_requires_an_integer(code: Any) -> None:
    """Reject strings and booleans that would otherwise resemble a valid code."""
    with pytest.raises(TypeError, match="code must be an integer"):
        s30_self_clean_parameter(code)


@pytest.mark.parametrize("code", [0, 5])
def test_s30_self_clean_rejects_unsupported_codes(code: int) -> None:
    """Restrict the wire code range to the four documented values."""
    with pytest.raises(ValueError, match="between 1 and 4"):
        s30_self_clean_parameter(code)


@pytest.mark.parametrize(
    ("speed", "expected"),
    [(0, "0"), (3, "3"), (VacuumFanSpeed.QUIET, "0"), (VacuumFanSpeed.MAX, "3")],
)
def test_legacy_fan_speed(speed: VacuumFanSpeed | int, expected: str) -> None:
    """Legacy PowLevel includes zero and ends at three, unlike modern levels."""
    assert vacuum_fan_speed_parameter(speed) == expected


@pytest.mark.parametrize("speed", [-1, 4])
def test_legacy_speed_range(speed: int) -> None:
    """Never reuse modern MAX=4 as a legacy PowLevel."""
    with pytest.raises(ValueError, match="between 0 and 3"):
        vacuum_fan_speed_parameter(speed)


@pytest.mark.parametrize("speed", [True, "1", 1.5, VacuumFanLevel.MAX])
def test_legacy_speed_type(speed: Any) -> None:
    """Reject the wrong family's enum and coercible external values."""
    with pytest.raises(TypeError, match="integer"):
        vacuum_fan_speed_parameter(speed)


@pytest.mark.parametrize("volume", [0, 100])
def test_volume_endpoints(volume: int) -> None:
    """Include zero, explicitly allowed in command parameter tables."""
    assert vacuum_volume_parameter(volume) == str(volume)


@pytest.mark.parametrize("volume", [-1, 101])
def test_volume_range(volume: int) -> None:
    """Do not send volumes outside the supported interval."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        vacuum_volume_parameter(volume)


@pytest.mark.parametrize("volume", [True, "50", 50.0])
def test_volume_type(volume: Any) -> None:
    """Volume parameters originate from exact integers."""
    with pytest.raises(TypeError, match="integer"):
        vacuum_volume_parameter(volume)


@pytest.mark.parametrize(
    ("command", "parameter", "expected"),
    [
        (
            RobotVacuumCleanerS1Commands.SET_FAN_SPEED,
            vacuum_fan_speed_parameter(VacuumFanSpeed.QUIET),
            "PowLevel",
        ),
        (RobotVacuumCleanerS1PlusCommands.START, "default", "start"),
        (MiniRobotVacuumK10Commands.STOP, "default", "stop"),
        (MiniRobotVacuumK10ProCommands.DOCK, "default", "dock"),
        (
            FloorCleaningRobotS10Commands.START_CLEAN,
            vacuum_start_clean_parameters(
                FLOOR_CLEANING_ROBOT_S10, VacuumCleanMode.SWEEP_MOP, 4, water_level=2
            ),
            "startClean",
        ),
        (
            FloorCleaningRobotS10Commands.CHANGE_PARAMETERS,
            vacuum_change_parameters(FLOOR_CLEANING_ROBOT_S10, fan_level=2),
            "changeParam",
        ),
        (
            FloorCleaningRobotS20Commands.START_CLEAN,
            vacuum_start_clean_parameters(
                FLOOR_CLEANING_ROBOT_S20,
                VacuumCleanMode.FIRST_SWEEP_THEN_MOP,
                2,
                water_level=1,
            ),
            "startClean",
        ),
        (
            FloorCleaningRobotS20Commands.SELF_CLEAN,
            VacuumSelfCleanMode.TERMINATE.value,
            "selfClean",
        ),
        (
            FloorCleaningRobotS30Commands.START_CLEAN,
            s30_start_clean_parameters(VacuumCleanMode.SWEEP, 1, water_level=1),
            "startClean",
        ),
        (FloorCleaningRobotS30Commands.PAUSE, "default", "pause"),
        (FloorCleaningRobotS30Commands.DOCK, "default", "dock"),
        (
            FloorCleaningRobotS30Commands.SET_VOLUME,
            s30_volume_parameter(80),
            "setVolume",
        ),
        (
            FloorCleaningRobotS30Commands.SELF_CLEAN,
            s30_self_clean_parameter(4),
            "selfClean",
        ),
        (
            FloorCleaningRobotS30Commands.CHANGE_PARAMETERS,
            s30_change_parameters(fan_level=3),
            "changeParam",
        ),
        (
            FloorCleaningRobotS10Commands.ADD_WATER_FOR_HUMIDIFIER,
            "default",
            "addWaterForHumi",
        ),
        (
            K10ProComboCommands.START_CLEAN,
            vacuum_start_clean_parameters(K10_PRO_COMBO, VacuumCleanMode.MOP, 1),
            "startClean",
        ),
        (
            K20ProCommands.CHANGE_PARAMETERS,
            vacuum_change_parameters(K20_PRO, fan_level=2, water_level=1, times=2),
            "changeParam",
        ),
        (RobotVacuumK11Commands.SET_VOLUME, vacuum_volume_parameter(0), "setVolume"),
        (
            RobotVacuumK11ProCommands.CHANGE_PARAMETERS,
            vacuum_change_parameters(ROBOT_VACUUM_K11_PRO, times=2639999),
            "changeParam",
        ),
    ],
)
async def test_vacuum_command_serialization(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    parameter: dict[str, Any] | str | int,
    expected: str,
) -> None:
    """Serialize each family and accept empty success bodies without a command ID."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Serialize nested parameter objects to reject leaked Enum objects."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/vacuum-id/commands", callback=capture)
    await client.send_command(
        "vacuum-id",
        command,
        parameters=parameter,
    )
    assert captured == [
        {"command": expected, "commandType": "command", "parameter": parameter},
    ]


def test_documented_working_status_spelling() -> None:
    """Keep Clearing as the protocol value despite its unusual spelling."""
    assert VacuumWorkingStatus("Clearing") is VacuumWorkingStatus.CLEANING
