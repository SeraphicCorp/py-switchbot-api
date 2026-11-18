"""Vacuum commands with model-specific scalar and object parameters.

S10/S20 support selfClean and addWaterForHumi. S30 supports numeric selfClean
codes and does not document addWaterForHumi.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/robot-vacuum
"""

from switchbot_api.common.commands import Commands


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


class FloorCleaningRobotS30Commands(Commands):
    """S30 controls; successful responses may contain an empty body."""

    START_CLEAN = "startClean"
    PAUSE = "pause"
    DOCK = "dock"
    # A numeric value from 0 to 100.
    SET_VOLUME = "setVolume"
    # A numeric code from 1 to 4; code meanings await firmware confirmation.
    SELF_CLEAN = "selfClean"
    CHANGE_PARAMETERS = "changeParam"


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
