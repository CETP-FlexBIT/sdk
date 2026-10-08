"""Global platform data/control API. Configuration comes from environment variables."""

from __future__ import annotations

import json
import os
import re
import threading
from collections.abc import Callable
from typing import Any, TypedDict
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .module_lifecycle import RegisteredModule


class ModuleOrganization(TypedDict):
    id: str
    name: str
    slug: str


class ModuleSite(TypedDict):
    id: str
    organizationId: str
    name: str
    type: str
    description: str
    metadata: dict[str, Any] | None
    offlineThreshold: int
    organization: ModuleOrganization | None
    country: str | None


class MetricSample(TypedDict):
    timestamp: str
    quality: str | None
    source: str | None
    values: dict[str, float | str | bool | None]


class ModuleApiError(RuntimeError):
    def __init__(self, status: int):
        self.status = status
        super().__init__(f"FlexBIT module API returned HTTP {status}")


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ModuleApi:
    def __init__(self) -> None:
        self._registration: RegisteredModule | None = None
        self._registration_lock = threading.Lock()

    def register_module(
        self,
        module_id: str,
        *,
        on_enable: Callable[[threading.Event], None],
        on_disable: Callable[[], None],
        on_error: Callable[[Exception], None] | None = None,
        name: str | None = None,
        description: str | None = None,
        version: str | None = None,
    ) -> RegisteredModule:
        """Register and check status every 30s. on_enable starts work and returns promptly.

        The cancellation Event passed to on_enable is set on disable or shutdown.
        on_disable must stop and join the background work before returning.
        """
        if (
            not isinstance(module_id, str)
            or len(module_id) > 100
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", module_id)
        ):
            raise ValueError(
                "Module ID must be a lowercase slug of at most 100 characters"
            )
        data: dict[str, Any] = {"id": module_id}
        for field, value, limit in [
            ("name", name, 255),
            ("description", description, 2000),
            ("version", version, 100),
        ]:
            if value is not None:
                if (
                    not isinstance(value, str)
                    or len(value) > limit
                    or (field == "name" and not value.strip())
                ):
                    raise ValueError(f"Invalid module {field}")
                data[field] = value

        def parse_status(status: Any) -> bool:
            if (
                not isinstance(status, dict)
                or status.get("id") != module_id
                or type(status.get("enabled")) is not bool
            ):
                raise ValueError("Invalid module status response")
            return status["enabled"]

        with self._registration_lock:
            if self._registration is not None:
                raise ValueError("This API client already registered a module")
            enabled = parse_status(self._request("register", data))
            module = RegisteredModule(
                module_id,
                lambda: parse_status(self._request("heartbeat", {"id": module_id})),
                on_enable,
                on_disable,
                on_error,
            )
            self._registration = module
        module._start(enabled)
        return module

    def _request(self, path: str, data: dict[str, Any]) -> Any:
        url = os.environ.get("FLEXBIT_PLATFORM_URL")
        key = os.environ.get("FLEXBIT_API_KEY")
        if not url or not key:
            raise ValueError("Set FLEXBIT_PLATFORM_URL and FLEXBIT_API_KEY")
        if urlparse(url).scheme not in ("http", "https"):
            raise ValueError("FLEXBIT_PLATFORM_URL must be an HTTP or HTTPS URL")
        request = Request(
            urljoin(url, f"/api/v1/module/{path}"),
            data=json.dumps(data).encode(),
            method="POST",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with build_opener(_NoRedirect()).open(request, timeout=10) as response:
                return json.load(response)
        except HTTPError as error:
            raise ModuleApiError(error.code) from error

    def list_sites(self, *, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        return self._request("sites/list", {"limit": limit, "offset": offset})

    def get_site(self, site_id: str) -> ModuleSite:
        """Return site details, its organization, and the organization's country code."""
        return self._request("sites/get", {"siteId": site_id})

    def list_assets(
        self, *, site_id: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        data: dict[str, Any] = {"limit": limit, "offset": offset}
        if site_id is not None:
            data["siteId"] = site_id
        return self._request("assets/list", data)

    def get_asset(self, asset_id: str) -> dict[str, Any]:
        return self._request("assets/get", {"assetId": asset_id})

    def metric_definitions(self, asset_id: str) -> list[dict[str, Any]]:
        return self._request("metrics/definitions", {"assetId": asset_id})

    def latest_metrics(self, asset_id: str) -> MetricSample | None:
        return self._request("metrics/latest", {"assetId": asset_id})

    def metrics_history(
        self, asset_id: str, *, start: str, end: str, limit: int = 1000, offset: int = 0
    ) -> list[MetricSample]:
        return self._request(
            "metrics/history",
            {
                "assetId": asset_id,
                "from": start,
                "to": end,
                "limit": limit,
                "offset": offset,
            },
        )

    def control(self, asset_id: str, values: dict[str, Any]) -> dict[str, bool]:
        if self._registration is not None and not self._registration.enabled:
            raise RuntimeError("Module is disabled or its status cannot be confirmed")
        return self._request("control", {"assetId": asset_id, "values": values})


def create_module_api() -> ModuleApi:
    return ModuleApi()
