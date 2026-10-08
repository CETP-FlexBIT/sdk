"""Module lifecycle monitoring with cooperative cancellation."""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable


class RegisteredModule:
    def __init__(
        self,
        module_id: str,
        heartbeat: Callable[[], bool],
        on_enable: Callable[[threading.Event], None],
        on_disable: Callable[[], None],
        on_error: Callable[[Exception], None] | None,
    ) -> None:
        self.id = module_id
        self._heartbeat = heartbeat
        self._on_enable = on_enable
        self._on_disable = on_disable
        self._on_error = on_error
        self._enabled = False
        self._closed = threading.Event()
        self._cancel: threading.Event | None = None
        self._lock = threading.RLock()
        self._thread: threading.Thread | None = None

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _report(self, error: Exception) -> None:
        try:
            if self._on_error:
                self._on_error(error)
            else:
                logging.getLogger(__name__).error("Module lifecycle error: %s", error)
        except Exception:
            logging.getLogger(__name__).exception("Module error callback failed")

    def _stop(self) -> None:
        self._enabled = False
        if self._cancel is None:
            return
        self._cancel.set()
        self._on_disable()
        self._cancel = None

    def _apply(self, enabled: bool) -> None:
        if not enabled or self._closed.is_set():
            self._stop()
            return
        if self._enabled:
            return
        self._stop()  # Retry failed cleanup before starting another job.
        if self._closed.is_set():
            return
        self._cancel = threading.Event()
        self._enabled = True
        self._on_enable(self._cancel)

    def _fail(self, error: Exception) -> None:
        try:
            self._stop()
        except Exception as cleanup_error:
            self._report(cleanup_error)
        self._report(error)

    def _start(self, enabled: bool) -> None:
        with self._lock:
            try:
                self._apply(enabled)
            except Exception as error:
                self._fail(error)
        if not self._closed.is_set():
            self._thread = threading.Thread(
                target=self._run, name=f"flexbit-module:{self.id}", daemon=True
            )
            self._thread.start()

    def _check(self) -> None:
        with self._lock:
            if self._closed.is_set():
                return
            try:
                self._apply(self._heartbeat())
            except Exception as error:
                self._fail(error)

    def _run(self) -> None:
        next_check = time.monotonic() + 30
        while not self._closed.wait(max(0, next_check - time.monotonic())):
            self._check()
            next_check += 30
            # Keep the 30-second cadence while skipping missed checks.
            now = time.monotonic()
            if next_check <= now:
                next_check += (int((now - next_check) // 30) + 1) * 30

    def close(self) -> None:
        """Cancel polling and stop work. Cleanup errors propagate to the caller."""
        self._closed.set()
        self._enabled = False
        if self._cancel is not None:
            self._cancel.set()
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join()
        with self._lock:
            self._stop()

    def __enter__(self) -> RegisteredModule:
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()
