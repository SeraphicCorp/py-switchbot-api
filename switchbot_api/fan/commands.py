"""Fan command enums from SwitchBot API v1.1.

Commands inherit common.Commands. Scalar parameters are strings; power actions
use default. Oscillation is reported by status but has no documented command
in these device specifications.
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
