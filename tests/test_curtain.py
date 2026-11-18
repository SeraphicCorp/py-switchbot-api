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
    blind_tilt_open_percentage,
    blind_tilt_open_percentage_parameter,
    blind_tilt_position_parameter,
    curtain_open_percentage,
    curtain_position_parameter,
    roller_shade_position_parameter,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from collections.abc import Callable

    from switchbot_api.common import Commands
    from tests import CommandSender


@pytest.mark.parametrize(
    ("slide_position", "expected"),
    [(0, 100), (20, 80), ("20", 80), ("100", 0), (None, None)],
)
def test_curtain_open_percentage(
    slide_position: int | str | None, expected: int | None
) -> None:
    """Read Curtain 3's REST string and the equivalent integer Webhook value."""
    assert curtain_open_percentage(slide_position) == expected


@pytest.mark.parametrize("slide_position", [-1, "101", "", "20.5"])
def test_curtain_open_percentage_rejects_invalid_readings(
    slide_position: int | str,
) -> None:
    """Reject malformed strings and out-of-range readings."""
    with pytest.raises(ValueError, match="slide_position"):
        curtain_open_percentage(slide_position)


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
    ("slide_position", "expected"),
    [(0, 0), (25, 50), (50, 100), (75, 50), (100, 0), (None, None)],
)
def test_blind_tilt_open_percentage(
    slide_position: int | None, expected: int | None
) -> None:
    """Read both halves of Blind Tilt travel using the Home Assistant scale."""
    assert blind_tilt_open_percentage(slide_position) == expected


@pytest.mark.parametrize(
    ("direction", "open_percentage", "expected"),
    [
        (BlindTiltDirection.UP, 0, "up;0"),
        ("Down", 1, "down;2"),
        ("UP", 49, "up;48"),
        (BlindTiltDirection.DOWN, 99, "down;98"),
        ("down", 100, "down;100"),
        (None, 48, None),
        ("unknown", 48, None),
    ],
)
def test_blind_tilt_slider_parameter(
    direction: BlindTiltDirection | str | None,
    open_percentage: int,
    expected: str | None,
) -> None:
    """Encode valid steps without guessing which way an unknown blind tilts."""
    assert blind_tilt_open_percentage_parameter(direction, open_percentage) == expected


def test_blind_tilt_slider_rejects_out_of_range_input() -> None:
    """Validate the slider before converting to an even device step."""
    with pytest.raises(ValueError, match="open_percentage must be between"):
        blind_tilt_open_percentage_parameter("up", 101)


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


@pytest.mark.parametrize(("position", "expected"), [(0, 0), (20, 20), (100, 100)])
def test_roller_shade_position(position: int, expected: int) -> None:
    """Roller Shade takes a JSON integer without direction or mode fields."""
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
    builder: Callable[[int], str | int],
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
    builder: Callable[[int], str | int],
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
            blind_tilt_open_percentage_parameter(BlindTiltDirection.DOWN, 49),
            "setPosition",
            "down;48",
        ),
        (BlindTiltCommands.FULLY_OPEN, "default", "fullyOpen", "default"),
        (
            RollerShadeCommands.SET_POSITION,
            roller_shade_position_parameter(0),
            "setPosition",
            0,
        ),
        (
            RollerShadeCommands.SET_POSITION,
            roller_shade_position_parameter(20),
            "setPosition",
            20,
        ),
        (
            RollerShadeCommands.SET_POSITION,
            roller_shade_position_parameter(100),
            "setPosition",
            100,
        ),
    ],
)
async def test_send_curtain_command(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands,
    parameter: str | int,
    expected_command: str,
    expected_parameter: str | int,
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
    await send_command(
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
