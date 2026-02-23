"""Mertik Maxitrol number platform."""

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .mertikdatacoordinator import MertikDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mertik number entities from a config entry."""
    dataservice: MertikDataCoordinator = entry.runtime_data

    async_add_entities(
        [MertikFlameHeightEntity(dataservice, entry.entry_id, entry.data["name"])]
    )


class MertikFlameHeightEntity(CoordinatorEntity[MertikDataCoordinator], NumberEntity):
    """Representation of a Mertik flame height number entity."""

    def __init__(
        self, dataservice: MertikDataCoordinator, entry_id: str, name: str
    ) -> None:
        """Initialize the flame height entity."""
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name + " Flame Height"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 12
        self._attr_unique_id = entry_id + "-FlameHeight"

    @property
    def native_value(self) -> float:
        """Return the current flame height value."""
        return self._dataservice.get_flame_height()

    async def async_set_native_value(self, value: float) -> None:
        """Set the flame height value."""
        await self.hass.async_add_executor_job(
            self._dataservice.set_flame_height, int(value)
        )
        self._dataservice.async_set_updated_data(None)

    @property
    def icon(self) -> str:
        """Return the icon of the entity."""
        return "mdi:fire"
