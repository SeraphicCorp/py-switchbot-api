"""Test curtain parameter formats and compatibility with the existing client."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.curtain import (
    BlindTiltCommands,
    BlindTiltDirection,
    Curtain3Commands,
    Curtain4Commands,
    CurtainCommands,
    CurtainMode,
    RollerShadeCommands,
    blind_tilt_position_parameter,
    curtain_position_parameter,
    roller_shade_position_parameter,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from collections.abc import Callable

    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands


@pytest.mark.parametrize(
    ("position", "mode", "expected"),
    [
        (0, CurtainMode.NORMAL, "0,0,0"),
        (100, CurtainMode.SILENT, "0,1,100"),
        (80, CurtainMode.DEFAULT, "0,ff,80"),
    ],
)
def test_curtain_position(position: int, mode: CurtainMode, expected: str) -> None:
    """Encode the documented modes and open/closed boundary positions."""
    assert curtain_position_parameter(position, mode) == expected


@pytest.mark.parametrize(
    ("direction", "position", "expected"),
    [
        (BlindTiltDirection.UP, 0, "up;0"),
        (BlindTiltDirection.UP, 100, "up;100"),
        (BlindTiltDirection.DOWN, 0, "down;0"),
        (BlindTiltDirection.DOWN, 48, "down;48"),
    ],
)
def test_blind_tilt_position(
    direction: BlindTiltDirection,
    position: int,
    expected: str,
) -> None:
    """Encode Blind Tilt directions with the required semicolon separator."""
    assert blind_tilt_position_parameter(direction, position) == expected


@pytest.mark.parametrize(("position", "expected"), [(0, "0"), (100, "100")])
def test_roller_shade_position(position: int, expected: str) -> None:
    """Roller Shade takes a scalar string without direction or mode fields."""
    assert roller_shade_position_parameter(position) == expected


@pytest.mark.parametrize(
    "builder",
    [
        curtain_position_parameter,
        partial(blind_tilt_position_parameter, BlindTiltDirection.UP),
        roller_shade_position_parameter,
    ],
    ids=["curtain", "blind_tilt", "roller_shade"],
)
@pytest.mark.parametrize("position", [-1, 101])
def test_reject_position_out_of_range(
    builder: Callable[[int], str],
    position: int,
) -> None:
    """Reject percentages outside the documented 0-100 range."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        builder(position)


@pytest.mark.parametrize(
    "builder",
    [
        curtain_position_parameter,
        partial(blind_tilt_position_parameter, BlindTiltDirection.UP),
        roller_shade_position_parameter,
    ],
    ids=["curtain", "blind_tilt", "roller_shade"],
)
@pytest.mark.parametrize("position", [True, False, 48.5, "48", None])
def test_reject_non_integer_position(
    builder: Callable[[int], str],
    position: Any,
) -> None:
    """Prevent invalid input from being coerced into a movement command."""
    with pytest.raises(TypeError, match="must be an integer"):
        builder(position)


@pytest.mark.parametrize("position", [1, 49, 99])
def test_reject_odd_blind_tilt_position(position: int) -> None:
    """Blind Tilt requires a multiple of two, unlike the other devices."""
    with pytest.raises(ValueError, match="multiple of 2"):
        blind_tilt_position_parameter(BlindTiltDirection.DOWN, position)


def test_reject_invalid_curtain_mode() -> None:
    """Only explicitly selected CurtainMode members are accepted."""
    with pytest.raises(TypeError, match="CurtainMode member"):
        curtain_position_parameter(50, "ff")  # type: ignore[arg-type]


def test_reject_invalid_blind_tilt_direction() -> None:
    """Reject raw direction strings instead of producing a malformed payload."""
    with pytest.raises(TypeError, match="BlindTiltDirection member"):
        blind_tilt_position_parameter("left", 50)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("command", "parameter", "expected_command", "expected_parameter"),
    [
        (
            CurtainCommands.SET_POSITION,
            curtain_position_parameter(80),
            "setPosition",
            "0,ff,80",
        ),
        (Curtain3Commands.OFF, "default", "turnOff", "default"),
        (Curtain4Commands.PAUSE, "default", "pause", "default"),
        (
            Curtain4Commands.SET_POSITION,
            curtain_position_parameter(100, CurtainMode.SILENT),
            "setPosition",
            "0,1,100",
        ),
        (
            BlindTiltCommands.SET_POSITION,
            blind_tilt_position_parameter(BlindTiltDirection.DOWN, 48),
            "setPosition",
            "down;48",
        ),
        (BlindTiltCommands.FULLY_OPEN, "default", "fullyOpen", "default"),
        (
            RollerShadeCommands.SET_POSITION,
            roller_shade_position_parameter(0),
            "setPosition",
            "0",
        ),
    ],
)
async def test_send_curtain_command(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    parameter: str,
    expected_command: str,
    expected_parameter: str,
) -> None:
    """Shared Commands members and parameter builders produce the API payload."""
    captured: list[dict[str, Any]] = []

    def capture_request(_: str, **kwargs: Any) -> CallbackResult:
        """Record the command JSON without contacting a physical device."""
        captured.append(kwargs["json"])
        return CallbackResult(
            status=200,
            payload={"statusCode": 100, "body": {}, "message": "success"},
        )

    responses.post(f"{MOCK_URL}/devices/curtain-id/commands", callback=capture_request)
    await client.send_command(
        "curtain-id",
        command,
        parameters=parameter,
    )
    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": expected_parameter,
        },
    ]
