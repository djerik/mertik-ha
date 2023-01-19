from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.number import NumberEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    entities = []

    entities.append(
        MertikFlameHeightEntity(hass, dataservice, entry.entry_id, entry.data["name"])
    )

    async_add_entities(entities)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )


class MertikFlameHeightEntity(CoordinatorEntity, NumberEntity):
    def __init__(self, hass, dataservice, entry_id, name):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name + " Flame Height"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 12
        self._attr_unique_id = entry_id + "-FlameHeight"

    @property
    def native_value(self) -> float:
        return self._dataservice.get_flame_height()

    async def async_set_native_value(self, value: float) -> None:
        await( self.hass.async_add_executor_job(self._dataservice.set_flame_height, int(value)))
        self._dataservice.async_set_updated_data(None)

    @property
    def icon(self) -> str:
        """Icon of the entity."""
        return "mdi:fire"
