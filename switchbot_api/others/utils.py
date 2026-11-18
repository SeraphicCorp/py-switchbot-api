"""Build documented image, infrared, and other device command parameters."""

from __future__ import annotations

import base64
import binascii
from urllib.parse import urlsplit

from switchbot_api.common.models import PowerState
from switchbot_api.common.utils import finite_number
from switchbot_api.others.models import (
    ArtFrameDeleteImageMode,
    InfraredAirConditionerFanSpeed,
    InfraredAirConditionerMode,
    KataFriendsMode,
)


def art_frame_upload_image_parameters(
    *,
    image_url: str | None = None,
    image_base64: str | None = None,
) -> dict[str, str]:
    """Build uploadImage with exactly one source, without fetching the image.

    AI Art Frame 2 explicitly accepts bare Base64 or a data:image/...;base64,
    prefix. Preserve the supplied representation and do not impose a size limit
    absent from the specifications; the server may return statusCode 402.
    """
    if (image_url is None) == (image_base64 is None):
        msg = "provide exactly one of image_url and image_base64"
        raise ValueError(msg)
    if image_url is not None:
        if not isinstance(image_url, str):
            msg = "image_url must be a string"
            raise TypeError(msg)
        url = urlsplit(image_url)
        if url.scheme not in {"http", "https"} or not url.hostname:
            msg = "image_url must be an absolute HTTP or HTTPS URL"
            raise ValueError(msg)
        return {"imageUrl": image_url}
    if not isinstance(image_base64, str):
        msg = "image_base64 must be a string"
        raise TypeError(msg)
    encoded = image_base64
    if encoded.startswith("data:"):
        header, separator, encoded = encoded.partition(",")
        if (
            not separator
            or not header.startswith("data:image/")
            or not header.endswith(";base64")
        ):
            msg = "image_base64 must use an image Base64 data URI"
            raise ValueError(msg)
    if not encoded:
        msg = "image_base64 must contain nonempty Base64 image data"
        raise ValueError(msg)
    try:
        base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as err:
        msg = "image_base64 must contain valid Base64 data"
        raise ValueError(msg) from err
    return {"imageBase64": image_base64}


def kata_friends_mode_parameter(mode: KataFriendsMode) -> str:
    """Preserve the command's capitalized mode spelling."""
    if not isinstance(mode, KataFriendsMode):
        msg = "mode must be a KataFriendsMode member"
        raise TypeError(msg)
    return str(mode.value)


def on_off_parameter(state: PowerState) -> str:
    """Build lowercase on/off for Kata feature switches and infrared power."""
    if not isinstance(state, PowerState):
        msg = "state must be a common.PowerState member"
        raise TypeError(msg)
    if state is PowerState.PARTIAL:
        msg = "state must be ON or OFF"
        raise ValueError(msg)
    return str(state.value).lower()


def infrared_air_conditioner_parameter(
    temperature: float,
    mode: InfraredAirConditionerMode,
    fan_speed: InfraredAirConditionerFanSpeed,
    power: PowerState,
) -> str:
    """Build temperature,mode,fan,power in Celsius with no invented range."""
    temperature = finite_number(temperature, "temperature")
    if not isinstance(mode, InfraredAirConditionerMode):
        msg = "mode must be an InfraredAirConditionerMode member"
        raise TypeError(msg)
    if not isinstance(fan_speed, InfraredAirConditionerFanSpeed):
        msg = "fan_speed must be an InfraredAirConditionerFanSpeed member"
        raise TypeError(msg)
    return f"{temperature:g},{mode.value},{fan_speed.value},{on_off_parameter(power)}"


def infrared_channel_parameter(channel: str | int) -> str:
    """Build SetChannel, preserving leading zeros in numeric channel strings."""
    if isinstance(channel, bool) or not isinstance(channel, (str, int)):
        msg = "channel must be a nonnegative integer or ASCII digit string"
        raise TypeError(msg)
    value = str(channel)
    if not value or not value.isascii() or not value.isdigit():
        msg = "channel must contain only ASCII digits"
        raise ValueError(msg)
    return value


def weather_station_text_parameter(text: str) -> str:
    """Build customPage text without adding JSON string quotes."""
    if not isinstance(text, str):
        msg = "text must be a string"
        raise TypeError(msg)
    if not text.strip():
        msg = "text must not be blank"
        raise ValueError(msg)
    return text


def weather_station_quote_parameter(text: str) -> str:
    """Build customQuote text with its 100-character limit."""
    text = weather_station_text_parameter(text)
    if len(text) > 100:
        msg = "text must contain at most 100 characters"
        raise ValueError(msg)
    return text


def art_frame_delete_image_parameter(mode: ArtFrameDeleteImageMode) -> str:
    """Select random/newest/oldest for one-image deletion on either frame."""
    if not isinstance(mode, ArtFrameDeleteImageMode):
        msg = "mode must be an ArtFrameDeleteImageMode member"
        raise TypeError(msg)
    return str(mode.value)


def weather_station_component_parameters(
    template_id: int,
    component_id: int,
    text: str,
) -> dict[str, str | int]:
    """Build customPutComponent with exact ID casing and at most 100 characters."""
    for name, value in (("template_id", template_id), ("component_id", component_id)):
        if isinstance(value, bool) or not isinstance(value, int):
            msg = f"{name} must be an integer"
            raise TypeError(msg)
    if not isinstance(text, str):
        msg = "text must be a string"
        raise TypeError(msg)
    if len(text) > 100:
        msg = "text must contain at most 100 characters"
        raise ValueError(msg)
    return {"templateID": template_id, "componentID": component_id, "text": text}
