"""Asynchronous Python client for SwitchBot."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from switchbot_api.commands import Commands


class CommandSender(Protocol):
    """Runtime command signature exercised by the HTTP serialization tests."""

    async def __call__(
        self,
        device_id: str,
        command: Commands | str,
        command_type: str = "command",
        parameters: dict[str, Any] | list[dict[str, Any]] | str | int = "default",
    ) -> None:
        """Send the given command and parameter to the client."""
        ...


def load_fixture(filename: str) -> str:
    """Load a fixture."""
    path = Path(__package__) / "fixtures" / filename
    return path.read_text(encoding="utf-8")
