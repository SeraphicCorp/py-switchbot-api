"""Convert cover positions and build device command parameters."""

from __future__ import annotations

from switchbot_api.common.utils import integer_in_range
from switchbot_api.curtain.models import BlindTiltDirection, CurtainMode


def curtain_open_percentage(slide_position: int | str | None) -> int | None:
    """Convert Curtain slidePosition to an open percentage.

    Accept an integer or its ASCII decimal string form. For example, a
    Curtain reporting "30" is 70 percent open. A missing value stays unknown.
    """
    if slide_position is None:
        return None
    if isinstance(slide_position, str):
        if not (slide_position.isascii() and slide_position.isdecimal()):
            msg = "slide_position must be an integer or an ASCII decimal string"
            raise ValueError(msg)
        slide_position = int(slide_position)
    return 100 - integer_in_range(slide_position, 0, 100, "slide_position")


def blind_tilt_open_percentage(slide_position: int | None) -> int | None:
    """Convert the distance from the fully open midpoint into a percentage.

    Positions 25 and 75 both report 50 percent open. They represent opposite
    tilt directions on the status scale, so the percentage alone loses direction.
    """
    if slide_position is None:
        return None
    position = integer_in_range(slide_position, 0, 100, "slide_position")
    return 100 - 2 * abs(position - 50)


def curtain_position_parameter(
    position: int,
    mode: CurtainMode = CurtainMode.DEFAULT,
) -> str:
    """Build 0,mode,position for Curtain/3/4; 0 opens and 100 closes."""
    integer_in_range(position, 0, 100, "position")
    if not isinstance(mode, CurtainMode):
        msg = "mode must be a CurtainMode member"
        raise TypeError(msg)
    return f"0,{mode.value},{position}"


def blind_tilt_position_parameter(
    direction: BlindTiltDirection,
    position: int,
) -> str:
    """Build direction;position; even positions only, 0 closed and 100 open."""
    integer_in_range(position, 0, 100, "position")
    if not isinstance(direction, BlindTiltDirection):
        msg = "direction must be a BlindTiltDirection member"
        raise TypeError(msg)
    if position % 2:
        msg = "Blind Tilt position must be a multiple of 2"
        raise ValueError(msg)
    return f"{direction.value};{position}"


def blind_tilt_open_percentage_parameter(
    direction: BlindTiltDirection | str | None,
    open_percentage: int,
) -> str | None:
    """Build a command for a slider value, or return None if direction is unknown.

    Resolve odd values to the lower even step, except 1 becomes 2 so only
    explicit endpoint values produce a fully closed or fully open command.
    """
    position = integer_in_range(open_percentage, 0, 100, "open_percentage")
    try:
        tilt_direction = BlindTiltDirection(
            direction.lower() if isinstance(direction, str) else direction
        )
    except ValueError:
        return None

    if position % 2:
        position = max(2, position - 1)
    return blind_tilt_position_parameter(tilt_direction, position)


def roller_shade_position_parameter(position: int) -> int:
    """Build the Roller Shade position as a JSON integer.

    The device scale still uses 0 for fully open and 100 for fully closed.
    """
    return integer_in_range(position, 0, 100, "position")
