"""Sensor for Econet300"""
from dataclasses import dataclass
from typing import Callable, Any

import logging

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import EconetDataCoordinator, Econet300Api
from .const import (
    DOMAIN,
    SERVICE_COORDINATOR,
    SERVICE_API,
    REG_PARAM_MAP,
    REG_PARAM_PRECICION,
    REG_PARAM_UNIT,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes Econet sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


SENSOR_TYPES: tuple[EconetSensorEntityDescription, ...] = (
    EconetSensorEntityDescription(
        key="1031",
        name="Mixer 1 set temp.",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        process_val=lambda x: round(x, 2),
    ),
    EconetSensorEntityDescription(
        key="28",
        translation_key= REG_PARAM_MAP[28],
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature[REG_PARAM_UNIT[28]],
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=REG_PARAM_PRECICION[REG_PARAM_MAP[28]],
        process_val=lambda x: x,
    ),
    EconetSensorEntityDescription(
        key="1794",
        translation_key=REG_PARAM_MAP[1794],
        icon="mdi:thermometer",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        suggested_display_precision=REG_PARAM_PRECICION[REG_PARAM_MAP[1794]],
        process_val=lambda x: x,
    ),
)


class EconetSensor(SensorEntity):
    """Econet Sensor"""

    def __init__(self, entity_description, name, unique_id):
        super().__init__(name=name, unique_id=unique_id)
        self.entity_description = entity_description
        self._attr_native_value = None

    def _sync_state(self, value):
        """Sync state"""
        _LOGGER.debug("Update EconetSensor entity: %s", self.entity_description.name)

        self._attr_native_value = self.entity_description.process_val(value)

        self.async_write_ha_state()


class ControllerSensor(EconetEntity, EconetSensor):
    """class controller"""

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        super().__init__(description, coordinator, api)


def can_add(desc: EconetSensorEntityDescription, coordinator: EconetDataCoordinator):
    """Check it can add key"""
    _LOGGER.debug(
                "Coordinator hass data: %s does not exist, entity will not be added",
                coordinator.data,
            )
    return coordinator.has_data(desc.key) and coordinator.data[desc.key] is not None


def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """add key"""
    entities = []

    for description in SENSOR_TYPES:
        if can_add(description, coordinator):
            entities.append(ControllerSensor(description, coordinator, api))
        else:
            _LOGGER.debug(
                "Availability key: %s does not exist, entity will not be added",
                description.key,
            )

    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSensor] = []
    entities = entities + create_controller_sensors(coordinator, api)

    return async_add_entities(entities)
