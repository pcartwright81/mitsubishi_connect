"""Custom types for mitsubishi_connect."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration
    from mitsubishi_connect_client.mitsubishi_connect_client import (
        MitsubishiConnectClient,
    )

    from .coordinator import MitsbishiConnectDataUpdateCoordinator


type MitsubishiConnectConfigEntry = ConfigEntry[MitsubishiConnectData]


@dataclass
class MitsubishiConnectData:
    """Data for the Blueprint integration."""

    client: MitsubishiConnectClient
    coordinator: MitsbishiConnectDataUpdateCoordinator
    integration: Integration
