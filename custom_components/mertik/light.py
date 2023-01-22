from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    entities = []

    entities.append(
        MertikLightEntity(hass, dataservice, entry.entry_id, entry.data["name"])
    )

    async_add_entities(entities)


class MertikLightEntity(CoordinatorEntity, LightEntity):
    def __init__(self, hass, dataservice, entry_id, name):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name + " Light"
        self._attr_unique_id = entry_id + "-Light"
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    @property
    def is_on(self):
        """Return true if the device is on."""
        return self._dataservice.is_light_on

    @property
    def brightness(self):
        """Return true if the device is on."""
        return self._dataservice.light_brightness

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        await(self.hass.async_add_executor_job(self._dataservice.set_light_brightness, int(kwargs.get(ATTR_BRIGHTNESS))))
        self._dataservice.async_set_updated_data(None)

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        await(self.hass.async_add_executor_job(self._dataservice.light_off))
        self._dataservice.async_set_updated_data(None)
