"""Other physical devices and infrared remote models.

Physical deviceType and virtual remoteType lists are separate. AI Art Frame 2
and AI Art Frame Luma are deviceType names used by different versions of the
same generation. Weather Station uses WeatherStation.
Shared ON/OFF and online/offline states live in common.models. MindClip uses
numeric charging codes and therefore has a separate protocol enum.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/others
"""

from enum import Enum
from typing import Final

BOT: Final = "Bot"
REMOTE: Final = "Remote"
AI_ART_FRAME: Final = "AI Art Frame"
AI_ART_FRAME_2: Final = "AI Art Frame 2"
AI_ART_FRAME_LUMA: Final = "AI Art Frame Luma"
WEATHER_STATION: Final = "WeatherStation"
KATA_FRIENDS: Final = "Kata Friends"
AI_MINDCLIP: Final = "AI MindClip"

OTHERS_DEVICE_TYPES: Final[list[str]] = [
    BOT,
    REMOTE,
    AI_ART_FRAME,
    AI_ART_FRAME_2,
    AI_ART_FRAME_LUMA,
    WEATHER_STATION,
    KATA_FRIENDS,
    AI_MINDCLIP,
]

INFRARED_AIR_CONDITIONER: Final = "Air Conditioner"
INFRARED_TV: Final = "TV"
INFRARED_IPTV_STREAMER: Final = "IPTV/Streamer"
INFRARED_SET_TOP_BOX: Final = "Set Top Box"
INFRARED_DVD: Final = "DVD"
INFRARED_SPEAKER: Final = "Speaker"
INFRARED_FAN: Final = "Fan"
INFRARED_LIGHT: Final = "Light"
INFRARED_OTHERS: Final = "Others"

INFRARED_REMOTE_TYPES: Final[list[str]] = [
    INFRARED_AIR_CONDITIONER,
    INFRARED_TV,
    INFRARED_IPTV_STREAMER,
    INFRARED_SET_TOP_BOX,
    INFRARED_DVD,
    INFRARED_SPEAKER,
    INFRARED_FAN,
    INFRARED_LIGHT,
    INFRARED_OTHERS,
]


class BotMode(Enum):
    """Bot state; power readings are meaningful only in SWITCH mode."""

    PRESS = "pressMode"
    SWITCH = "switchMode"
    CUSTOMIZE = "customizeMode"


class ArtFrameDisplayMode(Enum):
    """AI Art Frame status mode, with no documented set-mode command."""

    STATIC = 0
    SLIDESHOW = 1


class ArtFrameDeleteImageMode(Enum):
    """Choose one cloud image to delete, excluding the currently displayed one."""

    RANDOM = "random"
    NEWEST = "newest"
    OLDEST = "oldest"


class KataFriendsMode(Enum):
    """Case-sensitive Kata Friends command and status modes."""

    NORMAL = "Normal"
    STANDBY = "Standby"
    SLEEP = "Sleep"


class KataFriendsWorkStatus(Enum):
    """Kata Friends activity strings reported in status."""

    STROLLING = "Strolling"
    WELCOMING_HOME = "Welcoming Home"
    WAKE_UP_CALL = "Wake-up Call"
    SLEEPING = "Sleeping"
    PLAYING = "Playing"
    RETURNING = "Returning"


class KataFriendsServiceStatus(Enum):
    """Numeric hospitalized service states."""

    NORMAL = 0
    REPAIR = 1
    MAINTENANCE = 2
    CLEANING = 3


class MindClipChargingStatus(Enum):
    """AI MindClip integer chargingStatus; other devices use string codes."""

    UNCHARGED = 0
    CHARGING = 1


class MindClipRecordingStatus(Enum):
    """AI MindClip recordingStatus."""

    NOT_RECORDING = 0
    RECORDING = 1


class MindClipUploadStatus(Enum):
    """AI MindClip uploadStatus; zero does not mean upload completed."""

    NOT_UPLOADED = 0
    UPLOADING = 1


class MindClipTranscriptionStatus(Enum):
    """AI MindClip transcript status, including the webhook-only initial code."""

    NOT_TRANSCRIBED = 0
    TRANSCRIBING = 1
    SUCCEEDED = 2
    FAILED = 3
    TIMED_OUT = 4
    SPEECH_TRANSCRIPTION_FAILED = 5


class InfraredAirConditionerMode(Enum):
    """setAll mode codes; both 0 and 1 are documented as auto."""

    AUTO_LEGACY = 0
    AUTO = 1
    COOL = 2
    DRY = 3
    FAN = 4
    HEAT = 5


class InfraredAirConditionerFanSpeed(Enum):
    """setAll fan speed codes."""

    AUTO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
