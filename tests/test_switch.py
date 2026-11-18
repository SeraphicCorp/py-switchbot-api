"""Test relay wire formats and inverted garage status codes."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.common import PowerState
from switchbot_api.switch import (
    GarageDoorOpenerCommands,
    GarageDoorStatus,
    PlugCommands,
    PlugMiniEUCommands,
    PlugMiniJPCommands,
    PlugMiniUSCommands,
    RelayChannel,
    RelaySwitch1Commands,
    RelaySwitch1PMCommands,
    RelaySwitch2PMCommands,
    RelaySwitchMode,
    SwitchStatus,
    relay_channel_parameter,
    relay_mode_parameter,
    relay_position_parameter,
    switch_power_state,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands


@pytest.mark.parametrize(
    ("value", "garage", "expected"),
    [
        (0, False, PowerState.OFF),
        (1, False, PowerState.ON),
        (0, True, PowerState.ON),
        (1, True, PowerState.OFF),
        (SwitchStatus.ON, False, PowerState.ON),
        (GarageDoorStatus.ON, False, PowerState.ON),
        (GarageDoorStatus.OFF, True, PowerState.OFF),
    ],
)
def test_power_protocols(
    value: SwitchStatus | GarageDoorStatus | int,
    expected: PowerState,
    *,
    garage: bool,
) -> None:
    """The same raw number has opposite meaning in the garage protocol."""
    assert switch_power_state(value, garage_door=garage) is expected


@pytest.mark.parametrize("value", [True, "1", 1.0, None])
def test_reject_noninteger_status(value: Any) -> None:
    """Avoid treating booleans or floating-point power measurements as state."""
    with pytest.raises(TypeError, match="status must be"):
        switch_power_state(value)


@pytest.mark.parametrize("value", [-1, 2])
def test_reject_unknown_status_code(value: int) -> None:
    """Unknown status codes must not silently become ON."""
    with pytest.raises(ValueError, match="SwitchStatus"):
        switch_power_state(value)


@pytest.mark.parametrize(
    ("mode", "expected"),
    [(RelaySwitchMode.TOGGLE, "0"), (RelaySwitchMode.MOMENTARY, "3")],
)
def test_single_and_dual_relay_modes(mode: RelaySwitchMode, expected: str) -> None:
    """Relay 2PM uses a semicolon separator, not a comma."""
    assert relay_mode_parameter(mode) == expected
    assert relay_mode_parameter(mode, channel=RelayChannel.CHANNEL_2) == f"2;{expected}"


@pytest.mark.parametrize("channel", [1, "1", True, None])
def test_reject_raw_channels(channel: Any) -> None:
    """Use explicit channel enums so a default parameter cannot be confused."""
    with pytest.raises(TypeError, match="RelayChannel"):
        relay_channel_parameter(channel)


def test_reject_raw_relay_mode() -> None:
    """Require mode enums, consistent with the other device modules."""
    with pytest.raises(TypeError, match="RelaySwitchMode"):
        relay_mode_parameter(0)  # type: ignore[arg-type]


@pytest.mark.parametrize("position", [0, 100])
def test_relay_position_endpoints(position: int) -> None:
    """Preserve fully open and fully closed numeric endpoints."""
    assert relay_position_parameter(position) == str(position)


@pytest.mark.parametrize("position", [-1, 101])
def test_relay_position_out_of_range(position: int) -> None:
    """Reject percentages outside the documented interval."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        relay_position_parameter(position)


@pytest.mark.parametrize("position", [True, 50.5, "50"])
def test_relay_position_types(position: Any) -> None:
    """Do not coerce noninteger positions."""
    with pytest.raises(TypeError, match="must be an integer"):
        relay_position_parameter(position)


@pytest.mark.parametrize(
    ("command", "parameter", "expected"),
    [
        (PlugCommands.ON, "default", "turnOn"),
        (PlugMiniEUCommands.TOGGLE, "default", "toggle"),
        (PlugMiniJPCommands.OFF, "default", "turnOff"),
        (PlugMiniUSCommands.ON, "default", "turnOn"),
        (GarageDoorOpenerCommands.OFF, "default", "turnOff"),
        (
            RelaySwitch1Commands.SET_MODE,
            relay_mode_parameter(RelaySwitchMode.EDGE),
            "setMode",
        ),
        (
            RelaySwitch1PMCommands.SET_MODE,
            relay_mode_parameter(RelaySwitchMode.DETACHED),
            "setMode",
        ),
        (
            RelaySwitch2PMCommands.ON,
            relay_channel_parameter(RelayChannel.CHANNEL_1),
            "turnOn",
        ),
        (
            RelaySwitch2PMCommands.SET_MODE,
            relay_mode_parameter(
                RelaySwitchMode.TOGGLE, channel=RelayChannel.CHANNEL_2
            ),
            "setMode",
        ),
        (
            RelaySwitch2PMCommands.SET_POSITION,
            relay_position_parameter(0),
            "setPosition",
        ),
    ],
)
async def test_switch_command_serialization(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    parameter: str,
    expected: str,
) -> None:
    """Send ordinary command enums through the existing client as wire strings."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Capture actual JSON-serializable payloads."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/switch-id/commands", callback=capture)
    await client.send_command(
        "switch-id",
        command,
        parameters=parameter,
    )
    assert captured == [
        {"command": expected, "commandType": "command", "parameter": parameter}
    ]
