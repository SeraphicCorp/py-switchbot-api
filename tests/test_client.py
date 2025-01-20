"""Tests for the client."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aioresponses import aioresponses
import pytest

from tests import load_fixture
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api import SwitchBotAPI
    from syrupy import SnapshotAssertion


async def test_device_list(
    responses: aioresponses,
    client: SwitchBotAPI,
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
