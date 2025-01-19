"""Tests for the client."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

import aiohttp
from aiohttp import ClientError
from aiohttp.hdrs import METH_GET, METH_POST
from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api import SwitchBotAPI
from tests import load_fixture
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from syrupy import SnapshotAssertion



async def test_device_list(
    responses: aioresponses,
    client: SwitchBotAPI,
    snapshot: SnapshotAssertion,
) -> None:
    """Test searching for media."""
    responses.get(
        f"{MOCK_URL}/devices",
        status=200,
        body=load_fixture("device_list.json"),
    )
    assert await client.list_devices() == snapshot
    # responses.assert_called_once_with(
    #     f"{MOCK_URL}/search",
    #     METH_GET,
    #     headers=HEADERS,
    #     params={"query": "frosty"},
    #     json=None,
    # )