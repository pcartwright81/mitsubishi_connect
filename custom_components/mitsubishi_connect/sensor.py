"""Sensor platform for mitsubishi_connect."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant, callback

from .entity import MitsubishiConnectEntity

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime, time

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from mitsubishi_connect_client.mitsubishi_connect_client import VehicleState

    from .coordinator import MitsbishiConnectDataUpdateCoordinator
    from .data import MitsubishiConnectConfigEntry


@dataclass(frozen=True, kw_only=True)
class MitsubishiConnectSensorEntityDescription(
    SensorEntityDescription, frozen_or_thawed=True
):
    """A class that describes binary sensor entities."""

    icon_on: str | None = None
    value_fn: Callable[[VehicleState], float | str | datetime | time | None]


ENTITY_DESCRIPTIONS = (
    MitsubishiConnectSensorEntityDescription(
        key="odometer",
        name="Odometer",
        icon="mdi:counter",
        value_fn=lambda x: next(iter(x.state.odo[-1].values())),  # get the last odo
    ),
    MitsubishiConnectSensorEntityDescription(
        key="range",
        name="range",
        icon="mdi:numeric",
        value_fn=lambda x: x.state.charging_control.cruising_range_combined,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MitsubishiConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        MitsubishiConnectSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            vehicle_state=vehicle_state,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for vehicle_state in entry.runtime_data.coordinator.data.values()
    )


class MitsubishiConnectSensor(MitsubishiConnectEntity, SensorEntity):
    """mitsubishi_connect Sensor class."""

    entity_description: MitsubishiConnectSensorEntityDescription

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        entity_description: MitsubishiConnectSensorEntityDescription,
        vehicle_state: VehicleState,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, vehicle_state, entity_description)
        self.entity_description = entity_description

    @property
    def native_value(self) -> Any:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(self.vehicle_state)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.vehicle_state.vin in self.coordinator.data:
            self.vehicle_state = self.coordinator.data[self.vehicle_state.vin]
            self.async_write_ha_state()
