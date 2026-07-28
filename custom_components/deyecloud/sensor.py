"""Sensor platform for the DeyeCloud integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import DeyeCloudCoordinator
from .entity import DeyeCloudEntity
from .sensor_descriptions import (
    DeyeCloudSensorEntityDescription,
    SENSOR_DESCRIPTIONS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DeyeCloud sensors from a config entry."""
    entry_data = hass.data[DOMAIN][entry.entry_id]

    coordinator: DeyeCloudCoordinator = entry_data["coordinator"]
    devices = entry_data.get("devices", [])

    devices_by_serial = _index_devices_by_serial(devices)
    entities: list[DeyeCloudSensor] = []

    for device_sn in coordinator.device_sns:
        device_data = _get_device_data(
            coordinator=coordinator,
            device_sn=device_sn,
        )
        available_keys = _get_available_measurement_keys(
            device_data
        )
        device_metadata = devices_by_serial.get(device_sn, {})

        created_count = 0

        for description in SENSOR_DESCRIPTIONS:
            if description.data_key not in available_keys:
                continue

            entities.append(
                DeyeCloudSensor(
                    coordinator=coordinator,
                    device_sn=device_sn,
                    device=device_metadata,
                    description=description,
                )
            )
            created_count += 1

        _LOGGER.debug(
            "Creating %s DeyeCloud sensors for device %s "
            "from %s available measurements",
            created_count,
            device_sn,
            len(available_keys),
        )

    async_add_entities(entities)


def _index_devices_by_serial(
    devices: Any,
) -> dict[str, dict[str, Any]]:
    """Return device metadata indexed by serial number."""
    devices_by_serial: dict[str, dict[str, Any]] = {}

    if not isinstance(devices, list):
        return devices_by_serial

    for device in devices:
        if not isinstance(device, dict):
            continue

        device_sn = device.get("deviceSn")

        if device_sn in (None, ""):
            continue

        devices_by_serial[str(device_sn)] = device

    return devices_by_serial


def _get_device_data(
    coordinator: DeyeCloudCoordinator,
    device_sn: str,
) -> dict[str, Any]:
    """Return coordinator data for one device."""
    coordinator_data = coordinator.data

    if not isinstance(coordinator_data, dict):
        return {}

    device_data = coordinator_data.get(device_sn, {})

    if not isinstance(device_data, dict):
        return {}

    return device_data


def _get_available_measurement_keys(
    device_data: dict[str, Any],
) -> set[str]:
    """Return measurement keys available for a device."""
    values = device_data.get("values", {})

    if not isinstance(values, dict):
        return set()

    return {
        str(data_key)
        for data_key, measurement in values.items()
        if isinstance(measurement, dict)
    }


class DeyeCloudSensor(
    DeyeCloudEntity,
    SensorEntity,
):
    """Representation of a DeyeCloud sensor."""

    _attr_has_entity_name = True

    entity_description: DeyeCloudSensorEntityDescription

    def __init__(
        self,
        coordinator: DeyeCloudCoordinator,
        device_sn: str,
        device: dict[str, Any],
        description: DeyeCloudSensorEntityDescription,
    ) -> None:
        """Initialize a DeyeCloud sensor."""
        super().__init__(
            coordinator=coordinator,
            device_sn=device_sn,
            device=device,
        )

        self.entity_description = description

        # Keep the established unique ID format so existing entities
        # retain their registry entries and history.
        self._attr_unique_id = (
            f"{device_sn}_{description.data_key}"
        )

    @property
    def available(self) -> bool:
        """Return whether the sensor is available."""
        if not super().available:
            return False

        measurement = self.get_measurement(
            self.entity_description.data_key
        )

        if measurement is None:
            return False

        return measurement.get("value") not in (None, "")

    @property
    def native_value(self) -> float | None:
        """Return the current numeric sensor value."""
        raw_value = self.get_measurement_value(
            self.entity_description.data_key
        )

        if raw_value in (None, ""):
            return None

        try:
            return float(raw_value)
        except (TypeError, ValueError):
            _LOGGER.debug(
                "Unable to convert DeyeCloud value %r for %s "
                "on device %s",
                raw_value,
                self.entity_description.data_key,
                self._device_sn,
            )
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return diagnostic attributes for the measurement."""
        device_data = self.device_data

        attributes: dict[str, Any] = {
            "device_serial_number": self._device_sn,
            "deye_data_key": self.entity_description.data_key,
        }

        device_type = device_data.get("device_type")
        device_state = device_data.get("device_state")
        collection_time = device_data.get("collection_time")

        if device_type is not None:
            attributes["device_type"] = device_type

        if device_state is not None:
            attributes["device_state"] = device_state

        if collection_time is not None:
            attributes["collection_time"] = collection_time

        api_unit = self.get_measurement_unit(
            self.entity_description.data_key
        )

        if api_unit is not None:
            attributes["deye_api_unit"] = api_unit

        return attributes