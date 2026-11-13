"""Test Art Frame 2 commands."""

from __future__ import annotations

from typing import Any
from unittest.mock import ANY

from aioresponses import aioresponses
import pytest

from switchbot_api import ArtFrameCommands, SwitchBotAPI
from tests.const import MOCK_URL


def test_supported_devices() -> None:
    """Keep the original frame models and recognize Art Frame 2."""
    assert ArtFrameCommands.get_supported_devices() == [
        "AI Art Frame",
        "AI Art Frame Luma",
        "AI Art Frame 2",
    ]


@pytest.mark.parametrize(
    ("command", "parameter"),
    [
        (ArtFrameCommands.PREVIOUS, "default"),
        (ArtFrameCommands.NEXT, "default"),
        (ArtFrameCommands.UPLOAD, {"imageUrl": "https://example.com/art-frame-2.jpg"}),
    ],
)
async def test_commands(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: ArtFrameCommands,
    parameter: str | dict[str, Any],
) -> None:
    """Serialize the documented Art Frame 2 commands."""
    url = f"{MOCK_URL}/devices/B0E9FEC395F0/commands"
    responses.post(url, payload={"statusCode": 100, "body": {}, "message": "success"})
    await client.send_command("B0E9FEC395F0", command.value, parameters=parameter)
    responses.assert_called_once_with(
        url,
        method="POST",
        headers=ANY,
        json={
            "commandType": "command",
            "command": command.value,
            "parameter": parameter,
        },
    )
