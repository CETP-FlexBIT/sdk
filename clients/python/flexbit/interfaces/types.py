"""Auto-generated from OpenAPI spec — do not edit manually.
Run: cd packages/client-generator && bun generate.ts
"""

from typing import Literal

MetaDataQuality = Literal["raw", "estimated", "bad"]
"""Data quality indicator: raw (direct measurement), estimated (calculated), bad (invalid)"""

MetaSource = Literal["BMS", "PCS", "SCADA", "EMS", "EVSE", "PV_INV"]
"""Signal source system: BMS (Battery Management), PCS (Power Conversion), SCADA, EMS (Energy Management), EVSE (EV Supply Equipment), PV_INV (PV Inverter)"""

BessStorageStatus = Literal["idle", "charge", "discharge", "standby", "fault"]
"""Current operating mode of the energy storage asset"""

EvConnectorStatus = Literal[
    "available", "occupied", "reserved", "unavailable", "faulted"
]
"""EV charger connector state"""

EvChgStatus = Literal["charging", "idle", "suspended_ev", "suspended_evse"]
"""Charging session status"""

EvChgEnergyTransferMode = Literal["ac", "dc", "ac_bpt", "dc_bpt"]
"""Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC)"""

EvChgPowerFlowDirection = Literal["import", "export", "idle"]
"""Power flow direction: import (grid to EV), export (EV to grid), idle"""

DemandProsumerCapabilityLevel = Literal["1", "2", "3"]
"""Prosumer capability level"""

EvChgSetEnergyTransferMode = Literal["ac", "dc", "ac_bpt", "dc_bpt"]
"""Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC)"""

EvChgSetPowerFlowDirection = Literal["import", "export"]
