"""
Custom integration to integrate mitsubishi_connect with Home Assistant.

For more details about this integration, please refer to
https://github.com/pcartwright81/mitsubishi_connect
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.loader import async_get_loaded_integration
from mitsubishi_connect_client.mitsubishi_connect_client import MitsubishiConnectClient

from .const import DOMAIN, LOGGER
from .coordinator import MitsbishiConnectDataUpdateCoordinator
from .data import MitsubishiConnectData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MitsubishiConnectConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: MitsubishiConnectConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = MitsbishiConnectDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=10),
    )
    entry.runtime_data = MitsubishiConnectData(
        client=MitsubishiConnectClient(),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MitsubishiConnectConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: MitsubishiConnectConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
