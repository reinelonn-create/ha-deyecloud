"""Base entities for the DeyeCloud integration."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DeyeCloudCoordinator


class DeyeCloudEntity(CoordinatorEntity[DeyeCloudCoordinator]):
    """Base class for DeyeCloud entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DeyeCloudCoordinator,
        device_sn: str,
        device: dict[str, Any] | None = None,
    ) -> None:
        """Initialize a DeyeCloud entity."""
        super().__init__(coordinator)

        self._device_sn = device_sn
        self._device = device or {}

        product_id = self._device.get("productId")
        device_type = (
            self._device.get("deviceType")
            or "INVERTER"
        )

        device_info: dict[str, Any] = {
            "identifiers": {(DOMAIN, device_sn)},
            "manufacturer": "Deye",
            "model": self._format_model(device_type),
            "name": f"Deye inverter {device_sn}",
            "serial_number": device_sn,
        }

        if product_id not in (None, ""):
            device_info["model_id"] = str(product_id)

        self._attr_device_info = DeviceInfo(**device_info)

    @staticmethod
    def _format_model(device_type: Any) -> str:
        """Return a readable model name."""
        if not isinstance(device_type, str):
            return "DeyeCloud inverter"

        normalized = device_type.strip()

        if not normalized:
            return "DeyeCloud inverter"

        if normalized.upper() == "INVERTER":
            return "DeyeCloud inverter"

        return f"DeyeCloud {normalized.replace('_', ' ').lower()}"

    @property
    def device_data(self) -> dict[str, Any]:
        """Return coordinator data for this inverter."""
        coordinator_data = self.coordinator.data

        if not isinstance(coordinator_data, dict):
            return {}

        device_data = coordinator_data.get(
            self._device_sn,
            {},
        )

        if not isinstance(device_data, dict):
            return {}

        return device_data

    @property
    def device_values(self) -> dict[str, dict[str, Any]]:
        """Return normalized measurement values."""
        values = self.device_data.get("values", {})

        if not isinstance(values, dict):
            return {}

        return values

    @property
    def device_metadata(self) -> dict[str, Any]:
        """Return metadata supplied by the device-list endpoint."""
        return self._device

    def get_measurement(
        self,
        data_key: str,
    ) -> dict[str, Any] | None:
        """Return a measurement by its DeyeCloud data key."""
        item = self.device_values.get(data_key)

        if not isinstance(item, dict):
            return None

        return item

    def get_measurement_value(
        self,
        data_key: str,
    ) -> Any:
        """Return the raw value for a measurement."""
        item = self.get_measurement(data_key)

        if item is None:
            return None

        return item.get("value")

    def get_measurement_unit(
        self,
        data_key: str,
    ) -> str | None:
        """Return the API unit for a measurement."""
        item = self.get_measurement(data_key)

        if item is None:
            return None

        unit = item.get("unit")

        if unit in (None, ""):
            return None

        return str(unit)