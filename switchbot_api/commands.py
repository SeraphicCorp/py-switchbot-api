"""Base Commands for SwitchBot API."""

from __future__ import annotations

from enum import Enum
from typing import TypeVar


class Commands(Enum):
    """Base command class."""

    @classmethod
    def is_supported(cls, device_type: str) -> bool:
        """Is this commands supported this device type."""
        return device_type in cls.get_supported_devices()

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return []


class CommonCommands(Commands):
    """Common commands."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    PRESS = "press"

    # Considering the wide range of CommonCommands, they are not inherited here.
    @classmethod
    def is_supported(cls, device_type: str) -> bool:
        """Is this commands supported this device type."""
        error_msg = "CommonCommands not implement this method"
        raise NotImplementedError(error_msg)

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        error_msg = "CommonCommands not implement this method"
        raise NotImplementedError(error_msg)


class BotCommands(Commands):
    """Bot commands."""

    PRESS = "press"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Bot"]


class OthersCommands(Commands):
    """Others commands."""

    CUSTOMIZE = "customize"  # Command {user-defined button name}


class CurtainCommands(Commands):
    """Curtain & Curtain3 commands."""

    SET_POSITION = "setPosition"  # parameter(str): index0,mode0,position0  e.g. 0,ff,80
    PAUSE = "pause"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Curtain", "Curtain 3"]


class LockCommands(Commands):
    """Lock commands."""

    LOCK = "lock"
    UNLOCK = "unlock"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Smart Lock", "Smart Lock Lite", "Smart Lock Pro", "Smart Lock Ultra"]


class LockV2Commands(Commands):
    """Lock commands."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Smart Lock", "Smart Lock Pro", "Smart Lock Ultra"]


class HumidifierCommands(Commands):
    """Humidifier commands."""

    # parameter: auto, set to Auto Mode
    # 101, set atomization efficiency to 34%
    # 102, set atomization efficiency to 67%
    # 103, set atomization efficiency to 100%
    SET_MODE = "setMode"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Humidifier"]


class HumidifierV2Commands(Commands):
    """Humidifier 2 commands."""

    SET_MODE = "setMode"
    SET_CHILD_LOCK = "setChildLock"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Humidifier 2"]


class AirPurifierCommands(Commands):
    """Purifier commands."""

    # Supported Device list:
    # Air Purifier VOC
    # Air Purifier Table VOC
    # Air Purifier PM2.5
    # Air Purifier Table PM2.5

    SET_MODE = "setMode"
    SET_CHILD_LOCK = "setChildLock"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return [
            "Air Purifier VOC",
            "Air Purifier Table VOC",
            "Air Purifier PM2.5",
            "Air Purifier Table PM2.5",
        ]


class AirConditionerCommands(Commands):
    """Air conditioner commands."""

    SET_ALL = "setAll"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Air Conditioner"]


class SwitchCommands(Commands):
    """Switch commands."""

    # Supported Device list:
    # Relay Switch 1
    # Relay Switch 1PM
    SET_MODE = "setMode"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Relay Switch 1", "Relay Switch 1PM"]


class Switch2PMCommands(Commands):
    """Switch commands."""

    # Supported Device list:
    # Relay Switch 2PM
    SET_MODE = "setMode"
    SET_POSITION = "setPosition"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Relay Switch 2PM"]


class RGBWLightCommands(Commands):
    """RGBWLight commands."""

    # Supported Device list:
    # Strip Light
    SET_BRIGHTNESS = "setBrightness"
    SET_COLOR = "setColor"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Strip Light"]


class RGBWWLightCommands(Commands):
    """RGBWwLight commands."""

    # Supported Device list:
    # Floor Lamp
    # Strip Light 3
    # Color Bulb
    SET_BRIGHTNESS = "setBrightness"
    SET_COLOR = "setColor"
    SET_COLOR_TEMPERATURE = "setColorTemperature"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Strip Light 3", "Floor Lamp", "Color Bulb"]


class DoorBellCommands(Commands):
    """Door Bell commands."""

    ENABLE = "enableMotionDetection"
    DISABLE = "disableMotionDetection"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Video Doorbell"]


class VacuumCommands(Commands):
    """Vacuum commands."""

    START = "start"
    STOP = "stop"
    DOCK = "dock"
    POW_LEVEL = "PowLevel"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return [
            "K10+",
            "K10+ Pro",
            "Robot Vacuum Cleaner S1",
            "Robot Vacuum Cleaner S1 Plus",
        ]


class VacuumCleanerV2Commands(Commands):
    """VacuumCleanerV2 commands."""

    # Supported Device list:
    # K20+ Pro
    # Robot Vacuum Cleaner K10+ Pro Combo
    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAM = "changeParam"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["K20+ Pro", "Robot Vacuum Cleaner K10+ Pro Combo"]


class VacuumCleanerV3Commands(Commands):
    """VacuumCleanerV3 commands."""

    # Supported Device list:
    # Floor Cleaning Robot S10
    # S20
    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAM = "changeParam"
    ADD_WATER_FOR_HUMI = "addWaterForHumi"
    SELF_CLEAN = "selfClean"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Robot Vacuum Cleaner S10", "S20"]


class CeilingLightCommands(Commands):
    """Ceiling light commands."""

    # 1-100
    SET_BRIGHTNESS = "setBrightness"
    # 2700-6500
    SET_COLOR_TEMPERATURE = "setColorTemperature"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Ceiling Light", "Ceiling Light Pro"]


class BlindTiltCommands(Commands):
    """Blind Tilt commands."""

    SET_POSITION = "setPosition"
    FULLY_OPEN = "fullyOpen"
    CLOSE_UP = "closeUp"
    CLOSE_DOWN = "closeDown"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Blind Tilt"]


class RollerShadeCommands(Commands):
    """Roller Shade commands."""

    SET_POSITION = "setPosition"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Roller Shade"]


class BatteryCirculatorFanCommands(Commands):
    """Command types for [Battery Circulator Fan] API."""

    SET_WIND_SPEED = "setWindSpeed"
    SET_WIND_MODE = "setWindMode"
    SET_NIGHT_LIGHT_MODE = "setNightLightMode"

    @classmethod
    def get_supported_devices(cls) -> list[str]:
        """Get supported devices."""
        return ["Circulator Fan", "Battery Circulator Fan"]


class TVCommands(Commands):
    """TV commands."""

    SET_CHANNEL = "SetChannel"
    VOLUME_ADD = "volumeAdd"
    VOLUME_SUB = "volumeSub"
    CHANNEL_ADD = "channelAdd"
    CHANNEL_SUB = "channelSub"


class DVDCommands(Commands):
    """DVD commands."""

    SET_MUTE = "setMute"
    FAST_FORWARD = "FastForward"
    REWIND = "Rewind"
    NEXT = "Next"
    PREVIOUS = "Previous"
    PAUSE = "Pause"
    PLAY = "Play"
    STOP = "Stop"


class SpeakerCommands(Commands):
    """Speaker commands."""

    VOLUME_ADD = "volumeAdd"
    VOLUME_SUB = "volumeSub"


class FanCommands(Commands):
    """Fan commands."""

    SWING = "swing"
    TIMER = "timer"
    LOW_SPEED = "lowSpeed"
    MIDDLE_SPEED = "middleSpeed"
    HIGH_SPEED = "highSpeed"


class LightCommands(Commands):
    """Light commands."""

    BRIGHTNESS_UP = "brightnessUp"
    BRIGHTNESS_DOWN = "brightnessDown"


T = TypeVar("T", bound=CommonCommands)
