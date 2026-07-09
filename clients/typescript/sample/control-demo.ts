/**
 * FlexBIT SDK - TypeScript module sample
 *
 * Reactive control loop:
 *  - Consumes ingestion messages for the configured site
 *  - When BESS State of Charge crosses a threshold, sends a stop command
 *    back to the originating asset
 *
 * Run this alongside device-demo.ts.
 *
 * Environment variables required:
 *   FLEXBIT_HOST, FLEXBIT_API_ID, FLEXBIT_API_SECRET
 */

import { createModuleConnector } from "@flexbit/sdk";

declare const process: {
  env: Record<string, string | undefined>;
  exitCode?: number;
};

const SITE_ID = "44a7a2f2-1cc9-464d-96f4-b767045f8206";
const SOC_THRESHOLD = 75;

const env = (name: string) => {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
};

const kafkaHost = () => {
  const host = env("FLEXBIT_HOST");
  return host.includes(":") ? host : `${host}:9092`;
};

async function main() {
  const module = createModuleConnector({
    siteId: SITE_ID,
    clientId: "flexbit-typescript-module-sample",
    host: kafkaHost(),
    api: {
      id: env("FLEXBIT_API_ID"),
      secret: env("FLEXBIT_API_SECRET"),
    },
  });

  const alreadyStopped = new Set<string>();

  await module.subscribe(async (telemetry) => {
    if (telemetry.type !== "bess") {
      return;
    }

    const soc = telemetry.bess_storage_soc;
    if (soc === undefined) {
      return;
    }

    console.log(
      `[Module] BESS telemetry site=${telemetry.meta_site_id} asset=${telemetry.meta_asset_id} soc=${soc}`,
    );

    if (soc <= SOC_THRESHOLD || alreadyStopped.has(telemetry.meta_asset_id)) {
      return;
    }

    alreadyStopped.add(telemetry.meta_asset_id);

    await module.control("bess", telemetry.meta_asset_id, {
      meta_site_id: telemetry.meta_site_id,
      meta_asset_id: telemetry.meta_asset_id,
      bess_inv_set_enable: false,
    });

    console.log(
      `[Module] SOC ${soc} > ${SOC_THRESHOLD}; stop command sent to ${telemetry.meta_asset_id}`,
    );
  });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
