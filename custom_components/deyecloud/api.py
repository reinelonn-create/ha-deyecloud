"""Minimal asynchronous client for the DeyeCloud OpenAPI."""

from __future__ import annotations

import hashlib
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession


class DeyeCloudApiError(Exception):
    """Base exception for DeyeCloud API failures."""


class DeyeCloudAuthError(DeyeCloudApiError):
    """Raised when authentication fails."""


class DeyeCloudConnectionError(DeyeCloudApiError):
    """Raised when DeyeCloud cannot be reached."""


class DeyeCloudApi:
    """DeyeCloud OpenAPI client."""

    def __init__(
        self,
        session: ClientSession,
        *,
        base_url: str,
        app_id: str,
        app_secret: str,
        email: str,
        password: str,
    ) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._app_id = app_id
        self._app_secret = app_secret
        self._email = email
        self._password = password
        self._access_token: str | None = None

    async def async_authenticate(self) -> None:
        """Authenticate and cache an access token."""
        password_hash = hashlib.sha256(self._password.encode("utf-8")).hexdigest()
        url = f"{self._base_url}/v1.0/account/token?appId={self._app_id}"
        payload = {
            "appSecret": self._app_secret,
            "email": self._email,
            "password": password_hash,
        }

        try:
            async with self._session.post(url, json=payload, timeout=30) as response:
                response.raise_for_status()
                data: dict[str, Any] = await response.json(content_type=None)
        except ClientResponseError as err:
            raise DeyeCloudAuthError(f"HTTP error during authentication: {err.status}") from err
        except (ClientError, TimeoutError, ValueError) as err:
            raise DeyeCloudConnectionError("Unable to contact DeyeCloud") from err

        if not data.get("success") or not data.get("accessToken"):
            message = data.get("msg") or data.get("code") or "Authentication failed"
            raise DeyeCloudAuthError(str(message))

        self._access_token = str(data["accessToken"])

    async def async_list_stations(self) -> list[dict[str, Any]]:
        """Return stations available to the account."""
        if self._access_token is None:
            await self.async_authenticate()

        url = f"{self._base_url}/v1.0/station/list"
        headers = {"Authorization": f"Bearer {self._access_token}"}
        payload = {"page": 1, "size": 200}

        try:
            async with self._session.post(
                url, headers=headers, json=payload, timeout=30
            ) as response:
                response.raise_for_status()
                data: dict[str, Any] = await response.json(content_type=None)
        except ClientResponseError as err:
            if err.status in (401, 403):
                self._access_token = None
                raise DeyeCloudAuthError("DeyeCloud rejected the access token") from err
            raise DeyeCloudApiError(f"HTTP error while listing stations: {err.status}") from err
        except (ClientError, TimeoutError, ValueError) as err:
            raise DeyeCloudConnectionError("Unable to contact DeyeCloud") from err

        if not data.get("success"):
            message = data.get("msg") or data.get("code") or "Station query failed"
            raise DeyeCloudApiError(str(message))

        for key in ("stationList", "stationListItems", "list"):
            value = data.get(key)
            if isinstance(value, list):
                return value

        # Keep the first version tolerant of response-wrapper differences.
        for value in data.values():
            if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                return value

        return []
