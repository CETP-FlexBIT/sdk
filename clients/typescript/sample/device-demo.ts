/**
 * FlexBIT SDK - TypeScript device sample
 *
 * Demonstrates:
 *  1. Sending EV charger telemetry through the device connector
 *  2. Streaming BESS telemetry with progressively rising SoC up to 100%
 *  3. Listening for control commands sent back to the device
 *
 * Environment variables required:
 *   FLEXBIT_HOST, FLEXBIT_API_ID, FLEXBIT_API_SECRET
 */

import { createDeviceConnector } from "@flexbit/sdk";

declare const process: {
  env: Record<string, string | undefined>;
  exitCode?: number;
};

const SITE_ID = "936930ec-432e-4939-ab73-13e0274445d4"
const EV1_ID = "8a30a702-3d25-4f33-96ac-03189ea70ef3";
const BESS_ID = "eee3d813-7758-4728-ae83-8ca9f379e10a";

const SOC_START = 50;
const SOC_END = 100;
const SOC_STEP = 10;
const SOC_INTERVAL_MS = 1_000;

const env = (name: string) => {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
};

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  const device = createDeviceConnector({
    siteId: SITE_ID,
    clientId: "flexbit-typescript-device-sample",
    host: env("FLEXBIT_HOST"),
    api: {
      id: env("FLEXBIT_API_ID"),
      secret: env("FLEXBIT_API_SECRET"),
    },
  });

  void device.subscribe((command) => {
    if (command.type !== "bess") {
      return;
    }
    console.log("[Device] Received BESS control command:", command);
  });

  await device.ingest("ev_charger", EV1_ID, {
    meta_asset_id: EV1_ID,
    ev_chg_power_active: 7.4,
    ev_connector_status: "occupied",
    ev_chg_status: "charging",
    ev_vehicle_soc: Math.random() * 100,
  });
  console.log("[Device] EV charger telemetry written:", EV1_ID);

  for (let soc = SOC_START; soc <= SOC_END; soc += SOC_STEP) {
    await device.ingest("bess", BESS_ID, {
      meta_asset_id: BESS_ID,
      bess_storage_soc: soc,
      bess_storage_soh: 97.0,
      bess_inv_power_active: -15.3,
      bess_storage_status: "charge",
    });
    console.log(`[Device] BESS telemetry written (SoC=${soc}%)`);
    await sleep(SOC_INTERVAL_MS);
  }

  // Test Alarm
    device.ingest("alarm", BESS_ID, {
      meta_asset_id: BESS_ID,
      alarm_code: 1000,
      active: true
  })

  console.log(`[Device] BESS alarm written`);

  setInterval(() => undefined, 60_000);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
