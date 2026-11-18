"""Robot vacuum constants and ordinary protocol enums.

Device constants contain discovery/status deviceType strings, which differ
from several product headings. Clearing is the documented workingStatus
spelling. Shared connectivity states live in common.OnlineStatus.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/robot-vacuum
"""

from enum import Enum
from typing import Final

FLOOR_CLEANING_ROBOT_S10: Final = "Robot Vacuum Cleaner S10"
FLOOR_CLEANING_ROBOT_S20: Final = "Robot Vacuum Cleaner S20"
K10_PRO_COMBO: Final = "Robot Vacuum Cleaner K10+ Pro Combo"
K20_PRO: Final = "Robot Vacuum Cleaner K20 Plus Pro"
MINI_ROBOT_VACUUM_K10: Final = "K10+"
MINI_ROBOT_VACUUM_K10_PRO: Final = "K10+ Pro"
ROBOT_VACUUM_CLEANER_S1: Final = "Robot Vacuum Cleaner S1"
ROBOT_VACUUM_CLEANER_S1_PLUS: Final = "Robot Vacuum Cleaner S1 Plus"
ROBOT_VACUUM_K11: Final = "Robot Vacuum Cleaner K11+"
ROBOT_VACUUM_K11_PRO: Final = "Robot Vacuum Cleaner K11 Plus Pro"

VACUUM_DEVICE_TYPES: Final[list[str]] = [
    FLOOR_CLEANING_ROBOT_S10,
    FLOOR_CLEANING_ROBOT_S20,
    K10_PRO_COMBO,
    K20_PRO,
    MINI_ROBOT_VACUUM_K10,
    MINI_ROBOT_VACUUM_K10_PRO,
    ROBOT_VACUUM_CLEANER_S1,
    ROBOT_VACUUM_CLEANER_S1_PLUS,
    ROBOT_VACUUM_K11,
    ROBOT_VACUUM_K11_PRO,
]


class VacuumFanSpeed(Enum):
    """Legacy PowLevel parameter strings for S1/S1 Plus/K10+/K10+ Pro."""

    QUIET = "0"
    STANDARD = "1"
    STRONG = "2"
    MAX = "3"


class VacuumFanLevel(Enum):
    """JSON fanLevel codes for startClean/changeParam, distinct from PowLevel."""

    QUIET = 1
    STANDARD = 2
    STRONG = 3
    MAX = 4


class VacuumWaterLevel(Enum):
    """JSON waterLevel codes for models that accept mop moisture."""

    LOW = 1
    HIGH = 2


class VacuumCleanMode(Enum):
    """Actions across modern vacuums; accepted modes depend on the model."""

    SWEEP = "sweep"
    MOP = "mop"
    SWEEP_MOP = "sweep_mop"


class VacuumSelfCleanMode(Enum):
    """S10/S20 selfClean parameter strings."""

    WASH = "1"
    DRY = "2"
    TERMINATE = "3"


class VacuumWorkingStatus(Enum):
    """workingStatus strings shared by vacuum status and webhook payloads."""

    STANDBY = "StandBy"
    CLEANING = "Clearing"
    PAUSED = "Paused"
    GOING_TO_CHARGE_BASE = "GotoChargeBase"
    CHARGING = "Charging"
    CHARGE_DONE = "ChargeDone"
    DORMANT = "Dormant"
    IN_TROUBLE = "InTrouble"
    IN_REMOTE_CONTROL = "InRemoteControl"
    IN_DUST_COLLECTING = "InDustCollecting"


class VacuumTaskType(Enum):
    """Task strings across vacuum models; not all models report every task."""

    STANDBY = "standBy"
    EXPLORE = "explore"
    CLEAN_ALL = "cleanAll"
    CLEAN_AREA = "cleanArea"
    CLEAN_ROOM = "cleanRoom"
    FILL_WATER = "fillWater"
    DEEP_WASHING = "deepWashing"
    BACK_TO_CHARGE = "backToCharge"
    MARKING_WATER_BASE = "markingWaterBase"
    DRYING = "drying"
    COLLECT_DUST = "collectDust"
    REMOTE_CONTROL = "remoteControl"
    CLEAN_WITH_EXPLORER = "cleanWithExplorer"
    FILL_WATER_FOR_HUMIDIFIER = "fillWaterForHumi"
    MARKING_HUMIDIFIER = "markingHumi"
