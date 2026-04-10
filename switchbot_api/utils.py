"""util for  SwitchBot API."""

import aiohttp
from aiohttp import ClientResponse

from . import DeviceSupportMap
from .exceptions import SwitchBotDeviceRequestError


def check_response_status(response: ClientResponse) -> None:
    """Check https response status."""
    if response.status != 200:
        msg = f"status code != 200 (actual: {response.status})"
        raise SwitchBotDeviceRequestError(msg)


async def get_file_stream_from_cloud(url: str, timeout: float = 5) -> bytes:
    """Get file stream from cloud."""
    # now only for download <AI Art Frame> Picture
    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response,
        ):
            check_response_status(response)
            return await response.read()
    except Exception as e:
        msg = f"{e}"
        raise SwitchBotDeviceRequestError(msg) from e


def assert_device_is_supported(device_model: str) -> bool:
    """Determine whether the device is included in the supported list."""
    return device_model in DeviceSupportMap
