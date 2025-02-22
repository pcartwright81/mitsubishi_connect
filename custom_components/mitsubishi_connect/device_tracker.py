"""Define a device tracker."""

from collections.abc import Callable

from attr import dataclass
from homeassistant.components.device_tracker import (
    TrackerEntity,  # type: ignore i am pretty sure it is but ?
    TrackerEntityDescription,  # type: ignore i am pretty sure it is but ?
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from mitsubishi_connect_client.mitsubishi_connect_client import VehicleState

from .coordinator import MitsbishiConnectDataUpdateCoordinator
from .data import MitsubishiConnectConfigEntry
from .entity import MitsubishiConnectEntity


@dataclass(frozen=True, kw_only=True)
class MitsubishiConnectTrackerEntityDescription(
    TrackerEntityDescription, frozen_or_thawed=True
):
    """Describes a here comes the bus tracker."""

    latitude_fn: Callable[[VehicleState], float | None]
    longitude_fn: Callable[[VehicleState], float | None]


DEVICE_TRACKERS = [
    MitsubishiConnectTrackerEntityDescription(
        name="",
        key="location",
        latitude_fn=lambda x: x.state.ext_loc_map.lat,
        longitude_fn=lambda x: x.state.ext_loc_map.lon,
    ),
]


async def async_setup_entry(
    _: HomeAssistant,
    entry: MitsubishiConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up bus sensors."""
    async_add_entities(
        MitsubishiConnectTracker(entry.runtime_data.coordinator, vehicle_state, tracker)
        for vehicle_state in entry.runtime_data.coordinator.data.values()
        for tracker in DEVICE_TRACKERS
    )


class MitsubishiConnectTracker(MitsubishiConnectEntity, TrackerEntity):
    """Defines a single bus sensor."""

    entity_description: MitsubishiConnectTrackerEntityDescription

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        vehicle_state: VehicleState,
        description: MitsubishiConnectTrackerEntityDescription,
    ) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, vehicle_state, description)

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self.entity_description.latitude_fn(self.vehicle_state)

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self.entity_description.longitude_fn(self.vehicle_state)

    @property
    def location_accuracy(self) -> int:
        """Return the gps accuracy of the device."""
        return 100

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.vehicle_state.vin in self.coordinator.data:
            self.vehicle_state = self.coordinator.data[self.vehicle_state.vin]
            self.async_write_ha_state()
