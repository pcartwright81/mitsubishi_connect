"""Mitsubishi Connect Entity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import MitsbishiConnectDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription

    from custom_components.mitsubishi_connect.data import VehicleData


class MitsubishiConnectEntity(CoordinatorEntity[MitsbishiConnectDataUpdateCoordinator]):
    """Mitsubishi Connect Entity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        vehicle_data: VehicleData,
        description: EntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        self.vehicle_data = vehicle_data
        self.vin = vehicle_data.vin
        self._attr_unique_id = f"{self.vin[-4:]}_{self.entity_description.key}".lower()
        self.entity_id = (
            f"{DOMAIN}.{self.vin[-4:]}_{self.entity_description.key}".lower()
        )
        self.use_device_name = True
        vehicle = vehicle_data.vehicle
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.vin[-4:])},
            manufacturer="Mitsubishi",
            name=f"{vehicle.year} {vehicle.model_description}",
        )
