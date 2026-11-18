"""Verify Hub 4 discovery and the distinct status and webhook readings."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from switchbot_api.common import DetectionState
from switchbot_api.hub import HUB_4, HUB_4_LIGHT_LEVEL_RANGE, HUB_DEVICE_TYPES
from switchbot_api.sensor import sensor_detection_state
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from aioresponses import aioresponses

    from switchbot_api import SwitchBotAPI


async def test_hub_4_discovery_and_status(
    client: SwitchBotAPI, responses: aioresponses
) -> None:
    """Preserve the discovery name and raw status fields through the client."""
    device = {
        "deviceId": "hub-4-id",
        "deviceName": "Living room Hub",
        "deviceType": "Hub 4",
        "enableCloudService": True,
        "hubDeviceId": "",
    }
    status = {
        "deviceId": "hub-4-id",
        "deviceType": "Hub 4",
        "hubDeviceId": "hub-4-id",
        "version": "V0.5-0.3",
        "temperature": 24.4,
        "humidity": 53,
        "lightLevel": 1,
        "moveDetected": False,
        "onlineStatus": "online",
    }
    responses.get(
        f"{MOCK_URL}/devices",
        payload={
            "statusCode": 100,
            "body": {"deviceList": [device], "infraredRemoteList": []},
        },
    )
    responses.get(
        f"{MOCK_URL}/devices/hub-4-id/status",
        payload={"statusCode": 100, "body": status},
    )

    (hub,) = await client.list_devices()
    assert hub.device_type == HUB_4
    assert hub.device_type in HUB_DEVICE_TYPES
    readings = await client.get_status(hub.device_id)
    assert readings == status
    assert readings["lightLevel"] in HUB_4_LIGHT_LEVEL_RANGE
    assert sensor_detection_state(readings) is DetectionState.NOT_DETECTED


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        ("DETECTED", DetectionState.DETECTED),
        ("NOT_DETECTED", DetectionState.NOT_DETECTED),
    ],
)
def test_hub_4_webhook_motion(state: str, expected: DetectionState) -> None:
    """Parse the detectionState string from the changeReport context."""
    context = {
        "deviceType": "Hub 4",
        "scale": "CELSIUS",
        "lightLevel": 10,
        "detectionState": state,
    }
    assert context["lightLevel"] in HUB_4_LIGHT_LEVEL_RANGE
    assert 0 not in HUB_4_LIGHT_LEVEL_RANGE
    assert 11 not in HUB_4_LIGHT_LEVEL_RANGE
    assert sensor_detection_state(context) is expected
