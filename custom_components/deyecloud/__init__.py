"""DeyeCloud integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import UpdateFailed

from .api import (
    DeyeCloudApi,
    DeyeCloudApiError,
    DeyeCloudAuthError,
    DeyeCloudConnectionError,
)
from .const import (
    CONF_APP_ID,
    CONF_APP_SECRET,
    CONF_BASE_URL,
    CONF_EMAIL,
    CONF_PASSWORD,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import DeyeCloudCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up DeyeCloud from a config entry."""
    session = async_get_clientsession(hass)

    api = DeyeCloudApi(
        session,
        base_url=entry.data[CONF_BASE_URL],
        app_id=entry.data[CONF_APP_ID],
        app_secret=entry.data[CONF_APP_SECRET],
        email=entry.data[CONF_EMAIL],
        password=entry.data[CONF_PASSWORD],
    )

    try:
        stations = await api.async_list_stations()

        devices: list[dict[str, Any]] = []

        for station in stations:
            station_id = (
                station.get("id")
                or station.get("stationId")
            )

            if station_id is None:
                _LOGGER.warning(
                    "DeyeCloud station has no station ID: %s",
                    station,
                )
                continue

            station_devices = await api.async_list_station_devices(
                station_id
            )
            devices.extend(station_devices)

    except DeyeCloudAuthError as err:
        raise ConfigEntryAuthFailed(
            "DeyeCloud authentication failed"
        ) from err
    except (
        DeyeCloudConnectionError,
        DeyeCloudApiError,
    ) as err:
        raise UpdateFailed(
            f"Unable to initialize DeyeCloud: {err}"
        ) from err

    inverter_sns = [
        str(device["deviceSn"])
        for device in devices
        if device.get("deviceType") == "INVERTER"
        and device.get("deviceSn")
    ]

    if not inverter_sns:
        raise UpdateFailed(
            "No DeyeCloud inverter devices were found"
        )

    coordinator = DeyeCloudCoordinator(
        hass=hass,
        api=api,
        device_sns=inverter_sns,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
        "stations": stations,
        "devices": devices,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    _LOGGER.info(
        "Loaded %s DeyeCloud stations, %s devices and %s inverters",
        len(stations),
        len(devices),
        len(inverter_sns),
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a DeyeCloud config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        domain_data = hass.data.get(DOMAIN)

        if domain_data is not None:
            domain_data.pop(entry.entry_id, None)

            if not domain_data:
                hass.data.pop(DOMAIN, None)

    return unload_ok