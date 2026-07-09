"""
FlexBIT SDK - Python device sample

Demonstrates:
 1. Sending EV charger telemetry through the device connector
 2. Streaming BESS telemetry with progressively rising SoC up to 100%
 3. Listening for control commands sent back to the device

Environment variables required:
  FLEXBIT_HOST, FLEXBIT_API_ID, FLEXBIT_API_SECRET
"""

import os
import random
import threading
import time

from src import create_device_connector

SITE_ID = "44a7a2f2-1cc9-464d-96f4-b767045f8206"
EV1_ID = "01829d47-9a2d-4439-ba7e-dc538ea44dd1"
EV2_ID = "144b82e8-d0b2-491b-ada2-bb4d4af23ea6"
BESS_ID = "86d33428-2fb7-40f1-8bb9-01b5a476bb29"

SOC_START = 50
SOC_END = 100
SOC_STEP = 10
SOC_INTERVAL_SECONDS = 1


def env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    device = create_device_connector(
        {
            "siteId": SITE_ID,
            "clientId": "flexbit-python-device-sample",
            "host": env("FLEXBIT_HOST"),
            "api": {
                "id": env("FLEXBIT_API_ID"),
                "secret": env("FLEXBIT_API_SECRET"),
            },
        }
    )

    def handle_command(command: dict) -> None:
        if command.get("type") != "bess":
            return
        print("[Device] Received BESS control command:", command)

    threading.Thread(
        target=lambda: device.subscribe(handle_command), daemon=True
    ).start()

    device.ingest(
        "ev_charger",
        EV1_ID,
        {
            "meta_asset_id": EV1_ID,
            "ev_chg_power_active": 7.4,
            "ev_connector_status": "occupied",
            "ev_chg_status": "charging",
            "ev_vehicle_soc": random.random() * 100,
        },
    )
    print("[Device] EV charger telemetry written:", EV1_ID)

    device.ingest(
        "ev_charger",
        EV2_ID,
        {
            "meta_asset_id": EV2_ID,
            "ev_chg_power_active": 11.0,
            "ev_connector_status": "occupied",
            "ev_chg_status": "charging",
            "ev_vehicle_soc": random.random() * 100,
        },
    )
    print("[Device] EV charger telemetry written:", EV2_ID)

    for soc in range(SOC_START, SOC_END + 1, SOC_STEP):
        device.ingest(
            "bess",
            BESS_ID,
            {
                "meta_asset_id": BESS_ID,
                "bess_storage_soc": soc,
                "bess_storage_soh": 97.0,
                "bess_inv_power_active": -15.3,
                "bess_storage_status": "charge",
            },
        )
        print(f"[Device] BESS telemetry written (SoC={soc}%)")
        time.sleep(SOC_INTERVAL_SECONDS)

    device.ingest(
        "alarm",
        BESS_ID,
        {
            "meta_asset_id": BESS_ID,
            "alarm_code": 1000,
            "active": True,
        },
    )
    print("[Device] Alarm telemetry written:", BESS_ID)

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
