import threading
import unittest
from unittest.mock import Mock, patch
from flexbit import create_module_api
from flexbit.module_lifecycle import RegisteredModule


class ModuleLifecycleTests(unittest.TestCase):
    def register(self, enabled=False):
        api = create_module_api()
        request = Mock(return_value={"id": "forecasting-module", "enabled": enabled})
        api._request = request
        events = []
        cancellation = []

        def start(cancel):
            events.append("start")
            cancellation.append(cancel)

        def stop():
            self.assertTrue(cancellation[-1].is_set())
            events.append("stop")

        module = api.register_module(
            "forecasting-module",
            name="Forecasting",
            on_enable=start,
            on_disable=stop,
            on_error=lambda error: events.append(str(error)),
        )
        self.addCleanup(module.close)
        return api, module, request, events

    def test_registration_transitions_and_shutdown(self):
        api, module, request, events = self.register()
        request.assert_called_once_with(
            "register", {"id": "forecasting-module", "name": "Forecasting"}
        )
        self.assertFalse(module.enabled)
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            api.control("asset", {})
        request.return_value["enabled"] = True
        module._check()
        module._check()
        self.assertEqual(events, ["start"])
        request.assert_called_with("heartbeat", {"id": "forecasting-module"})
        request.return_value["enabled"] = False
        module._check()
        self.assertEqual(events, ["start", "stop"])
        request.return_value["enabled"] = True
        module._check()
        module.close()
        module.close()
        self.assertEqual(events, ["start", "stop", "start", "stop"])
        self.assertFalse(module._thread.is_alive())
        calls = request.call_count
        module._check()
        self.assertEqual(request.call_count, calls)

    def test_failure_pauses_and_recovery_resumes(self):
        api, module, request, events = self.register(True)
        request.side_effect = OSError("offline")
        module._check()
        self.assertFalse(module.enabled)
        self.assertEqual(events, ["start", "stop", "offline"])
        with self.assertRaises(RuntimeError):
            api.control("asset", {})
        request.side_effect = None
        module._check()
        self.assertTrue(module.enabled)
        self.assertEqual(events[-1], "start")

    def test_malformed_status_pauses(self):
        _, module, request, events = self.register(True)
        for response in [
            {"id": "other", "enabled": True},
            {"id": module.id, "enabled": "false"},
        ]:
            request.return_value = response
            module._check()
            self.assertFalse(module.enabled)
            self.assertIn("Invalid module status response", events)

    def test_validates_id_and_prevents_multiple_watchers(self):
        api, _, request, _ = self.register()
        with self.assertRaisesRegex(ValueError, "already registered"):
            api.register_module("other-module", on_enable=Mock(), on_disable=Mock())
        for module_id in ["", "Uppercase", "two--hyphens", "a" * 101]:
            with self.assertRaises(ValueError):
                create_module_api().register_module(
                    module_id, on_enable=Mock(), on_disable=Mock()
                )
        self.assertEqual(request.call_count, 1)

    def test_poll_interval_is_30_seconds(self):
        module = RegisteredModule(
            "forecasting-module", Mock(return_value=False), Mock(), Mock(), Mock()
        )
        module._closed = Mock()
        module._closed.wait.side_effect = [False, True]
        module._closed.is_set.return_value = False
        with patch("flexbit.module_lifecycle.time.monotonic", return_value=0):
            module._run()
        self.assertEqual(module._closed.wait.call_args_list[0].args, (30,))
        module._heartbeat.assert_called_once()

    def test_close_during_heartbeat_does_not_start_work(self):
        api, module, request, events = self.register()
        entered, release = threading.Event(), threading.Event()

        def heartbeat(*args):
            entered.set()
            release.wait(2)
            return {"id": module.id, "enabled": True}

        request.side_effect = heartbeat
        checking = threading.Thread(target=module._check)
        checking.start()
        self.assertTrue(entered.wait(1))
        closing = threading.Thread(target=module.close)
        closing.start()
        self.assertTrue(module._closed.wait(1))
        release.set()
        checking.join(2)
        closing.join(2)
        self.assertFalse(checking.is_alive())
        self.assertFalse(closing.is_alive())
        self.assertEqual(events, [])

    def test_callback_failure_stops_and_retries_cleanup(self):
        heartbeat = Mock(return_value=True)
        start = Mock(side_effect=RuntimeError("start failed"))
        stop = Mock(side_effect=RuntimeError("stop failed"))
        errors = Mock()
        module = RegisteredModule("forecasting-module", heartbeat, start, stop, errors)
        module._check()
        self.assertFalse(module.enabled)
        module._check()
        self.assertEqual(start.call_count, 1)
        stop.side_effect = None
        start.side_effect = None
        module._check()
        self.assertTrue(module.enabled)
        self.assertEqual(start.call_count, 2)
        module.close()
