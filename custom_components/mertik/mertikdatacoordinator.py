from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

import logging

_LOGGER = logging.getLogger(__name__)

from datetime import timedelta

from .mertik import Mertik


class MertikDataCoordinator(DataUpdateCoordinator):
    """Mertik custom coordinator."""

    def __init__(self, hass, mertik):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Mertik",
            update_interval=timedelta(seconds=10),
        )
        self.mertik = mertik

    @property
    def is_on(self) -> bool:
        return self.mertik.is_on or self.mertik.is_igniting

    def ignite_fireplace(self):
        self.mertik.ignite_fireplace()

    def guard_flame_off(self):
        self.mertik.guard_flame_off()

    @property
    def is_aux_on(self) -> bool:
        return self.mertik.is_on and self.mertik.is_aux_on

    def aux_on(self):
        self.mertik.aux_on()

    def aux_off(self):
        self.mertik.aux_off()

    def get_flame_height(self) -> int:
        """Getting flame via Mertik Module"""
        return self.mertik.get_flame_height()

    def set_flame_height(self, flame_height) -> None:
        """Setting flame via Mertik Module"""
        self.mertik.set_flame_height(flame_height)

    @property
    def ambient_temperature(self) -> float:
        return self.mertik.ambient_temperature

    @property
    def is_light_on(self) -> bool:
        return self.mertik.is_light_on

    def light_on(self):
        self.mertik.light_on()

    def light_off(self):
        self.mertik.light_off()

    def set_light_brightness(self, brightness) -> None:
        self.mertik.set_light_brightness(brightness)

    @property
    def light_brightness(self) -> int:
        return self.mertik.light_brightness

    async def _async_update_data(self):
        self.mertik.refresh_status()
