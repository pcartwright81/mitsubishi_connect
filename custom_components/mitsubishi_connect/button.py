"""Button platform for Mitsubishi Connect control."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from custom_components.mitsubishi_connect.const import LIGHTS

from .entity import MitsubishiConnectEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MitsbishiConnectDataUpdateCoordinator
    from .data import MitsubishiConnectConfigEntry, VehicleData

ENTITY_DESCRIPTIONS = (
    ButtonEntityDescription(
        key=LIGHTS.lower(),
    ),
)


async def async_setup_entry(
    _: HomeAssistant,
    entry: MitsubishiConnectConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        MitsubishiConnectButton(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            vehicle_data=vehicle_data,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for vehicle_data in entry.runtime_data.coordinator.data.values()
    )


class MitsubishiConnectButton(MitsubishiConnectEntity, ButtonEntity):
    """Control Button class."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MitsbishiConnectDataUpdateCoordinator,
        vehicle_data: VehicleData,
        entity_description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button class."""
        super().__init__(coordinator, vehicle_data, entity_description)
        self.entity_description: ButtonEntityDescription = entity_description

    @property
    def translation_key(self) -> str:
        """Return the translation key for the entity."""
        return self.entity_description.key

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.send_command(self.vin, self.entity_description.key)
