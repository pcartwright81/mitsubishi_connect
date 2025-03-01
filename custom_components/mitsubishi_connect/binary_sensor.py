"""Binary sensor platform for mitsubishi_connect."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant, callback

from .entity import MitsubishiConnectEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.mitsubishi_connect.data import VehicleData

    from .coordinator import MitsbishiConnectDataUpdateCoordinator
    from .data import MitsubishiConnectConfigEntry


@dataclass(frozen=True, kw_only=True)
class MitsubishiConnectBinarySensorEntityDescription(
    BinarySensorEntityDescription, frozen_or_thawed=True
):
    """A class that describes binary sensor entities."""

    icon_on: str | None = None
    value_fn: Callable[[VehicleData], bool | None]


ENTITY_DESCRIPTIONS = (
    MitsubishiConnectBinarySensorEntityDescription(
        key="cst",
        name="cst",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.cst),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="tu_state",
        name="tu_state",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.tu_state),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="ods",
        name="ods",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.ods),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="ignition",
        name="Ignition",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.ignition_state),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="theft_alarm",
        name="theft_alarm",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.theft_alarm),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="svla",
        name="svla",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.svla),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="svtb",
        name="svtb",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.svtb),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="diagnostic",
        name="diagnostic",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.diagnostic),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="privacy",
        name="privacy",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.privacy),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="factory_reset",
        name="factory_reset",
        icon="mdi:engine-off",
        icon_on="mdi:engine",
        value_fn=lambda x: bool(x.vehicle_state.state.factory_reset),
    ),
    MitsubishiConnectBinarySensorEntityDescription(
        key="accessible",
        name="Accessible",
        icon="mdi:engine-off",
        icon_on="mdi:car-connected",
        value_fn=lambda x: bool(x.vehicle_state.state.accessible),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MitsubishiConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        MitsubishiConnectBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            vehicle_data=vehicle_data,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for vehicle_data in entry.runtime_data.coordinator.data.values()
    )


class MitsubishiConnectBinarySensor(MitsubishiConnectEntity, BinarySensorEntity):
    """mitsubishi_connect binary_sensor class."""

    entity_description: MitsubishiConnectBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        entity_description: MitsubishiConnectBinarySensorEntityDescription,
        vehicle_data: VehicleData,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator, vehicle_data, entity_description)
        self.entity_description = entity_description
        self._is_on: bool | None = None

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        self._is_on = self.entity_description.value_fn(self.vehicle_data)
        return self._is_on

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        if self._is_on:
            return self.entity_description.icon_on
        return self.entity_description.icon

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.vin in self.coordinator.data:
            self.vehicle_data.vehicle_state = self.coordinator.data[
                self.vin
            ].vehicle_state
            self.vehicle_data.vhr_item = self.coordinator.data[self.vin].vhr_item
            self.async_write_ha_state()
