"""Sensor for Econet300SOL."""

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300SOLApi, EconetDataCoordinator
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_CATEGORY,
    ENTITY_ICON,
    ENTITY_PRECISION,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    SENSOR_MAP_KEY,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    STATE_CLASS_MAP,
)
from .entity import EconetEntity, LambdaEntity, MixerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes ecoNET sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


class EconetSensor(EconetEntity, SensorEntity):
    """Represents an ecoNET sensor entity."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300SOLApi,
    ):
        """Initialize a new ecoNET sensor entity."""
        self.entity_description = entity_description
        self.api = api
        self._attr_native_value = None
        super().__init__(coordinator)

    def _sync_state(self, value) -> None:
        """Synchronize the state of the sensor entity."""
        if isinstance(value, dict):
            value = value.get("value")
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


# Add MixerSensor check class Mypy warning
# Definition of "entity_description" in base class "EconetEntity" is incompatible with definition in base
# class "SensorEntity"
class MixerSensor(MixerEntity, EconetSensor):
    """Mixer sensor class."""

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300SOLApi,
        idx: int,
    ):
        """Initialize a new instance of the EconetSensor class."""
        super().__init__(description, coordinator, api, idx)


class LambdaSensors(LambdaEntity, EconetSensor):
    """Lambda sensor class."""

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300SOLApi,
    ):
        """Initialize a new instance of the EconetSensor class."""
        super().__init__(description, coordinator, api)


def create_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create ecoNET300SOL sensor entity based on supplied key."""
    _LOGGER.debug("Creating sensor entity description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        name=key,
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        entity_category=ENTITY_CATEGORY.get(key, None),
        translation_key=camel_to_snake(key),
        icon=ENTITY_ICON.get(key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, SensorStateClass.MEASUREMENT),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),
    )
    _LOGGER.debug("Created sensor entity description: %s", entity_description)
    return entity_description


def create_controller_sensors(
    coordinator: EconetDataCoordinator, api: Econet300SOLApi
) -> list[EconetSensor]:
    """Create controller sensor entities."""
    entities: list[EconetSensor] = []

    data_regParams = coordinator.data.get("regParams", {})
    data_sysParams = coordinator.data.get("sysParams", {})

    for data_key in SENSOR_MAP_KEY["_default"]:
        _LOGGER.debug(
            "Processing entity sensor data_key: %s from regParams & sysParams", data_key
        )
        if data_key in data_regParams:
            entity = EconetSensor(
                create_sensor_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug(
                "Created and appended sensor entity from regParams: %s", entity
            )
        elif data_key in data_sysParams:
            if data_sysParams.get(data_key) is None:
                _LOGGER.warning(
                    "%s in sysParams is null, sensor will not be created.", data_key
                )
                continue
            entity = EconetSensor(
                create_sensor_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug(
                "Created and appended sensor entity from sysParams: %s", entity
            )
        else:
            _LOGGER.debug(
                "Key: %s is not mapped in regParams or sysParams, sensor entity will not be added.",
                data_key,
            )
    _LOGGER.info("Total sensor entities created: %d", len(entities))
    return entities


def can_add_mixer(key: str, coordinator: EconetDataCoordinator) -> bool:
    """Check if a mixer can be added."""
    _LOGGER.debug(
        "Checking if mixer can be added for key: %s, data %s",
        key,
        coordinator.data.get("regParams", {}),
    )
    return (
        coordinator.has_reg_data(key)
        and coordinator.data.get("regParams", {}).get(key) is not None
    )


def create_mixer_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create a sensor entity description for a mixer."""
    _LOGGER.debug("Creating Mixer entity sensor description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        icon=ENTITY_ICON.get(key, None),
        entity_category=ENTITY_CATEGORY.get(key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, SensorStateClass.MEASUREMENT),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),
    )
    _LOGGER.debug("Created Mixer entity description: %s", entity_description)
    return entity_description


def create_mixer_sensors(
    coordinator: EconetDataCoordinator, api: Econet300SOLApi
) -> list[MixerSensor]:
    """Create individual sensor descriptions for mixer sensors."""
    entities: list[MixerSensor] = []

    for key, mixer_keys in SENSOR_MIXER_KEY.items():
        # Check if all required mixer keys have valid (non-null) values
        if any(
            coordinator.data.get("regParams", {}).get(mixer_key) is None
            for mixer_key in mixer_keys
        ):
            _LOGGER.warning("Mixer: %s will not be created due to invalid data.", key)
            continue

        # Create sensors for this mixer
        for mixer_key in mixer_keys:
            mixer_sensor_entity = create_mixer_sensor_entity_description(mixer_key)
            entities.append(MixerSensor(mixer_sensor_entity, coordinator, api, key))
            _LOGGER.debug("Added Mixer: %s, Sensor: %s", key, mixer_key)

    return entities


# Create Lambda sensor entity description and Lambda sensor


def create_lambda_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create a sensor entity description for a Lambda."""
    _LOGGER.debug("Creating Lambda entity sensor description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        icon=ENTITY_ICON.get(key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, None),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x / 10),
    )
    _LOGGER.debug("Created LambdaSensors entity description: %s", entity_description)
    return entity_description


def create_lambda_sensors(coordinator: EconetDataCoordinator, api: Econet300SOLApi):
    """Create controller sensor entities."""
    entities: list[LambdaSensors] = []
    sys_params = coordinator.data.get("sysParams", {})

    # Check if moduleLambdaSoftVer is None
    if sys_params.get("moduleLambdaSoftVer") is None:
        _LOGGER.info("moduleLambdaSoftVer is None, no lambda sensors will be created")
        return entities

    coordinator_data = coordinator.data.get("regParams", {})

    for data_key in SENSOR_MAP_KEY["lambda"]:
        if data_key in coordinator_data:
            entities.append(
                LambdaSensors(
                    create_lambda_sensor_entity_description(data_key), coordinator, api
                )
            )
            _LOGGER.debug(
                "Key: %s mapped, lamda sensor entity will be added",
                data_key,
            )
            continue
        _LOGGER.warning(
            "Key: %s is not mapped, lamda sensor entity will not be added",
            data_key,
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
    entities.extend(create_controller_sensors(coordinator, api))
    entities.extend(create_mixer_sensors(coordinator, api))
    entities.extend(create_lambda_sensors(coordinator, api))

    async_add_entities(entities)
    return True
