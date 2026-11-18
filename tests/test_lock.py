"""Test lock states, passcode payloads, and asynchronous Keypad results."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from aioresponses import CallbackResult, aioresponses
import pytest

from switchbot_api.common import DoorState
from switchbot_api.lock import (
    LOCK_DEVICE_TYPES,
    LOCK_NANO_WEBHOOK,
    SMART_LOCK_NANO,
    SMART_SWITCHBOT_UWB_LOCK,
    SWITCHBOT_UWB_LOCK_WEBHOOK,
    KeyCommandResult,
    KeypadCommands,
    KeypadTouchCommands,
    KeypadVisionCommands,
    KeypadVisionProCommands,
    LockCommands,
    LockLiteCommands,
    LockNanoCommands,
    LockProCommands,
    LockProMatterEnabledCommands,
    LockState,
    LockUltraCommands,
    LockUltraMaxCommands,
    LockVisionCommands,
    LockVisionProCommands,
    PasscodeType,
    UWBLockCommands,
    delete_key_parameters,
    get_key_command_result,
    keypad_create_key_parameters,
    lock_door_state,
    lock_state,
    vision_lock_create_key_parameters,
)
from tests.const import MOCK_URL

if TYPE_CHECKING:
    from switchbot_api.common import Commands
    from tests import CommandSender

START_TIME = 1_800_000_000
END_TIME = 1_800_000_060


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("lock", LockState.LOCKED),
        ("LOCK", LockState.LOCKED),
        ("locked", LockState.LOCKED),
        ("LOCKED", LockState.LOCKED),
        ("unlock", LockState.UNLOCKED),
        ("UNLOCKED", LockState.UNLOCKED),
        ("LOCKING", LockState.LOCKING),
        ("UNLOCKING", LockState.UNLOCKING),
        ("JAMMED", LockState.JAMMED),
        ("latchBoltLocked", LockState.LATCH_BOLT_LOCKED),
        ("LATCHBOLTLOCKED", LockState.LATCH_BOLT_LOCKED),
        ("halfLocked", LockState.HALF_LOCKED),
        ("HALFLOCKED", LockState.HALF_LOCKED),
    ],
)
def test_parse_lock_state(value: str, expected: LockState) -> None:
    """Resolve documented status spellings and uppercase webhook states."""
    assert LockState(value) is expected
    assert lock_state({"lockState": value}) is expected


@pytest.mark.parametrize("value", ["unknown", "", None, True, 1])
def test_reject_invalid_lock_state(value: object) -> None:
    """Never interpret an unknown state as locked or unlocked."""
    with pytest.raises(ValueError, match="is not a valid LockState"):
        LockState(value)
    assert lock_state({"lockState": value}) is None


def test_lock_state_is_unknown_when_missing() -> None:
    """A status update may omit the lock state entirely."""
    assert lock_state({"battery": 75, "doorState": "closed"}) is None


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (LockState.LOCKED, True),
        (LockState.LATCH_BOLT_LOCKED, True),
        (LockState.HALF_LOCKED, True),
        (LockState.UNLOCKED, False),
        (LockState.LOCKING, False),
        (LockState.UNLOCKING, False),
        (LockState.JAMMED, False),
    ],
)
def test_lock_state_uses_home_assistant_locked_semantics(
    state: LockState, *, expected: bool
) -> None:
    """Use HA's locked classification while retaining the underlying state."""
    assert state.is_locked is expected


@pytest.mark.parametrize(
    ("device_type", "webhook_type", "wire_types"),
    [
        (SMART_LOCK_NANO, LOCK_NANO_WEBHOOK, ("Smart Lock Nano", "Lock Nano")),
        (
            SMART_SWITCHBOT_UWB_LOCK,
            SWITCHBOT_UWB_LOCK_WEBHOOK,
            ("Smart SwitchBot UWB Lock", "SwitchBot UWB Lock"),
        ),
    ],
)
def test_lock_device_type_identifiers(
    device_type: str, webhook_type: str, wire_types: tuple[str, str]
) -> None:
    """Preserve the distinct REST and webhook identifiers."""
    assert (device_type, webhook_type) == wire_types
    assert device_type in LOCK_DEVICE_TYPES
    assert webhook_type not in LOCK_DEVICE_TYPES


@pytest.mark.parametrize(
    ("door_state", "expected"),
    [
        ("open", DoorState.OPEN),
        ("opened", DoorState.OPEN),
        ("OPENED", DoorState.OPEN),
        ("close", DoorState.CLOSED),
        ("closed", DoorState.CLOSED),
        ("CLOSED", DoorState.CLOSED),
    ],
)
def test_lock_door_state(door_state: str, expected: DoorState) -> None:
    """Normalize the open and closed spellings from status and webhooks."""
    assert lock_door_state({"doorState": door_state}) is expected


def test_nano_rest_without_door_state() -> None:
    """An available lock state does not imply a known door position."""
    status = {"deviceType": SMART_LOCK_NANO, "lockState": "unlocked"}
    assert lock_state(status) is LockState.UNLOCKED
    assert lock_door_state(status) is None


@pytest.mark.parametrize("value", ["unknown", "", None, True, 1])
def test_unknown_lock_door_state(value: object) -> None:
    """Unknown values must not be interpreted as a closed door."""
    assert lock_door_state({"doorState": value}) is None


@pytest.mark.parametrize("kind", [PasscodeType.PERMANENT, PasscodeType.URGENT])
def test_keypad_permanent_and_urgent_payload(kind: PasscodeType) -> None:
    """Preserve leading zeros and omit absent non-temporary validity fields."""
    assert keypad_create_key_parameters("Example", "000001", kind) == {
        "name": "Example",
        "password": "000001",
        "type": kind.value,
    }


@pytest.mark.parametrize("kind", [PasscodeType.TIME_LIMIT, PasscodeType.DISPOSABLE])
def test_keypad_temporary_payload(kind: PasscodeType) -> None:
    """Temporal keys retain their type and 10-digit Unix seconds."""
    assert keypad_create_key_parameters(
        "Example",
        "000001234567",
        kind,
        start_time=START_TIME,
        end_time=END_TIME,
    ) == {
        "name": "Example",
        "password": "000001234567",
        "type": kind.value,
        "startTime": START_TIME,
        "endTime": END_TIME,
    }


@pytest.mark.parametrize(
    "password",
    [
        "",
        "12345",
        "1234567890123",
        "\uff11\uff12\uff13\uff14\uff15\uff16",
        "123abc",
        "123 456",
    ],
)
def test_keypad_rejects_invalid_password(password: str) -> None:
    """Enforce ASCII digits and the documented inclusive 6-12 length range."""
    with pytest.raises(ValueError, match="password"):
        keypad_create_key_parameters("Example", password, PasscodeType.PERMANENT)


@pytest.mark.parametrize("password", [123456, None, True])
def test_keypad_rejects_password_coercion(password: Any) -> None:
    """Reject non-string passcodes instead of losing leading zeros."""
    with pytest.raises(TypeError, match="password must be a string"):
        keypad_create_key_parameters("Example", password, PasscodeType.PERMANENT)


@pytest.mark.parametrize("name", ["", "   "])
def test_keypad_requires_nonempty_name(name: str) -> None:
    """A local builder cannot check server uniqueness but rejects blank names."""
    with pytest.raises(ValueError, match="name must not be empty"):
        keypad_create_key_parameters(name, "000001", PasscodeType.PERMANENT)


def test_keypad_requires_name_string() -> None:
    """Names are not silently converted from numeric input."""
    with pytest.raises(TypeError, match="name must be a string"):
        keypad_create_key_parameters(123, "000001", PasscodeType.PERMANENT)  # type: ignore[arg-type]


def test_keypad_requires_type_enum() -> None:
    """Require an explicitly selected passcode type."""
    with pytest.raises(TypeError, match="PasscodeType member"):
        keypad_create_key_parameters("Example", "000001", "permanent")  # type: ignore[arg-type]


@pytest.mark.parametrize("kind", [PasscodeType.TIME_LIMIT, PasscodeType.DISPOSABLE])
def test_temporary_key_requires_window(kind: PasscodeType) -> None:
    """Time-limited and one-time passcodes require both validity timestamps."""
    with pytest.raises(ValueError, match="are required"):
        keypad_create_key_parameters("Example", "000001", kind)


@pytest.mark.parametrize(("start", "end"), [(START_TIME, None), (None, END_TIME)])
def test_key_requires_paired_timestamps(start: int | None, end: int | None) -> None:
    """Do not construct a validity window with only one endpoint."""
    with pytest.raises(ValueError, match="provided together"):
        keypad_create_key_parameters(
            "Example",
            "000001",
            PasscodeType.PERMANENT,
            start_time=start,
            end_time=end,
        )


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (999_999_999, END_TIME),
        (START_TIME * 1000, END_TIME * 1000),
        (START_TIME, 10_000_000_000),
        (END_TIME, START_TIME),
        (START_TIME, START_TIME),
    ],
)
def test_key_rejects_invalid_window(start: int, end: int) -> None:
    """Reject milliseconds, short timestamps, equal endpoints, and reverse time."""
    with pytest.raises(ValueError, match="timestamp|later than"):
        keypad_create_key_parameters(
            "Example",
            "000001",
            PasscodeType.TIME_LIMIT,
            start_time=start,
            end_time=end,
        )


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (True, END_TIME),
        (float(START_TIME), END_TIME),
        (START_TIME, str(END_TIME)),
    ],
)
def test_key_rejects_timestamp_coercion(start: Any, end: Any) -> None:
    """Validity fields are JSON integers without implicit unit/type conversion."""
    with pytest.raises(TypeError, match="integer Unix timestamp"):
        keypad_create_key_parameters(
            "Example",
            "000001",
            PasscodeType.TIME_LIMIT,
            start_time=start,
            end_time=end,
        )


def test_passcode_validation_does_not_echo_password() -> None:
    """Validation errors describe the rule rather than including credentials."""
    password = "example-invalid-secret"
    with pytest.raises(ValueError, match="ASCII digits") as error:
        keypad_create_key_parameters("Example", password, PasscodeType.PERMANENT)
    assert password not in str(error.value)


def test_vision_permanent_payload() -> None:
    """Vision permanent keys use the zero validity fields shown in its schema."""
    assert vision_lock_create_key_parameters(
        "Example", "000001", PasscodeType.PERMANENT
    ) == {
        "name": "Example",
        "password": "000001",
        "type": "permanent",
        "startTime": 0,
        "endTime": 0,
    }


def test_vision_temporary_payload() -> None:
    """Vision temporary keys carry the explicitly requested validity window."""
    payload = vision_lock_create_key_parameters(
        "Example",
        "000001",
        PasscodeType.TIME_LIMIT,
        start_time=START_TIME,
        end_time=END_TIME,
    )
    assert payload["startTime"] == START_TIME
    assert payload["endTime"] == END_TIME
    assert payload["type"] == "timeLimit"


def test_vision_rejects_urgent_type() -> None:
    """URGENT is a Keypad type, absent from Vision lock specifications."""
    with pytest.raises(ValueError, match="not documented for Vision"):
        vision_lock_create_key_parameters("Example", "000001", PasscodeType.URGENT)


@pytest.mark.parametrize("key_id", ["007", 7, 0])
def test_delete_key_preserves_id_type(key_id: str | int) -> None:
    """Both ID types are documented and string leading zeros must survive."""
    result = delete_key_parameters(key_id)
    assert result == {"id": key_id}
    assert type(result["id"]) is type(key_id)


@pytest.mark.parametrize("key_id", ["", "  ", -1])
def test_delete_key_rejects_invalid_id(key_id: str | int) -> None:
    """Reject blank IDs and negative numeric IDs."""
    with pytest.raises(ValueError, match="key_id"):
        delete_key_parameters(key_id)


@pytest.mark.parametrize("key_id", [True, 1.5, None, []])
def test_delete_key_rejects_id_coercion(key_id: Any) -> None:
    """Booleans and fractions must not become another credential's ID."""
    with pytest.raises(TypeError, match="string or integer"):
        delete_key_parameters(key_id)


@pytest.mark.parametrize("name", ["createKey", "deleteKey", "deleteKey "])
@pytest.mark.parametrize("result", list(KeyCommandResult))
def test_key_command_webhook_result(name: str, result: KeyCommandResult) -> None:
    """Parse actual final outcomes, including padded delete event names."""
    event = {
        "context": {
            "eventName": name,
            "commandId": "CMD-example",
            "result": result.value,
        }
    }
    assert get_key_command_result(event, command_id="CMD-example") is result


@pytest.mark.parametrize(
    "event",
    [
        {},
        {"context": None},
        {"context": []},
        {"statusCode": 100, "body": {"commandId": "CMD-example"}},
        {
            "context": {
                "eventName": "lock",
                "commandId": "CMD-example",
                "result": "success",
            }
        },
        {"context": {"eventName": "createKey", "result": "success"}},
        {"context": {"eventName": "createKey", "commandId": "CMD-example"}},
        {
            "context": {
                "eventName": "createKey",
                "commandId": "other",
                "result": "success",
            }
        },
    ],
)
def test_key_command_ignores_unrelated_or_incomplete_events(
    event: dict[str, Any],
) -> None:
    """An acknowledgement, malformed event, or other ID is not a final outcome."""
    assert get_key_command_result(event, command_id="CMD-example") is None


def test_key_command_rejects_unknown_result() -> None:
    """Unknown result codes must not be considered success."""
    event = {
        "context": {
            "eventName": "createKey",
            "commandId": "CMD-example",
            "result": "pending",
        }
    }
    with pytest.raises(ValueError, match="is not a valid KeyCommandResult"):
        get_key_command_result(event)


@pytest.mark.parametrize(
    ("command", "parameter", "expected_command", "expected_parameter"),
    [
        (LockCommands.LOCK, "default", "lock", "default"),
        (LockLiteCommands.DEADBOLT, "default", "deadbolt", "default"),
        (LockNanoCommands.LOCK, "default", "lock", "default"),
        (LockNanoCommands.UNLOCK, "default", "unlock", "default"),
        (LockNanoCommands.DEADBOLT, "default", "deadbolt", "default"),
        (UWBLockCommands.LOCK, "default", "lock", "default"),
        (UWBLockCommands.UNLOCK, "default", "unlock", "default"),
        (UWBLockCommands.DEADBOLT, "default", "deadbolt", "default"),
        (LockProCommands.UNLOCK, "default", "unlock", "default"),
        (
            LockProMatterEnabledCommands.NIGHT_LATCH_UNLOCK,
            "default",
            "nightLatchUnlock",
            "default",
        ),
        (LockUltraCommands.LOCK, "default", "lock", "default"),
        (LockUltraMaxCommands.DEADBOLT, "default", "deadbolt", "default"),
        (
            LockVisionCommands.CREATE_KEY,
            vision_lock_create_key_parameters(
                "Example", "000001", PasscodeType.PERMANENT
            ),
            "createKey",
            {
                "name": "Example",
                "password": "000001",
                "type": "permanent",
                "startTime": 0,
                "endTime": 0,
            },
        ),
        (
            LockVisionProCommands.DELETE_KEY,
            delete_key_parameters("007"),
            "deleteKey",
            {"id": "007"},
        ),
        (
            KeypadCommands.CREATE_KEY,
            keypad_create_key_parameters("Example", "000001", PasscodeType.PERMANENT),
            "createKey",
            {"name": "Example", "password": "000001", "type": "permanent"},
        ),
        (
            KeypadTouchCommands.CREATE_KEY,
            keypad_create_key_parameters(
                "Example",
                "000001",
                PasscodeType.TIME_LIMIT,
                start_time=START_TIME,
                end_time=END_TIME,
            ),
            "createKey",
            {
                "name": "Example",
                "password": "000001",
                "type": "timeLimit",
                "startTime": START_TIME,
                "endTime": END_TIME,
            },
        ),
        (
            KeypadVisionCommands.DELETE_KEY,
            delete_key_parameters(7),
            "deleteKey",
            {"id": 7},
        ),
        (
            KeypadVisionProCommands.CREATE_KEY,
            keypad_create_key_parameters(
                "Example",
                "000001",
                PasscodeType.DISPOSABLE,
                start_time=START_TIME,
                end_time=END_TIME,
            ),
            "createKey",
            {
                "name": "Example",
                "password": "000001",
                "type": "disposable",
                "startTime": START_TIME,
                "endTime": END_TIME,
            },
        ),
    ],
)
async def test_send_lock_command(
    send_command: CommandSender,
    responses: aioresponses,
    command: Commands,
    parameter: dict[str, str | int] | str,
    expected_command: str,
    expected_parameter: dict[str, str | int] | str,
) -> None:
    """Serialize documented commands for all twelve device families with mocks."""
    captured: list[dict[str, Any]] = []

    def capture(_: str, **kwargs: Any) -> CallbackResult:
        """Capture JSON without sending commands to a physical lock."""
        captured.append(json.loads(json.dumps(kwargs["json"])))
        return CallbackResult(
            status=200,
            payload={"statusCode": 100, "body": {"commandId": "CMD-example"}},
        )

    responses.post(f"{MOCK_URL}/devices/lock-id/commands", callback=capture)
    await send_command(
        "lock-id",
        command,
        parameters=parameter,
    )
    assert captured == [
        {
            "commandType": "command",
            "command": expected_command,
            "parameter": expected_parameter,
        }
    ]
