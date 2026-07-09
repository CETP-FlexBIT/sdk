import type {
  AlarmRecord,
  BaseTelemetry,
  BessControl,
  BessTelemetry,
  CaesTelemetry,
  CommunityControl,
  CommunityTelemetry,
  ControlBase,
  EnergyDemandConsumerTelemetry,
  EnergyDemandProsumerControl,
  EnergyDemandProsumerTelemetry,
  EvChargerControl,
  EvChargerTelemetry,
  GridMeterControl,
  GridMeterTelemetry,
  HydrogenControl,
  HydrogenLocalPlantTelemetry,
  PvControl,
  PvTelemetry,
  ThermalColdControl,
  ThermalColdTelemetry,
  ThermalHeatControl,
  ThermalHeatTelemetry,
} from "./types.js";

export type Type =
  | "alarm"
  | "bess"
  | "ev_charger"
  | "pv"
  | "caes"
  | "community"
  | "thermal_cold"
  | "thermal_heat"
  | "energy_demand_consumer"
  | "energy_demand_prosumer"
  | "hydrogen_local_plant"
  | "grid_meter";

export type Ingestion =
  | BessTelemetry
  | PvTelemetry
  | CaesTelemetry
  | EvChargerTelemetry
  | CommunityTelemetry
  | GridMeterTelemetry
  | ThermalColdTelemetry
  | ThermalHeatTelemetry
  | EnergyDemandConsumerTelemetry
  | EnergyDemandProsumerTelemetry
  | HydrogenLocalPlantTelemetry;

export type IngestionByType = {
  alarm: AlarmRecord;
  bess: BessTelemetry;
  ev_charger: EvChargerTelemetry;
  pv: PvTelemetry;
  caes: CaesTelemetry;
  community: CommunityTelemetry;
  thermal_cold: ThermalColdTelemetry;
  thermal_heat: ThermalHeatTelemetry;
  hydrogen_local_plant: HydrogenLocalPlantTelemetry;
  grid_meter: GridMeterTelemetry;
  energy_demand_consumer: EnergyDemandConsumerTelemetry;
  energy_demand_prosumer: EnergyDemandProsumerTelemetry;
};

export type Control =
  | BessControl
  | PvControl
  | EvChargerControl
  | CommunityControl
  | GridMeterControl
  | ThermalColdControl
  | ThermalHeatControl
  | HydrogenControl
  | EnergyDemandProsumerControl;

export type ControlByType = {
  alarm: never;
  bess: BessControl;
  ev_charger: EvChargerControl;
  pv: PvControl;
  community: CommunityControl;
  thermal_cold: ThermalColdControl;
  thermal_heat: ThermalHeatControl;
  hydrogen_local_plant: HydrogenControl;
  grid_meter: GridMeterControl;
  caes: never;
  energy_demand_consumer: never;
  energy_demand_prosumer: EnergyDemandProsumerControl;
};

export type IngestionMeta = Partial<Omit<BaseTelemetry, "meta_site_id" | "meta_asset_id" | "type">>;

export type ControlMeta = Partial<Omit<ControlBase, "meta_site_id" | "meta_asset_id" | "type">>;

export type IngestionMessage = {
  [TType in keyof IngestionByType]: IngestionByType[TType] &
    IngestionMeta & {
      type: TType;
      meta_site_id: string;
      meta_asset_id: string;
      meta_timestamp: string;
    };
}[keyof IngestionByType];

type NonNeverKeys<T> = {
  [K in keyof T]: T[K] extends never ? never : K;
}[keyof T];

export type ControlMessage = {
  [TType in NonNeverKeys<ControlByType>]: ControlByType[TType] &
    ControlMeta & {
      type: TType;
      meta_site_id: string;
      meta_asset_id: string;
      meta_timestamp: string;
    };
}[NonNeverKeys<ControlByType>];
