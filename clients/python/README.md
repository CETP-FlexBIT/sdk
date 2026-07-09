# FlexBIT Python Client

[![PyPI version](https://img.shields.io/pypi/v/flexbit-sdk?logo=pypi)](https://pypi.org/project/flexbit-sdk/)

Official FlexBIT SDK client for Python. It publishes telemetry and consumes control messages over Kafka.

## Installation

```bash
uv add flexbit-sdk
# or
pip install flexbit-sdk
```

For local development from this repository:

```bash
uv sync
```

Python 3.10 or newer is required.

## Configuration

Create a connector with a site ID, client ID, Kafka host, and API credentials:

```python
options = {
    "siteId": "44a7a2f2-1cc9-464d-96f4-b767045f8206",
    "clientId": "my-flexbit-client",
    "host": "your-kafka-host:9092",
    "api": {
        "id": "your_api_id",
        "secret": "your_api_secret",
    },
}
```

The SDK also accepts Python-style option names:

```python
from flexbit import CreateConnectorOptions

options = CreateConnectorOptions(
    site_id="44a7a2f2-1cc9-464d-96f4-b767045f8206",
    client_id="my-flexbit-client",
    host="your-kafka-host:9092",
    api={"id": "your_api_id", "secret": "your_api_secret"},
)
```

The runnable samples can read these values from environment variables:

```bash
FLEXBIT_HOST=your-kafka-host:9092
FLEXBIT_API_ID=your_api_id
FLEXBIT_API_SECRET=your_api_secret
```

If `host` is omitted, the client defaults to `127.0.0.1:9092`. API credentials are used as SASL/SCRAM-SHA-256 credentials for Kafka.

## Device Connector

Use a device connector from an on-site integration. It sends telemetry to FlexBIT and subscribes to control commands for the same site.

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
        lambda command: print(
            "Control command:", command["type"], command["meta_asset_id"]
        )
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

## Module Connector

Use a module connector from a platform-side module. It subscribes to telemetry for the configured site and sends control commands back to assets at that site.

```python
import os

from flexbit import create_module_connector

site_id = "44a7a2f2-1cc9-464d-96f4-b767045f8206"

module = create_module_connector(
    {
        "siteId": site_id,
        "clientId": "platform-module-client",
        "host": os.environ["FLEXBIT_HOST"],
        "api": {
            "id": os.environ["FLEXBIT_API_ID"],
            "secret": os.environ["FLEXBIT_API_SECRET"],
        },
    }
)


def handle_telemetry(telemetry: dict) -> None:
    if telemetry.get("type") != "bess" or "bess_storage_soc" not in telemetry:
        return

    if telemetry["bess_storage_soc"] > 90:
        module.control(
            "bess",
            telemetry["meta_asset_id"],
            {
                "meta_site_id": telemetry["meta_site_id"],
                "meta_asset_id": telemetry["meta_asset_id"],
                "bess_inv_set_enable": False,
            },
        )


module.subscribe(handle_telemetry)
```

## API

```python
create_device_connector(options)
```

Returns:

- `ingest(type, asset_id, content, meta=None)` - publish telemetry to `ingestion.{siteId}`.
- `subscribe(callback)` - consume control messages from `control.{siteId}`.
- `close()` - close any open Kafka producer or consumer.

```python
create_module_connector(options)
```

Returns:

- `control(type, asset_id, content, meta=None)` - publish control commands to `control.{siteId}`.
- `subscribe(callback)` - consume telemetry messages from `ingestion.{siteId}`.
- `close()` - close any open Kafka producer or consumer.

The lower-level `create_connector(options)` helper returns a `Connector` with `ingest`, `control`, `subscribe_ingestion`, `subscribe_control`, and `close`.

The SDK injects `type`, `meta_site_id`, `meta_asset_id`, and `meta_timestamp` into every produced message. `meta_timestamp` defaults to the current UTC time when not provided.

`content` and `meta` may be mappings, dataclasses, or objects with a `__dict__`.

## Supported Asset Types

Telemetry:

`alarm`, `bess`, `ev_charger`, `pv`, `caes`, `community`, `thermal_cold`, `thermal_heat`, `energy_demand_consumer`, `energy_demand_prosumer`, `hydrogen_local_plant`, `grid_meter`

Control:

`bess`, `ev_charger`, `pv`, `community`, `thermal_cold`, `thermal_heat`, `hydrogen_local_plant`, `grid_meter`, `energy_demand_prosumer`

## Topics

| Direction | Topic |
| --- | --- |
| Telemetry, device to module | `ingestion.{siteId}` |
| Control, module to device | `control.{siteId}` |

Messages are JSON payloads. The asset kind is carried in the message `type` field.

## Types

The package exports generated payload dataclasses and message aliases:

```python
from flexbit.interfaces import BessTelemetry, BessControl
from flexbit.interfaces.export import ControlMessage, IngestionMessage
```

Generated payload shapes live under `flexbit/interfaces`.

## Samples

Runnable examples live in [`sample`](./sample):

- `device-demo.py` sends EV charger and BESS telemetry and listens for control commands.
- `control-demo.py` subscribes to telemetry and sends a BESS control command when a threshold is crossed.

The sample files currently import from `src`, while the package exported by this project is `flexbit`. Check the imports before running them against an installed `flexbit-sdk` package.

## License

GNU Affero General Public License v3.0.
