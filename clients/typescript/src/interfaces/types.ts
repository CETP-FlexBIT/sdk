// Auto-generated from OpenAPI spec — do not edit manually.
// Run: cd packages/client-generator && bun generate.ts

/** Data quality indicator: raw (direct measurement), estimated (calculated), bad (invalid) */
export type MetaDataQuality = "raw" | "estimated" | "bad";

/** Signal source system: BMS (Battery Management), PCS (Power Conversion), SCADA, EMS (Energy Management), EVSE (EV Supply Equipment), PV_INV (PV Inverter) */
export type MetaSource = "BMS" | "PCS" | "SCADA" | "EMS" | "EVSE" | "PV_INV";

/** Current operating mode of the energy storage asset */
export type BessStorageStatus = "idle" | "charge" | "discharge" | "standby" | "fault";

/** EV charger connector state */
export type EvConnectorStatus = "available" | "occupied" | "reserved" | "unavailable" | "faulted";

/** Charging session status */
export type EvChgStatus = "charging" | "idle" | "suspended_ev" | "suspended_evse";

/** Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC) */
export type EvChgEnergyTransferMode = "ac" | "dc" | "ac_bpt" | "dc_bpt";

/** Power flow direction: import (grid to EV), export (EV to grid), idle */
export type EvChgPowerFlowDirection = "import" | "export" | "idle";

/** Prosumer capability level */
export type DemandProsumerCapabilityLevel = "1" | "2" | "3";

/** Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC) */
export type EvChgSetEnergyTransferMode = "ac" | "dc" | "ac_bpt" | "dc_bpt";

export type EvChgSetPowerFlowDirection = "import" | "export";

import type {
  BaseTelemetry,
  BessTelemetry,
  EvChargerTelemetry,
  PvTelemetry,
  ThermalColdTelemetry,
  ThermalHeatTelemetry,
  HydrogenLocalPlantTelemetry,
  CommunityTelemetry,
  EnergyDemandConsumerTelemetry,
  EnergyDemandProsumerTelemetry,
  CaesTelemetry,
  GridMeterTelemetry,
  AlarmRecord,
  IngestionResponse,
} from "./ingestion.interfaces.js";

export type {
  BaseTelemetry,
  BessTelemetry,
  EvChargerTelemetry,
  PvTelemetry,
  ThermalColdTelemetry,
  ThermalHeatTelemetry,
  HydrogenLocalPlantTelemetry,
  CommunityTelemetry,
  EnergyDemandConsumerTelemetry,
  EnergyDemandProsumerTelemetry,
  CaesTelemetry,
  GridMeterTelemetry,
  AlarmRecord,
  IngestionResponse,
};

import type {
  ControlBase,
  BessControl,
  EvChargerControl,
  PvControl,
  ThermalColdControl,
  ThermalHeatControl,
  HydrogenControl,
  CommunityControl,
  EnergyDemandProsumerControl,
  GridMeterControl,
  ControlResponse,
} from "./control.interfaces.js";

export type {
  ControlBase,
  BessControl,
  EvChargerControl,
  PvControl,
  ThermalColdControl,
  ThermalHeatControl,
  HydrogenControl,
  CommunityControl,
  EnergyDemandProsumerControl,
  GridMeterControl,
  ControlResponse,
};