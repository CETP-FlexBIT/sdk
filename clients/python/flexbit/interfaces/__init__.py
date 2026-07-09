from importlib import util
from pathlib import Path
from types import ModuleType
from typing import Any

from .types import (
    BessStorageStatus,
    DemandProsumerCapabilityLevel,
    EvChgEnergyTransferMode,
    EvChgPowerFlowDirection,
    EvChgSetEnergyTransferMode,
    EvChgSetPowerFlowDirection,
    EvChgStatus,
    EvConnectorStatus,
    MetaDataQuality,
    MetaSource,
)


def _load_generated_module(module_name: str, filename: str) -> ModuleType:
    path = Path(__file__).with_name(filename)
    spec = util.spec_from_file_location(f"{__name__}.{module_name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load generated module: {filename}")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_ingestion = _load_generated_module("ingestion_interfaces", "ingestion.interfaces.py")
_control = _load_generated_module("control_interfaces", "control.interfaces.py")

_exported_generated_names = [
    "BaseTelemetry",
    "BessTelemetry",
    "EvChargerTelemetry",
    "PvTelemetry",
    "ThermalColdTelemetry",
    "ThermalHeatTelemetry",
    "HydrogenLocalPlantTelemetry",
    "CommunityTelemetry",
    "EnergyDemandConsumerTelemetry",
    "EnergyDemandProsumerTelemetry",
    "CaesTelemetry",
    "GridMeterTelemetry",
    "AlarmRecord",
    "ControlBase",
    "BessControl",
    "EvChargerControl",
    "PvControl",
    "ThermalColdControl",
    "ThermalHeatControl",
    "HydrogenControl",
    "CommunityControl",
    "EnergyDemandProsumerControl",
    "GridMeterControl",
]

for _name in _exported_generated_names:
    _module: Any = _ingestion if hasattr(_ingestion, _name) else _control
    globals()[_name] = getattr(_module, _name)

__all__ = [
    "MetaDataQuality",
    "MetaSource",
    "BessStorageStatus",
    "EvConnectorStatus",
    "EvChgStatus",
    "EvChgEnergyTransferMode",
    "EvChgPowerFlowDirection",
    "DemandProsumerCapabilityLevel",
    "EvChgSetEnergyTransferMode",
    "EvChgSetPowerFlowDirection",
    *_exported_generated_names,
]
