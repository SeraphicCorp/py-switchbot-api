"""Documented plug, relay, and garage command enums.

Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/plugs-switches
"""

from switchbot_api.common import Commands


class GarageDoorOpenerCommands(Commands):
    """Garage door on/off actions; default parameter."""

    ON = "turnOn"
    OFF = "turnOff"


class PlugCommands(Commands):
    """Original Plug controls; toggle is not documented."""

    ON = "turnOn"
    OFF = "turnOff"


class PlugMiniEUCommands(Commands):
    """Plug Mini on/off/toggle actions; default parameter."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"


class PlugMiniITCommands(Commands):
    """Plug Mini (IT) on/off/toggle actions with the default parameter."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"


class OutdoorPlugEUCommands(Commands):
    """Outdoor Plug (EU) on/off/toggle actions with the default parameter."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"


class PlugMiniJPCommands(Commands):
    """Plug Mini on/off/toggle actions; default parameter."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"


class PlugMiniUSCommands(Commands):
    """Plug Mini on/off/toggle actions; default parameter."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"


class RelaySwitch1Commands(Commands):
    """Single-channel relay actions; setMode uses a string code 0-3."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    SET_MODE = "setMode"


class RelaySwitch1PMCommands(Commands):
    """Single-channel relay actions; setMode uses a string code 0-3."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    SET_MODE = "setMode"


class RelaySwitch2PMCommands(Commands):
    """Dual relay actions need channel 1/2; setMode uses channel;mode."""

    ON = "turnOn"
    OFF = "turnOff"
    TOGGLE = "toggle"
    SET_MODE = "setMode"
    SET_POSITION = "setPosition"
