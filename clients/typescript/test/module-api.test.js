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
