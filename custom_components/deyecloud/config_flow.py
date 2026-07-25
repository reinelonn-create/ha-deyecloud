"""Config flow for DeyeCloud."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import DeyeCloudApi, DeyeCloudAuthError, DeyeCloudConnectionError
from .const import (
    CONF_APP_ID,
    CONF_APP_SECRET,
    CONF_BASE_URL,
    DEFAULT_BASE_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class DeyeCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a DeyeCloud config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api = DeyeCloudApi(
                async_get_clientsession(self.hass),
                base_url=user_input[CONF_BASE_URL],
                app_id=user_input[CONF_APP_ID],
                app_secret=user_input[CONF_APP_SECRET],
                email=user_input[CONF_EMAIL],
                password=user_input[CONF_PASSWORD],
            )

            try:
                stations = await api.async_list_stations()
            except DeyeCloudAuthError:
                errors["base"] = "invalid_auth"
            except DeyeCloudConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error while validating DeyeCloud")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_EMAIL].strip().lower())
                self._abort_if_unique_id_configured()
                title = "DeyeCloud"
                if len(stations) == 1:
                    title = str(stations[0].get("name") or title)
                return self.async_create_entry(title=title, data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_APP_ID): str,
                vol.Required(CONF_APP_SECRET): str,
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
