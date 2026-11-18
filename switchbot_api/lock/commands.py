"""Documented lock and keypad commands for SwitchBot API v1.1.

All enums inherit common.Commands. Lock/latch actions use parameter default.
Keypad password commands return their actual outcome asynchronously through
webhooks; an accepted HTTP request does not establish completion.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/locks-security
"""

from switchbot_api.common import Commands


class LockCommands(Commands):
    """Documented lock, unlock, and deadbolt/latch controls."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class LockLiteCommands(Commands):
    """Documented lock, unlock, and deadbolt/latch controls."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class LockNanoCommands(Commands):
    """Lock Nano controls with the default parameter."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class UWBLockCommands(Commands):
    """UWB Lock controls with the default parameter."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class LockProCommands(Commands):
    """Documented lock, unlock, and deadbolt/latch controls."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class LockUltraCommands(Commands):
    """Documented lock, unlock, and deadbolt/latch controls."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class LockUltraMaxCommands(Commands):
    """Documented lock, unlock, and deadbolt/latch controls."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"


class LockProMatterEnabledCommands(Commands):
    """Matter/Wi-Fi Lock Pro controls, including the EU night latch."""

    LOCK = "lock"
    UNLOCK = "unlock"
    DEADBOLT = "deadbolt"
    NIGHT_LATCH_UNLOCK = "nightLatchUnlock"


class LockVisionCommands(Commands):
    """Lock/unlock and passcode management for a Vision lock."""

    LOCK = "lock"
    UNLOCK = "unlock"
    # Object parameter: name, type, password, and optional validity times.
    CREATE_KEY = "createKey"
    # Object parameter: id; the source includes both integer and string IDs.
    DELETE_KEY = "deleteKey"


class LockVisionProCommands(Commands):
    """Lock/unlock and passcode management for a Vision lock."""

    LOCK = "lock"
    UNLOCK = "unlock"
    # Object parameter: name, type, password, and optional validity times.
    CREATE_KEY = "createKey"
    # Object parameter: id; the source includes both integer and string IDs.
    DELETE_KEY = "deleteKey"


class KeypadCommands(Commands):
    """Passcode creation/deletion; final results arrive via webhook."""

    # Object parameter: name, type, password, and optional validity times.
    CREATE_KEY = "createKey"
    # Object parameter: id; the source includes both integer and string IDs.
    DELETE_KEY = "deleteKey"


class KeypadTouchCommands(Commands):
    """Passcode creation/deletion; final results arrive via webhook."""

    # Object parameter: name, type, password, and optional validity times.
    CREATE_KEY = "createKey"
    # Object parameter: id; the source includes both integer and string IDs.
    DELETE_KEY = "deleteKey"


class KeypadVisionCommands(Commands):
    """Passcode creation/deletion; final results arrive via webhook."""

    # Object parameter: name, type, password, and optional validity times.
    CREATE_KEY = "createKey"
    # Object parameter: id; the source includes both integer and string IDs.
    DELETE_KEY = "deleteKey"


class KeypadVisionProCommands(Commands):
    """Passcode creation/deletion; final results arrive via webhook."""

    # Object parameter: name, type, password, and optional validity times.
    CREATE_KEY = "createKey"
    # Object parameter: id; the source includes both integer and string IDs.
    DELETE_KEY = "deleteKey"
