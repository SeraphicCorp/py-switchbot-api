"""Asynchronous Python client for SwitchBot."""

from collections.abc import Generator

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
async def client() -> SwitchBotAPI:
    """Return a SwitchBot client."""
    return SwitchBotAPI("token", "secret")


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
