"""Read unexpired image URLs from documented camera status responses."""

from __future__ import annotations

from collections.abc import Mapping
from time import time
from typing import Any


def get_latest_image_url(
    status: Mapping[str, Any],
    *,
    now: float | None = None,
) -> str | None:
    """Return a usable latestImage URL from an Outdoor 3K or Solar 2K status.

    expireAt and now use Unix seconds. Missing, empty, malformed, and expired
    image metadata return None. This only inspects the supplied status body.
    """
    image = status.get("latestImage")
    if not isinstance(image, Mapping):
        return None
    url = image.get("imageUrl")
    expires_at = image.get("expireAt")
    if not isinstance(url, str) or not url:
        return None
    if isinstance(expires_at, bool) or not isinstance(expires_at, int):
        return None
    if expires_at <= (time() if now is None else now):
        return None
    return url
