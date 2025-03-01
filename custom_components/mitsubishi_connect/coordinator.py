"""DataUpdateCoordinator for mitsubishi_connect."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.mitsubishi_connect.const import LIGHTS
from custom_components.mitsubishi_connect.data import VehicleData

if TYPE_CHECKING:
    from .data import MitsubishiConnectConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class MitsbishiConnectDataUpdateCoordinator(
    DataUpdateCoordinator[dict[str, VehicleData]]
):
    """Class to manage fetching data from the API."""

    config_entry: MitsubishiConnectConfigEntry
    token_expiration: datetime
    refresh_expiration: datetime

    async def _async_update_data(self) -> dict[str, VehicleData]:
        """Update data via library."""
        client = self.config_entry.runtime_data.client
        await self._check_login()
        for vin in self.data:
            self.data[vin].vehicle_state = await client.get_vehicle_state(vin)
            self.data[vin].vhr_item = await client.get_status(vin)

        return self.data

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh."""
        client = self.config_entry.runtime_data.client
        self.data = {}
        await self._check_login()
        vehicles = await client.get_vehicles()
        for vehicle in vehicles.vehicles:
            vehicle_state = await client.get_vehicle_state(vehicle.vin)
            vehicle_status = await client.get_status(vehicle.vin)
            self.data[vehicle.vin] = VehicleData(vehicle, vehicle_state, vehicle_status)

    async def send_command(self, vin: str, key: str) -> None:
        """Send a command to the api."""
        client = self.config_entry.runtime_data.client
        if key == LIGHTS:
            await client.flash_lights(vin)

    async def _check_login(self) -> None:
        """Ensure the api is ready to use."""

        def set_token() -> None:
            self.token_expiration = datetime.now(tz=UTC) + timedelta(
                seconds=client.token.expires_in
            )
            self.refresh_expiration = datetime.now(tz=UTC) + timedelta(
                seconds=client.token.refresh_expires_in
            )

        client = self.config_entry.runtime_data.client
        if not hasattr(client, "token"):
            await client.login()
            set_token()
            return
        if datetime.now(tz=UTC) + timedelta(minutes=5) > self.token_expiration:
            await client.refresh_token()
            set_token()
