from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.sensor import SensorEntity

from homeassistant.const import TEMP_CELSIUS

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    entities = []

    entities.append(
        MertikAmbientTemperatureSensorEntity(
            hass, dataservice, entry.entry_id, entry.data["name"]
        )
    )

    async_add_entities(entities)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "light")
    )


class MertikAmbientTemperatureSensorEntity(CoordinatorEntity, SensorEntity):
    def __init__(self, hass, dataservice, entry_id, name):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name + " Ambient Temperature"
        self._device_class = "temperature"
        self._attr_unique_id = entry_id + "-AmbientTemperature"

    @property
    def state(self):
        return self._dataservice.ambient_temperature

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS
