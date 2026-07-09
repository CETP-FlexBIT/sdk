# FlexBIT TypeScript Client

[![npm version](https://img.shields.io/npm/v/%40flexbit%2Fsdk?logo=npm)](https://www.npmjs.com/package/@flexbit/sdk)

Official FlexBIT SDK client for TypeScript and JavaScript. It publishes telemetry and consumes control messages over Kafka.

## Installation

```bash
npm install @flexbit/sdk
```

For local development from this repository:

```bash
npm install
npm run build
```

The package is ESM-only and publishes compiled JavaScript and TypeScript declarations from `dist/`.

## Configuration

Create a connector with a site ID, client ID, Kafka host, and API credentials:

```typescript
const options = {
  siteId: "44a7a2f2-1cc9-464d-96f4-b767045f8206",
  clientId: "my-flexbit-client",
  host: "your-kafka-host:9092",
  api: {
    id: "your_api_id",
    secret: "your_api_secret",
  },
};
```

The runnable samples read the same values from environment variables:

```bash
FLEXBIT_HOST=your-kafka-host:9092
FLEXBIT_API_ID=your_api_id
FLEXBIT_API_SECRET=your_api_secret
```

If `host` is omitted, the client defaults to `127.0.0.1:9092`. API credentials are used as SASL/SCRAM-SHA-256 credentials for Kafka.

## Device Connector

Use a device connector from an on-site integration. It sends telemetry to FlexBIT and subscribes to control commands for the same site.

```typescript
import { createDeviceConnector } from "@flexbit/sdk";

const siteId = "44a7a2f2-1cc9-464d-96f4-b767045f8206";
const assetId = "86d33428-2fb7-40f1-8bb9-01b5a476bb29";

const device = createDeviceConnector({
  siteId,
  clientId: "site-device-client",
  host: process.env.FLEXBIT_HOST,
  api: {
    id: process.env.FLEXBIT_API_ID!,
    secret: process.env.FLEXBIT_API_SECRET!,
  },
});

void device.subscribe((command) => {
  console.log("Control command:", command.type, command.meta_asset_id);
});

await device.ingest("bess", assetId, {
  meta_asset_id: assetId,
  bess_storage_soc: 82.5,
  bess_inv_power_active: -15.3,
  bess_storage_status: "charge",
});
```

## Module Connector

Use a module connector from a platform-side module. It subscribes to telemetry for the configured site and sends control commands back to assets at that site.

```typescript
import { createModuleConnector } from "@flexbit/sdk";

const siteId = "44a7a2f2-1cc9-464d-96f4-b767045f8206";

const module = createModuleConnector({
  siteId,
  clientId: "platform-module-client",
  host: process.env.FLEXBIT_HOST,
  api: {
    id: process.env.FLEXBIT_API_ID!,
    secret: process.env.FLEXBIT_API_SECRET!,
  },
});

await module.subscribe(async (telemetry) => {
  if (telemetry.type !== "bess" || telemetry.bess_storage_soc === undefined) {
    return;
  }

  if (telemetry.bess_storage_soc > 90) {
    await module.control("bess", telemetry.meta_asset_id, {
      meta_site_id: telemetry.meta_site_id,
      meta_asset_id: telemetry.meta_asset_id,
      bess_inv_set_enable: false,
    });
  }
});
```

## API

```typescript
createDeviceConnector(options);
```

Returns:

- `ingest(type, assetId, content, meta?)` - publish telemetry to `ingestion.{siteId}`.
- `subscribe(callback)` - consume control messages from `control.{siteId}`.

```typescript
createModuleConnector(options);
```

Returns:

- `control(type, assetId, content, meta?)` - publish control commands to `control.{siteId}`.
- `subscribe(callback)` - consume telemetry messages from `ingestion.{siteId}`.

The SDK injects `type`, `meta_site_id`, `meta_asset_id`, and `meta_timestamp` into every produced message. `meta_timestamp` defaults to the current time when not provided.

## Supported Asset Types

Telemetry:

`bess`, `ev_charger`, `pv`, `caes`, `community`, `thermal_cold`, `thermal_heat`, `energy_demand_consumer`, `energy_demand_prosumer`, `hydrogen_local_plant`, `grid_meter`

Control:

`bess`, `ev_charger`, `pv`, `community`, `thermal_cold`, `thermal_heat`, `hydrogen_local_plant`, `grid_meter`, `energy_demand_prosumer`

## Topics

| Direction | Topic |
| --- | --- |
| Telemetry, device to module | `ingestion.{siteId}` |
| Control, module to device | `control.{siteId}` |

Messages are JSON payloads. The asset kind is carried in the message `type` field.

## Types

The package exports received message union types:

```typescript
import type { ControlMessage, IngestionMessage } from "@flexbit/sdk";
```

Generated payload shapes live under `src/interfaces`.

## Samples

Runnable examples live in [`sample`](./sample):

- `device-demo.ts` sends EV charger and BESS telemetry and listens for control commands.
- `control-demo.ts` subscribes to telemetry and sends a BESS control command when a threshold is crossed.

Run them with:

```bash
npm run sample:device
npm run sample:module
```

## License

GNU Affero General Public License v3.0.