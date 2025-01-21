"""Asynchronous Python client for SwitchBot."""

from collections.abc import AsyncGenerator, Generator

from aiohttp import ClientSession
from aioresponses import aioresponses
import pytest

from switchbot_api import SwitchBotAPI
from syrupy import SnapshotAssertion

from .syrupy import SwitchBotSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the SwitchBot extension."""
    return snapshot.use_extension(SwitchBotSnapshotExtension)


@pytest.fixture
async def client() -> AsyncGenerator[SwitchBotAPI, None]:
    """Return a SwitchBot client."""
    async with (
        ClientSession() as session,
        SwitchBotAPI("token", "secret", session) as client,
    ):
        yield client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
