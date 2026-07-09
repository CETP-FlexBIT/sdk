"""
FlexBIT SDK - Python module sample

Reactive control loop:
  - Consumes ingestion messages for the configured site
  - When BESS State of Charge crosses a threshold, sends a stop command
    back to the originating asset

Run this alongside device-demo.py.

Environment variables required:
  FLEXBIT_HOST, FLEXBIT_API_ID, FLEXBIT_API_SECRET
"""

import os

from src import create_module_connector

SITE_ID = "44a7a2f2-1cc9-464d-96f4-b767045f8206"
SOC_THRESHOLD = 75


def env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def kafka_host() -> str:
    host = env("FLEXBIT_HOST")
    return host if ":" in host else f"{host}:9092"


def main() -> None:
    module = create_module_connector(
        {
            "siteId": SITE_ID,
            "clientId": "flexbit-python-module-sample",
            "host": kafka_host(),
            "api": {
                "id": env("FLEXBIT_API_ID"),
                "secret": env("FLEXBIT_API_SECRET"),
            },
        }
    )

    already_stopped: set[str] = set()

    def handle_telemetry(telemetry: dict) -> None:
        if telemetry.get("type") != "bess":
            return

        soc = telemetry.get("bess_storage_soc")
        if soc is None:
            return

        print(
            "[Module] BESS telemetry "
            f"site={telemetry.get('meta_site_id')} "
            f"asset={telemetry.get('meta_asset_id')} "
            f"soc={soc}"
        )

        asset_id = telemetry["meta_asset_id"]
        if soc <= SOC_THRESHOLD or asset_id in already_stopped:
            return

        already_stopped.add(asset_id)

        module.control(
            "bess",
            asset_id,
            {
                "meta_site_id": telemetry["meta_site_id"],
                "meta_asset_id": asset_id,
                "bess_inv_set_enable": False,
            },
        )

        print(f"[Module] SOC {soc} > {SOC_THRESHOLD}; stop command sent to {asset_id}")

    module.subscribe(handle_telemetry)


if __name__ == "__main__":
    main()
