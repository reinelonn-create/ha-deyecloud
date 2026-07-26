"""Data update coordinator for DeyeCloud."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import (
    DeyeCloudApi,
    DeyeCloudApiError,
    DeyeCloudAuthError,
    DeyeCloudConnectionError,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=60)


class DeyeCloudCoordinator(
    DataUpdateCoordinator[dict[str, dict[str, Any]]]
):
    """Coordinate updates from DeyeCloud."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api: DeyeCloudApi,
        device_sns: list[str],
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

        self.api = api
        self.device_sns = device_sns

    async def _async_update_data(
        self,
    ) -> dict[str, dict[str, Any]]:
        """Fetch the latest inverter data."""
        try:
            latest_devices = await self.api.async_get_device_latest(
                self.device_sns
            )
        except DeyeCloudAuthError as err:
            raise UpdateFailed(
                f"Authentication failed: {err}"
            ) from err
        except DeyeCloudConnectionError as err:
            raise UpdateFailed(
                f"Unable to connect to DeyeCloud: {err}"
            ) from err
        except DeyeCloudApiError as err:
            raise UpdateFailed(
                f"DeyeCloud API error: {err}"
            ) from err

        coordinator_data: dict[str, dict[str, Any]] = {}

        for device in latest_devices:
            device_sn = device.get("deviceSn")

            if not device_sn:
                continue

            values: dict[str, dict[str, Any]] = {}

            data_list = device.get("dataList")

            if isinstance(data_list, list):
                for item in data_list:
                    if not isinstance(item, dict):
                        continue

                    key = item.get("key")

                    if not key:
                        continue

                    values[str(key)] = {
                        "value": item.get("value"),
                        "unit": item.get("unit"),
                    }

            coordinator_data[str(device_sn)] = {
                "device_sn": str(device_sn),
                "device_type": device.get("deviceType"),
                "device_state": device.get("deviceState"),
                "collection_time": device.get("collectionTime"),
                "values": values,
            }

        return coordinator_data