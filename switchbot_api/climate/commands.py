"""Climate control commands from SwitchBot API v1.1.

All enums inherit common.Commands. Power actions use default parameters.
Home Climate Panel exposes readings and webhooks, with no control commands.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/climate-control
"""

from switchbot_api.common.commands import Commands


class HumidifierCommands(Commands):
    """Original Humidifier controls; no webhook is documented."""

    ON = "turnOn"
    OFF = "turnOff"
    # String parameter: auto, percentage 0-100, or preset 101/102/103.
    SET_MODE = "setMode"


class EvaporativeHumidifierCommands(Commands):
    """Controls shared by both Humidifier2 evaporative humidifier variants."""

    ON = "turnOn"
    OFF = "turnOff"
    # Object parameter: mode 1-8 and optional targetHumidify 0-100 (API spelling).
    SET_MODE = "setMode"
    # String parameter: true or false, unlike purifier's numeric 0/1.
    SET_CHILD_LOCK = "setChildLock"
    # Array parameter: up to ten weekDay/start/end objects; [] clears settings.
    SET_AUTO_ADD_TIME = "setAutoAddTime"


class AirPurifierCommands(Commands):
    """Controls shared by the four VOC and PM2.5 purifier variants."""

    ON = "turnOn"
    OFF = "turnOff"
    # Object parameter: mode 1-4; optional fanGear 1-3 only for NORMAL mode (1).
    SET_MODE = "setMode"
    # String parameter: 0 (disable) or 1 (enable).
    SET_CHILD_LOCK = "setChildLock"
    # Object parameter: red, green, blue integers, each 0-255.
    SET_LIGHT_COLOR = "setLightColor"
    # Integer parameter: 0-100.
    SET_BRIGHTNESS = "setBrightness"
    # String parameter: on, off, or steadyMode.
    SET_LIGHT_SENSOR = "setLightSensor"


class SmartRadiatorThermostatCommands(Commands):
    """Radiator thermostat controls with manual targets from 4 to 35 celsius."""

    ON = "turnOn"
    OFF = "turnOff"
    # Integer parameter: 0-5.
    SET_MODE = "setMode"
    # String parameter: 4-35 celsius, inclusive; no step size is documented.
    SET_MANUAL_MODE_TEMPERATURE = "setManualModeTemperature"
