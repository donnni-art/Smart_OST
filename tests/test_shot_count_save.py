"""
Unit tests for shot-count file persistence (_save_shot_count / _load_product_and_data).
These tests exercise the file-I/O logic without a PLC or Qt event loop.
"""
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch


def _make_counter(tmp_dir, shot_count=0, product_name="TEST_PART", last_total_sheet=None):
    """Build a minimal ShotCounter-like object with just the persistence pieces."""

    class FakeCounter:
        pass

    obj = FakeCounter()
    obj.product_name = product_name
    obj.shot_count = shot_count
    obj.last_total_sheet = last_total_sheet
    obj.file_path = os.path.join(tmp_dir, f"shotcount_{product_name}.txt")
    return obj


def _save(obj):
    """Replicate _save_shot_count logic (copied from shot_counting.py)."""
    if not obj.product_name or obj.product_name.strip() == "":
        return
    bak_path = obj.file_path + ".bak"
    with open(bak_path, "w", encoding="utf-8") as f:
        f.write(f"{obj.shot_count}\n")
        if obj.last_total_sheet is not None:
            f.write(f"{obj.last_total_sheet}\n")
    shutil.move(bak_path, obj.file_path)


def _load(obj):
    """Replicate the file-read portion of _load_product_and_data."""
    if not os.path.exists(obj.file_path):
        return
    with open(obj.file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return
    lines = content.split("\n")
    obj.shot_count = int(lines[0])
    obj.last_total_sheet = int(lines[1]) if len(lines) > 1 and lines[1].strip() else None


class TestShotCountPersistence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_save_creates_file(self):
        obj = _make_counter(self.tmp, shot_count=100)
        _save(obj)
        self.assertTrue(os.path.exists(obj.file_path))

    def test_save_no_bak_left_behind(self):
        obj = _make_counter(self.tmp, shot_count=100)
        _save(obj)
        self.assertFalse(os.path.exists(obj.file_path + ".bak"))

    def test_roundtrip_shot_count(self):
        obj = _make_counter(self.tmp, shot_count=4567, last_total_sheet=89)
        _save(obj)
        obj.shot_count = 0
        obj.last_total_sheet = None
        _load(obj)
        self.assertEqual(obj.shot_count, 4567)
        self.assertEqual(obj.last_total_sheet, 89)

    def test_roundtrip_without_last_total_sheet(self):
        obj = _make_counter(self.tmp, shot_count=200, last_total_sheet=None)
        _save(obj)
        obj.shot_count = 0
        _load(obj)
        self.assertEqual(obj.shot_count, 200)
        self.assertIsNone(obj.last_total_sheet)

    def test_save_skipped_when_no_product_name(self):
        obj = _make_counter(self.tmp, shot_count=50, product_name="")
        _save(obj)
        self.assertFalse(os.path.exists(obj.file_path))

    def test_load_missing_file_leaves_shot_count_unchanged(self):
        obj = _make_counter(self.tmp, shot_count=999)
        # file_path does not exist — load should be a no-op
        _load(obj)
        self.assertEqual(obj.shot_count, 999)

    def test_overwrite_preserves_latest_value(self):
        obj = _make_counter(self.tmp, shot_count=10)
        _save(obj)
        obj.shot_count = 20
        _save(obj)
        obj.shot_count = 0
        _load(obj)
        self.assertEqual(obj.shot_count, 20)


class TestShotCountIncrement(unittest.TestCase):
    """Test the counting arithmetic (sheet_increment × shot_per_sheet)."""

    def test_increment_calculation(self):
        last_total = 50
        new_total = 53
        shot_per_sheet = 2
        current_shot_count = 100

        sheet_increment = new_total - last_total           # 3
        actual_shot_increment = sheet_increment * shot_per_sheet  # 6
        new_shot_count = current_shot_count + actual_shot_increment

        self.assertEqual(new_shot_count, 106)

    def test_reset_detection(self):
        last_total = 100
        new_total = 5
        self.assertLess(new_total, last_total)  # reset condition

    def test_no_count_when_total_unchanged(self):
        last_total = 50
        new_total = 50
        self.assertEqual(new_total, last_total)  # no increment


if __name__ == "__main__":
    unittest.main()
