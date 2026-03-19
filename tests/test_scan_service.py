"""Tests for scan_service."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from storix.services.scan_service import run_scan
from storix.models.enums import Category, RiskLevel
from storix.models.candidate import Candidate
from storix.models.summary import DiskSummary


def make_candidate(name: str, category: Category, risk: RiskLevel, size: int, path: Path) -> Candidate:
    return Candidate(
        path=path,
        name=name,
        category=category,
        risk=risk,
        size_bytes=size,
        reason="test",
    )


@patch("storix.scanners.disk_scanner.scan_disk")
@patch("storix.scanners.xcode_scanner.scan_xcode")
@patch("storix.scanners.android_scanner.scan_android")
@patch("storix.scanners.flutter_scanner.scan_flutter")
@patch("storix.scanners.node_scanner.scan_node")
@patch("storix.scanners.python_scanner.scan_python")
@patch("storix.scanners.vscode_scanner.scan_vscode")
@patch("storix.scanners.general_scanner.scan_general")
def test_run_scan_all_categories(
    mock_general, mock_vscode, mock_python, mock_node,
    mock_flutter, mock_android, mock_xcode, mock_disk,
    tmp_path,
):
    mock_disk.return_value = DiskSummary(
        total_bytes=500 * 1024**3,
        used_bytes=250 * 1024**3,
        free_bytes=250 * 1024**3,
    )

    xcode_candidate = make_candidate(
        "Xcode DerivedData", Category.XCODE, RiskLevel.SAFE, 5 * 1024**3, tmp_path / "DerivedData"
    )
    mock_xcode.return_value = [xcode_candidate]
    mock_android.return_value = []
    mock_flutter.return_value = []
    mock_node.return_value = []
    mock_python.return_value = []
    mock_vscode.return_value = []
    mock_general.return_value = []

    summary = run_scan()

    assert summary.disk.total_bytes == 500 * 1024**3
    assert len(summary.categories) == 1
    assert summary.categories[0].category == Category.XCODE
    assert summary.categories[0].candidates[0].name == "Xcode DerivedData"


@patch("storix.scanners.disk_scanner.scan_disk")
@patch("storix.scanners.xcode_scanner.scan_xcode")
def test_run_scan_single_category(mock_xcode, mock_disk, tmp_path):
    mock_disk.return_value = DiskSummary(
        total_bytes=500 * 1024**3,
        used_bytes=200 * 1024**3,
        free_bytes=300 * 1024**3,
    )
    c = make_candidate("DerivedData", Category.XCODE, RiskLevel.SAFE, 2 * 1024**3, tmp_path / "dd")
    mock_xcode.return_value = [c]

    summary = run_scan(categories=[Category.XCODE])

    mock_xcode.assert_called_once()
    assert len(summary.categories) == 1


@patch("storix.scanners.disk_scanner.scan_disk")
@patch("storix.scanners.xcode_scanner.scan_xcode")
def test_run_scan_scanner_exception_returns_partial(mock_xcode, mock_disk, tmp_path):
    """Scanner exceptions should not crash the whole scan."""
    mock_disk.return_value = DiskSummary(
        total_bytes=500 * 1024**3,
        used_bytes=200 * 1024**3,
        free_bytes=300 * 1024**3,
    )
    mock_xcode.side_effect = RuntimeError("scanner crashed")

    # Should not raise
    summary = run_scan(categories=[Category.XCODE])
    assert summary.categories == []
