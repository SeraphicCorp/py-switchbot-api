"""Camera device constants from the SwitchBot API v1.1 specifications.

Discovery, status, and webhook payloads remain ordinary dictionaries.
Indoor Cam and Pan/Tilt Cam expose detection webhooks, using WoCamera and
WoPanTiltCam as webhook device types. The 2K and Plus 2K/3K variants document
discovery only. Outdoor Pan/Tilt Cam 3K exposes latestImage in its status.

Solar Pan/Tilt Cam 2K and Video Doorbell expose firmware, battery, and boolean
online status. The Solar camera also exposes latestImage; only its outdoor
unit is listed, not the paired indoor unit. latestImage may be empty, and
expireAt is a Unix timestamp in seconds. Solar webhook timeOfSample is in
milliseconds; detectionState is absent in battery-only events and never
reports NOT_DETECTED. Video Doorbell also reports the boolean press field.

The shared DetectionState enum is defined in common.models.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/cameras
"""

from typing import Final

INDOOR_CAM: Final = "Indoor Cam"
PAN_TILT_CAM: Final = "Pan/Tilt Cam"
PAN_TILT_CAM_2K: Final = "Pan/Tilt Cam 2K"
PAN_TILT_CAM_PLUS_2K: Final = "Pan/Tilt Cam Plus 2K"
PAN_TILT_CAM_PLUS_3K: Final = "Pan/Tilt Cam Plus 3K"
OUTDOOR_PAN_TILT_CAM_3K: Final = "Outdoor Pan/Tilt Cam 3K"
SOLAR_PAN_TILT_CAM_2K: Final = "Solar Pan/Tilt Cam 2K"
VIDEO_DOORBELL: Final = "Video Doorbell"

CAMERA_DEVICE_TYPES: Final[list[str]] = [
    INDOOR_CAM,
    PAN_TILT_CAM,
    PAN_TILT_CAM_2K,
    PAN_TILT_CAM_PLUS_2K,
    PAN_TILT_CAM_PLUS_3K,
    OUTDOOR_PAN_TILT_CAM_3K,
    SOLAR_PAN_TILT_CAM_2K,
    VIDEO_DOORBELL,
]
