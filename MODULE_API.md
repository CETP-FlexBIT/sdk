# Global module API

The TypeScript and Python module SDKs can query the platform and send control feedback over HTTP. They use a global API key created in the platform's `/admin/api-keys` page. This key works from inside Kubernetes and from external clients. It grants access to the module data/control API across every organization. User and organization administration still require an authenticated admin session.

Configure the client through environment variables:

```text
FLEXBIT_PLATFORM_URL=https://your-platform.example.com
FLEXBIT_API_KEY=your-global-api-key
```

Secret provisioning and injection are managed outside the SDK. The client reads the environment at request time. It does not call Kubernetes or Infisical.

## TypeScript

```typescript
import { createModuleApi } from "@flexbit/sdk/module";

const platform = createModuleApi();
const sites = await platform.sites.list({ limit: 100 });
const assets = await platform.assets.list({ siteId: sites[0].id });
const battery = assets.find((asset) => asset.type === "bess");
if (!battery) throw new Error("No battery configured");

const definitions = await platform.metrics.definitions(battery.id);
const latest = await platform.metrics.latest(battery.id);
const history = await platform.metrics.history({
  assetId: battery.id,
  from: "2026-10-07T00:00:00Z",
  to: "2026-10-08T00:00:00Z",
  limit: 1000,
  offset: 0,
});

await platform.control(battery.id, { bess_inv_set_power_active: 15 });
```

An existing `createModuleConnector()` also exposes this client as `connector.platform`. Its Kafka `control()` and `subscribe()` methods keep their existing behavior. Device connectors do not expose the platform query client.

## Python

```python
from flexbit import create_module_api

platform = create_module_api()
sites = platform.list_sites(limit=100)
assets = platform.list_assets(site_id=sites[0]['id'])
battery = next(asset for asset in assets if asset['type'] == 'bess')

definitions = platform.metric_definitions(battery['id'])
latest = platform.latest_metrics(battery['id'])
history = platform.metrics_history(
    battery['id'],
    start='2026-10-07T00:00:00Z',
    end='2026-10-08T00:00:00Z',
    limit=1000,
    offset=0,
)
platform.control(battery['id'], {'bess_inv_set_power_active': 15})
```

Existing Python module connectors expose the client as `connector.platform`.

## Queries and feedback

- Sites include organization IDs, descriptions, offline thresholds, and metadata.
- Assets include site IDs, asset types, and metadata. Omitting the site filter lists assets globally.
- Metric definitions include canonical field names, types, and descriptions. Units are included in the canonical descriptions where specified.
- Latest metrics return a sample or `null` / `None` when no rows exist.
- History returns up to 1,000 samples per request, newest first, within `[from, to)`. Use `offset` for further pages. Site and asset lists allow 100 rows per page.
- Each sample contains `timestamp`, `quality`, `source`, and a `values` dictionary. Missing values are `null` / `None`.
- Control validates the command against the target asset's schema and supplies its real site, asset, type, and timestamp. Unsupported asset types and empty commands return HTTP 400. Publishing success acknowledges Kafka delivery, not device execution.

All calls use POST JSON under `/api/v1/module`: `sites/list`, `assets/list`, `assets/get`, `metrics/definitions`, `metrics/latest`, `metrics/history`, and `control`. Send the key as `Authorization: Bearer <key>`. The SDK uses a ten-second timeout and rejects redirects. TypeScript validates response shapes; both clients raise `ModuleApiError` with the HTTP status on API failures.

## Keys and revocation

Only global admins can create, list, or revoke global keys. The platform stores a hash of each secret and shows the full secret only when it is created. Revocation is checked in the database on every API request; already-authorized in-flight requests may finish. Ordinary organization keys and browser sessions do not authorize this global module API.

The platform migration adding `global_api_key` must be applied before using the admin section or API. Key management is available in the global admin view and its session-authenticated RPC procedures, and is not accessible with a global integration key.
