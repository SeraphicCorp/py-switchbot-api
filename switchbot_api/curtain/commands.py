"""Curtain and blind commands from the SwitchBot API v1.1 specifications.

Each enum inherits common.Commands. Default actions use the client's
default parameter; utils provides position parameter builders.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/curtains-blinds
"""

from switchbot_api.common import Commands


class CurtainCommands(Commands):
    """Commands for Curtain; turnOn opens and turnOff closes the curtain."""

    ON = "turnOn"
    OFF = "turnOff"
    PAUSE = "pause"
    # String parameter: 0,mode,position; mode 0/1/ff, position 0-100.
    # Position 0 opens the curtain; 100 closes it.
    SET_POSITION = "setPosition"


class Curtain3Commands(Commands):
    """Commands for Curtain 3, sharing Curtain's modes and position semantics."""

    ON = "turnOn"
    OFF = "turnOff"
    PAUSE = "pause"
    # String parameter: 0,mode,position; mode 0/1/ff, 0 open, 100 closed.
    SET_POSITION = "setPosition"


class Curtain4Commands(Commands):
    """Commands for Curtain 4, sharing Curtain's modes and position semantics."""

    ON = "turnOn"
    OFF = "turnOff"
    PAUSE = "pause"
    # String parameter: 0,mode,position; mode 0/1/ff, 0 open, 100 closed.
    SET_POSITION = "setPosition"


class BlindTiltCommands(Commands):
    """Blind Tilt commands; no turnOn, turnOff, or pause command is documented."""

    # String parameter: up;position or down;position.
    # Position must be even, 0-100; 0 closed, 100 open.
    SET_POSITION = "setPosition"
    FULLY_OPEN = "fullyOpen"
    CLOSE_UP = "closeUp"
    CLOSE_DOWN = "closeDown"


class RollerShadeCommands(Commands):
    """Roller Shade exposes only the documented setPosition command."""

    # String parameter: 0-100; 0 open, 100 closed.
    SET_POSITION = "setPosition"
