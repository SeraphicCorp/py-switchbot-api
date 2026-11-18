"""Documented camera commands from the SwitchBot API v1.1 specifications.

Only Video Doorbell and Solar Pan/Tilt Cam 2K document device control commands.
Both use commandType command and parameter default. Other camera types have
no documented control commands, including no image-refresh or PTZ command.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/cameras
"""

from switchbot_api.common import Commands


class VideoDoorbellCommands(Commands):
    """Enable or disable Video Doorbell motion detection."""

    ENABLE_MOTION_DETECTION = "enableMotionDetection"
    DISABLE_MOTION_DETECTION = "disableMotionDetection"


class SolarPanTiltCam2KCommands(Commands):
    """Enable or disable motion detection on the Solar camera outdoor unit."""

    ENABLE_MOTION_DETECTION = "enableMotionDetection"
    DISABLE_MOTION_DETECTION = "disableMotionDetection"
