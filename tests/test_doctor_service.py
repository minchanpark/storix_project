"""Tests for doctor_service."""

import pytest
from unittest.mock import patch
from pathlib import Path

from storix.models.enums import Category, RiskLevel
from storix.models.candidate import Candidate
from storix.models.summary import DiskSummary, CategorySummary, ScanSummary


def make_summary(candidates_by_category: dict) -> ScanSummary:
    disk = DiskSummary(total_bytes=500 * 1024**3, used_bytes=300 * 1024**3, free_bytes=200 * 1024**3)
    categories = []
    for cat, cands in candidates_by_category.items():
        categories.append(CategorySummary(category=cat, candidates=cands))
    return ScanSummary(disk=disk, categories=categories)


def make_candidate(name: str, category: Category, risk: RiskLevel, size: int, path: Path) -> Candidate:
    return Candidate(path=path, name=name, category=category, risk=risk, size_bytes=size, reason="test")


@patch("storix.services.doctor_service.run_scan")
def test_doctor_sorts_by_size(mock_scan, tmp_path):
    from storix.services.doctor_service import run_doctor

    small = make_candidate("small", Category.XCODE, RiskLevel.SAFE, 100 * 1024**2, tmp_path / "s")
    large = make_candidate("large", Category.XCODE, RiskLevel.SAFE, 10 * 1024**3, tmp_path / "l")

    mock_scan.return_value = make_summary({
        Category.XCODE: [small, large],
    })

    result = run_doctor()

    xcode = result.get_category(Category.XCODE)
    assert xcode is not None
    assert xcode.candidates[0].name == "large"


@patch("storix.services.doctor_service.run_scan")
def test_doctor_categories_sorted_by_total(mock_scan, tmp_path):
    from storix.services.doctor_service import run_doctor

    small_xcode = make_candidate("xs", Category.XCODE, RiskLevel.SAFE, 100 * 1024**2, tmp_path / "xs")
    large_android = make_candidate("al", Category.ANDROID, RiskLevel.CAUTION, 5 * 1024**3, tmp_path / "al")

    mock_scan.return_value = make_summary({
        Category.XCODE: [small_xcode],
        Category.ANDROID: [large_android],
    })

    result = run_doctor()

    assert result.categories[0].category == Category.ANDROID


@patch("storix.services.doctor_service.run_scan")
def test_doctor_empty_returns_empty_categories(mock_scan):
    from storix.services.doctor_service import run_doctor

    disk = DiskSummary(total_bytes=500 * 1024**3, used_bytes=200 * 1024**3, free_bytes=300 * 1024**3)
    mock_scan.return_value = ScanSummary(disk=disk, categories=[])

    result = run_doctor()
    assert result.categories == []
