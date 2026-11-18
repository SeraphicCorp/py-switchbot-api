"""Lock and keypad device constants and enums for SwitchBot API v1.1.

Constants retain the documented discovery/status spellings. Older Smart Lock
Lite/Vision names and the Lock Ultra status spelling are included as aliases.
Webhook deviceType identifiers may differ from these discovery names.
Status and webhook payloads remain ordinary dictionaries; DoorState is shared
in common.models. Passcode lists are discovery data, not keypad status data.
Nano omits doorState from the documented REST status. UWB REST doorState
uses closed/opened; both devices' webhooks use CLOSED/OPENED.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/locks-security
"""

from __future__ import annotations

from enum import Enum
from typing import Final

SMART_LOCK: Final = "Smart Lock"
LOCK_LITE: Final = "Lock Lite"
SMART_LOCK_LITE: Final = "Smart Lock Lite"
SMART_LOCK_NANO: Final = "Smart Lock Nano"
SMART_LOCK_PRO: Final = "Smart Lock Pro"
SMART_LOCK_PRO_WIFI: Final = "Smart Lock Pro Wifi"
SMART_LOCK_ULTRA: Final = "Smart Lock Ultra"
LOCK_ULTRA: Final = "Lock Ultra"
SMART_LOCK_ULTRA_MAX: Final = "Smart Lock Ultra Max"
LOCK_VISION: Final = "Lock Vision"
SMART_LOCK_VISION: Final = "Smart Lock Vision"
LOCK_VISION_PRO: Final = "Lock Vision Pro"
SMART_LOCK_VISION_PRO: Final = "Smart Lock Vision Pro"
SMART_SWITCHBOT_UWB_LOCK: Final = "Smart SwitchBot UWB Lock"
LOCK_NANO_WEBHOOK: Final = "Lock Nano"
SWITCHBOT_UWB_LOCK_WEBHOOK: Final = "SwitchBot UWB Lock"
KEYPAD: Final = "Keypad"
KEYPAD_TOUCH: Final = "Keypad Touch"
KEYPAD_VISION: Final = "Keypad Vision"
KEYPAD_VISION_PRO: Final = "Keypad Vision Pro"

LOCK_DEVICE_TYPES: Final[list[str]] = [
    SMART_LOCK,
    LOCK_LITE,
    SMART_LOCK_LITE,
    SMART_LOCK_NANO,
    SMART_LOCK_PRO,
    SMART_LOCK_PRO_WIFI,
    SMART_LOCK_ULTRA,
    LOCK_ULTRA,
    SMART_LOCK_ULTRA_MAX,
    LOCK_VISION,
    SMART_LOCK_VISION,
    LOCK_VISION_PRO,
    SMART_LOCK_VISION_PRO,
    SMART_SWITCHBOT_UWB_LOCK,
    KEYPAD,
    KEYPAD_TOUCH,
    KEYPAD_VISION,
    KEYPAD_VISION_PRO,
]


class LockState(Enum):
    """Normalize REST and webhook lock states without changing raw payloads."""

    LOCKED = "locked"
    UNLOCKED = "unlocked"
    LOCKING = "locking"
    UNLOCKING = "unlocking"
    JAMMED = "jammed"
    LATCH_BOLT_LOCKED = "latchBoltLocked"
    HALF_LOCKED = "halfLocked"

    @classmethod
    def _missing_(cls, value: object) -> LockState | None:
        """Accept case differences and the REST lock/unlock spellings."""
        if not isinstance(value, str):
            return None
        normalized = value.casefold()
        if normalized == "lock":
            return cls.LOCKED
        if normalized == "unlock":
            return cls.UNLOCKED
        return next(
            (state for state in cls if state.value.casefold() == normalized),
            None,
        )


class PasscodeType(Enum):
    """Passcode types; URGENT is documented for Keypads, not Vision locks."""

    PERMANENT = "permanent"
    TIME_LIMIT = "timeLimit"
    DISPOSABLE = "disposable"
    URGENT = "urgent"


class PasscodeStatus(Enum):
    """Validity states reported by passcode entries in keyList."""

    NORMAL = "normal"
    EXPIRED = "expired"


class KeyCommandResult(Enum):
    """Asynchronous Keypad createKey/deleteKey webhook results."""

    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
