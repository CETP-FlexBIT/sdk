# FlexBIT SDK

[![npm version](https://img.shields.io/npm/v/%40flexbit%2Fsdk?logo=npm)](https://www.npmjs.com/package/@flexbit/sdk)
[![PyPI version](https://img.shields.io/pypi/v/flexbit-sdk?logo=pypi)](https://pypi.org/project/flexbit-sdk/)

Official FlexBIT SDK repository for Kafka-based telemetry ingestion and control of distributed energy assets.

This repository currently contains:

- `clients/typescript` - the `@flexbit/sdk` TypeScript/JavaScript client.
- `clients/python` - the `flexbit-sdk` Python client.

## Clients

| Language | Package | Location |
| --- | --- | --- |
| TypeScript | `@flexbit/sdk` | [`clients/typescript`](./clients/typescript) |
| Python | `flexbit-sdk` | [`clients/python`](./clients/python) |

Both clients expose the same connector model:

- **Device connector** - for on-site integrations. Publishes telemetry to FlexBIT and consumes control commands for one site.
- **Module connector** - for platform-side modules. Consumes telemetry for one site and publishes control commands back to assets at that site.

Messages are JSON payloads over Kafka. The SDK injects `type`, `meta_site_id`, `meta_asset_id`, and `meta_timestamp` into produced messages.

## Installation

### TypeScript

```bash
npm install @flexbit/sdk
```

### Python

```bash
uv add flexbit-sdk
# or
pip install flexbit-sdk
```

## Configuration

Both clients expect Kafka connection settings when a connector is created:

```bash
FLEXBIT_HOST=your-kafka-host:9092
FLEXBIT_API_ID=your_api_id
FLEXBIT_API_SECRET=your_api_secret
```

If `host` is omitted, both clients default to `127.0.0.1:9092`. API credentials are used as SASL/SCRAM-SHA-256 credentials for Kafka.

## Quick Start

### TypeScript Device

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

### Python Device

```python
import os
import threading

from flexbit import create_device_connector

site_id = "44a7a2f2-1cc9-464d-96f4-b767045f8206"
asset_id = "86d33428-2fb7-40f1-8bb9-01b5a476bb29"

device = create_device_connector(
    {
        "siteId": site_id,
        "clientId": "site-device-client",
        "host": os.environ["FLEXBIT_HOST"],
        "api": {
            "id": os.environ["FLEXBIT_API_ID"],
            "secret": os.environ["FLEXBIT_API_SECRET"],
        },
    }
)

threading.Thread(
    target=lambda: device.subscribe(
        lambda command: print("Control command:", command["type"], command["meta_asset_id"])
    ),
    daemon=True,
).start()

device.ingest(
    "bess",
    asset_id,
    {
        "meta_asset_id": asset_id,
        "bess_storage_soc": 82.5,
        "bess_inv_power_active": -15.3,
        "bess_storage_status": "charge",
    },
)
```

## Topics

| Direction | Topic |
| --- | --- |
| Telemetry, device to module | `ingestion.{siteId}` |
| Control, module to device | `control.{siteId}` |

The asset kind is carried in the message `type` field.

## Supported Asset Types

Telemetry:

`bess`, `ev_charger`, `pv`, `caes`, `community`, `thermal_cold`, `thermal_heat`, `energy_demand_consumer`, `energy_demand_prosumer`, `hydrogen_local_plant`, `grid_meter`

Control:

`bess`, `ev_charger`, `pv`, `community`, `thermal_cold`, `thermal_heat`, `hydrogen_local_plant`, `grid_meter`, `energy_demand_prosumer`

## Samples

TypeScript samples live in [`clients/typescript/sample`](./clients/typescript/sample):

```bash
cd clients/typescript
npm run sample:device
npm run sample:module
```

Python samples live in [`clients/python/sample`](./clients/python/sample):

The Python sample files show the same device/module flow. They currently import from `src`, while the package exported by this project is `flexbit`, so check the imports before running them against an installed `flexbit-sdk` package.

Each sample requires `FLEXBIT_HOST`, `FLEXBIT_API_ID`, and `FLEXBIT_API_SECRET`.

## License

This repository and its packages are licensed under the GNU Affero General Public License v3.0. See [LICENSE](./LICENSE).
