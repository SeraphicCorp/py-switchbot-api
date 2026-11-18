"""Build relay parameters and translate device-specific power codes."""

from __future__ import annotations

from switchbot_api.common import PowerState

from .models import GarageDoorStatus, RelayChannel, RelaySwitchMode, SwitchStatus


def relay_channel_parameter(channel: RelayChannel) -> str:
    """Build the channel string required by Relay 2PM on/off/toggle."""
    if not isinstance(channel, RelayChannel):
        msg = "channel must be a RelayChannel member"
        raise TypeError(msg)
    return str(channel.value)


def relay_mode_parameter(
    mode: RelaySwitchMode,
    *,
    channel: RelayChannel | None = None,
) -> str:
    """Build mode for Relay 1/1PM, or channel;mode for Relay 2PM."""
    if not isinstance(mode, RelaySwitchMode):
        msg = "mode must be a RelaySwitchMode member"
        raise TypeError(msg)
    if channel is None:
        return str(mode.value)
    return f"{relay_channel_parameter(channel)};{mode.value}"


def relay_position_parameter(position: int) -> str:
    """Build Relay 2PM roller position; 0 fully opens and 100 fully closes."""
    if isinstance(position, bool) or not isinstance(position, int):
        msg = "position must be an integer"
        raise TypeError(msg)
    if not 0 <= position <= 100:
        msg = "position must be between 0 and 100"
        raise ValueError(msg)
    return str(position)


def switch_power_state(
    status: SwitchStatus | GarageDoorStatus | int,
    *,
    garage_door: bool = False,
) -> PowerState:
    """Translate switchStatus or garage doorStatus into shared ON/OFF.

    Use garage_door=True for raw garage integers. Enum arguments carry their
    own protocol, so GarageDoorStatus.ON always means ON.
    """
    if isinstance(status, (SwitchStatus, GarageDoorStatus)):
        return PowerState[status.name]
    if isinstance(status, bool) or not isinstance(status, int):
        msg = "status must be an integer switch code or a switch status enum"
        raise TypeError(msg)
    status_type = GarageDoorStatus if garage_door else SwitchStatus
    return PowerState[status_type(status).name]
