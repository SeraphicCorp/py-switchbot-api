"""Build documented Curtain and Blind Tilt position parameter strings."""

from .models import BlindTiltDirection, CurtainMode


def _validate_position(position: int) -> None:
    """Require an integer percentage without coercing floats or booleans."""
    if isinstance(position, bool) or not isinstance(position, int):
        msg = "position must be an integer"
        raise TypeError(msg)
    if not 0 <= position <= 100:
        msg = "position must be between 0 and 100"
        raise ValueError(msg)


def curtain_position_parameter(
    position: int,
    mode: CurtainMode = CurtainMode.DEFAULT,
) -> str:
    """Build 0,mode,position for Curtain/3/4; 0 opens and 100 closes."""
    _validate_position(position)
    if not isinstance(mode, CurtainMode):
        msg = "mode must be a CurtainMode member"
        raise TypeError(msg)
    return f"0,{mode.value},{position}"


def blind_tilt_position_parameter(
    direction: BlindTiltDirection,
    position: int,
) -> str:
    """Build direction;position; even positions only, 0 closed and 100 open."""
    _validate_position(position)
    if not isinstance(direction, BlindTiltDirection):
        msg = "direction must be a BlindTiltDirection member"
        raise TypeError(msg)
    if position % 2:
        msg = "Blind Tilt position must be a multiple of 2"
        raise ValueError(msg)
    return f"{direction.value};{position}"


def roller_shade_position_parameter(position: int) -> str:
    """Build the Roller Shade position string; 0 opens and 100 closes."""
    _validate_position(position)
    return str(position)
