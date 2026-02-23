"""Sensor platform for Mertik integration."""

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .mertikdatacoordinator import MertikDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mertik sensor entities from a config entry."""
    dataservice: MertikDataCoordinator = entry.runtime_data

    async_add_entities(
        [
            MertikAmbientTemperatureSensorEntity(
                dataservice, entry.entry_id, entry.data["name"]
            )
        ]
    )


class MertikAmbientTemperatureSensorEntity(
    CoordinatorEntity[MertikDataCoordinator], SensorEntity
):
    """Sensor entity for Mertik ambient temperature."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(
        self, dataservice: MertikDataCoordinator, entry_id: str, name: str
    ) -> None:
        """Initialize the ambient temperature sensor."""
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._attr_name = name + " Ambient Temperature"
        self._attr_unique_id = entry_id + "-AmbientTemperature"

    @property
    def native_value(self) -> float:
        """Return the current ambient temperature."""
        return self._dataservice.ambient_temperature
