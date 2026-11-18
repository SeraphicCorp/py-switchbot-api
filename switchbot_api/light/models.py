"""Lighting device constants and enums for SwitchBot API v1.1.

Use enum members' value attributes when building command parameter dictionaries.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/lighting
"""

from enum import Enum
from typing import Final

CANDLE_WARMER_LAMP: Final = "Candle Warmer Lamp"
CEILING_LIGHT: Final = "Ceiling Light"
CEILING_LIGHT_PRO: Final = "Ceiling Light Pro"
COLOR_BULB: Final = "Color Bulb"
FLOOR_LAMP: Final = "Floor Lamp"
RGBIC_NEON_ROPE_LIGHT: Final = "RGBIC Neon Rope Light"
RGBIC_NEON_WIRE_ROPE_LIGHT: Final = "RGBIC Neon Wire Rope Light"
RGBICWW_FLOOR_LAMP: Final = "RGBICWW Floor Lamp"
RGBICWW_STRIP_LIGHT: Final = "RGBICWW Strip Light"
STRIP_LIGHT: Final = "Strip Light"
STRIP_LIGHT_3: Final = "Strip Light 3"
RGBICWW_LIGHT_BARS: Final = "RGBICWW Light Bars"
PERMANENT_OUTDOOR_LIGHTS: Final = "Permanent Outdoor Lights"
RGBICWW_CEILING_LIGHT: Final = "RGBICWW Ceiling Light"

LIGHT_DEVICE_TYPES: Final[list[str]] = [
    CANDLE_WARMER_LAMP,
    CEILING_LIGHT,
    CEILING_LIGHT_PRO,
    COLOR_BULB,
    FLOOR_LAMP,
    RGBIC_NEON_ROPE_LIGHT,
    RGBIC_NEON_WIRE_ROPE_LIGHT,
    RGBICWW_FLOOR_LAMP,
    RGBICWW_STRIP_LIGHT,
    STRIP_LIGHT,
    STRIP_LIGHT_3,
    RGBICWW_LIGHT_BARS,
    PERMANENT_OUTDOOR_LIGHTS,
    RGBICWW_CEILING_LIGHT,
]


class LightEffect(Enum):
    """Preset IDs for Neon Rope, RGBICWW Floor/Strip, and RGBICWW Light Bars."""

    ROMANCE = 0
    VITALITY = 1
    HEARTTHROB = 2
    PARTY = 3
    DYNAMIC = 4
    MYSTERY = 5
    LIGHTNING = 6
    ROCK = 7
    STARLIGHT = 8
    VALENTINES_DAY = 9
    DREAM = 10
    ALARM = 11
    FIREWORKS = 12
    WAVES = 13
    CHRISTMAS = 14
    RAINBOW = 15
    GAME = 16
    HALLOWEEN = 17
    MEDITATION = 18
    STARLIT_SKY = 19
    SLEEP = 20
    FILM = 21
    SUNRISE = 22
    SUNSET = 23
    NEW_YEAR = 24
    CHERRY_BLOSSOM = 25


class RGBICWWLightBarsMusicMode(Enum):
    """Music modes for the Light Bars setMusicParamMode command."""

    DYNAMIC = 0
    WAVE = 1
    BLOOM = 2
    CRASH = 3
    FLOW = 4
    ENERGY = 5


class RGBICWWLightBarsControlMode(Enum):
    """Music controller modes for the Light Bars setMusicParamMode command."""

    CONTROLLER = 0
    PHONE = 1
    VOLUME = 2
