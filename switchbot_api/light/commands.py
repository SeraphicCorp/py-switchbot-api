"""Lighting commands from the SwitchBot API v1.1 device specifications.

Each enum inherits the shared Commands class. Pass a member or its ``value``
to the client; parameter shapes and ranges are noted alongside each command.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/lighting
"""

from switchbot_api.common import Commands


class CandleWarmerLampCommands(Commands):
    """Commands for Candle Warmer Lamp.

    Source: devices/lighting/candle-warmer-lamp.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100 in the public command table; Feishu lists 1-100.
    SET_BRIGHTNESS = "setBrightness"


class CeilingLightCommands(Commands):
    """Commands for Ceiling Light.

    Source: devices/lighting/ceiling-light.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 1-100 in the public command table; Feishu lists 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"


class CeilingLightProCommands(Commands):
    """Commands for Ceiling Light Pro.

    Source: devices/lighting/ceiling-light-pro.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 1-100 in the public command table; Feishu lists 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"


class ColorBulbCommands(Commands):
    """Commands for Color Bulb.

    Source: devices/lighting/color-bulb.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # String parameter: 1-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # String parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"


class FloorLampCommands(Commands):
    """Commands for Floor Lamp.

    Source: devices/lighting/floor-lamp.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"


class RGBICNeonRopeLightCommands(Commands):
    """Commands for RGBIC Neon Rope Light.

    Source: devices/lighting/rgbic-neon-rope-light.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Object parameter: effectId 0-25.
    SET_LIGHT_EFFECT = "setLightEffect"


class RGBICNeonWireRopeLightCommands(Commands):
    """Commands for RGBIC Neon Wire Rope Light.

    Source: OpenWonderLabs/SwitchBotAPI,
    devices/lighting/rgbic-neon-wire-rope-light.md.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Object parameter with an integer effectId.
    SET_LIGHT_EFFECT = "setLightEffect"


class RGBICWWFloorLampCommands(Commands):
    """Commands for RGBICWW Floor Lamp.

    Source: devices/lighting/rgbicww-floor-lamp.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"
    # Object parameter: effectId 0-25.
    SET_LIGHT_EFFECT = "setLightEffect"


class RGBICWWStripLightCommands(Commands):
    """Commands for RGBICWW Strip Light.

    Source: devices/lighting/rgbicww-strip-light.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"
    # Object parameter: effectId 0-25.
    SET_LIGHT_EFFECT = "setLightEffect"


class StripLightCommands(Commands):
    """Commands for Strip Light.

    Source: devices/lighting/strip-light.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # String parameter: 1-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"


class StripLight3Commands(Commands):
    """Commands for Strip Light 3.

    Source: devices/lighting/strip-light-3.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"


class RGBICWWLightBarsCommands(Commands):
    """Commands for RGBICWW Light Bars.

    Source: devices/lighting/rgbicww-light-bars.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"
    # Object parameter: brightness 1-100, temperature 2700-6500.
    SET_BRIGHTNESS_AND_TEMPERATURE = "setBrightnessAndTemperature"
    # Object parameter: colorList of R:G:B strings.
    SET_MUSIC_COLOR_MODE = "setMusicColorMode"
    # Object parameter: musicMode 0-5, musicLevel/sensitivity 1-100,
    # controllerMode 0-2.
    SET_MUSIC_PARAM_MODE = "setMusicParamMode"
    # Object parameter: algorithm style integer and colorList.
    SET_EFFECT_COLOR_MODE = "setEffectColorMode"
    # Object parameter: speed 1-255.
    SET_EFFECT_SPEED_MODE = "setEffectSpeedMode"
    # Object parameter: R:G:B color and lightIndex 0-11.
    SET_SEGMENT_COLOR_MODE = "setSegmentColorMode"
    # Object parameter: effectId 0-25.
    SET_LIGHT_EFFECT = "setLightEffect"


class PermanentOutdoorLightsCommands(Commands):
    """Commands for Permanent Outdoor Lights.

    Source: devices/lighting/permanent-outdoor-lights.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR = "setColor"
    # Integer parameter: 2700-6500 kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"
    # Feishu revision 11124: object parameter with an integer effectId.
    SET_LIGHT_EFFECT = "setLightEffect"


class RGBICWWCeilingLightCommands(Commands):
    """Commands for RGBICWW Ceiling Light.

    Source: devices/lighting/rgbicww-ceiling-light.md in OpenWonderLabs/SwitchBotAPI.
    """

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    TURN_ON_MAIN_LIGHT = "turnOnMainLight"
    TURN_OFF_MAIN_LIGHT = "turnOffMainLight"
    TURN_ON_COLOR_LIGHT = "turnOnColorLight"
    TURN_OFF_COLOR_LIGHT = "turnOffColorLight"
    # Integer parameter: 1-100.
    SET_MAIN_LIGHT_BRIGHTNESS = "setMainLightBrightness"
    # Integer parameter: 2700-6500 kelvin.
    SET_MAIN_LIGHT_COLOR_TEMP = "setMainLightColorTemp"
    # Integer parameter: 1-100.
    SET_COLOR_LIGHT_BRIGHTNESS = "setColorLightBrightness"
    # String parameter: R:G:B, each component 0-255.
    SET_COLOR_LIGHT_RGB = "setColorLightRGB"
    # Feishu revision 11124: object parameter with an integer effectId.
    SET_LIGHT_EFFECT = "setLightEffect"
