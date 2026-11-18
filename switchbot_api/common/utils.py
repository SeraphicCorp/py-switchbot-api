"""Shared device utilities."""

from math import isfinite


def integer_in_range(value: int, minimum: int, maximum: int, name: str) -> int:
    """Return an integer in the inclusive range, excluding booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{name} must be an integer"
        raise TypeError(msg)
    if not minimum <= value <= maximum:
        msg = f"{name} must be between {minimum} and {maximum}"
        raise ValueError(msg)
    return value


def finite_number(value: float, name: str) -> float:
    """Return a finite integer or float without converting its type."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        msg = f"{name} must be a number"
        raise TypeError(msg)
    if isinstance(value, float) and not isfinite(value):
        msg = f"{name} must be finite"
        raise ValueError(msg)
    return value


def rgb_component(value: int, name: str) -> int:
    """Return a validated 8-bit RGB channel value."""
    return integer_in_range(value, 0, 255, name)
