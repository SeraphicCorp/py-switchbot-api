"""Test camera command serialization and expiring image metadata."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.camera import (
    SolarPanTiltCam2KCommands,
    VideoDoorbellCommands,
    get_latest_image_url,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api import SwitchBotAPI
    from switchbot_api.common import Commands

IMAGE_URL = "https://example.com/latest.jpg"


@pytest.mark.parametrize(
    ("command", "expected_command"),
    [
        (VideoDoorbellCommands.ENABLE_MOTION_DETECTION, "enableMotionDetection"),
        (VideoDoorbellCommands.DISABLE_MOTION_DETECTION, "disableMotionDetection"),
        (SolarPanTiltCam2KCommands.ENABLE_MOTION_DETECTION, "enableMotionDetection"),
        (SolarPanTiltCam2KCommands.DISABLE_MOTION_DETECTION, "disableMotionDetection"),
    ],
)
async def test_send_camera_command(
    client: SwitchBotAPI,
    responses: aioresponses,
    command: Commands,
    expected_command: str,
) -> None:
    """Both camera command enums produce the documented default payload."""
    captured: list[dict[str, Any]] = []

    def capture_request(_: str, **kwargs: Any) -> CallbackResult:
        """Capture request JSON without contacting a camera."""
        captured.append(kwargs["json"])
        return CallbackResult(
            status=200,
            payload={"statusCode": 100, "body": {}, "message": "success"},
        )

    responses.post(f"{MOCK_URL}/devices/camera-id/commands", callback=capture_request)
    await client.send_command("camera-id", command)
    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": "default",
        },
    ]


@pytest.mark.parametrize(
    ("status", "now", "expected"),
    [
        ({}, 1000, None),
        ({"latestImage": {}}, 1000, None),
        ({"latestImage": None}, 1000, None),
        ({"latestImage": []}, 1000, None),
        ({"latestImage": {"imageUrl": IMAGE_URL}}, 1000, None),
        ({"latestImage": {"expireAt": 1001}}, 1000, None),
        ({"latestImage": {"imageUrl": "", "expireAt": 1001}}, 1000, None),
        ({"latestImage": {"imageUrl": 123, "expireAt": 1001}}, 1000, None),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": "1001"}}, 1000, None),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": True}}, 0, None),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": 1001.5}}, 1000, None),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": 999}}, 1000, None),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": 1000}}, 1000, None),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": 1001}}, 1000, IMAGE_URL),
        ({"latestImage": {"imageUrl": IMAGE_URL, "expireAt": 1}}, 0, IMAGE_URL),
    ],
)
def test_latest_image_url(
    status: dict[str, Any],
    now: float,
    expected: str | None,
) -> None:
    """Handle absent metadata and expiration boundaries in Unix seconds."""
    assert get_latest_image_url(status, now=now) == expected


def test_latest_image_url_uses_current_time(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default to the current clock when no explicit time is supplied."""
    monkeypatch.setattr("switchbot_api.camera.utils.time", lambda: 1000.5)
    status = {"latestImage": {"imageUrl": IMAGE_URL, "expireAt": 1001}}
    assert get_latest_image_url(status) == IMAGE_URL
    monkeypatch.setattr("switchbot_api.camera.utils.time", lambda: 1001.0)
    assert get_latest_image_url(status) is None
