"""Read lock states, build passcode dictionaries, and parse Keypad events.

These helpers do not send requests or infer completion from an HTTP response.
Keypad passcodes are supplied as plaintext strings to createKey; encrypted
passwords in keyList use the existing client's AES decryption helper.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from switchbot_api.common.models import DoorState
from switchbot_api.lock.models import KeyCommandResult, LockState, PasscodeType


def lock_state(payload: Mapping[str, Any]) -> LockState | None:
    """Read lockState from a status or webhook payload, returning None if unknown."""
    try:
        return LockState(payload.get("lockState"))
    except ValueError:
        return None


def lock_door_state(payload: Mapping[str, Any]) -> DoorState | None:
    """Read doorState from a status or webhook payload, returning None if unknown."""
    try:
        return DoorState(payload.get("doorState"))
    except ValueError:
        return None


def _validate_key_identity(
    name: str,
    password: str,
    passcode_type: PasscodeType,
) -> None:
    """Require nonempty strings and an explicit passcode type without coercion."""
    if not isinstance(name, str):
        msg = "name must be a string"
        raise TypeError(msg)
    if not name.strip():
        msg = "name must not be empty"
        raise ValueError(msg)
    if not isinstance(password, str):
        msg = "password must be a string"
        raise TypeError(msg)
    if not password:
        msg = "password must not be empty"
        raise ValueError(msg)
    if not isinstance(passcode_type, PasscodeType):
        msg = "passcode_type must be a PasscodeType member"
        raise TypeError(msg)


def _unix_seconds(value: int, field: str) -> int:
    """Require the documented 10-digit Unix seconds, not milliseconds."""
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{field} must be an integer Unix timestamp in seconds"
        raise TypeError(msg)
    if not 1_000_000_000 <= value <= 9_999_999_999:
        msg = f"{field} must be a 10-digit Unix timestamp in seconds"
        raise ValueError(msg)
    return value


def _validity_parameters(
    passcode_type: PasscodeType,
    start_time: int | None,
    end_time: int | None,
) -> dict[str, int]:
    """Require complete, ordered validity windows for time-limited passcodes."""
    if start_time is None and end_time is None:
        if passcode_type in {PasscodeType.TIME_LIMIT, PasscodeType.DISPOSABLE}:
            msg = "start_time and end_time are required for this passcode type"
            raise ValueError(msg)
        return {}
    if start_time is None or end_time is None:
        msg = "start_time and end_time must be provided together"
        raise ValueError(msg)
    start = _unix_seconds(start_time, "start_time")
    end = _unix_seconds(end_time, "end_time")
    if end <= start:
        msg = "end_time must be later than start_time"
        raise ValueError(msg)
    return {"startTime": start, "endTime": end}


def keypad_create_key_parameters(
    name: str,
    password: str,
    passcode_type: PasscodeType,
    *,
    start_time: int | None = None,
    end_time: int | None = None,
) -> dict[str, str | int]:
    """Build createKey for the four Keypads, preserving leading password zeros.

    Passwords require 6-12 ASCII digits. The server checks name uniqueness.
    Validity windows use 10-digit Unix seconds, not signature milliseconds.
    """
    _validate_key_identity(name, password, passcode_type)
    if not password.isascii() or not password.isdigit() or not 6 <= len(password) <= 12:
        msg = "password must contain 6 to 12 ASCII digits"
        raise ValueError(msg)
    validity = _validity_parameters(passcode_type, start_time, end_time)
    return {
        "name": name,
        "type": passcode_type.value,
        "password": password,
        **validity,
    }


def vision_lock_create_key_parameters(
    name: str,
    password: str,
    passcode_type: PasscodeType,
    *,
    start_time: int | None = None,
    end_time: int | None = None,
) -> dict[str, str | int]:
    """Build createKey for Lock Vision and Vision Pro without URGENT support.

    Their tables do not specify password length/digits; only a nonempty string
    is checked locally. Permanent keys use the documented zero time fields
    when no explicit window is supplied.
    """
    _validate_key_identity(name, password, passcode_type)
    if passcode_type is PasscodeType.URGENT:
        msg = "URGENT passcodes are not documented for Vision locks"
        raise ValueError(msg)
    validity = _validity_parameters(passcode_type, start_time, end_time)
    if not validity:
        validity = {"startTime": 0, "endTime": 0}
    return {
        "name": name,
        "type": passcode_type.value,
        "password": password,
        **validity,
    }


def delete_key_parameters(key_id: str | int) -> dict[str, str | int]:
    """Build deleteKey while preserving documented string or integer IDs."""
    if isinstance(key_id, bool) or not isinstance(key_id, (str, int)):
        msg = "key_id must be a string or integer"
        raise TypeError(msg)
    if isinstance(key_id, str) and not key_id.strip():
        msg = "key_id must not be empty"
        raise ValueError(msg)
    if isinstance(key_id, int) and key_id < 0:
        msg = "key_id must not be negative"
        raise ValueError(msg)
    return {"id": key_id}


def get_key_command_result(
    event: Mapping[str, Any],
    *,
    command_id: str | None = None,
) -> KeyCommandResult | None:
    """Parse a Keypad createKey/deleteKey webhook, optionally matching commandId.

    Non-key events, missing context/result/ID, and other command IDs return
    None. The documented trailing space in deleteKey eventName is accepted.
    Unknown result strings raise ValueError rather than implying success.
    """
    context = event.get("context")
    if not isinstance(context, Mapping):
        return None
    name = context.get("eventName")
    if not isinstance(name, str) or name.strip() not in {"createKey", "deleteKey"}:
        return None
    event_id = context.get("commandId")
    if not isinstance(event_id, str) or not event_id:
        return None
    if command_id is not None and event_id != command_id:
        return None
    result = context.get("result")
    if result is None:
        return None
    return KeyCommandResult(result)
