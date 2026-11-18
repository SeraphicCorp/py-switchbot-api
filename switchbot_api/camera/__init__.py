"""Camera device support."""

from .commands import SolarPanTiltCam2KCommands, VideoDoorbellCommands
from .models import (
    CAMERA_DEVICE_TYPES,
    INDOOR_CAM,
    OUTDOOR_PAN_TILT_CAM_3K,
    PAN_TILT_CAM,
    PAN_TILT_CAM_2K,
    PAN_TILT_CAM_PLUS_2K,
    PAN_TILT_CAM_PLUS_3K,
    SOLAR_PAN_TILT_CAM_2K,
    VIDEO_DOORBELL,
)
from .utils import get_latest_image_url

__all__ = [
    "CAMERA_DEVICE_TYPES",
    "INDOOR_CAM",
    "OUTDOOR_PAN_TILT_CAM_3K",
    "PAN_TILT_CAM",
    "PAN_TILT_CAM_2K",
    "PAN_TILT_CAM_PLUS_2K",
    "PAN_TILT_CAM_PLUS_3K",
    "SOLAR_PAN_TILT_CAM_2K",
    "VIDEO_DOORBELL",
    "SolarPanTiltCam2KCommands",
    "VideoDoorbellCommands",
    "get_latest_image_url",
]
