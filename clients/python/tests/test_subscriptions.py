import json
import re
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from flexbit import create_device_connector, create_module_connector


class SubscriptionTests(unittest.TestCase):
    def setUp(self):
        self.options = {
            "site_id": "site-a",
            "client_id": "test-client",
            "api": {"id": "test-id", "secret": "test-secret"},
        }

    def test_module_subscribes_to_ingestion_from_multiple_sites(self):
        payloads = [
            {"type": "bess", "meta_site_id": "site-a"},
            {"type": "pv", "meta_site_id": "site-b"},
        ]
        callback = Mock()
        with patch("flexbit.lib._kafka_consumer_class") as consumer_class:
            consumer = consumer_class.return_value.return_value
            consumer.__iter__.return_value = iter(
                SimpleNamespace(value=json.dumps(payload).encode())
                for payload in payloads
            )
            module = create_module_connector(self.options)
            module.subscribe(callback)

            self.assertEqual(consumer_class.return_value.call_args.args, ())
            pattern = consumer.subscribe.call_args.kwargs["pattern"]
            for topic in ("ingestion.site-a", "ingestion.site-b", "ingestion.new-site"):
                self.assertIsNotNone(re.match(pattern, topic))
            for topic in ("control.site-a", "ingestionXsite-a", "other.ingestion.site-a"):
                self.assertIsNone(re.match(pattern, topic))
            self.assertEqual(
                [call.args[0] for call in callback.call_args_list], payloads
            )
            module.close()
            consumer.close.assert_called_once_with()

    def test_device_subscribes_only_to_configured_site_control(self):
        with patch("flexbit.lib._kafka_consumer_class") as consumer_class:
            consumer = consumer_class.return_value.return_value
            consumer.__iter__.return_value = iter(())
            create_device_connector(self.options).subscribe(Mock())

            consumer.subscribe.assert_called_once_with(topics=["control.site-a"])


if __name__ == "__main__":
    unittest.main()
