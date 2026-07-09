// Auto-generated from OpenAPI spec — do not edit manually.
// Run: cd packages/client-generator && bun generate.ts

import type {
  BessStorageStatus,
  DemandProsumerCapabilityLevel,
  EvChgEnergyTransferMode,
  EvChgPowerFlowDirection,
  EvChgStatus,
  EvConnectorStatus,
  MetaDataQuality,
  MetaSource,
} from "./types.js";

export interface BaseTelemetry {
  /** Telemetry asset type. Automatically injected by SDK producers. */
  type?: string;
  /** Unique identifier of the asset (UUID format) */
  meta_asset_id: string;
  /** Site identifier (UUID) this telemetry belongs to */
  meta_site_id?: string;
  /** ISO 8601 UTC timestamp of the measurement (e.g. 2026-04-08T12:00:00.000Z). Defaults to server time if not provided */
  meta_timestamp?: string;
  /** Data quality indicator: raw (direct measurement), estimated (calculated), bad (invalid) */
  meta_data_quality?: MetaDataQuality;
  /** Signal source system: BMS (Battery Management), PCS (Power Conversion), SCADA, EMS (Energy Management), EVSE (EV Supply Equipment), PV_INV (PV Inverter) */
  meta_source?: MetaSource;
}

export interface BessTelemetry extends BaseTelemetry {
  /** State of Charge as percentage (0-100%) */
  bess_storage_soc?: number;
  /** State of Health as percentage (0-100%) */
  bess_storage_soh?: number;
  /** Currently available energy capacity in kWh */
  bess_storage_energy_available?: number;
  /** Total nominal energy capacity in kWh */
  bess_storage_energy_nominal?: number;
  /** Active power in kW. Positive = discharge, Negative = charge */
  bess_inv_power_active?: number;
  /** Current charge rate in kW */
  bess_inv_power_charge_rate?: number;
  /** Reactive power in kVar. Positive = inductive, Negative = capacitive */
  bess_inv_power_reactive?: number;
  /** Apparent power in kVA */
  bess_inv_power_apparent?: number;
  /** Maximum charging power available now in kW */
  bess_inv_power_charge_max?: number;
  /** Maximum discharging power available now in kW */
  bess_inv_power_discharge_max?: number;
  /** DC bus voltage in V */
  bess_dc_voltage?: number;
  /** Minimum cell voltage in V */
  bess_dc_voltage_min?: number;
  /** Maximum cell voltage in V */
  bess_dc_voltage_max?: number;
  /** AC voltage phase L1 in V */
  bess_ac_voltage_l1?: number;
  /** AC voltage phase L2 in V */
  bess_ac_voltage_l2?: number;
  /** AC voltage phase L3 in V */
  bess_ac_voltage_l3?: number;
  /** Grid voltage phase L1 in V */
  bess_grid_voltage_l1?: number;
  /** Grid voltage phase L2 in V */
  bess_grid_voltage_l2?: number;
  /** Grid voltage phase L3 in V */
  bess_grid_voltage_l3?: number;
  /** DC bus current in A */
  bess_dc_current?: number;
  /** Load current in A */
  bess_load_current?: number;
  /** Grid current phase L1 in A */
  bess_grid_current_l1?: number;
  /** Grid current phase L2 in A */
  bess_grid_current_l2?: number;
  /** Grid current phase L3 in A */
  bess_grid_current_l3?: number;
  /** Charging current in A */
  bess_bat_current_charge?: number;
  /** Discharging current in A */
  bess_bat_current_discharge?: number;
  /** Average battery temperature in °C */
  bess_bat_temp_avg?: number;
  /** Inverter temperature in °C */
  bess_inv_temp?: number;
  /** Cabinet/enclosure temperature in °C */
  bess_cabinet_temp?: number;
  /** Ambient outside temperature in °C */
  bess_ambient_temp?: number;
  /** Grid frequency at PCC in Hz */
  bess_grid_frequency?: number;
  /** Power factor (cos phi) */
  bess_inv_power_factor?: number;
  /** Cumulative energy imported (charging) in kWh */
  bess_grid_energy_import?: number;
  /** Cumulative energy exported (discharging) in kWh */
  bess_grid_energy_export?: number;
  /** Total energy throughput in kWh */
  bess_grid_energy_total?: number;
  /** Current operating mode of the energy storage asset */
  bess_storage_status?: BessStorageStatus;
  /** Battery is ready to accept charge commands */
  bess_storage_charge_ready?: boolean;
  /** Battery is ready to accept discharge commands */
  bess_storage_discharge_ready?: boolean;
  /** Battery is currently charging */
  bess_storage_charging?: boolean;
  /** Battery is currently discharging */
  bess_storage_discharging?: boolean;
  /** Any alarms active */
  bess_storage_alarms_active?: boolean;
}

export interface EvChargerTelemetry extends BaseTelemetry {
  /** Active power in kW. Positive = to vehicle, Negative = from vehicle (V2G) */
  ev_chg_power_active?: number;
  /** Reactive power in kVar */
  ev_chg_power_reactive?: number;
  /** Apparent power in kVA */
  ev_chg_power_apparent?: number;
  /** Cumulative energy delivered to vehicle in kWh */
  ev_chg_energy_delivered?: number;
  /** Cumulative energy received from vehicle (V2G) in kWh */
  ev_chg_energy_received?: number;
  /** Energy provided to vehicle in kWh */
  ev_chg_energy_provided?: number;
  /** Energy consumed from grid in kWh */
  ev_chg_energy_consumed?: number;
  /** DC output voltage in V */
  ev_chg_dc_voltage?: number;
  /** DC output current in A */
  ev_chg_dc_current?: number;
  /** Voltage phase L1 in V */
  ev_chg_voltage_l1?: number;
  /** Voltage phase L2 in V */
  ev_chg_voltage_l2?: number;
  /** Voltage phase L3 in V */
  ev_chg_voltage_l3?: number;
  /** Current phase L1 in A */
  ev_chg_current_l1?: number;
  /** Current phase L2 in A */
  ev_chg_current_l2?: number;
  /** Current phase L3 in A */
  ev_chg_current_l3?: number;
  /** Frequency in Hz */
  ev_chg_frequency?: number;
  /** Power factor */
  ev_chg_power_factor?: number;
  /** EV charger connector state */
  ev_connector_status?: EvConnectorStatus;
  /** Charging session status */
  ev_chg_status?: EvChgStatus;
  /** Station availability */
  ev_chg_availability?: boolean;
  /** Vehicle is physically connected to the charger */
  ev_vehicle_connected?: boolean;
  /** Connected vehicle supports Vehicle-to-Grid */
  ev_chg_v2g_capable?: boolean;
  /** Vehicle-to-Grid mode is currently active */
  ev_chg_v2g_active?: boolean;
  /** Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC) */
  ev_chg_energy_transfer_mode?: EvChgEnergyTransferMode;
  /** Power flow direction: import (grid to EV), export (EV to grid), idle */
  ev_chg_power_flow_direction?: EvChgPowerFlowDirection;
  /** Communication status */
  ev_chg_comm_status?: boolean;
  /** Active error/fault code */
  ev_chg_error_code?: string;
  /** EV battery state of charge (%) */
  ev_vehicle_soc?: number;
  /** EV battery voltage in V */
  ev_vehicle_voltage?: number;
  /** Remaining battery capacity in kWh */
  ev_vehicle_energy_available?: number;
  /** Maximum battery capacity in kWh */
  ev_vehicle_energy_nominal?: number;
  /** EV battery temperature in °C */
  ev_vehicle_temp?: number;
  /** Vehicle type/compatibility */
  ev_vehicle_type?: string;
  /** Maximum EV charging current in A */
  ev_vehicle_current_max?: number;
  /** Maximum EV charging voltage in V */
  ev_vehicle_voltage_max?: number;
  /** Current charge level (%) */
  ev_vehicle_charge_level?: number;
}

export interface PvTelemetry extends BaseTelemetry {
  /** Unique identifier of the PV system */
  pv_system_id?: string;
  /** Active power generation in kW */
  pv_inv_power_active?: number;
  /** Reactive power in kVar */
  pv_inv_power_reactive?: number;
  /** Cumulative energy produced in kWh */
  pv_system_energy_produced?: number;
  /** Maximum possible production (best case) in kW */
  pv_system_power_nominal?: number;
  /** Solar irradiance in W/m2 */
  pv_system_irradiance?: number;
  /** PV module temperature in C */
  pv_system_module_temp?: number;
  /** Power from/to batteries (hybrid) in kW */
  pv_bat_power_active?: number;
  /** Power request from loads in kW */
  pv_load_power_active?: number;
  /** Power injected into the grid in kW */
  pv_grid_power_active?: number;
  /** Power fed into grid (export) in kW */
  pv_grid_power_export?: number;
  /** Power pulled from grid (import) in kW */
  pv_grid_power_import?: number;
  /** Grid voltage phase R in V */
  pv_grid_voltage_l1?: number;
  /** Grid voltage phase S in V */
  pv_grid_voltage_l2?: number;
  /** Grid voltage phase T in V */
  pv_grid_voltage_l3?: number;
  /** AC current phase R in A */
  pv_ac_current_l1?: number;
  /** AC current phase S in A */
  pv_ac_current_l2?: number;
  /** AC current phase T in A */
  pv_ac_current_l3?: number;
  /** Grid frequency in Hz */
  pv_grid_frequency?: number;
  /** Voltage of PV generator in 1st MPPT in V */
  pv_mppt1_voltage?: number;
  /** Current of PV generator in 1st MPPT in A */
  pv_mppt1_current?: number;
  /** Power of PV generator in 1st MPPT in W */
  pv_mppt1_power_active?: number;
  /** Voltage of PV generator in 2nd MPPT in V */
  pv_mppt2_voltage?: number;
  /** Current of PV generator in 2nd MPPT in A */
  pv_mppt2_current?: number;
  /** Power of PV generator in 2nd MPPT in W */
  pv_mppt2_power_active?: number;
  /** Active power phase L1 (inverter output) in kW */
  pv_ac_power_active_l1?: number;
  /** Active power phase L2 (inverter output) in kW */
  pv_ac_power_active_l2?: number;
  /** Active power phase L3 (inverter output) in kW */
  pv_ac_power_active_l3?: number;
  /** Total reactive power (inverter output) in kVar */
  pv_ac_power_reactive?: number;
  /** Reactive power phase L1 (inverter output) in kVar */
  pv_ac_power_reactive_l1?: number;
  /** Reactive power phase L2 (inverter output) in kVar */
  pv_ac_power_reactive_l2?: number;
  /** Reactive power phase L3 (inverter output) in kVar */
  pv_ac_power_reactive_l3?: number;
  /** Total apparent power (inverter output) in kVA */
  pv_ac_power_apparent?: number;
  /** Power factor phase L1 (inverter output) */
  pv_ac_power_factor_l1?: number;
  /** Power factor phase L2 (inverter output) */
  pv_ac_power_factor_l2?: number;
  /** Power factor phase L3 (inverter output) */
  pv_ac_power_factor_l3?: number;
  /** Active power phase L1 at PCC in kW */
  pv_pcc_power_active_l1?: number;
  /** Active power phase L2 at PCC in kW */
  pv_pcc_power_active_l2?: number;
  /** Active power phase L3 at PCC in kW */
  pv_pcc_power_active_l3?: number;
  /** Current phase L1 at PCC in A */
  pv_pcc_current_l1?: number;
  /** Current phase L2 at PCC in A */
  pv_pcc_current_l2?: number;
  /** Current phase L3 at PCC in A */
  pv_pcc_current_l3?: number;
  /** Total reactive power at PCC in kVar */
  pv_pcc_power_reactive?: number;
  /** Reactive power phase L1 at PCC in kVar */
  pv_pcc_power_reactive_l1?: number;
  /** Reactive power phase L2 at PCC in kVar */
  pv_pcc_power_reactive_l2?: number;
  /** Reactive power phase L3 at PCC in kVar */
  pv_pcc_power_reactive_l3?: number;
  /** Total apparent power at PCC in kVA */
  pv_pcc_power_apparent?: number;
  /** Power factor phase L1 at PCC */
  pv_pcc_power_factor_l1?: number;
  /** Power factor phase L2 at PCC */
  pv_pcc_power_factor_l2?: number;
  /** Power factor phase L3 at PCC */
  pv_pcc_power_factor_l3?: number;
  /** Active power from external PV source in kW */
  pv_ext_power_active?: number;
  /** Ambient air temperature at PV site in °C */
  pv_ambient_temp?: number;
  /** Inverter radiator/heatsink temperature in °C */
  pv_inv_temp?: number;
  /** Inverter operating status: grid-connected, off-grid, standby, fault */
  pv_inv_status?: string;
  /** Inverter communication status: connected, disconnected */
  pv_inv_connection_status?: string;
}

export interface ThermalColdTelemetry extends BaseTelemetry {
  /** Power consumption in kW */
  therm_system_power_active?: number;
  /** Electric power consumption in W */
  therm_system_power_electric?: number;
  /** Current storage temperature in C */
  therm_storage_temp?: number;
  /** Maximum allowable temperature in C */
  therm_storage_temp_max?: number;
  /** Minimum allowable temperature in C */
  therm_storage_temp_min?: number;
  /** Output air relative humidity (%) */
  therm_air_humidity_output?: number;
  /** Output air temperature in C */
  therm_air_temp_output?: number;
  /** Input air relative humidity (%) */
  therm_air_humidity_input?: number;
  /** Input air temperature in C */
  therm_air_temp_input?: number;
  /** Internal temperature in C */
  therm_system_temp_internal?: number;
  /** Internal air relative humidity (%) */
  therm_system_humidity_internal?: number;
  /** Hot water input temperature in C */
  therm_water_temp_hot_in?: number;
  /** Hot water output temperature in C */
  therm_water_temp_hot_out?: number;
  /** Coefficient of Performance (efficiency ratio) */
  therm_system_cop?: number;
  /** Energy Efficiency Ratio */
  therm_system_eer?: number;
  /** Hot water flow rate in L/h */
  therm_water_flow_hot?: number;
  /** Maximum thermal storage capacity in kWh */
  therm_storage_energy_nominal?: number;
  /** Operational state identifier */
  therm_system_state?: string;
}

export interface ThermalHeatTelemetry extends BaseTelemetry {
  /** Power consumption in kW */
  therm_system_power_active?: number;
  /** Electric power consumption in W */
  therm_system_power_electric?: number;
  /** Current storage temperature in C */
  therm_storage_temp?: number;
  /** Maximum allowable temperature in C */
  therm_storage_temp_max?: number;
  /** Minimum allowable temperature in C */
  therm_storage_temp_min?: number;
  /** Hot water input temperature in C */
  therm_water_temp_hot_in?: number;
  /** Hot water output temperature in C */
  therm_water_temp_hot_out?: number;
  /** Coefficient of Performance (efficiency ratio) */
  therm_system_cop?: number;
  /** Hot water flow rate in L/h */
  therm_water_flow_hot?: number;
  /** Maximum thermal storage capacity in kWh */
  therm_storage_energy_nominal?: number;
  /** Operational state identifier */
  therm_system_state?: string;
}

export interface HydrogenLocalPlantTelemetry extends BaseTelemetry {
  /** PV Power in kW */
  h2_plant_pv_power_active?: number;
  /** Electrolyzer Power in kW */
  h2_electrolyzer_power_active?: number;
  /** Electrolyzer Hydrogen Mass Flow Rate in kg/s */
  h2_electrolyzer_mass_flow?: number;
  /** Produced hydrogen from the Electrolyzer in kg */
  h2_electrolyzer_mass_total?: number;
  /** Stored hydrogen mass in kg */
  h2_storage_mass?: number;
}

export interface CommunityTelemetry extends BaseTelemetry {
  /** Community power exchange with external grid in kW. Positive = export, Negative = import */
  com_grid_power_exchange?: number;
  /** Plant community power exchange in kW */
  com_plant_community_power?: number;
  /** Consumer community power exchange in kW */
  com_consumer_community_power?: number;
  /** Prosumer community power exchange in kW */
  com_prosumer_community_power?: number;
  /** Smart Prosumer LV1 community power exchange in kW */
  com_prosumer_lv1_community_power?: number;
  /** Smart Prosumer LV2 community power exchange in kW */
  com_prosumer_lv2_community_power?: number;
  /** Smart Prosumer LV3 community power exchange in kW */
  com_prosumer_lv3_community_power?: number;
}

export interface EnergyDemandConsumerTelemetry extends BaseTelemetry {
  /** Load electrical power in kW */
  demand_load_power_active?: number;
}

export interface EnergyDemandProsumerTelemetry extends BaseTelemetry {
  /** Prosumer capability level */
  demand_prosumer_capability_level?: DemandProsumerCapabilityLevel;
  /** [Level 1+] PV Power in kW */
  demand_prosumer_pv_power_active?: number;
  /** [Level 1+] Load Power in kW */
  demand_prosumer_load_power_active?: number;
  /** [Level 1+] Battery State of Charge in % */
  demand_prosumer_bess_soc?: number;
  /** [Level 1+] Battery Power in kW. Positive = discharging, Negative = charging */
  demand_prosumer_bess_power_active?: number;
  /** [Level 2+] Fuel Cell Power in kW */
  demand_fuelcell_power_active?: number;
  /** [Level 2+] Fuel Cell H2 Mass Flow Rate in kg/s */
  demand_fuelcell_mass_flow?: number;
  /** [Level 2+] Consumed H2 from Fuel Cell in kg */
  demand_fuelcell_mass_consumed?: number;
  /** [Level 2+] Stored Hydrogen Mass in kg */
  demand_prosumer_storage_mass?: number;
  /** [Level 3] Recoverable Heat Power from Fuel Cell in kW */
  demand_fuelcell_power_thermal?: number;
}

export interface CaesTelemetry extends BaseTelemetry {
  /** Compressor power consumption in kW */
  caes_compressor_power_active?: number;
  /** Current air pressure in bar */
  caes_storage_pressure?: number;
  /** Maximum rated pressure in bar */
  caes_storage_pressure_max?: number;
  /** Operating state: 0 = Off, 1 = On, 2 = Standby, 3 = Fault */
  caes_compressor_state?: number;
}

export interface GridMeterTelemetry extends BaseTelemetry {
  /** Power fed into grid (export) in kW */
  grid_power_export?: number;
  /** Power pulled from grid (import) in kW */
  grid_power_import?: number;
  /** Instantaneous grid power in kW. Positive = import, Negative = export */
  grid_bus_power_active?: number;
  /** AC voltage in V */
  grid_ac_voltage_input?: number;
  /** AC current in A */
  grid_ac_current_input?: number;
  /** Active power in W */
  grid_meter_power_active?: number;
  /** Reactive power in Var */
  grid_bus_power_reactive?: number;
  /** Apparent power in VA */
  grid_bus_power_apparent?: number;
  /** Power factor */
  grid_bus_power_factor?: number;
  /** Voltage phase L1 in V */
  grid_bus_voltage_l1?: number;
  /** Current phase L1 in A */
  grid_bus_current_l1?: number;
  /** Grid frequency in Hz */
  grid_frequency?: number;
  /** Input power of inverter in VA */
  grid_inv_power_input?: number;
  /** Output power of inverter in VA */
  grid_inv_power_output?: number;
  /** AC consumption (load) in W */
  grid_load_power_consumption?: number;
  /** Total active energy imported in kWh */
  grid_energy_import?: number;
  /** Total active energy exported in kWh */
  grid_energy_export?: number;
  /** Total active energy in kWh */
  grid_energy_total?: number;
  /** Total reactive energy imported in kVarh */
  grid_energy_reactive_import?: number;
  /** Total reactive energy exported in kVarh */
  grid_energy_reactive_export?: number;
  /** Total reactive energy in kVarh */
  grid_energy_reactive_total?: number;
  /** DC bus voltage in V */
  grid_dc_voltage?: number;
  /** DC bus current in A */
  grid_dc_current?: number;
  /** DC power in W */
  grid_dc_power_active?: number;
  /** DC energy imported (taken in) in kWh */
  grid_dc_energy_import?: number;
  /** DC energy exported (given out) in kWh */
  grid_dc_energy_export?: number;
  /** Load apparent power in VA */
  grid_load_power_apparent?: number;
  /** Load active power in W */
  grid_load_power_active?: number;
  /** Load reactive power in Var */
  grid_load_power_reactive?: number;
  /** Load power factor */
  grid_load_power_factor?: number;
}

export interface AlarmRecord extends BaseTelemetry {
  /** Alarm code identifier (see alarm codes documentation) */
  alarm_code: number;
  /** Alarm is currently active */
  active: boolean;
}

export interface IngestionResponse {
  written: number;
}
