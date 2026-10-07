"""Global platform data/control API. Configuration comes from environment variables."""

from __future__ import annotations

import json
import os
from typing import Any, TypedDict
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


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
        return self._request("control", {"assetId": asset_id, "values": values})


def create_module_api() -> ModuleApi:
    return ModuleApi()
