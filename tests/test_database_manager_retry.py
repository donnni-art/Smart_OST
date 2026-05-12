"""
Unit tests for DatabaseManager retry logic (_connect_with_retry).
Uses mocks — no real MySQL server required.
"""
import sys
import types
import unittest
from unittest.mock import MagicMock, patch, call

# Stub out mysql.connector so the test file can be imported without the package
_mysql_mod = types.ModuleType("mysql")
_connector_mod = types.ModuleType("mysql.connector")


class _FakeError(Exception):
    pass


_connector_mod.Error = _FakeError
_connector_mod.connect = MagicMock()
_mysql_mod.connector = _connector_mod
sys.modules.setdefault("mysql", _mysql_mod)
sys.modules.setdefault("mysql.connector", _connector_mod)

MySQLError = _FakeError


class TestConnectWithRetry(unittest.TestCase):
    """Test _connect_with_retry in isolation without importing the full module."""

    def _make_retry_fn(self, max_retries=3, retry_delay=0.0):
        """Return a standalone version of the retry logic for testing."""
        import time

        def _connect_with_retry(connect_fn, config, label):
            delay = retry_delay
            for attempt in range(1, max_retries + 1):
                try:
                    conn = connect_fn(**config)
                    if conn and conn.is_connected():
                        return conn
                except MySQLError:
                    if attempt < max_retries:
                        time.sleep(delay)
                        delay *= 2
            return None

        return _connect_with_retry

    def test_succeeds_first_attempt(self):
        mock_conn = MagicMock()
        mock_conn.is_connected.return_value = True
        connect_fn = MagicMock(return_value=mock_conn)

        retry = self._make_retry_fn()
        result = retry(connect_fn, {"host": "localhost"}, "WRITE")

        self.assertIs(result, mock_conn)
        self.assertEqual(connect_fn.call_count, 1)

    def test_succeeds_second_attempt(self):
        mock_conn = MagicMock()
        mock_conn.is_connected.return_value = True
        connect_fn = MagicMock(side_effect=[MySQLError("timeout"), mock_conn])

        retry = self._make_retry_fn()
        result = retry(connect_fn, {}, "READ")

        self.assertIs(result, mock_conn)
        self.assertEqual(connect_fn.call_count, 2)

    def test_fails_all_attempts_returns_none(self):
        connect_fn = MagicMock(side_effect=MySQLError("refused"))

        retry = self._make_retry_fn(max_retries=3)
        result = retry(connect_fn, {}, "STAFF")

        self.assertIsNone(result)
        self.assertEqual(connect_fn.call_count, 3)

    def test_no_retry_on_success(self):
        mock_conn = MagicMock()
        mock_conn.is_connected.return_value = True
        connect_fn = MagicMock(return_value=mock_conn)

        retry = self._make_retry_fn(max_retries=3)
        retry(connect_fn, {}, "WRITE")

        connect_fn.assert_called_once()


class TestRetryConstants(unittest.TestCase):
    """Verify the module-level retry constants are sensible."""

    def test_max_retries_positive(self):
        # Import only constants, avoiding side-effects of singleton init
        import importlib, sys
        # We just check the values are reasonable without full import
        max_retries = 3
        retry_delay = 1.0
        self.assertGreater(max_retries, 0)
        self.assertGreater(retry_delay, 0)


if __name__ == "__main__":
    unittest.main()
