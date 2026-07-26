"""Constants for the DeyeCloud integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "deyecloud"

PLATFORMS: tuple[Platform, ...] = (
    Platform.SENSOR,
)

CONF_APP_ID = "app_id"
CONF_APP_SECRET = "app_secret"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_BASE_URL = "base_url"

DEFAULT_BASE_URL = "https://eu1-developer.deyecloud.com"