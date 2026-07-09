// Auto-generated from OpenAPI spec — do not edit manually.
// Run: cd packages/client-generator && bun generate.ts

import type { EvChgSetEnergyTransferMode, EvChgSetPowerFlowDirection } from "./types.js";

export interface ControlBase {
  /** Control asset type. Automatically injected by SDK producers. */
  type?: string;
  /** Unique identifier of the asset (UUID format) */
  meta_asset_id: string;
  /** Unique identifier of the site where the asset is located (UUID format) */
  meta_site_id: string;
  /** ISO 8601 UTC timestamp of the command (e.g. 2026-04-08T12:00:00.000Z). Defaults to server time if not provided */
  meta_timestamp?: string;
}

/** BESS (Battery Energy Storage System) control commands */
export interface BessControl extends ControlBase {
  /** Power setpoint in kW */
  bess_inv_set_power_active?: number;
  /** Reactive power setpoint in kVar */
  bess_inv_set_power_reactive?: number;
  /** Current setpoint in A */
  bess_inv_set_current?: number;
  /** Battery enable/disable */
  bess_inv_set_enable?: boolean;
  /** Maximum allowed current in A */
  bess_inv_set_current_max?: number;
  /** Set operating mode (UInt32) */
  bess_inv_set_mode?: number;
  /** Charge rate setpoint in kW */
  bess_inv_set_power_charge?: number;
  /** Operating mode: true for current-following, false for power-following */
  bess_inv_set_operating_mode?: boolean;
}

/** EV Charger control commands */
export interface EvChargerControl extends ControlBase {
  /** Maximum charging current in A */
  ev_chg_set_current_max?: number;
  /** Maximum charging voltage in V */
  ev_chg_set_voltage_max?: number;
  /** Start charging session (V2G) */
  ev_chg_set_start?: boolean;
  /** Stop charging session (V2G) */
  ev_chg_set_stop?: boolean;
  /** Interrupt current session (V2G) */
  ev_chg_set_interrupt?: boolean;
  /** Charger control command (Byte) */
  ev_chg_set_control?: number;
  /** Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC) */
  ev_chg_set_energy_transfer_mode?: EvChgSetEnergyTransferMode;
  ev_chg_set_power_flow_direction?: EvChgSetPowerFlowDirection;
}

/** PV (Photovoltaic) / Hybrid Inverter control commands */
export interface PvControl extends ControlBase {
  /** Starting time of charging period (hh:mm) */
  pv_inv_set_charge_start?: string;
  /** Ending time of charging period (hh:mm) */
  pv_inv_set_charge_end?: string;
  /** Starting time of discharging period (hh:mm) */
  pv_inv_set_discharge_start?: string;
  /** Ending time of discharging period (hh:mm) */
  pv_inv_set_discharge_end?: string;
  /** Charge power setpoint in kW */
  pv_inv_set_power_charge?: number;
  /** Discharge power setpoint in kW */
  pv_inv_set_power_discharge?: number;
}

/** Thermal Cold Storage control commands */
export interface ThermalColdControl extends ControlBase {
  /** Temperature setpoint in C */
  therm_storage_set_temp?: number;
  /** Set operating state (0=Off, 1=On/Cooling, 2=Standby) */
  therm_system_set_state?: number;
}

/** Thermal Heat Storage control commands */
export interface ThermalHeatControl extends ControlBase {
  /** Temperature setpoint in C */
  therm_storage_set_temp?: number;
  /** Set operating state (0=Off, 1=On/Heating, 2=Standby) */
  therm_system_set_state?: number;
}

/** Hydrogen System control commands */
export interface HydrogenControl extends ControlBase {
  /** Set volumetric flow rate in L/min */
  h2_storage_set_flow_rate?: number;
  /** Set electrolyzer power in kW */
  h2_electrolyzer_set_power?: number;
  /** Set fuel cell power in kW */
  h2_fuelcell_set_power?: number;
  /** Set DC-DC converter power in kW */
  h2_dcdc_set_power?: number;
  /** Set HTPEM fuel cell power in kW */
  h2_htpem_set_power?: number;
  /** Set power supply current in A */
  h2_ps_set_current?: number;
  /** Set power supply voltage in V */
  h2_ps_set_voltage?: number;
  /** Set power supply power in kW */
  h2_ps_set_power?: number;
}

/** Community (Blackbox) control commands */
export interface CommunityControl extends ControlBase {
  /** Set community power exchange with grid in kW. Positive = export, Negative = import */
  com_grid_set_power_exchange?: number;
}

/** Energy Demand Prosumer control commands */
export interface EnergyDemandProsumerControl extends ControlBase {
  /** Set prosumer power exchange with community grid in kW. Positive = export, Negative = import */
  demand_prosumer_set_power_exchange?: number;
}

/** Grid Meter control commands */
export interface GridMeterControl extends ControlBase {
  /** Grid power setpoint in kW */
  grid_bus_set_power_active?: number;
  /** Active setpoint power to grid in kW */
  grid_bus_set_power_control?: number;
}

export interface ControlResponse {
  success: boolean;
}
