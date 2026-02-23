"""Mertik data update coordinator."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .mertik import Mertik

_LOGGER = logging.getLogger(__name__)


class MertikDataCoordinator(DataUpdateCoordinator[None]):
    """Mertik custom coordinator."""

    def __init__(self, hass: HomeAssistant, mertik: Mertik, config_entry: ConfigEntry) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Mertik",
            update_interval=timedelta(seconds=10),
            config_entry=config_entry,
        )
        self.mertik = mertik

    @property
    def is_on(self) -> bool:
        """Return true if the fireplace is on or igniting."""
        return self.mertik.is_on or self.mertik.is_igniting

    def ignite_fireplace(self):
        """Ignite the fireplace."""
        self.mertik.ignite_fireplace()

    def guard_flame_off(self):
        """Turn off the fireplace via guard flame off."""
        self.mertik.guard_flame_off()

    @property
    def is_aux_on(self) -> bool:
        """Return true if the auxiliary flame is on."""
        return self.mertik.is_on and self.mertik.is_aux_on

    def aux_on(self):
        """Turn on the auxiliary flame."""
        self.mertik.aux_on()

    def aux_off(self):
        """Turn off the auxiliary flame."""
        self.mertik.aux_off()

    def get_flame_height(self) -> int:
        """Get flame height via Mertik module."""
        return self.mertik.get_flame_height()

    def set_flame_height(self, flame_height) -> None:
        """Set flame height via Mertik module."""
        self.mertik.set_flame_height(flame_height)

    @property
    def ambient_temperature(self) -> float:
        """Return the ambient temperature."""
        return self.mertik.ambient_temperature

    @property
    def is_light_on(self) -> bool:
        """Return true if the light is on."""
        return self.mertik.is_light_on

    @property
    def dim_level(self) -> float:
        """Return the dim level as a 0.0–1.0 value."""
        return self.mertik.dim_level

    def set_light_dim(self, dim_level: float) -> None:
        """Set the light dim level (0.0–1.0) via Mertik module."""
        self.mertik.set_light_dim(dim_level)

    async def _async_update_data(self):
        """Fetch data from the fireplace device."""
        await self.hass.async_add_executor_job(self.mertik.refresh_status)
