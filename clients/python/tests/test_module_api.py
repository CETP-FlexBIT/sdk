import io
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from flexbit import create_module_api, create_module_connector, ModuleApiError


class ModuleApiTests(unittest.TestCase):
    def test_module_get_site_returns_organization_and_country(self):
        site = {
            "id": "site-b",
            "organizationId": "organization-b",
            "name": "Site B",
            "type": "physical",
            "description": "Demonstrator",
            "metadata": None,
            "offlineThreshold": 5,
            "organization": {
                "id": "organization-b",
                "name": "Organization B",
                "slug": "org-b",
            },
            "country": "IT",
        }
        with (
            patch.dict(
                os.environ,
                {
                    "FLEXBIT_PLATFORM_URL": "https://platform.example.com",
                    "FLEXBIT_API_KEY": "flexbit_global_test",
                },
            ),
            patch("flexbit.module_api.build_opener") as opener,
        ):
            opener.return_value.open.return_value = io.BytesIO(json.dumps(site).encode())
            module = create_module_connector(
                {
                    "site_id": "site-a",
                    "client_id": "test-module",
                    "api": {"id": "test-id", "secret": "test-secret"},
                }
            )
            self.assertEqual(module.platform.get_site("site-b"), site)
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(
                request.full_url,
                "https://platform.example.com/api/v1/module/sites/get",
            )
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(json.loads(request.data), {"siteId": "site-b"})
            self.assertEqual(
                request.get_header("Authorization"), "Bearer flexbit_global_test"
            )

    def test_get_site_reports_unknown_site(self):
        with (
            patch.dict(
                os.environ,
                {
                    "FLEXBIT_PLATFORM_URL": "https://platform.example.com",
                    "FLEXBIT_API_KEY": "flexbit_global_test",
                },
            ),
            patch("flexbit.module_api.build_opener") as opener,
        ):
            opener.return_value.open.side_effect = HTTPError(
                "url", 404, "Not Found", {}, None
            )
            with self.assertRaises(ModuleApiError) as error:
                create_module_api().get_site("unknown-site")
            self.assertEqual(error.exception.status, 404)

    def test_history_uses_injected_url_key_and_pagination(self):
        with (
            patch.dict(
                os.environ,
                {
                    "FLEXBIT_PLATFORM_URL": "https://platform.example.com",
                    "FLEXBIT_API_KEY": "flexbit_global_test",
                },
            ),
            patch("flexbit.module_api.build_opener") as opener,
        ):
            opener.return_value.open.return_value = io.BytesIO(json.dumps([]).encode())
            self.assertEqual(
                create_module_api().metrics_history(
                    "asset",
                    start="2026-10-07T00:00:00Z",
                    end="2026-10-08T00:00:00Z",
                    offset=20,
                    limit=10,
                ),
                [],
            )
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(
                request.full_url,
                "https://platform.example.com/api/v1/module/metrics/history",
            )
            self.assertEqual(
                request.get_header("Authorization"), "Bearer flexbit_global_test"
            )
            self.assertEqual(json.loads(request.data)["offset"], 20)
            self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 10)

    def test_revoked_key_error_includes_status(self):
        with (
            patch.dict(
                os.environ,
                {
                    "FLEXBIT_PLATFORM_URL": "https://platform.example.com",
                    "FLEXBIT_API_KEY": "flexbit_global_test",
                },
            ),
            patch("flexbit.module_api.build_opener") as opener,
        ):
            opener.return_value.open.side_effect = HTTPError(
                "url", 401, "Unauthorized", {}, None
            )
            with self.assertRaises(ModuleApiError) as error:
                create_module_api().get_asset("asset")
            self.assertEqual(error.exception.status, 401)

    def test_missing_configuration_is_reported_at_request_time(self):
        with patch.dict(os.environ, {}, clear=True):
            api = create_module_api()
            with self.assertRaisesRegex(ValueError, "FLEXBIT_PLATFORM_URL"):
                api.list_sites()

    def test_control_feedback(self):
        with (
            patch.dict(
                os.environ,
                {
                    "FLEXBIT_PLATFORM_URL": "https://platform.example.com",
                    "FLEXBIT_API_KEY": "flexbit_global_test",
                },
            ),
            patch("flexbit.module_api.build_opener") as opener,
        ):
            opener.return_value.open.return_value = io.BytesIO(b'{"success":true}')
            self.assertEqual(
                create_module_api().control("asset", {"bess_inv_set_power_active": 15}),
                {"success": True},
            )
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(
                json.loads(request.data),
                {"assetId": "asset", "values": {"bess_inv_set_power_active": 15}},
            )


if __name__ == "__main__":
    unittest.main()
