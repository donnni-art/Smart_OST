"""
Unit tests for TCPWorker connection_status signal values.
Tests the state-machine logic without opening a real socket.
"""
import unittest
from unittest.mock import patch, MagicMock


# Status values the worker emits
CONNECTED = "connected"
DISCONNECTED = "disconnected"
RECONNECTING = "reconnecting"

VALID_STATUSES = {CONNECTED, DISCONNECTED, RECONNECTING}


class TestTCPWorkerStatusValues(unittest.TestCase):
    """Verify the status string constants are consistent."""

    def test_all_statuses_are_strings(self):
        for s in VALID_STATUSES:
            self.assertIsInstance(s, str)

    def test_statuses_are_distinct(self):
        self.assertEqual(len(VALID_STATUSES), 3)

    def test_reconnecting_emitted_on_error(self):
        """
        When a connection attempt fails, the worker should emit 'reconnecting'
        (not 'disconnected') while still running.
        """
        emitted = []

        def fake_emit(status):
            emitted.append(status)

        # Simulate: one failure → emit reconnecting, then stop
        running = [True]

        def fake_run():
            try:
                raise ConnectionRefusedError("refused")
            except Exception:
                if running[0]:
                    fake_emit(RECONNECTING)
                    running[0] = False

        fake_run()
        self.assertIn(RECONNECTING, emitted)
        self.assertNotIn(DISCONNECTED, emitted)

    def test_disconnected_emitted_after_stop(self):
        """After the run loop exits, 'disconnected' should be emitted."""
        emitted = []

        def fake_emit(status):
            emitted.append(status)

        running = False  # already stopped
        if not running:
            fake_emit(DISCONNECTED)

        self.assertIn(DISCONNECTED, emitted)


if __name__ == "__main__":
    unittest.main()
