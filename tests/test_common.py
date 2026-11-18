"""Tests for shared device models."""

import pytest

from switchbot_api.common import PowerState


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("ON", PowerState.ON),
        ("on", PowerState.ON),
        ("On", PowerState.ON),
        ("OFF", PowerState.OFF),
        ("off", PowerState.OFF),
        ("oFf", PowerState.OFF),
        ("PARTIAL", PowerState.PARTIAL),
        ("partial", PowerState.PARTIAL),
        ("Partial", PowerState.PARTIAL),
    ],
)
def test_parse_power_state(value: str, expected: PowerState) -> None:
    """Status power and webhook powerState values resolve to the same enum."""
    assert PowerState(value) is expected


@pytest.mark.parametrize("value", ["unknown", "", None, 1, True])
def test_reject_invalid_power_state(value: object) -> None:
    """Unknown and non-string states must not silently become ON or OFF."""
    with pytest.raises(ValueError, match="is not a valid PowerState"):
        PowerState(value)
