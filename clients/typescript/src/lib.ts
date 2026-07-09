import { Consumer, Producer, stringSerializers } from "@platformatic/kafka";
import type {
  Control,
  ControlByType,
  ControlMessage,
  ControlMeta,
  Ingestion,
  IngestionByType,
  IngestionMessage,
  IngestionMeta,
  Type,
} from "./interfaces/export.js";

type ConnectorType = "ingestion" | "control";

type MessageByConnectorType = {
  ingestion: IngestionMessage;
  control: ControlMessage;
};
type MessageCallback<TMessage> = (message: TMessage) => void | Promise<void>;

export type CreateConnectorOptions = {
  siteId: string;
  clientId: string;
  host?: string;
  api: {
    id: string;
    secret: string;
  };
};

const parseMessageValue = <TMessage>(value: unknown): TMessage => {
  if (typeof value === "string") {
    return JSON.parse(value) as TMessage;
  }
  if (value instanceof Uint8Array) {
    return JSON.parse(new TextDecoder().decode(value)) as TMessage;
  }
  return value as TMessage;
};

const hostName = (host: string) => host.replace(/:\d+$/, "");

export const createConnector = ({
  siteId,
  clientId,
  api,
  host = "127.0.0.1:9092",
}: CreateConnectorOptions) => {
  const options = {
    clientId,
    groupId: clientId,
    bootstrapBrokers: [host],
    autocreateTopics: true,
    tls: {
      rejectUnauthorized: false,
    },
    tlsServerName: hostName(host),
    sasl: {
      mechanism: "SCRAM-SHA-256" as const,
      username: api.id,
      password: api.secret,
    },
  };

  const producerId = `flexbit-sdk:${clientId}:producer`;
  const consumerId = `flexbit-sdk:${clientId}:consumer`;

  const consumer = new Consumer({
    ...options,
    clientId: consumerId,
    groupId: consumerId,
  });

  const producer = new Producer({
    ...options,
    clientId: producerId,
    serializers: stringSerializers,
  });

  const send = <Meta extends IngestionMeta | ControlMeta, T>(
    key: "ingestion" | "control",
    siteId: string,
    assetId: string,
    type: Type,
    content: T,
    meta?: Meta,
  ) => {
    const message = {
      ...content,
      ...meta,
      type,
      meta_site_id: siteId,
      meta_asset_id: assetId,
      meta_timestamp: meta?.meta_timestamp ?? new Date().toISOString(),
    };
    return producer.send({
      messages: [
        {
          topic: `${key}.${siteId}`,
          value: JSON.stringify(message),
        },
      ],
    });
  };

  const subscribe = async <TConnectorType extends ConnectorType>(
    type: TConnectorType,
    callback: MessageCallback<MessageByConnectorType[TConnectorType]>,
  ) => {
    const stream = await consumer.consume({
      autocommit: true,
      topics: [`${type}.${siteId}`],
      sessionTimeout: 10000,
      heartbeatInterval: 500,
    });
    for await (const message of stream) {
      await callback(parseMessageValue<MessageByConnectorType[TConnectorType]>(message.value));
    }
  };

  return {
    ingest: <TType extends Type>(
      type: TType,
      assetId: string,
      content: IngestionByType[TType],
      meta?: IngestionMeta,
    ) => send<IngestionMeta, Ingestion>("ingestion", siteId, assetId, type, content, meta),
    control: <TType extends Type>(
      type: TType,
      assetId: string,
      content: ControlByType[TType],
      meta?: ControlMeta,
    ) => send<ControlMeta, Control>("control", siteId, assetId, type, content, meta),
    subscribeIngestion: (callback: MessageCallback<IngestionMessage>) =>
      subscribe("ingestion", callback),
    subscribeControl: (callback: MessageCallback<ControlMessage>) => subscribe("control", callback),
  };
};

export type Connector = ReturnType<typeof createConnector>;
