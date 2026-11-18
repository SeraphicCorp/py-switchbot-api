"""Vacuum commands; scalar parameters are strings and clean settings are objects.

S10/S20 support selfClean and addWaterForHumi. Other modern vacuums do not.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/robot-vacuum
"""

from switchbot_api.common import Commands


class RobotVacuumCleanerS1Commands(Commands):
    """Legacy cleaning controls; PowLevel is case-sensitive, range 0-3."""

    START = "start"
    STOP = "stop"
    DOCK = "dock"
    SET_FAN_SPEED = "PowLevel"


class RobotVacuumCleanerS1PlusCommands(Commands):
    """Legacy cleaning controls; PowLevel is case-sensitive, range 0-3."""

    START = "start"
    STOP = "stop"
    DOCK = "dock"
    SET_FAN_SPEED = "PowLevel"


class MiniRobotVacuumK10Commands(Commands):
    """Legacy cleaning controls; PowLevel is case-sensitive, range 0-3."""

    START = "start"
    STOP = "stop"
    DOCK = "dock"
    SET_FAN_SPEED = "PowLevel"


class MiniRobotVacuumK10ProCommands(Commands):
    """Legacy cleaning controls; PowLevel is case-sensitive, range 0-3."""

    START = "start"
    STOP = "stop"
    DOCK = "dock"
    SET_FAN_SPEED = "PowLevel"


class FloorCleaningRobotS10Commands(Commands):
    """Modern cleaning controls with structured startClean/changeParam."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAMETERS = "changeParam"
    SELF_CLEAN = "selfClean"
    ADD_WATER_FOR_HUMIDIFIER = "addWaterForHumi"


class FloorCleaningRobotS20Commands(Commands):
    """Modern cleaning controls with structured startClean/changeParam."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAMETERS = "changeParam"
    SELF_CLEAN = "selfClean"
    ADD_WATER_FOR_HUMIDIFIER = "addWaterForHumi"


class K10ProComboCommands(Commands):
    """Modern cleaning controls with structured startClean/changeParam."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAMETERS = "changeParam"


class K20ProCommands(Commands):
    """Modern cleaning controls with structured startClean/changeParam."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAMETERS = "changeParam"


class RobotVacuumK11Commands(Commands):
    """Modern cleaning controls with structured startClean/changeParam."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAMETERS = "changeParam"


class RobotVacuumK11ProCommands(Commands):
    """Modern cleaning controls with structured startClean/changeParam."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    SET_VOLUME = "setVolume"
    CHANGE_PARAMETERS = "changeParam"
