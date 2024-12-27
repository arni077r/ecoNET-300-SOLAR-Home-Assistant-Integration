"""Constants from the Home Assistant."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PROBLEM,
    STATE_UNKNOWN,
    EntityCategory,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

# Constant for the econet Integration integration
DOMAIN = "econet300SOL"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300SOL"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300SOL"
DEVICE_INFO_MIXER_NAME = "Mixer device"
DEVICE_INFO_LAMBDA_NAME = "Module Lambda"

CONF_ENTRY_TITLE = "ecoNET300SOL"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300SOL"

## Sys params
API_SYS_PARAMS_URI = "sysParams"
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_MODEL_ID = "controllerID"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

## Reg params
API_REG_PARAMS_URI = "regParams"
API_REG_PARAMS_PARAM_DATA = "curr"

## Reg params data all in one
API_REG_PARAMS_DATA_URI = "regParams"
API_REG_PARAMS_DATA_PARAM_DATA = "curr"

# Boiler status keys map
OPERATION_MODE_NAMES = {
    0: STATE_OFF,
    1: "fire_up",
    2: "operation",
    3: "work",
    4: "supervision",
    5: STATE_PAUSED,  # "halted",
    6: "stop",
    7: "burning_off",
    8: "manual",
    9: STATE_PROBLEM,  # "alarm",
    10: "unsealing",
    11: "chimney",
    12: "stabilization",
    13: "no_transmission",
}

TRYB_MODE_NAMES = {
    1: "auto",
    2: "stop",
    3: "holiday",
}

## Editable params limits
API_EDIT_PARAM_URI = "newParam"
API_EDITABLE_PARAMS_LIMITS_URI = "editParams"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

###################################
#    NUMBER of AVAILABLE MIXERS
###################################
AVAILABLE_NUMBER_OF_MIXERS = 6
MIXER_AVAILABILITY_KEY = "mixerTemp"
MIXER_SET_AVAILABILITY_KEY = "mixerSetTemp"

# Dynamically generate SENSOR_MIXER_KEY
SENSOR_MIXER_KEY = {
    i: {f"{MIXER_AVAILABILITY_KEY}{i}", f"{MIXER_SET_AVAILABILITY_KEY}{i}"}
    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1)
}

#######################
#    REG PARAM MAPS
#######################

SENSOR_MAP_KEY = {
    "ecoster": {
        "ecoSterTemp1",
        "ecoSterTemp2",
        "Tryb_pracy",
    },
    "lambda": {
        "lambdaStatus",
        "lambdaSet",
        "lambdaLevel",
    },
    "_default": {
        "Uzysk_ca_kowity",
        "boilerPower",
        "boilerPowerKW",
        "P1",
        "P2",
        "T1",
        "T2",
        "T3",
        "T4",
        "Tryb_pracy",
        "TzCWU",
        "Moc_chwilowa",
        "tempFeeder",
        "fuelLevel",
        "tempCO",
        "tempCOSet",
        "statusCWU",
        "tempCWU",
        "tempCWUSet",
        "tempFlueGas",
        "mode",
        "fanPower",
        "thermostat",
        "tempExternalSensor",
        "tempLowerBuffer",
        "tempUpperBuffer",
        "quality",
        "signal",
        "softVer",
        "controllerID",
        "moduleASoftVer",
        "moduleBSoftVer",
        "moduleCSoftVer",
        "moduleLambdaSoftVer",
        "modulePanelSoftVer",
    },
}

BINARY_SENSOR_MAP_KEY = {
    "_default": {
        "Sch__kot_em",
        "Sch__nocne",
        "mainSrv",
        "wifi",
        "lan",
    },
}

NUMBER_MAP = {
    "Tryb_pracy":"Tryb_pracy",
    "P1":"P1",
    "P2":"P2",
    "Sch__kot_em":"Sch__kot_em",
    "Sch__nocne":"Sch__nocne",
    "Tsch__W_":"Tsch__W_",
    "Tsch__WY_":"Tsch__WY_",
    "T_aktyw_sch_":"T_aktyw_sch_",
    "Tsch__kot_em_w_":"Tsch__kot_em_w_",
    "Tsch__kot_em_wy_":"Tsch__kot_em_wy_",
    "auto_scl_akt":"auto_scl_akt",
    "Auto_sch__noc":"Auto_sch__noc",
}

# By default all sensors unit_of_measurement are None
ENTITY_UNIT_MAP = {
    "T1": UnitOfTemperature.CELSIUS,
    "T2": UnitOfTemperature.CELSIUS,
    "T3": UnitOfTemperature.CELSIUS,
    "T4": UnitOfTemperature.CELSIUS,
    "P1":PERCENTAGE,
    "P2":PERCENTAGE,
    "tempCO": UnitOfTemperature.CELSIUS,
    "tempCOSet": UnitOfTemperature.CELSIUS,
    "tempCWUSet": UnitOfTemperature.CELSIUS,
    "tempExternalSensor": UnitOfTemperature.CELSIUS,
    "tempFeeder": UnitOfTemperature.CELSIUS,
    "lambdaLevel": PERCENTAGE,
    "lambdaSet": PERCENTAGE,
    "workAt100": UnitOfTime.HOURS,
    "workAt50": UnitOfTime.HOURS,
    "workAt30": UnitOfTime.HOURS,
    "FeederWork": UnitOfTime.HOURS,
    "thermoTemp": UnitOfTemperature.CELSIUS,
    "fanPower": PERCENTAGE,
    "tempFlueGas": UnitOfTemperature.CELSIUS,
    "mixerSetTemp1": UnitOfTemperature.CELSIUS,
    "mixerTemp1": UnitOfTemperature.CELSIUS,
    "tempBack": UnitOfTemperature.CELSIUS,
    "tempCWU": UnitOfTemperature.CELSIUS,
    "boilerPower": PERCENTAGE,
    "boilerPowerKW": UnitOfPower.KILO_WATT,
    "fuelLevel": PERCENTAGE,
    "tempUpperBuffer": UnitOfTemperature.CELSIUS,
    "tempLowerBuffer": UnitOfTemperature.CELSIUS,
    "signal": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    "quality": PERCENTAGE,
    "valveMixer1": PERCENTAGE,
    "burnerOutput": PERCENTAGE,
    "mixerTemp": UnitOfTemperature.CELSIUS,
    "mixerSetTemp": UnitOfTemperature.CELSIUS,
}

# By default all sensors state_class are MEASUREMENT
STATE_CLASS_MAP: dict[str, SensorStateClass | None] = {
    "lambdaStatus": None,
    "mode": None,
    "thermostat": None,
    "statusCWU": None,
    "softVer": None,
    "controllerID": None,
    "moduleASoftVer": None,
    "moduleBSoftVer": None,
    "moduleCSoftVer": None,
    "moduleLambdaSoftVer": None,
    "modulePanelSoftVer": None,
}

# By default all sensors device_class are None
ENTITY_SENSOR_DEVICE_CLASS_MAP: dict[str, SensorDeviceClass | None] = {
    #############################
    #          SENSORS
    #############################
    "T1": SensorDeviceClass.TEMPERATURE,
    "T2": SensorDeviceClass.TEMPERATURE,
    "T3": SensorDeviceClass.TEMPERATURE,
    "T4": SensorDeviceClass.TEMPERATURE,
    "tempFeeder": SensorDeviceClass.TEMPERATURE,
    "tempExternalSensor": SensorDeviceClass.TEMPERATURE,
    "tempCO": SensorDeviceClass.TEMPERATURE,
    "tempCOSet": SensorDeviceClass.TEMPERATURE,
    "boilerPower": SensorDeviceClass.POWER_FACTOR,
    "boilerPowerKW": SensorDeviceClass.POWER,
    "fanPower": SensorDeviceClass.POWER_FACTOR,
    "tempFlueGas": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp1": SensorDeviceClass.TEMPERATURE,
    "mixerTemp": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp": SensorDeviceClass.TEMPERATURE,
    "tempBack": SensorDeviceClass.TEMPERATURE,
    "tempCWU": SensorDeviceClass.TEMPERATURE,
    "statusCWU": None,
    "tempUpperBuffer": SensorDeviceClass.TEMPERATURE,
    "tempLowerBuffer": SensorDeviceClass.TEMPERATURE,
    "signal": SensorDeviceClass.SIGNAL_STRENGTH,
    "servoMixer1": SensorDeviceClass.ENUM,
}

ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP = {
    #############################
    #       NUMBER SENSORS
    #############################
    "P1": PERCENTAGE,
    "P2": PERCENTAGE,
    "tempCOSet": NumberDeviceClass.TEMPERATURE,
    "tempCWUSet": NumberDeviceClass.TEMPERATURE,
}


ENTITY_BINARY_DEVICE_CLASS_MAP = {
    #############################
    #      BINARY SENSORS
    #############################
    # By default all binary sensors device_class are RUNNING
    "mainSrv": BinarySensorDeviceClass.CONNECTIVITY,
    "wifi": BinarySensorDeviceClass.CONNECTIVITY,
    "lan": BinarySensorDeviceClass.CONNECTIVITY,
}

"""Add only keys where precision more than 0 needed"""
ENTITY_PRECISION = {
    "T1": 1,
    "T2": 1,
    "T3": 1,
    "T4": 1,
    "tempFeeder": 1,
    "tempExternalSensor": 1,
    "lambdaLevel": 1,
    "lambdaSet": 1,
    "tempCO": 1,
    "mixerTemp1": 1,
    "tempBack": 2,
    "tempUpperBuffer": 1,
    "tempLowerBuffer": 1,
    "tempCWU": 1,
    "tempFlueGas": 1,
    "fanPower": 0,
    "statusCWU": None,
    "thermostat": None,
    "lambdaStatus": None,
    "mode": None,
    "softVer": None,
    "controllerID": None,
    "moduleASoftVer": None,
    "moduleBSoftVer": None,
    "moduleCSoftVer": None,
    "moduleLambdaSoftVer": None,
    "modulePanelSoftVer": None,
}

ENTITY_ICON = {
    "T1": "mdi:thermometer",
    "T2": "mdi:thermometer",
    "T3": "mdi:thermometer",
    "T4": "mdi:thermometer",
    "P1": "mdi:pump",
    "P2": "mdi:pump",
    "mode": "mdi:sync",
    "fanPower": "mdi:fan",
    "temCO": "mdi:thermometer-lines",
    "statusCWU": "mdi:water-boiler",
    "thermostat": "mdi:thermostat",
    "boilerPower": "mdi:gauge",
    "boilerPowerKW": "mdi:gauge",
    "fuelLevel": "mdi:gas-station",
    "lambdaLevel": "mdi:lambda",
    "lambdaSet": "mdi:lambda",
    "lambdaStatus": "mdi:lambda",
    "lighterWorks": "mdi:fire",
    "workAt100": "mdi:counter",
    "workAt50": "mdi:counter",
    "workAt30": "mdi:counter",
    "FeederWork": "mdi:counter",
    "feederWorks": "mdi:screw-lag",
    "FiringUpCount": "mdi:counter",
    "quality": "mdi:signal",
    "pumpCOWorks": "mdi:pump",
    "fanWorks": "mdi:fan",
    "additionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump",
    "pumpCWUWorks": "mdi:pump",
    "mixerPumpWorks": "mdi:pump",
    "mixerTemp": "mdi:thermometer",
    "mixerSetTemp": "mdi:thermometer",
    "valveMixer1": "mdi:valve",
    "servoMixer1": "mdi:valve",
    "mixerTemp1": "mdi:thermometer",
    "mainSrv": "mdi:server-network",
    "lan": "mdi:lan-connect",
    "softVer": "mdi:alarm-panel-outline",
    "controllerID": "mdi:alarm-panel-outline",
    "moduleASoftVer": "mdi:raspberry-pi",
    "moduleBSoftVer": "mdi:raspberry-pi",
    "moduleCSoftVer": "mdi:raspberry-pi",
    "moduleLambdaSoftVer": "mdi:raspberry-pi",
    "modulePanelSoftVer": "mdi:alarm-panel-outline",
}

ENTITY_ICON_OFF = {
    "P1": "mdi:pump-off",
    "P2": "mdi:pump-off",
    "pumpCOWorks": "mdi:pump-off",
    "fanWorks": "mdi:fan-off",
    "additionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump-off",
    "pumpCWUWorks": "mdi:pump-off",
    "statusCWU": "mdi:water-boiler-off",
    "mainSrv": "mdi:server-network-off",
    "lan": "mdi:lan-disconnect",
    "lighterWorks": "mdi:fire-off",
}

NO_CWU_TEMP_SET_STATUS_CODE = 128

ENTITY_VALUE_PROCESSOR = {
    "mode": lambda x: OPERATION_MODE_NAMES.get(x, STATE_UNKNOWN),
    "Tryb_pracy": lambda x: TRYB_MODE_NAMES.get(x, STATE_UNKNOWN),
    "lambdaStatus": (
        lambda x: (
            "stop"
            if x == 0
            else ("start" if x == 1 else ("working" if x == 2 else STATE_UNKNOWN))
        )
    ),
    "statusCWU": lambda x: "Not set" if x == NO_CWU_TEMP_SET_STATUS_CODE else "Set",
    "thermostat": lambda x: "ON" if x == 1 else "OFF",
}


ENTITY_CATEGORY = {
    "signal": EntityCategory.DIAGNOSTIC,
    "quality": EntityCategory.DIAGNOSTIC,
    "softVer": EntityCategory.DIAGNOSTIC,
    "moduleASoftVer": EntityCategory.DIAGNOSTIC,
    "moduleBSoftVer": EntityCategory.DIAGNOSTIC,
    "modulePanelSoftVer": EntityCategory.DIAGNOSTIC,
    "moduleLambdaSoftVer": EntityCategory.DIAGNOSTIC,
    "protocolType": EntityCategory.DIAGNOSTIC,
    "controllerID": EntityCategory.DIAGNOSTIC,
    "moduleCSoftVer": EntityCategory.DIAGNOSTIC,
    "mainSrv": EntityCategory.DIAGNOSTIC,
    "wifi": EntityCategory.DIAGNOSTIC,
    "lan": EntityCategory.DIAGNOSTIC,
    "Sch__kot_em": EntityCategory.CONFIG,
    "Sch__nocne": EntityCategory.CONFIG,
    "Tsch__WY_": EntityCategory.CONFIG,
    "Tsch__W_": EntityCategory.CONFIG,
    "Tsch__kot_em_w_": EntityCategory.CONFIG,
    "Tsch__kot_em_wy_": EntityCategory.CONFIG,
    "auto_scl_akt": EntityCategory.CONFIG,
    "T_aktyw_sch_": EntityCategory.CONFIG,
    "Auto_sch__noc": EntityCategory.CONFIG,
}

ENTITY_MIN_VALUE = {
    "tempCOSet": 27,
    "tempCWUSet": 20,
}

ENTITY_MAX_VALUE = {
    "tempCOSet": 68,
    "tempCWUSet": 55,
    "Sch__kot_em": 1,
    "Sch__nocne": 1,
    "auto_scl_akt": 1,
    "T_aktyw_sch_": 1,
    "Auto_sch__noc": 1,
}

ENTITY_STEP = {
    "tempCOSet": 1,
    "tempCWUSet": 1,
    "Sch__kot_em":1,
    "P1": 10,
    "P2": 100,
}
