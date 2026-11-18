"""Build documented Curtain and Blind Tilt position parameter strings."""

from switchbot_api.common.utils import integer_in_range
from switchbot_api.curtain.models import BlindTiltDirection, CurtainMode


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


def roller_shade_position_parameter(position: int) -> str:
    """Build the Roller Shade position string; 0 opens and 100 closes."""
    return str(integer_in_range(position, 0, 100, "position"))
