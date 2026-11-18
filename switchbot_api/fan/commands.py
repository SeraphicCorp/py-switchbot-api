"""Fan command enums from SwitchBot API v1.1.

Commands inherit common.Commands. Power actions use default. Circulator fans
use string settings, while Modern Ceiling Fan uses several integer settings.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/climate-control
"""

from switchbot_api.common import Commands


class BatteryCirculatorFanCommands(Commands):
    """Fan controls with direct, natural, sleep, and baby modes."""

    ON = "turnOn"
    OFF = "turnOff"
    # String parameter: off / 1 (bright) / 2 (dim).
    SET_NIGHT_LIGHT_MODE = "setNightLightMode"
    # String parameter: direct / natural / sleep / baby.
    SET_WIND_MODE = "setWindMode"
    # String parameter: 1-100.
    SET_WIND_SPEED = "setWindSpeed"
    # String parameter: 1-36000; the specification does not state the unit.
    CLOSE_DELAY = "closeDelay"


class CirculatorFanCommands(Commands):
    """Fan controls with direct, natural, sleep, and baby modes."""

    ON = "turnOn"
    OFF = "turnOff"
    # String parameter: off / 1 (bright) / 2 (dim).
    SET_NIGHT_LIGHT_MODE = "setNightLightMode"
    # String parameter: direct / natural / sleep / baby.
    SET_WIND_MODE = "setWindMode"
    # String parameter: 1-100.
    SET_WIND_SPEED = "setWindSpeed"
    # String parameter: 1-36000; the specification does not state the unit.
    CLOSE_DELAY = "closeDelay"


class StandingCirculatorFanCommands(Commands):
    """Fan controls with direct, natural, sleep, and baby modes."""

    ON = "turnOn"
    OFF = "turnOff"
    # String parameter: off / 1 (bright) / 2 (dim).
    SET_NIGHT_LIGHT_MODE = "setNightLightMode"
    # String parameter: direct / natural / sleep / baby.
    SET_WIND_MODE = "setWindMode"
    # String parameter: 1-100.
    SET_WIND_SPEED = "setWindSpeed"
    # String parameter: 1-36000; the specification does not state the unit.
    CLOSE_DELAY = "closeDelay"


class BatteryCirculatorFan2ProCommands(Commands):
    """Battery Circulator Fan 2 Pro controls, without closeDelay."""

    ON = "turnOn"
    OFF = "turnOff"
    # String parameter: off / 0 (bright) / 1 (soft).
    SET_NIGHT_LIGHT_MODE = "setNightLightMode"
    # String parameter: direct / natural / sleep / hurricane.
    SET_WIND_MODE = "setWindMode"
    # String parameter: 1-100.
    SET_WIND_SPEED = "setWindSpeed"
    # String parameter: on or off.
    SET_OSCILLATION = "setOscillation"
    SET_VERTICAL_OSCILLATION = "setVerticalOscillation"


class ModernCeilingFanCommands(Commands):
    """Control the ceiling fan, main light and backlight."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    FAN_ON = "turnOnFan"
    FAN_OFF = "turnOffFan"
    SET_WIND_MODE = "setWindMode"
    # Integer parameter: 1-100.
    SET_WIND_SPEED = "setWindSpeed"
    # Positive integer parameter in minutes.
    CLOSE_DELAY = "closeDelay"
    MAIN_LIGHT_ON = "turnOnMainLight"
    MAIN_LIGHT_OFF = "turnOffMainLight"
    # Integer parameter: 0-100.
    SET_MAIN_BRIGHTNESS = "setMainBrightness"
    BACK_LIGHT_ON = "turnOnBackLight"
    BACK_LIGHT_OFF = "turnOffBackLight"
    # Integer parameter: 0-100.
    SET_BACK_BRIGHTNESS = "setBackBrightness"
    # Integer parameter: 2700-6500 Kelvin.
    SET_COLOR_TEMPERATURE = "setColorTemperature"
    # Backlight RGB string: R:G:B.
    SET_COLOR = "setColor"
