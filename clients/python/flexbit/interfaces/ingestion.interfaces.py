"""Auto-generated from OpenAPI spec — do not edit manually.
Run: cd packages/client-generator && bun generate.ts
"""

from dataclasses import dataclass
from .types import (
    BessStorageStatus,
    DemandProsumerCapabilityLevel,
    EvChgEnergyTransferMode,
    EvChgPowerFlowDirection,
    EvChgStatus,
    EvConnectorStatus,
    MetaDataQuality,
    MetaSource,
)


@dataclass(kw_only=True)
class BaseTelemetry:
    """Base telemetry record with common metadata fields."""

    type: str | None = None
    """Telemetry asset type. Automatically injected by SDK producers."""

    meta_asset_id: str
    """Unique identifier of the asset (UUID format)"""

    meta_site_id: str | None = None
    """Site identifier (UUID). Automatically injected by SDK producers; optional when using the HTTP API (siteId is at the envelope level)"""

    meta_timestamp: str | None = None
    """ISO 8601 UTC timestamp of the measurement (e.g. 2026-04-08T12:00:00.000Z). Defaults to server time if not provided"""

    meta_data_quality: MetaDataQuality | None = None
    """Data quality indicator: raw (direct measurement), estimated (calculated), bad (invalid)"""

    meta_source: MetaSource | None = None
    """Signal source system: BMS (Battery Management), PCS (Power Conversion), SCADA, EMS (Energy Management), EVSE (EV Supply Equipment), PV_INV (PV Inverter)"""


@dataclass(kw_only=True)
class BessTelemetry(BaseTelemetry):
    """BESS (Battery Energy Storage System) telemetry data"""

    bess_storage_soc: float | None = None
    """State of Charge as percentage (0-100%)"""

    bess_storage_soh: float | None = None
    """State of Health as percentage (0-100%)"""

    bess_storage_energy_available: float | None = None
    """Currently available energy capacity in kWh"""

    bess_storage_energy_nominal: float | None = None
    """Total nominal energy capacity in kWh"""

    bess_inv_power_active: float | None = None
    """Active power in kW. Positive = discharge, Negative = charge"""

    bess_inv_power_charge_rate: float | None = None
    """Current charge rate in kW"""

    bess_inv_power_reactive: float | None = None
    """Reactive power in kVar. Positive = inductive, Negative = capacitive"""

    bess_inv_power_apparent: float | None = None
    """Apparent power in kVA"""

    bess_inv_power_charge_max: float | None = None
    """Maximum charging power available now in kW"""

    bess_inv_power_discharge_max: float | None = None
    """Maximum discharging power available now in kW"""

    bess_dc_voltage: float | None = None
    """DC bus voltage in V"""

    bess_dc_voltage_min: float | None = None
    """Minimum cell voltage in V"""

    bess_dc_voltage_max: float | None = None
    """Maximum cell voltage in V"""

    bess_ac_voltage_l1: float | None = None
    """AC voltage phase L1 in V"""

    bess_ac_voltage_l2: float | None = None
    """AC voltage phase L2 in V"""

    bess_ac_voltage_l3: float | None = None
    """AC voltage phase L3 in V"""

    bess_grid_voltage_l1: float | None = None
    """Grid voltage phase L1 in V"""

    bess_grid_voltage_l2: float | None = None
    """Grid voltage phase L2 in V"""

    bess_grid_voltage_l3: float | None = None
    """Grid voltage phase L3 in V"""

    bess_dc_current: float | None = None
    """DC bus current in A"""

    bess_load_current: float | None = None
    """Load current in A"""

    bess_grid_current_l1: float | None = None
    """Grid current phase L1 in A"""

    bess_grid_current_l2: float | None = None
    """Grid current phase L2 in A"""

    bess_grid_current_l3: float | None = None
    """Grid current phase L3 in A"""

    bess_bat_current_charge: float | None = None
    """Charging current in A"""

    bess_bat_current_discharge: float | None = None
    """Discharging current in A"""

    bess_bat_temp_avg: float | None = None
    """Average battery temperature in °C"""

    bess_inv_temp: float | None = None
    """Inverter temperature in °C"""

    bess_cabinet_temp: float | None = None
    """Cabinet/enclosure temperature in °C"""

    bess_ambient_temp: float | None = None
    """Ambient outside temperature in °C"""

    bess_grid_frequency: float | None = None
    """Grid frequency at PCC in Hz"""

    bess_inv_power_factor: float | None = None
    """Power factor (cos phi)"""

    bess_grid_energy_import: float | None = None
    """Cumulative energy imported (charging) in kWh"""

    bess_grid_energy_export: float | None = None
    """Cumulative energy exported (discharging) in kWh"""

    bess_grid_energy_total: float | None = None
    """Total energy throughput in kWh"""

    bess_storage_status: BessStorageStatus | None = None
    """Current operating mode of the energy storage asset"""

    bess_storage_charge_ready: bool | None = None
    """Battery is ready to accept charge commands"""

    bess_storage_discharge_ready: bool | None = None
    """Battery is ready to accept discharge commands"""

    bess_storage_charging: bool | None = None
    """Battery is currently charging"""

    bess_storage_discharging: bool | None = None
    """Battery is currently discharging"""

    bess_storage_alarms_active: bool | None = None
    """Any alarms active"""


@dataclass(kw_only=True)
class EvChargerTelemetry(BaseTelemetry):
    """EV Charger telemetry data"""

    ev_chg_power_active: float | None = None
    """Active power in kW. Positive = to vehicle, Negative = from vehicle (V2G)"""

    ev_chg_power_reactive: float | None = None
    """Reactive power in kVar"""

    ev_chg_power_apparent: float | None = None
    """Apparent power in kVA"""

    ev_chg_energy_delivered: float | None = None
    """Cumulative energy delivered to vehicle in kWh"""

    ev_chg_energy_received: float | None = None
    """Cumulative energy received from vehicle (V2G) in kWh"""

    ev_chg_energy_provided: float | None = None
    """Energy provided to vehicle in kWh"""

    ev_chg_energy_consumed: float | None = None
    """Energy consumed from grid in kWh"""

    ev_chg_dc_voltage: float | None = None
    """DC output voltage in V"""

    ev_chg_dc_current: float | None = None
    """DC output current in A"""

    ev_chg_voltage_l1: float | None = None
    """Voltage phase L1 in V"""

    ev_chg_voltage_l2: float | None = None
    """Voltage phase L2 in V"""

    ev_chg_voltage_l3: float | None = None
    """Voltage phase L3 in V"""

    ev_chg_current_l1: float | None = None
    """Current phase L1 in A"""

    ev_chg_current_l2: float | None = None
    """Current phase L2 in A"""

    ev_chg_current_l3: float | None = None
    """Current phase L3 in A"""

    ev_chg_frequency: float | None = None
    """Frequency in Hz"""

    ev_chg_power_factor: float | None = None
    """Power factor"""

    ev_connector_status: EvConnectorStatus | None = None
    """EV charger connector state"""

    ev_chg_status: EvChgStatus | None = None
    """Charging session status"""

    ev_chg_availability: bool | None = None
    """Station availability"""

    ev_vehicle_connected: bool | None = None
    """Vehicle is physically connected to the charger"""

    ev_chg_v2g_capable: bool | None = None
    """Connected vehicle supports Vehicle-to-Grid"""

    ev_chg_v2g_active: bool | None = None
    """Vehicle-to-Grid mode is currently active"""

    ev_chg_energy_transfer_mode: EvChgEnergyTransferMode | None = None
    """Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC)"""

    ev_chg_power_flow_direction: EvChgPowerFlowDirection | None = None
    """Power flow direction: import (grid to EV), export (EV to grid), idle"""

    ev_chg_comm_status: bool | None = None
    """Communication status"""

    ev_chg_error_code: str | None = None
    """Active error/fault code"""

    ev_vehicle_soc: float | None = None
    """EV battery state of charge (%)"""

    ev_vehicle_voltage: float | None = None
    """EV battery voltage in V"""

    ev_vehicle_energy_available: float | None = None
    """Remaining battery capacity in kWh"""

    ev_vehicle_energy_nominal: float | None = None
    """Maximum battery capacity in kWh"""

    ev_vehicle_temp: float | None = None
    """EV battery temperature in °C"""

    ev_vehicle_type: str | None = None
    """Vehicle type/compatibility"""

    ev_vehicle_current_max: float | None = None
    """Maximum EV charging current in A"""

    ev_vehicle_voltage_max: float | None = None
    """Maximum EV charging voltage in V"""

    ev_vehicle_charge_level: float | None = None
    """Current charge level (%)"""


@dataclass(kw_only=True)
class PvTelemetry(BaseTelemetry):
    """PV (Photovoltaic) production telemetry data"""

    pv_system_id: str | None = None
    """Unique identifier of the PV system"""

    pv_inv_power_active: float | None = None
    """Active power generation in kW"""

    pv_inv_power_reactive: float | None = None
    """Reactive power in kVar"""

    pv_system_energy_produced: float | None = None
    """Cumulative energy produced in kWh"""

    pv_system_power_nominal: float | None = None
    """Maximum possible production (best case) in kW"""

    pv_system_irradiance: float | None = None
    """Solar irradiance in W/m2"""

    pv_system_module_temp: float | None = None
    """PV module temperature in C"""

    pv_bat_power_active: float | None = None
    """Power from/to batteries (hybrid) in kW"""

    pv_load_power_active: float | None = None
    """Power request from loads in kW"""

    pv_grid_power_active: float | None = None
    """Power injected into the grid in kW"""

    pv_grid_power_export: float | None = None
    """Power fed into grid (export) in kW"""

    pv_grid_power_import: float | None = None
    """Power pulled from grid (import) in kW"""

    pv_grid_voltage_l1: float | None = None
    """Grid voltage phase R in V"""

    pv_grid_voltage_l2: float | None = None
    """Grid voltage phase S in V"""

    pv_grid_voltage_l3: float | None = None
    """Grid voltage phase T in V"""

    pv_ac_current_l1: float | None = None
    """AC current phase R in A"""

    pv_ac_current_l2: float | None = None
    """AC current phase S in A"""

    pv_ac_current_l3: float | None = None
    """AC current phase T in A"""

    pv_grid_frequency: float | None = None
    """Grid frequency in Hz"""

    pv_mppt1_voltage: float | None = None
    """Voltage of PV generator in 1st MPPT in V"""

    pv_mppt1_current: float | None = None
    """Current of PV generator in 1st MPPT in A"""

    pv_mppt1_power_active: float | None = None
    """Power of PV generator in 1st MPPT in W"""

    pv_mppt2_voltage: float | None = None
    """Voltage of PV generator in 2nd MPPT in V"""

    pv_mppt2_current: float | None = None
    """Current of PV generator in 2nd MPPT in A"""

    pv_mppt2_power_active: float | None = None
    """Power of PV generator in 2nd MPPT in W"""

    pv_ac_power_active_l1: float | None = None
    """Active power phase L1 (inverter output) in kW"""

    pv_ac_power_active_l2: float | None = None
    """Active power phase L2 (inverter output) in kW"""

    pv_ac_power_active_l3: float | None = None
    """Active power phase L3 (inverter output) in kW"""

    pv_ac_power_reactive: float | None = None
    """Total reactive power (inverter output) in kVar"""

    pv_ac_power_reactive_l1: float | None = None
    """Reactive power phase L1 (inverter output) in kVar"""

    pv_ac_power_reactive_l2: float | None = None
    """Reactive power phase L2 (inverter output) in kVar"""

    pv_ac_power_reactive_l3: float | None = None
    """Reactive power phase L3 (inverter output) in kVar"""

    pv_ac_power_apparent: float | None = None
    """Total apparent power (inverter output) in kVA"""

    pv_ac_power_factor_l1: float | None = None
    """Power factor phase L1 (inverter output)"""

    pv_ac_power_factor_l2: float | None = None
    """Power factor phase L2 (inverter output)"""

    pv_ac_power_factor_l3: float | None = None
    """Power factor phase L3 (inverter output)"""

    pv_pcc_power_active_l1: float | None = None
    """Active power phase L1 at PCC in kW"""

    pv_pcc_power_active_l2: float | None = None
    """Active power phase L2 at PCC in kW"""

    pv_pcc_power_active_l3: float | None = None
    """Active power phase L3 at PCC in kW"""

    pv_pcc_current_l1: float | None = None
    """Current phase L1 at PCC in A"""

    pv_pcc_current_l2: float | None = None
    """Current phase L2 at PCC in A"""

    pv_pcc_current_l3: float | None = None
    """Current phase L3 at PCC in A"""

    pv_pcc_power_reactive: float | None = None
    """Total reactive power at PCC in kVar"""

    pv_pcc_power_reactive_l1: float | None = None
    """Reactive power phase L1 at PCC in kVar"""

    pv_pcc_power_reactive_l2: float | None = None
    """Reactive power phase L2 at PCC in kVar"""

    pv_pcc_power_reactive_l3: float | None = None
    """Reactive power phase L3 at PCC in kVar"""

    pv_pcc_power_apparent: float | None = None
    """Total apparent power at PCC in kVA"""

    pv_pcc_power_factor_l1: float | None = None
    """Power factor phase L1 at PCC"""

    pv_pcc_power_factor_l2: float | None = None
    """Power factor phase L2 at PCC"""

    pv_pcc_power_factor_l3: float | None = None
    """Power factor phase L3 at PCC"""

    pv_ext_power_active: float | None = None
    """Active power from external PV source in kW"""

    pv_ambient_temp: float | None = None
    """Ambient air temperature at PV site in °C"""

    pv_inv_temp: float | None = None
    """Inverter radiator/heatsink temperature in °C"""

    pv_inv_status: str | None = None
    """Inverter operating status: grid-connected, off-grid, standby, fault"""

    pv_inv_connection_status: str | None = None
    """Inverter communication status: connected, disconnected"""


@dataclass(kw_only=True)
class ThermalColdTelemetry(BaseTelemetry):
    """Thermal Cold Storage telemetry data"""

    therm_system_power_active: float | None = None
    """Power consumption in kW"""

    therm_system_power_electric: float | None = None
    """Electric power consumption in W"""

    therm_storage_temp: float | None = None
    """Current storage temperature in C"""

    therm_storage_temp_max: float | None = None
    """Maximum allowable temperature in C"""

    therm_storage_temp_min: float | None = None
    """Minimum allowable temperature in C"""

    therm_air_humidity_output: float | None = None
    """Output air relative humidity (%)"""

    therm_air_temp_output: float | None = None
    """Output air temperature in C"""

    therm_air_humidity_input: float | None = None
    """Input air relative humidity (%)"""

    therm_air_temp_input: float | None = None
    """Input air temperature in C"""

    therm_system_temp_internal: float | None = None
    """Internal temperature in C"""

    therm_system_humidity_internal: float | None = None
    """Internal air relative humidity (%)"""

    therm_water_temp_hot_in: float | None = None
    """Hot water input temperature in C"""

    therm_water_temp_hot_out: float | None = None
    """Hot water output temperature in C"""

    therm_system_cop: float | None = None
    """Coefficient of Performance (efficiency ratio)"""

    therm_system_eer: float | None = None
    """Energy Efficiency Ratio"""

    therm_water_flow_hot: float | None = None
    """Hot water flow rate in L/h"""

    therm_storage_energy_nominal: float | None = None
    """Maximum thermal storage capacity in kWh"""

    therm_system_state: str | None = None
    """Operational state identifier"""


@dataclass(kw_only=True)
class ThermalHeatTelemetry(BaseTelemetry):
    """Thermal Heat Storage telemetry data"""

    therm_system_power_active: float | None = None
    """Power consumption in kW"""

    therm_system_power_electric: float | None = None
    """Electric power consumption in W"""

    therm_storage_temp: float | None = None
    """Current storage temperature in C"""

    therm_storage_temp_max: float | None = None
    """Maximum allowable temperature in C"""

    therm_storage_temp_min: float | None = None
    """Minimum allowable temperature in C"""

    therm_water_temp_hot_in: float | None = None
    """Hot water input temperature in C"""

    therm_water_temp_hot_out: float | None = None
    """Hot water output temperature in C"""

    therm_system_cop: float | None = None
    """Coefficient of Performance (efficiency ratio)"""

    therm_water_flow_hot: float | None = None
    """Hot water flow rate in L/h"""

    therm_storage_energy_nominal: float | None = None
    """Maximum thermal storage capacity in kWh"""

    therm_system_state: str | None = None
    """Operational state identifier"""


@dataclass(kw_only=True)
class HydrogenLocalPlantTelemetry(BaseTelemetry):
    """Hydrogen Local Plant telemetry data (UniToV)"""

    h2_plant_pv_power_active: float | None = None
    """PV Power in kW"""

    h2_electrolyzer_power_active: float | None = None
    """Electrolyzer Power in kW"""

    h2_electrolyzer_mass_flow: float | None = None
    """Electrolyzer Hydrogen Mass Flow Rate in kg/s"""

    h2_electrolyzer_mass_total: float | None = None
    """Produced hydrogen from the Electrolyzer in kg"""

    h2_storage_mass: float | None = None
    """Stored hydrogen mass in kg"""


@dataclass(kw_only=True)
class CommunityTelemetry(BaseTelemetry):
    """Community (Blackbox) telemetry data (UniToV)"""

    com_grid_power_exchange: float | None = None
    """Community power exchange with external grid in kW. Positive = export, Negative = import"""

    com_plant_community_power: float | None = None
    """Plant community power exchange in kW"""

    com_consumer_community_power: float | None = None
    """Consumer community power exchange in kW"""

    com_prosumer_community_power: float | None = None
    """Prosumer community power exchange in kW"""

    com_prosumer_lv1_community_power: float | None = None
    """Smart Prosumer LV1 community power exchange in kW"""

    com_prosumer_lv2_community_power: float | None = None
    """Smart Prosumer LV2 community power exchange in kW"""

    com_prosumer_lv3_community_power: float | None = None
    """Smart Prosumer LV3 community power exchange in kW"""


@dataclass(kw_only=True)
class EnergyDemandConsumerTelemetry(BaseTelemetry):
    """Energy Demand Consumer telemetry data (UniToV)"""

    demand_load_power_active: float | None = None
    """Load electrical power in kW"""


@dataclass(kw_only=True)
class EnergyDemandProsumerTelemetry(BaseTelemetry):
    """Energy Demand Prosumer telemetry data (UniToV) - supports 3 capability levels"""

    demand_prosumer_capability_level: DemandProsumerCapabilityLevel | None = None
    """Prosumer capability level"""

    demand_prosumer_pv_power_active: float | None = None
    """[Level 1+] PV Power in kW"""

    demand_prosumer_load_power_active: float | None = None
    """[Level 1+] Load Power in kW"""

    demand_prosumer_bess_soc: float | None = None
    """[Level 1+] Battery State of Charge in %"""

    demand_prosumer_bess_power_active: float | None = None
    """[Level 1+] Battery Power in kW. Positive = discharging, Negative = charging"""

    demand_fuelcell_power_active: float | None = None
    """[Level 2+] Fuel Cell Power in kW"""

    demand_fuelcell_mass_flow: float | None = None
    """[Level 2+] Fuel Cell H2 Mass Flow Rate in kg/s"""

    demand_fuelcell_mass_consumed: float | None = None
    """[Level 2+] Consumed H2 from Fuel Cell in kg"""

    demand_prosumer_storage_mass: float | None = None
    """[Level 2+] Stored Hydrogen Mass in kg"""

    demand_fuelcell_power_thermal: float | None = None
    """[Level 3] Recoverable Heat Power from Fuel Cell in kW"""


@dataclass(kw_only=True)
class CaesTelemetry(BaseTelemetry):
    """CAES (Compressed Air Energy Storage) telemetry data"""

    caes_compressor_power_active: float | None = None
    """Compressor power consumption in kW"""

    caes_storage_pressure: float | None = None
    """Current air pressure in bar"""

    caes_storage_pressure_max: float | None = None
    """Maximum rated pressure in bar"""

    caes_compressor_state: int | None = None
    """Operating state: 0 = Off, 1 = On, 2 = Standby, 3 = Fault"""


@dataclass(kw_only=True)
class GridMeterTelemetry(BaseTelemetry):
    """Grid Meter telemetry data"""

    grid_power_export: float | None = None
    """Power fed into grid (export) in kW"""

    grid_power_import: float | None = None
    """Power pulled from grid (import) in kW"""

    grid_bus_power_active: float | None = None
    """Instantaneous grid power in kW. Positive = import, Negative = export"""

    grid_ac_voltage_input: float | None = None
    """AC voltage in V"""

    grid_ac_current_input: float | None = None
    """AC current in A"""

    grid_meter_power_active: float | None = None
    """Active power in W"""

    grid_bus_power_reactive: float | None = None
    """Reactive power in Var"""

    grid_bus_power_apparent: float | None = None
    """Apparent power in VA"""

    grid_bus_power_factor: float | None = None
    """Power factor"""

    grid_bus_voltage_l1: float | None = None
    """Voltage phase L1 in V"""

    grid_bus_current_l1: float | None = None
    """Current phase L1 in A"""

    grid_frequency: float | None = None
    """Grid frequency in Hz"""

    grid_inv_power_input: float | None = None
    """Input power of inverter in VA"""

    grid_inv_power_output: float | None = None
    """Output power of inverter in VA"""

    grid_load_power_consumption: float | None = None
    """AC consumption (load) in W"""

    grid_energy_import: float | None = None
    """Total active energy imported in kWh"""

    grid_energy_export: float | None = None
    """Total active energy exported in kWh"""

    grid_energy_total: float | None = None
    """Total active energy in kWh"""

    grid_energy_reactive_import: float | None = None
    """Total reactive energy imported in kVarh"""

    grid_energy_reactive_export: float | None = None
    """Total reactive energy exported in kVarh"""

    grid_energy_reactive_total: float | None = None
    """Total reactive energy in kVarh"""

    grid_dc_voltage: float | None = None
    """DC bus voltage in V"""

    grid_dc_current: float | None = None
    """DC bus current in A"""

    grid_dc_power_active: float | None = None
    """DC power in W"""

    grid_dc_energy_import: float | None = None
    """DC energy imported (taken in) in kWh"""

    grid_dc_energy_export: float | None = None
    """DC energy exported (given out) in kWh"""

    grid_load_power_apparent: float | None = None
    """Load apparent power in VA"""

    grid_load_power_active: float | None = None
    """Load active power in W"""

    grid_load_power_reactive: float | None = None
    """Load reactive power in Var"""

    grid_load_power_factor: float | None = None
    """Load power factor"""


@dataclass(kw_only=True)
class AlarmRecord(BaseTelemetry):
    """Alarm event record"""

    alarm_code: int
    """Alarm code identifier (see alarm codes documentation)"""

    active: bool
    """Alarm is currently active"""
