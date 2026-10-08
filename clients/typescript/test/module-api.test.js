import { test, afterEach, mock } from "node:test";
import assert from "node:assert/strict";
import { createModuleApi, ModuleApiError } from "../dist/module-api.js";

const previous = { url: process.env.FLEXBIT_PLATFORM_URL, key: process.env.FLEXBIT_API_KEY };
afterEach(() => {
  mock.restoreAll();
  for (const [name, value] of [
    ["FLEXBIT_PLATFORM_URL", previous.url],
    ["FLEXBIT_API_KEY", previous.key],
  ]) {
    if (value === undefined) delete process.env[name];
    else process.env[name] = value;
  }
});
const configure = () => {
  process.env.FLEXBIT_PLATFORM_URL = "https://platform.example.com";
  process.env.FLEXBIT_API_KEY = "flexbit_global_test";
};
const assetId = "22222222-2222-4222-8222-222222222222";
test("sends global-key authenticated queries to the platform", async () => {
  configure();
  const transport = mock.method(globalThis, "fetch", async (url, options) => {
    assert.equal(url.href, "https://platform.example.com/api/v1/module/metrics/history");
    assert.equal(options.headers.authorization, "Bearer flexbit_global_test");
    assert.equal(options.redirect, "error");
    assert.deepEqual(JSON.parse(options.body), {
      assetId,
      from: "2026-10-07T00:00:00Z",
      to: "2026-10-08T00:00:00Z",
      limit: 10,
      offset: 20,
    });
    return Response.json([
      {
        timestamp: "2026-10-07T10:00:00Z",
        quality: "raw",
        source: null,
        values: { bess_storage_soc: 60 },
      },
    ]);
  });
  const rows = await createModuleApi().metrics.history({
    assetId,
    from: "2026-10-07T00:00:00Z",
    to: "2026-10-08T00:00:00Z",
    limit: 10,
    offset: 20,
  });
  assert.equal(rows[0].values.bess_storage_soc, 60);
  assert.equal(transport.mock.callCount(), 1);
});
test("accepts missing latest metrics and rejects malformed server responses", async () => {
  configure();
  mock.method(globalThis, "fetch", async () => Response.json(null));
  assert.equal(await createModuleApi().metrics.latest(assetId), null);
  mock.restoreAll();
  mock.method(globalThis, "fetch", async () => Response.json({ timestamp: "invalid", values: {} }));
  await assert.rejects(createModuleApi().metrics.latest(assetId));
});
test("surfaces revoked-key HTTP errors with their status", async () => {
  configure();
  mock.method(globalThis, "fetch", async () => new Response("Unauthorized", { status: 401 }));
  await assert.rejects(
    createModuleApi().assets.get(assetId),
    (error) => error instanceof ModuleApiError && error.status === 401,
  );
});
test("requires connection environment variables only when making a query", async () => {
  delete process.env.FLEXBIT_PLATFORM_URL;
  delete process.env.FLEXBIT_API_KEY;
  const api = createModuleApi();
  await assert.rejects(api.sites.list(), /Set FLEXBIT_PLATFORM_URL and FLEXBIT_API_KEY/);
});
test("sends control feedback through the same API", async () => {
  configure();
  mock.method(globalThis, "fetch", async (url, options) => {
    assert.equal(url.pathname, "/api/v1/module/control");
    assert.deepEqual(JSON.parse(options.body), {
      assetId,
      values: { bess_inv_set_power_active: 15 },
    });
    return Response.json({ success: true });
  });
  assert.deepEqual(await createModuleApi().control(assetId, { bess_inv_set_power_active: 15 }), {
    success: true,
  });
});

const flush = async () => {
  for (let i = 0; i < 12; i++) await Promise.resolve();
};
test("registers metadata, polls every 30s, and reacts only to changes", async (t) => {
  configure();
  t.mock.timers.enable({ apis: ["setInterval"] });
  let enabled = false;
  const events = [];
  let signal;
  const transport = mock.method(globalThis, "fetch", async (url, options) => {
    const body = JSON.parse(options.body);
    if (url.pathname.endsWith("/register")) {
      assert.deepEqual(body, { id: "forecasting-module", name: "Forecasting" });
    } else {
      assert.equal(url.pathname, "/api/v1/module/heartbeat");
      assert.deepEqual(body, { id: "forecasting-module" });
    }
    return Response.json({ id: body.id, enabled });
  });
  const api = createModuleApi();
  const module = await api.registerModule({
    id: "forecasting-module",
    name: "Forecasting",
    onEnable: (context) => {
      signal = context.signal;
      events.push("start");
    },
    onDisable: () => {
      assert.equal(signal.aborted, true);
      events.push("stop");
    },
  });
  try {
    assert.equal(module.enabled, false);
    await assert.rejects(api.control(assetId, {}), /disabled/);
    assert.equal(transport.mock.callCount(), 1);
    enabled = true;
    t.mock.timers.tick(29_999);
    await flush();
    assert.deepEqual(events, []);
    t.mock.timers.tick(1);
    await flush();
    assert.deepEqual(events, ["start"]);
    assert.equal(module.enabled, true);
    t.mock.timers.tick(30_000);
    await flush();
    assert.deepEqual(events, ["start"]);
    enabled = false;
    t.mock.timers.tick(30_000);
    await flush();
    assert.deepEqual(events, ["start", "stop"]);
    enabled = true;
    t.mock.timers.tick(30_000);
    await flush();
    assert.deepEqual(events, ["start", "stop", "start"]);
    await assert.rejects(
      api.registerModule({ id: "other", onEnable() {}, onDisable() {} }),
      /already/,
    );
  } finally {
    await module.close();
  }
  assert.deepEqual(events, ["start", "stop", "start", "stop"]);
  await module.close();
  const count = transport.mock.callCount();
  t.mock.timers.tick(90_000);
  await flush();
  assert.equal(transport.mock.callCount(), count);
});

test("pauses on heartbeat errors and resumes after confirmation", async (t) => {
  configure();
  t.mock.timers.enable({ apis: ["setInterval"] });
  let broken = false;
  const events = [];
  mock.method(globalThis, "fetch", async () =>
    broken
      ? new Response("Unauthorized", { status: 401 })
      : Response.json({ id: "forecasting-module", enabled: true }),
  );
  const api = createModuleApi();
  const module = await api.registerModule({
    id: "forecasting-module",
    onEnable: () => {
      events.push("start");
    },
    onDisable: () => {
      events.push("stop");
    },
    onError: (error) => {
      events.push(error.status);
    },
  });
  try {
    broken = true;
    t.mock.timers.tick(30_000);
    await flush();
    assert.equal(module.enabled, false);
    assert.deepEqual(events, ["start", "stop", 401]);
    await assert.rejects(api.control(assetId, {}), /disabled/);
    broken = false;
    t.mock.timers.tick(30_000);
    await flush();
    assert.equal(module.enabled, true);
    assert.deepEqual(events, ["start", "stop", 401, "start"]);
  } finally {
    await module.close();
  }
});

test("does not overlap checks and closing cancels in-flight enablement", async (t) => {
  configure();
  t.mock.timers.enable({ apis: ["setInterval"] });
  let complete;
  let starts = 0;
  const transport = mock.method(globalThis, "fetch", async (url) => {
    if (url.pathname.endsWith("/register"))
      return Response.json({ id: "forecasting-module", enabled: false });
    return new Promise((resolve) => {
      complete = resolve;
    });
  });
  const module = await createModuleApi().registerModule({
    id: "forecasting-module",
    onEnable: () => {
      starts++;
    },
    onDisable() {},
  });
  t.mock.timers.tick(30_000);
  await flush();
  t.mock.timers.tick(60_000);
  await flush();
  assert.equal(transport.mock.callCount(), 2);
  const closing = module.close();
  complete(Response.json({ id: "forecasting-module", enabled: true }));
  await closing;
  assert.equal(starts, 0);
});

test("retries failed cleanup before resuming and reports callback errors", async (t) => {
  configure();
  t.mock.timers.enable({ apis: ["setInterval"] });
  let remoteEnabled = true;
  let cleanupFails = true;
  const events = [];
  mock.method(globalThis, "fetch", async () =>
    Response.json({ id: "forecasting-module", enabled: remoteEnabled }),
  );
  const module = await createModuleApi().registerModule({
    id: "forecasting-module",
    onEnable: () => {
      events.push("start");
    },
    onDisable: () => {
      events.push("stop");
      if (cleanupFails) throw new Error("cleanup");
    },
    onError: () => {
      events.push("error");
    },
  });
  try {
    remoteEnabled = false;
    t.mock.timers.tick(30_000);
    await flush();
    assert.equal(module.enabled, false);
    remoteEnabled = true;
    t.mock.timers.tick(30_000);
    await flush();
    assert.equal(events.filter((e) => e === "start").length, 1);
    cleanupFails = false;
    t.mock.timers.tick(30_000);
    await flush();
    assert.equal(module.enabled, true);
    assert.equal(events.filter((e) => e === "start").length, 2);
  } finally {
    cleanupFails = false;
    await module.close();
  }
});
