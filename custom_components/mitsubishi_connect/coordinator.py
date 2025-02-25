"""DataUpdateCoordinator for mitsubishi_connect."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

if TYPE_CHECKING:
    from mitsubishi_connect_client.mitsubishi_connect_client import VehicleState

    from .data import MitsubishiConnectConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class MitsbishiConnectDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: MitsubishiConnectConfigEntry

    async def _async_update_data(self) -> dict[str, VehicleState]:
        """Update data via library."""
        for vin in self.data:
            updated_state = (
                await self.config_entry.runtime_data.client.get_vehicle_state(vin)
            )
            self.data[vin] = updated_state
        return self.data

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh."""
        client = self.config_entry.runtime_data.client
        self.data = {}
        if not hasattr(client, "token"):
            await client.login()
            self.data["token_experation"] = datetime.now(tz=UTC) + timedelta(
                seconds=client.token.expires_in
            )
            self.data["refresh_experation"] = datetime.now(tz=UTC) + timedelta(
                seconds=client.token.refresh_expires_in
            )
        elif (
            datetime.now(tz=UTC) + timedelta(minutes=5) > self.data["token_experation"]
        ):
            await client.refresh_token()
        vehicles = await client.get_vehicles()
        for vehicle in vehicles.vehicles:
            vehicle_state = await client.get_vehicle_state(vehicle.vin)
            self.data[vehicle.vin] = vehicle_state
