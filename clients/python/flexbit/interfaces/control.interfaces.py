"""Auto-generated from OpenAPI spec — do not edit manually.
Run: cd packages/client-generator && bun generate.ts
"""

from dataclasses import dataclass
from .types import EvChgSetEnergyTransferMode, EvChgSetPowerFlowDirection


@dataclass(kw_only=True)
class ControlBase:
    """Base control record with common identifier fields."""

    type: str | None = None
    """Control asset type. Automatically injected by SDK producers."""

    meta_asset_id: str
    """Unique identifier of the asset (UUID format)"""

    meta_site_id: str
    """Unique identifier of the site where the asset is located (UUID format)"""

    meta_timestamp: str | None = None
    """ISO 8601 UTC timestamp of the command (e.g. 2026-04-08T12:00:00.000Z). Defaults to server time if not provided"""


@dataclass(kw_only=True)
class BessControl(ControlBase):
    """BESS (Battery Energy Storage System) control commands"""

    bess_inv_set_power_active: float | None = None
    """Power setpoint in kW"""

    bess_inv_set_power_reactive: float | None = None
    """Reactive power setpoint in kVar"""

    bess_inv_set_current: float | None = None
    """Current setpoint in A"""

    bess_inv_set_enable: bool | None = None
    """Battery enable/disable"""

    bess_inv_set_current_max: float | None = None
    """Maximum allowed current in A"""

    bess_inv_set_mode: int | None = None
    """Set operating mode (UInt32)"""

    bess_inv_set_power_charge: float | None = None
    """Charge rate setpoint in kW"""

    bess_inv_set_operating_mode: bool | None = None
    """Operating mode: true for current-following, false for power-following"""


@dataclass(kw_only=True)
class EvChargerControl(ControlBase):
    """EV Charger control commands"""

    ev_chg_set_current_max: float | None = None
    """Maximum charging current in A"""

    ev_chg_set_voltage_max: float | None = None
    """Maximum charging voltage in V"""

    ev_chg_set_start: bool | None = None
    """Start charging session (V2G)"""

    ev_chg_set_stop: bool | None = None
    """Stop charging session (V2G)"""

    ev_chg_set_interrupt: bool | None = None
    """Interrupt current session (V2G)"""

    ev_chg_set_control: int | None = None
    """Charger control command (Byte)"""

    ev_chg_set_energy_transfer_mode: EvChgSetEnergyTransferMode | None = None
    """Energy transfer mode per ISO 15118-20: ac, dc, ac_bpt (Bidirectional AC), dc_bpt (Bidirectional DC)"""

    ev_chg_set_power_flow_direction: EvChgSetPowerFlowDirection | None = None


@dataclass(kw_only=True)
class PvControl(ControlBase):
    """PV (Photovoltaic) / Hybrid Inverter control commands"""

    pv_inv_set_charge_start: str | None = None
    """Starting time of charging period (hh:mm)"""

    pv_inv_set_charge_end: str | None = None
    """Ending time of charging period (hh:mm)"""

    pv_inv_set_discharge_start: str | None = None
    """Starting time of discharging period (hh:mm)"""

    pv_inv_set_discharge_end: str | None = None
    """Ending time of discharging period (hh:mm)"""

    pv_inv_set_power_charge: float | None = None
    """Charge power setpoint in kW"""

    pv_inv_set_power_discharge: float | None = None
    """Discharge power setpoint in kW"""


@dataclass(kw_only=True)
class ThermalColdControl(ControlBase):
    """Thermal Cold Storage control commands"""

    therm_storage_set_temp: float | None = None
    """Temperature setpoint in C"""

    therm_system_set_state: int | None = None
    """Set operating state (0=Off, 1=On/Cooling, 2=Standby)"""


@dataclass(kw_only=True)
class ThermalHeatControl(ControlBase):
    """Thermal Heat Storage control commands"""

    therm_storage_set_temp: float | None = None
    """Temperature setpoint in C"""

    therm_system_set_state: int | None = None
    """Set operating state (0=Off, 1=On/Heating, 2=Standby)"""


@dataclass(kw_only=True)
class HydrogenControl(ControlBase):
    """Hydrogen System control commands"""

    h2_storage_set_flow_rate: float | None = None
    """Set volumetric flow rate in L/min"""

    h2_electrolyzer_set_power: float | None = None
    """Set electrolyzer power in kW"""

    h2_fuelcell_set_power: float | None = None
    """Set fuel cell power in kW"""

    h2_dcdc_set_power: float | None = None
    """Set DC-DC converter power in kW"""

    h2_htpem_set_power: float | None = None
    """Set HTPEM fuel cell power in kW"""

    h2_ps_set_current: float | None = None
    """Set power supply current in A"""

    h2_ps_set_voltage: float | None = None
    """Set power supply voltage in V"""

    h2_ps_set_power: float | None = None
    """Set power supply power in kW"""


@dataclass(kw_only=True)
class CommunityControl(ControlBase):
    """Community (Blackbox) control commands"""

    com_grid_set_power_exchange: float | None = None
    """Set community power exchange with grid in kW. Positive = export, Negative = import"""


@dataclass(kw_only=True)
class EnergyDemandProsumerControl(ControlBase):
    """Energy Demand Prosumer control commands"""

    demand_prosumer_set_power_exchange: float | None = None
    """Set prosumer power exchange with community grid in kW. Positive = export, Negative = import"""


@dataclass(kw_only=True)
class GridMeterControl(ControlBase):
    """Grid Meter control commands"""

    grid_bus_set_power_active: float | None = None
    """Grid power setpoint in kW"""

    grid_bus_set_power_control: float | None = None
    """Active setpoint power to grid in kW"""
