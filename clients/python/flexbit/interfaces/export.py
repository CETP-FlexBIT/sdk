from __future__ import annotations

from typing import Any, Literal, TypeAlias

from . import (
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
)

Type = Literal[
    "alarm",
    "bess",
    "ev_charger",
    "pv",
    "caes",
    "community",
    "thermal_cold",
    "thermal_heat",
    "energy_demand_consumer",
    "energy_demand_prosumer",
    "hydrogen_local_plant",
    "grid_meter",
]

Ingestion: TypeAlias = (
    AlarmRecord
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
    | HydrogenLocalPlantTelemetry
)

Control: TypeAlias = (
    BessControl
    | PvControl
    | EvChargerControl
    | CommunityControl
    | GridMeterControl
    | ThermalColdControl
    | ThermalHeatControl
    | HydrogenControl
    | EnergyDemandProsumerControl
)

IngestionMeta: TypeAlias = dict[str, Any]
ControlMeta: TypeAlias = dict[str, Any]
IngestionMessage: TypeAlias = dict[str, Any]
ControlMessage: TypeAlias = dict[str, Any]

IngestionByType = {
    "alarm": AlarmRecord,
    "bess": BessTelemetry,
    "ev_charger": EvChargerTelemetry,
    "pv": PvTelemetry,
    "caes": CaesTelemetry,
    "community": CommunityTelemetry,
    "thermal_cold": ThermalColdTelemetry,
    "thermal_heat": ThermalHeatTelemetry,
    "hydrogen_local_plant": HydrogenLocalPlantTelemetry,
    "grid_meter": GridMeterTelemetry,
    "energy_demand_consumer": EnergyDemandConsumerTelemetry,
    "energy_demand_prosumer": EnergyDemandProsumerTelemetry,
}

ControlByType = {
    "bess": BessControl,
    "ev_charger": EvChargerControl,
    "pv": PvControl,
    "community": CommunityControl,
    "thermal_cold": ThermalColdControl,
    "thermal_heat": ThermalHeatControl,
    "hydrogen_local_plant": HydrogenControl,
    "grid_meter": GridMeterControl,
    "energy_demand_prosumer": EnergyDemandProsumerControl,
}

__all__ = [
    "BaseTelemetry",
    "AlarmRecord",
    "ControlBase",
    "Type",
    "Ingestion",
    "Control",
    "IngestionMeta",
    "ControlMeta",
    "IngestionMessage",
    "ControlMessage",
    "IngestionByType",
    "ControlByType",
]
