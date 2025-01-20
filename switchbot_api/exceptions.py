"""Exceptions for the SwitchBot API."""


class SwitchBotError(Exception):
    """General SwitchBot error occurred."""


class SwitchBotConnectionError(SwitchBotError):
    """Cannot connect to the SwitchBot API."""


class SwitchBotAuthenticationError(SwitchBotError):
    """Invalid auth for the SwitchBot API."""


class SwitchBotDeviceOfflineError(SwitchBotError):
    """Device currently offline."""
