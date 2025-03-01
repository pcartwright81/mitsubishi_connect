"""Custom types for mitsubishi_connect."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration
    from mitsubishi_connect_client.mitsubishi_connect_client import (
        MitsubishiConnectClient,
        VehicleState,
    )
    from mitsubishi_connect_client.vehicle import Vehicle
    from mitsubishi_connect_client.vehicle_status import VhrItem

    from .coordinator import MitsbishiConnectDataUpdateCoordinator


type MitsubishiConnectConfigEntry = ConfigEntry[MitsubishiConnectData]


@dataclass
class MitsubishiConnectData:
    """Data for the Mitsubishi Connect integration."""

    client: MitsubishiConnectClient
    coordinator: MitsbishiConnectDataUpdateCoordinator
    integration: Integration


@dataclass
class VehicleData:
    """Data Class for the Mitsubishi Connect integration."""

    vehicle: Vehicle
    vehicle_state: VehicleState
    vhr_item: VhrItem

    @property
    def vin(self) -> str:
        """Return the vehicle VIN."""
        return self.vehicle.vin
