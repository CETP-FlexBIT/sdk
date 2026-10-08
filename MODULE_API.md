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
site = platform.get_site(sites[0]['id'])
organization = site['organization']  # id, name, slug
country = site['country']  # organization's country code, or None
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
- Python `get_site(site_id)` returns site details plus `organization` with its ID, name, and slug, and `country` from the organization's metadata. Missing organization or country data is `None`; unknown sites return HTTP 404.
- Assets include site IDs, asset types, and metadata. Omitting the site filter lists assets globally.
- Metric definitions include canonical field names, types, and descriptions. Units are included in the canonical descriptions where specified.
- Latest metrics return a sample or `null` / `None` when no rows exist.
- History returns up to 1,000 samples per request, newest first, within `[from, to)`. Use `offset` for further pages. Site and asset lists allow 100 rows per page.
- Each sample contains `timestamp`, `quality`, `source`, and a `values` dictionary. Missing values are `null` / `None`.
- Control validates the command against the target asset's schema and supplies its real site, asset, type, and timestamp. Unsupported asset types and empty commands return HTTP 400. Publishing success acknowledges Kafka delivery, not device execution.

All calls use POST JSON under `/api/v1/module`: `sites/list`, `sites/get`, `assets/list`, `assets/get`, `metrics/definitions`, `metrics/latest`, `metrics/history`, and `control`. Send the key as `Authorization: Bearer <key>`. The SDK uses a ten-second timeout and rejects redirects. TypeScript validates response shapes; both clients raise `ModuleApiError` with the HTTP status on API failures.

## Keys and revocation

Only global admins can create, list, or revoke global keys. The platform stores a hash of each secret and shows the full secret only when it is created. Revocation is checked in the database on every API request; already-authorized in-flight requests may finish. Ordinary organization keys and browser sessions do not authorize this global module API.

The platform migration adding `global_api_key` must be applied before using the admin section or API. Key management is available in the global admin view and its session-authenticated RPC procedures, and is not accessible with a global integration key.


## Registering and enabling a module

Create a dedicated global API key in `/admin/api-keys` for each logical module.
Replicas of the same module use the same key and ID. One key can register one ID;
another key cannot claim that ID. Keep the key across restarts. Revocation stops
its HTTP access and causes the SDK to pause at the next status check. Replacing a
bound key requires updating the registry binding through a database maintenance
operation; registering the existing ID with a new key is rejected.

IDs are lowercase slugs of at most 100 characters, such as `forecasting-module`.
Registration is idempotent, updates supplied metadata, and never changes the
admin's enabled setting. New modules start disabled. The SDK checks the initial
state immediately, then sends an authenticated heartbeat every 30 seconds,
including while disabled. Heartbeats update the platform's last contact time.
Each API client supports one registration and must be closed on shutdown.

Admins can list modules and toggle them at `/admin/modules`. The page shows
connectivity separately from the enabled setting; no heartbeat for 90 seconds
shows the module as offline. The timestamp reflects the most recent contact
from any replica, rather than individual replica health.

### TypeScript lifecycle

```typescript
import { createModuleApi } from "@flexbit/sdk/module";

const platform = createModuleApi();
let timer: ReturnType<typeof setInterval> | undefined;
const module = await platform.registerModule({
  id: "forecasting-module",
  name: "Forecasting",
  description: "Computes site forecasts",
  version: "1.0.0",
  onEnable: ({ signal }) => {
    // Launch background work and return promptly. Pass signal to cancellable I/O.
    timer = setInterval(() => {
      if (!signal.aborted) console.log("Run forecasting work");
    }, 5_000);
  },
  onDisable: async () => {
    clearInterval(timer);
    timer = undefined;
    // Also cancel and await any in-flight forecasting tasks here.
  },
  onError: (error) => console.error("Module lifecycle:", error),
});

process.once("SIGTERM", () => { void module.close(); });
process.once("SIGINT", () => { void module.close(); });
```

### Python lifecycle

```python
import threading
from flexbit import create_module_api

platform = create_module_api()
worker = None

def forecast(cancel):
    while not cancel.wait(5):
        print("Run forecasting work")
        # Pass cancellation into your jobs and check it before publishing results.

def start(cancel):
    global worker
    worker = threading.Thread(target=forecast, args=(cancel,))
    worker.start()

def stop():
    global worker
    if worker is not None:
        worker.join()  # The SDK has already set the cancellation Event.
        worker = None

with platform.register_module(
    "forecasting-module",
    name="Forecasting",
    version="1.0.0",
    on_enable=start,
    on_disable=stop,
    on_error=lambda error: print("Module lifecycle:", error),
) as module:
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
```

`onEnable` / `on_enable` runs on the initial enabled state and each transition to
enabled. It must launch background work and return promptly. It must not await
an entire long-running job. Python callbacks are synchronous and run on the
registering thread initially, then on the SDK monitoring thread; use appropriate
synchronization when sharing state with your application.

Disabling aborts the TypeScript signal or sets the Python cancellation Event
before invoking the stop callback. The stop callback must await or join active
work before returning. The SDK serializes lifecycle callbacks, avoids overlapping
heartbeat requests, and does not start another job until cleanup succeeds.
A failed status check, malformed response, or callback error pauses work and
reports the error. Subsequent successful enabled checks resume it. Failed cleanup
is retried at later checks. Shutdown stops polling, cancels active work, waits for
an in-flight check, and runs cleanup. Cleanup errors during shutdown propagate.

For registered keys, the platform checks the enabled setting on every HTTP
`control` request, even if a client omits its module ID. Disabled modules receive
HTTP 403. Controls already authorized before a toggle may finish. The SDK also
blocks control calls through the registered API client while paused or closed.
Existing keys that have never registered a module retain their previous behavior.
Data queries remain available while disabled for inspection.

Kafka connector calls use separate Kafka credentials and rely on cooperative
cancellation in your application. The HTTP toggle does not revoke Kafka access.
Guard Kafka processing and publishing with the cancellation signal/Event or the
registration handle's `enabled` property. Use `connector.platform.registerModule`
or `connector.platform.register_module` to register existing module connectors.

Apply the platform's `0003_module_registry` migration before using registration
or the admin page. Deploy the platform changes before using the new SDK methods.
