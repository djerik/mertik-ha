"""Mertik Maxitrol switch platform."""

from homeassistant.components.switch import SwitchEntity
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
    """Set up Mertik switches from a config entry."""
    dataservice: MertikDataCoordinator = entry.runtime_data

    async_add_entities(
        [
            MertikOnOffSwitchEntity(dataservice, entry.entry_id, entry.data["name"]),
            MertikAuxOnOffSwitchEntity(
                dataservice, entry.entry_id, entry.data["name"] + " Aux"
            ),
        ]
    )


class MertikOnOffSwitchEntity(CoordinatorEntity[MertikDataCoordinator], SwitchEntity):
    """Representation of a Mertik fireplace on/off switch."""

    def __init__(
        self, dataservice: MertikDataCoordinator, entry_id: str, name: str
    ) -> None:
        """Initialize the switch."""
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name
        self._attr_unique_id = entry_id + "-OnOff"

    @property
    def is_on(self) -> bool:
        """Return true if the device is on."""
        return bool(self._dataservice.is_on)

    async def async_turn_on(self, **_kwargs: object) -> None:
        """Turn on the fireplace."""
        await self.hass.async_add_executor_job(self._dataservice.ignite_fireplace)
        self._dataservice.async_set_updated_data(None)

    async def async_turn_off(self, **_kwargs: object) -> None:
        """Turn off the fireplace."""
        await self.hass.async_add_executor_job(self._dataservice.guard_flame_off)
        self._dataservice.async_set_updated_data(None)

    @property
    def icon(self) -> str:
        """Return the icon of the entity."""
        return "mdi:fireplace"


class MertikAuxOnOffSwitchEntity(
    CoordinatorEntity[MertikDataCoordinator], SwitchEntity
):
    """Representation of a Mertik auxiliary on/off switch."""

    def __init__(
        self, dataservice: MertikDataCoordinator, entry_id: str, name: str
    ) -> None:
        """Initialize the switch."""
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name
        self._attr_unique_id = entry_id + "-AuxOnOff"

    @property
    def is_on(self) -> bool:
        """Return true if the auxiliary is on."""
        return bool(self._dataservice.is_aux_on)

    async def async_turn_on(self, **_kwargs: object) -> None:
        """Turn on the auxiliary."""
        await self.hass.async_add_executor_job(self._dataservice.aux_on)
        self._dataservice.async_set_updated_data(None)

    async def async_turn_off(self, **_kwargs: object) -> None:
        """Turn off the auxiliary."""
        await self.hass.async_add_executor_job(self._dataservice.aux_off)
        self._dataservice.async_set_updated_data(None)

    @property
    def icon(self) -> str:
        """Return the icon of the entity."""
        return "mdi:fire"
