"""Define a device tracker."""

from collections.abc import Callable

from attr import dataclass
from homeassistant.components.device_tracker import (
    TrackerEntity,  # type: ignore i am pretty sure it is but ?
    TrackerEntityDescription,  # type: ignore i am pretty sure it is but ?
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import MitsbishiConnectDataUpdateCoordinator
from .data import MitsubishiConnectConfigEntry, VehicleData
from .entity import MitsubishiConnectEntity


@dataclass(frozen=True, kw_only=True)
class MitsubishiConnectTrackerEntityDescription(
    TrackerEntityDescription, frozen_or_thawed=True
):
    """Describes a here comes the bus tracker."""

    latitude_fn: Callable[[VehicleData], float | None]
    longitude_fn: Callable[[VehicleData], float | None]


ENTITY_DESCRIPTION = [
    MitsubishiConnectTrackerEntityDescription(
        key="location",
        latitude_fn=lambda x: x.vehicle_state.state.ext_loc_map.lat,
        longitude_fn=lambda x: x.vehicle_state.state.ext_loc_map.lon,
    ),
]


async def async_setup_entry(
    _: HomeAssistant,
    entry: MitsubishiConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up bus sensors."""
    async_add_entities(
        MitsubishiConnectTracker(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            vehicle_data=vehicle_data,
        )
        for entity_description in ENTITY_DESCRIPTION
        for vehicle_data in entry.runtime_data.coordinator.data.values()
    )


class MitsubishiConnectTracker(MitsubishiConnectEntity, TrackerEntity):
    """Defines a single bus sensor."""

    _attr_has_entity_name = True
    entity_description: MitsubishiConnectTrackerEntityDescription

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        vehicle_data: VehicleData,
        entity_description: MitsubishiConnectTrackerEntityDescription,
    ) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, vehicle_data, entity_description)

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self.entity_description.latitude_fn(self.vehicle_data)

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self.entity_description.longitude_fn(self.vehicle_data)

    @property
    def location_accuracy(self) -> int:
        """Return the gps accuracy of the device."""
        return 100

    @property
    def translation_key(self) -> str:
        """Return the translation key for the entity."""
        return self.entity_description.key

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.vin in self.coordinator.data:
            self.vehicle_data.vehicle_state = self.coordinator.data[
                self.vin
            ].vehicle_state
            self.async_write_ha_state()
