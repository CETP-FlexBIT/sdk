import { z } from "zod";

const metadata = z.record(z.string(), z.unknown()).nullable();
const siteSchema = z.object({
  id: z.uuid(),
  organizationId: z.string(),
  name: z.string(),
  type: z.string(),
  description: z.string(),
  metadata,
  offlineThreshold: z.number(),
});
const assetSchema = z.object({
  id: z.uuid(),
  siteId: z.uuid(),
  name: z.string(),
  type: z.string(),
  metadata,
});
const sampleSchema = z.object({
  timestamp: z.iso.datetime(),
  quality: z.string().nullable(),
  source: z.string().nullable(),
  values: z.record(z.string(), z.union([z.number(), z.string(), z.boolean(), z.null()])),
});
const definitionSchema = z.object({
  name: z.string(),
  description: z.string(),
  type: z.union([z.string(), z.array(z.string())]),
});
export type ModuleSite = z.infer<typeof siteSchema>;
export type ModuleAsset = z.infer<typeof assetSchema>;
export type MetricSample = z.infer<typeof sampleSchema>;
export type MetricDefinition = z.infer<typeof definitionSchema>;
export type MetricHistoryInput = {
  assetId: string;
  from: string;
  to: string;
  limit?: number;
  offset?: number;
};
type Page = { limit?: number; offset?: number };

export class ModuleApiError extends Error {
  constructor(readonly status: number) {
    super(`FlexBIT module API returned HTTP ${status}`);
  }
}

/** Uses the same global admin key inside Kubernetes and in external clients. */
export function createModuleApi() {
  async function request<T>(path: string, input: unknown, schema: z.ZodType<T>): Promise<T> {
    const url = process.env.FLEXBIT_PLATFORM_URL;
    const key = process.env.FLEXBIT_API_KEY;
    if (!url || !key) throw new Error("Set FLEXBIT_PLATFORM_URL and FLEXBIT_API_KEY");
    const response = await fetch(new URL(`/api/v1/module/${path}`, url), {
      method: "POST",
      headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
      body: JSON.stringify(input),
      redirect: "error",
      signal: AbortSignal.timeout(10_000),
    });
    if (!response.ok) throw new ModuleApiError(response.status);
    const body: unknown = await response.json();
    return schema.parse(body);
  }
  return {
    sites: { list: (page: Page = {}) => request("sites/list", page, z.array(siteSchema)) },
    assets: {
      list: (input: Page & { siteId?: string } = {}) =>
        request("assets/list", input, z.array(assetSchema)),
      get: (assetId: string) => request("assets/get", { assetId }, assetSchema),
    },
    metrics: {
      definitions: (assetId: string) =>
        request("metrics/definitions", { assetId }, z.array(definitionSchema)),
      latest: (assetId: string) => request("metrics/latest", { assetId }, sampleSchema.nullable()),
      history: (input: MetricHistoryInput) =>
        request("metrics/history", input, z.array(sampleSchema)),
    },
    control: (assetId: string, values: Record<string, unknown>) =>
      request("control", { assetId, values }, z.object({ success: z.literal(true) })),
  };
}
export type ModuleApi = ReturnType<typeof createModuleApi>;
