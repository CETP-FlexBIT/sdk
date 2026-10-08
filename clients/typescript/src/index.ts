import { createModuleApi } from "./module-api.js";
export { createModuleApi, ModuleApiError } from "./module-api.js";
export type {
  ModuleApi,
  ModuleRegistration,
  RegisteredModule,
  ModuleSite,
  ModuleAsset,
  MetricSample,
  MetricDefinition,
  MetricHistoryInput,
} from "./module-api.js";

import { createConnector, type CreateConnectorOptions } from "./lib.js";
export type { ControlMessage, IngestionMessage } from "./interfaces/export.js";

export const createDeviceConnector = (options: CreateConnectorOptions) => {
  const connector = createConnector(options);
  return {
    ingest: connector.ingest,
    subscribe: connector.subscribeControl,
  };
};

export const createModuleConnector = (options: CreateConnectorOptions) => {
  const connector = createConnector(options);
  return {
    control: connector.control,
    platform: createModuleApi(),
    subscribe: connector.subscribeIngestion,
  };
};
