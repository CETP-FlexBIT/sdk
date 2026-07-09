from __future__ import annotations

import asyncio
import dataclasses
import inspect
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from kafka import KafkaConsumer, KafkaProducer

ConnectorType = Literal["ingestion", "control"]
AssetType = Literal[
    "alarm",
    "bess",
    "ev_charger",
    "pv",
    "caes",
    "community",
    "thermal_cold",
    "thermal_heat",
    "energy_demand_consumer",
    "energy_demand_prosumer",
    "hydrogen_local_plant",
    "grid_meter",
]

MessageCallback = Callable[[dict[str, Any]], Any]


class ApiCredentials(TypedDict):
    id: str
    secret: str


@dataclass(kw_only=True)
class CreateConnectorOptions:
    site_id: str
    client_id: str
    api: ApiCredentials
    host: str | None = None


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_option(
    options: CreateConnectorOptions | Mapping[str, Any], *names: str
) -> Any:
    for name in names:
        if isinstance(options, Mapping) and name in options:
            return options[name]
        if not isinstance(options, Mapping) and hasattr(options, name):
            return getattr(options, name)
    return None


def _normalize_options(
    options: CreateConnectorOptions | Mapping[str, Any],
) -> tuple[str, str, str, str, str]:
    site_id = _read_option(options, "site_id", "siteId")
    client_id = _read_option(options, "client_id", "clientId")
    host = _read_option(options, "host") or "127.0.0.1:9092"
    api = _read_option(options, "api") or {}

    api_id = api.get("id") if isinstance(api, Mapping) else getattr(api, "id", None)
    api_secret = (
        api.get("secret") if isinstance(api, Mapping) else getattr(api, "secret", None)
    )

    missing = [
        name
        for name, value in (
            ("site_id", site_id),
            ("client_id", client_id),
            ("api.id", api_id),
            ("api.secret", api_secret),
        )
        if not value
    ]
    if missing:
        raise ValueError(f"Missing required connector option(s): {', '.join(missing)}")

    return site_id, client_id, host, api_id, api_secret


def _to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {str(k): v for k, v in value.items() if v is not None}
    if dataclasses.is_dataclass(value):
        return {
            field.name: getattr(value, field.name)
            for field in dataclasses.fields(value)
            if getattr(value, field.name) is not None
        }
    if hasattr(value, "__dict__"):
        return {str(k): v for k, v in vars(value).items() if v is not None}
    raise TypeError("Message content must be a mapping, dataclass, or object")


def _parse_message_value(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, bytes):
        return json.loads(value.decode("utf-8"))
    if isinstance(value, str):
        return json.loads(value)
    if isinstance(value, bytearray):
        return json.loads(bytes(value).decode("utf-8"))
    if isinstance(value, Mapping):
        return dict(value)
    return value


def _run_callback(callback: MessageCallback, message: dict[str, Any]) -> None:
    result = callback(message)
    if inspect.isawaitable(result):
        asyncio.run(result)


def _kafka_producer_class() -> type["KafkaProducer"]:
    from kafka import KafkaProducer

    return KafkaProducer


def _kafka_consumer_class() -> type["KafkaConsumer"]:
    from kafka import KafkaConsumer

    return KafkaConsumer


class Connector:
    def __init__(self, options: CreateConnectorOptions | Mapping[str, Any]) -> None:
        site_id, client_id, host, api_id, api_secret = _normalize_options(options)
        self.site_id = site_id
        self.client_id = client_id
        self._host = host
        self._api_id = api_id
        self._api_secret = api_secret
        self._producer: KafkaProducer | None = None
        self._consumer: KafkaConsumer | None = None

    def _kafka_config(self, client_id: str) -> dict[str, Any]:
        return {
            "bootstrap_servers": [self._host],
            "client_id": client_id,
            "security_protocol": "SASL_PLAINTEXT",
            "sasl_mechanism": "SCRAM-SHA-256",
            "sasl_plain_username": self._api_id,
            "sasl_plain_password": self._api_secret,
        }

    def _get_producer(self) -> KafkaProducer:
        if self._producer is None:
            producer_id = f"flexbit-sdk:{self.client_id}:producer"
            self._producer = _kafka_producer_class()(**self._kafka_config(producer_id))
        return self._producer

    def _send(
        self,
        key: ConnectorType,
        site_id: str,
        asset_id: str,
        type: str,
        content: Any,
        meta: Any | None = None,
    ) -> Any:
        meta_dict = _to_dict(meta)
        message = {
            **_to_dict(content),
            **meta_dict,
            "type": type,
            "meta_site_id": site_id,
            "meta_asset_id": asset_id,
            "meta_timestamp": meta_dict.get("meta_timestamp") or _utc_timestamp(),
        }
        future = self._get_producer().send(
            f"{key}.{site_id}",
            value=json.dumps(message).encode("utf-8"),
        )
        result = future.get(timeout=30)
        self._get_producer().flush()
        return result

    def _subscribe(self, type: ConnectorType, callback: MessageCallback) -> None:
        consumer_id = f"flexbit-sdk:{self.client_id}:consumer"
        self._consumer = _kafka_consumer_class()(
            f"{type}.{self.site_id}",
            group_id=consumer_id,
            enable_auto_commit=True,
            session_timeout_ms=10000,
            heartbeat_interval_ms=500,
            **self._kafka_config(consumer_id),
        )
        for message in self._consumer:
            _run_callback(callback, _parse_message_value(message.value))

    def ingest(
        self,
        type: str,
        asset_id: str,
        content: Any,
        meta: Any | None = None,
    ) -> Any:
        return self._send("ingestion", self.site_id, asset_id, type, content, meta)

    def control(
        self,
        type: str,
        asset_id: str,
        content: Any,
        meta: Any | None = None,
    ) -> Any:
        return self._send("control", self.site_id, asset_id, type, content, meta)

    def subscribe_ingestion(self, callback: MessageCallback) -> None:
        self._subscribe("ingestion", callback)

    def subscribe_control(self, callback: MessageCallback) -> None:
        self._subscribe("control", callback)

    def close(self) -> None:
        if self._consumer is not None:
            self._consumer.close()
            self._consumer = None
        if self._producer is not None:
            self._producer.close()
            self._producer = None


class DeviceConnector:
    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self.ingest = connector.ingest
        self.subscribe = connector.subscribe_control
        self.close = connector.close


class ModuleConnector:
    def __init__(self, connector: Connector) -> None:
        self._connector = connector
        self.control = connector.control
        self.subscribe = connector.subscribe_ingestion
        self.close = connector.close


def create_connector(options: CreateConnectorOptions | Mapping[str, Any]) -> Connector:
    return Connector(options)


def create_device_connector(
    options: CreateConnectorOptions | Mapping[str, Any],
) -> DeviceConnector:
    return DeviceConnector(create_connector(options))


def create_module_connector(
    options: CreateConnectorOptions | Mapping[str, Any],
) -> ModuleConnector:
    return ModuleConnector(create_connector(options))
