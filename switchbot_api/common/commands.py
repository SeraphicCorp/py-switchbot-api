"""Shared device commands."""

from typing import NoReturn

from switchbot_api.commands import Commands as LegacyCommands


class Commands(LegacyCommands):
    """Base for V2 command enums.

    The legacy base lets SwitchBotAPI.send_command serialize these enums by
    their value. Device type lookup uses constants from each V2 device module.
    """

    @classmethod
    def get_supported_devices(cls) -> NoReturn:
        """Raise because V2 device types are exposed as module constants."""
        msg = (
            f"{cls.__name__}.get_supported_devices() is deprecated for V2 commands. "
            "Use the device type constants from the device module."
        )
        raise NotImplementedError(msg)

    @classmethod
    def is_supported(cls, device_type: str) -> NoReturn:
        """Raise because callers should check V2 device type constants."""
        msg = (
            f"{cls.__name__}.is_supported() is deprecated for V2 commands. "
            f"Use the device type constants to check {device_type!r}."
        )
        raise NotImplementedError(msg)
