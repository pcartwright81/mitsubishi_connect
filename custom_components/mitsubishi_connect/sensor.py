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

    from custom_components.mitsubishi_connect.data import VehicleData

    from .coordinator import MitsbishiConnectDataUpdateCoordinator
    from .data import MitsubishiConnectConfigEntry


@dataclass(frozen=True, kw_only=True)
class MitsubishiConnectSensorEntityDescription(
    SensorEntityDescription, frozen_or_thawed=True
):
    """A class that describes binary sensor entities."""

    icon_on: str | None = None
    value_fn: Callable[[VehicleData], float | str | datetime | time | None]


ENTITY_DESCRIPTIONS = (
    MitsubishiConnectSensorEntityDescription(
        key="odometer",
        name="Odometer",
        icon="mdi:counter",
        value_fn=lambda x: next(
            iter(x.vehicle_state.state.odo[-1].values())
        ),  # get the last odo
    ),
    MitsubishiConnectSensorEntityDescription(
        key="range",
        name="range",
        icon="mdi:numeric",
        value_fn=lambda x: x.vehicle_state.state.charging_control.cruising_range_combined,  # noqa: E501
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
            vehicle_data=vehicle_data,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for vehicle_data in entry.runtime_data.coordinator.data.values()
    )


class MitsubishiConnectSensor(MitsubishiConnectEntity, SensorEntity):
    """mitsubishi_connect Sensor class."""

    entity_description: MitsubishiConnectSensorEntityDescription

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        entity_description: MitsubishiConnectSensorEntityDescription,
        vehicle_data: VehicleData,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, vehicle_data, entity_description)
        self.entity_description = entity_description

    @property
    def native_value(self) -> Any:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(self.vehicle_data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.vin in self.coordinator.data:
            self.vehicle_data.vehicle_state = self.coordinator.data[
                self.vin
            ].vehicle_state
            self.vehicle_data.vhr_item = self.coordinator.data[self.vin].vhr_item
            self.async_write_ha_state()
