from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    entities = []

    entities.append(
        MertikOnOffSwitchEntity(hass, dataservice, entry.entry_id, entry.data["name"])
    )

    entities.append(
        MertikAuxOnOffSwitchEntity(
            hass, dataservice, entry.entry_id, entry.data["name"] + " Aux"
        )
    )

    async_add_entities(entities)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "number")
    )


class MertikOnOffSwitchEntity(CoordinatorEntity, SwitchEntity):
    def __init__(self, hass, dataservice, entry_id, name):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name
        self._attr_unique_id = entry_id + "-OnOff"

    @property
    def is_on(self):
        """Return true if the device is on."""
        return bool(self._dataservice.is_on)

    async def async_turn_on(self, **kwargs):
        self._dataservice.ignite_fireplace()

    async def async_turn_off(self, **kwargs):
        self._dataservice.guard_flame_off()

    @property
    def icon(self) -> str:
        """Icon of the entity."""
        return "mdi:fireplace"


class MertikAuxOnOffSwitchEntity(CoordinatorEntity, SwitchEntity):
    def __init__(self, hass, dataservice, entry_id, name):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name
        self._attr_unique_id = entry_id + "-AuxOnOff"

    @property
    def is_on(self):
        """Return true if the device is on."""
        return bool(self._dataservice.is_aux_on)

    async def async_turn_on(self, **kwargs):
        self._dataservice.aux_on()

    async def async_turn_off(self, **kwargs):
        self._dataservice.aux_off()

    @property
    def icon(self) -> str:
        """Icon of the entity."""
        return "mdi:light"
