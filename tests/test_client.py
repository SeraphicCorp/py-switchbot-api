"""Tests for the client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from aiohttp import ClientError
from aioresponses import aioresponses, CallbackResult

from tests import load_fixture
from tests.const import MOCK_URL

from switchbot_api import SwitchBotConnectionError

if TYPE_CHECKING:
    from switchbot_api import SwitchBotAPI
    from syrupy import SnapshotAssertion


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
