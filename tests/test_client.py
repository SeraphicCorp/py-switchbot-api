"""Tests for the client."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aiohttp import ClientError, ClientSession
from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api import SwitchBotAPI, SwitchBotConnectionError
from switchbot_api.commands import BotCommands, CommonCommands
from switchbot_api.light import ColorBulbCommands
from tests import load_fixture
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api.commands import Commands
    from syrupy import SnapshotAssertion
    from tests import CommandSender


@pytest.mark.parametrize(
    ("command", "expected", "command_type"),
    [
        (CommonCommands.ON, "turnOn", "command"),
        (BotCommands.PRESS, "press", "command"),
        (ColorBulbCommands.ON, "turnOn", "command"),
        ("Custom button", "Custom button", "customize"),
    ],
)
async def test_send_v1_v2_and_custom_commands(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands | str,
    expected: str,
    command_type: str,
) -> None:
    """Accept both command bases and serialize their members as wire strings."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Reject leaked enum instances through actual JSON serialization."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(status=200, payload={"statusCode": 100, "body": {}})

    responses.post(f"{MOCK_URL}/devices/command-id/commands", callback=capture)
    await send_command(
        "command-id",
        command,
        command_type=command_type,
    )
    assert captured == [
        {"command": expected, "commandType": command_type, "parameter": "default"},
    ]


async def test_providing_session(
    responses: aioresponses,
) -> None:
    """Test putting in own session."""
    responses.get(
        f"{MOCK_URL}/devices",
        status=200,
        body=load_fixture("device_list.json"),
    )
    async with ClientSession() as session:
        client = SwitchBotAPI("abc", "def", session=session)
        await client.list_devices()
        assert client.session is not None
        assert not client.session.closed
        await client.close()
        assert not client.session.closed


async def test_using_default_session(
    responses: aioresponses,
) -> None:
    """Test creating own session."""
    responses.get(
        f"{MOCK_URL}/devices",
        status=200,
        body=load_fixture("device_list.json"),
    )
    client = SwitchBotAPI("abc", "def")
    await client.list_devices()
    assert client.session is not None
    assert not client.session.closed
    await client.close()
    assert client.session.closed


async def test_client_error(
    client: SwitchBotAPI,
    responses: aioresponses,
) -> None:
    """Test client error."""

    async def response_handler(_: str, **_kwargs: Any) -> CallbackResult:
        """Response handler for this test."""
        raise ClientError

    responses.get(
        f"{MOCK_URL}/devices",
        callback=response_handler,
    )
    with pytest.raises(SwitchBotConnectionError):
        await client.list_devices()


async def test_device_list(
    client: SwitchBotAPI,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test listing devices."""
    responses.get(
        f"{MOCK_URL}/devices",
        status=200,
        body=load_fixture("device_list.json"),
    )
    assert await client.list_devices() == snapshot


@pytest.mark.parametrize(
    "device_fixture",
    [
        "curtain",
        "curtain3",
        "hub_2",
    ],
)
async def test_device_status(
    client: SwitchBotAPI,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
    device_fixture: str,
) -> None:
    """Test fetching device status."""
    responses.get(
        f"{MOCK_URL}/devices/abc/status",
        status=200,
        body=load_fixture(f"{device_fixture}.json"),
    )
    assert await client.get_status("abc") == snapshot


async def test_device_status_ir_remote(
    client: SwitchBotAPI,
    responses: aioresponses,
) -> None:
    """Test that fetching status for an IR remote does not raise.

    The SwitchBot Cloud API returns an empty body for IR remote devices
    (the docstring on ``get_status`` already notes "No status for IR
    devices"), so the unwrapped response has no ``deviceType`` key.
    Regression test: previously this raised ``KeyError: 'deviceType'``.
    """
    responses.get(
        f"{MOCK_URL}/devices/abc/status",
        status=200,
        body=load_fixture("ir_remote.json"),
    )
    assert await client.get_status("abc") == {}
