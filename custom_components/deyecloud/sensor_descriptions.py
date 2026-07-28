"""Sensor descriptions for the DeyeCloud integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)


@dataclass(frozen=True, kw_only=True)
class DeyeCloudSensorEntityDescription(SensorEntityDescription):
    """Describe a DeyeCloud sensor."""

    data_key: str


def _sensor(
    key: str,
    _name: str,
    data_key: str,
    *,
    device_class: SensorDeviceClass | None = None,
    unit: str | None = None,
    state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT,
) -> DeyeCloudSensorEntityDescription:
    """Create a DeyeCloud sensor description."""

    return DeyeCloudSensorEntityDescription(
        key=key,
        translation_key=key,
        data_key=data_key,
        device_class=device_class,
        native_unit_of_measurement=unit,
        state_class=state_class,
    )


def _power(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a power sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.POWER,
        unit=UnitOfPower.WATT,
    )


def _voltage(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a voltage sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.VOLTAGE,
        unit=UnitOfElectricPotential.VOLT,
    )


def _current(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a current sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.CURRENT,
        unit=UnitOfElectricCurrent.AMPERE,
    )


def _frequency(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a frequency sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.FREQUENCY,
        unit=UnitOfFrequency.HERTZ,
    )


def _temperature(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a temperature sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.TEMPERATURE,
        unit=UnitOfTemperature.CELSIUS,
    )


def _energy_daily(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a daily energy sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
    )


def _energy_total(
    key: str,
    name: str,
    data_key: str,
) -> DeyeCloudSensorEntityDescription:
    """Create a lifetime energy sensor."""

    return _sensor(
        key,
        name,
        data_key,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    )


SENSOR_DESCRIPTIONS: tuple[DeyeCloudSensorEntityDescription, ...] = (
    # Totals
    _power("solar_power", "Solar power", "TotalSolarPower"),
    _power(
        "inverter_output_power",
        "Inverter output power",
        "TotalInverterOutputPower",
    ),
    _power(
        "consumption_power",
        "Consumption power",
        "TotalConsumptionPower",
    ),
    _sensor(
        "consumption_apparent_power",
        "Consumption apparent power",
        "TotalConsumptionApparentPower",
        unit="VA",
    ),
    _power("grid_power", "Grid power", "TotalGridPower"),
    _power("rated_power", "Rated power", "RatedPower"),

    # Production and consumption
    _energy_daily(
        "daily_production",
        "Daily production",
        "DailyActiveProduction",
    ),
    _energy_total(
        "total_production",
        "Total production",
        "TotalActiveProduction",
    ),
    _energy_daily(
        "daily_consumption",
        "Daily consumption",
        "DailyConsumption",
    ),
    _energy_total(
        "total_consumption",
        "Total consumption",
        "TotalConsumption",
    ),

    # Grid import and export
    _energy_daily(
        "daily_energy_purchased",
        "Daily grid import",
        "DailyEnergyPurchased",
    ),
    _energy_total(
        "total_energy_bought",
        "Total grid import",
        "TotalEnergyBuy",
    ),
    _energy_daily(
        "daily_grid_feed_in",
        "Daily grid export",
        "DailyGridFeedIn",
    ),
    _energy_total(
        "total_energy_sold",
        "Total grid export",
        "TotalEnergySell",
    ),

    # Frequencies and temperatures
    _frequency(
        "grid_frequency",
        "Grid frequency",
        "GridFrequency",
    ),
    _frequency(
        "load_frequency",
        "Load frequency",
        "LoadFrequency",
    ),
    _temperature(
        "battery_temperature",
        "Battery temperature",
        "Temperature- Battery",
    ),
    _temperature(
        "inverter_temperature",
        "Inverter temperature",
        "AC Temperature",
    ),

    # Battery
    _sensor(
        "battery_state_of_charge",
        "Battery state of charge",
        "SOC",
        device_class=SensorDeviceClass.BATTERY,
        unit=PERCENTAGE,
    ),
    _voltage(
        "battery_voltage",
        "Battery voltage",
        "BatteryVoltage",
    ),
    _current(
        "battery_current",
        "Battery current",
        "BatteryCurrent",
    ),
    _power(
        "battery_power",
        "Battery power",
        "BatteryPower",
    ),
    _energy_daily(
        "daily_battery_charge",
        "Daily battery charge",
        "DailyChargingEnergy",
    ),
    _energy_daily(
        "daily_battery_discharge",
        "Daily battery discharge",
        "DailyDischargingEnergy",
    ),
    _energy_total(
        "total_battery_charge",
        "Total battery charge",
        "TotalChargeEnergy",
    ),
    _energy_total(
        "total_battery_discharge",
        "Total battery discharge",
        "TotalDischargeEnergy",
    ),

    # Battery management system
    _voltage(
        "bms_voltage",
        "BMS voltage",
        "BMSVoltage",
    ),
    _current(
        "bms_current",
        "BMS current",
        "BMSCurrent",
    ),
    _voltage(
        "bms_charge_voltage",
        "BMS charge voltage",
        "BMSChargeVoltage",
    ),
    _voltage(
        "bms_discharge_voltage",
        "BMS discharge voltage",
        "BMSDisChargeVoltage",
    ),
    _sensor(
        "bms_state_of_charge",
        "BMS state of charge",
        "BMSSOC",
        device_class=SensorDeviceClass.BATTERY,
        unit=PERCENTAGE,
    ),
    _sensor(
        "battery_state_of_health",
        "Battery state of health",
        "LithiumBattery2SOH",
        unit=PERCENTAGE,
    ),
    _sensor(
        "battery_rated_capacity",
        "Battery rated capacity",
        "BatteryRatedCapacity",
        unit="Ah",
    ),

    # PV1-PV4
    *(
        description
        for pv in range(1, 5)
        for description in (
            _voltage(
                f"pv{pv}_voltage",
                f"PV{pv} voltage",
                f"DCVoltagePV{pv}",
            ),
            _current(
                f"pv{pv}_current",
                f"PV{pv} current",
                f"DCCurrentPV{pv}",
            ),
            _power(
                f"pv{pv}_power",
                f"PV{pv} power",
                f"DCPowerPV{pv}",
            ),
        )
    ),

    # Inverter AC output L1-L3
    *(
        description
        for phase, voltage_key, current_key in (
            (1, "ACVoltageRUA", "ACCurrentRUA"),
            (2, "ACVoltageSVB", "ACCurrentSVB"),
            (3, "ACVoltageTWC", "ACCurrentTWC"),
        )
        for description in (
            _voltage(
                f"ac_l{phase}_voltage",
                f"AC L{phase} voltage",
                voltage_key,
            ),
            _current(
                f"ac_l{phase}_current",
                f"AC L{phase} current",
                current_key,
            ),
            _power(
                f"ac_l{phase}_power",
                f"AC L{phase} power",
                f"InverterOutputPowerL{phase}",
            ),
        )
    ),

    # Grid L1-L3
    *(
        description
        for phase in range(1, 4)
        for description in (
            _voltage(
                f"grid_l{phase}_voltage",
                f"Grid L{phase} voltage",
                f"GridVoltageL{phase}",
            ),
            _current(
                f"grid_l{phase}_current",
                f"Grid L{phase} current",
                f"GridCurrentL{phase}",
            ),
            _power(
                f"grid_l{phase}_power",
                f"Grid L{phase} power",
                f"GridPowerL{phase}",
            ),
        )
    ),

    # Load L1-L3
    *(
        description
        for phase, phase_letter in (
            (1, "A"),
            (2, "B"),
            (3, "C"),
        )
        for description in (
            _voltage(
                f"load_l{phase}_voltage",
                f"Load L{phase} voltage",
                f"LoadVoltageL{phase}",
            ),
            _power(
                f"load_l{phase}_power",
                f"Load L{phase} power",
                f"LoadPowerL{phase}",
            ),
            _power(
                f"load_phase_{phase_letter.lower()}_power",
                f"Load phase {phase_letter} power",
                f"LoadPhasePower{phase_letter}",
            ),
        )
    ),

    # External current transformers
    *(
        _power(
            f"external_ct_l{phase}_power",
            f"External CT{phase} power",
            f"ExternalCT{phase}Power",
        )
        for phase in range(1, 4)
    ),
    _power(
        "external_ct_total_power",
        "External CT total power",
        "TotalExternalCTPower",
    ),

    # Generator
    *(
        _power(
            f"generator_l{phase}_power",
            f"Generator L{phase} power",
            f"GenPowerL{phase}",
        )
        for phase in range(1, 4)
    ),
    *(
        _voltage(
            f"generator_l{phase}_voltage",
            f"Generator L{phase} voltage",
            f"GenVoltageL{phase}",
        )
        for phase in range(1, 4)
    ),
    _power(
        "generator_active_power",
        "Generator active power",
        "GeneratorActivePower",
    ),
    _power(
        "generator_total_power",
        "Generator total power",
        "TotalGeneratorPower",
    ),
    _energy_total(
        "generator_total_production",
        "Generator total production",
        "TotalGeneratorProduction",
    ),

    # UPS
    _power(
        "ups_load_power",
        "UPS load power",
        "UPSLoadPower",
    ),
)
