"""Mitsubishi Connect Entity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import MitsbishiConnectDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription
    from mitsubishi_connect_client.mitsubishi_connect_client import VehicleState


class MitsubishiConnectEntity(CoordinatorEntity[MitsbishiConnectDataUpdateCoordinator]):
    """Mitsubishi Connect Entity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        vehicle_state: VehicleState,
        description: EntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        self.vehicle_state = vehicle_state
        self._attr_unique_id = (
            f"{self.vehicle_state.vin[-4:]}_{self.entity_description.key}".lower()
        )
        self.use_device_name = True
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.vehicle_state.vin[-4:])},
            manufacturer="Mitsubishi",
            name=f"{self.vehicle_state.vin}",
        )

    @property
    def unique_id(self) -> str | None:
        """Return a unique identifier for this sensor."""
        return f"{self.vehicle_state.vin[-4:]}_{self.entity_description.key}".lower()
