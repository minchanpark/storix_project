"""Tests for clean_service and cleaners/base."""

import pytest
from pathlib import Path
from unittest.mock import patch

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel, CleanStatus
from storix.models.summary import DiskSummary, CategorySummary, ScanSummary
from storix.cleaners.base import clean_candidates
from storix.services.clean_service import clean_all_safe


def make_candidate(
    tmp_path: Path,
    name: str = "test",
    risk: RiskLevel = RiskLevel.SAFE,
    size: int = 1024 * 1024,
    create: bool = True,
) -> Candidate:
    p = tmp_path / name
    if create:
        p.mkdir(parents=True, exist_ok=True)
        (p / "file.txt").write_text("content")
    return Candidate(
        path=p,
        name=name,
        category=Category.XCODE,
        risk=risk,
        size_bytes=size,
        reason="test",
    )


def test_dry_run_does_not_delete(tmp_path):
    c = make_candidate(tmp_path, "derived_data", RiskLevel.SAFE)
    assert c.path.exists()

    report = clean_candidates([c], dry_run=True)

    assert c.path.exists()
    assert len(report.dry_run_items) == 1
    assert report.dry_run_items[0].status == CleanStatus.DRY_RUN


def test_safe_candidate_is_deleted(tmp_path):
    c = make_candidate(tmp_path, "safe_cache", RiskLevel.SAFE)
    assert c.path.exists()

    report = clean_candidates([c], dry_run=False)

    assert not c.path.exists()
    assert len(report.succeeded) == 1


def test_caution_skipped_by_default(tmp_path):
    c = make_candidate(tmp_path, "caution_item", RiskLevel.CAUTION)

    report = clean_candidates([c], dry_run=False, allow_caution=False)

    assert c.path.exists()  # not deleted
    assert len(report.skipped) == 1


def test_caution_deleted_when_allowed(tmp_path):
    c = make_candidate(tmp_path, "caution_item", RiskLevel.CAUTION)

    report = clean_candidates([c], dry_run=False, allow_caution=True)

    assert not c.path.exists()
    assert len(report.succeeded) == 1


def test_dangerous_always_skipped(tmp_path):
    c = make_candidate(tmp_path, "dangerous_item", RiskLevel.DANGEROUS)

    report = clean_candidates([c], dry_run=False, allow_dangerous=False)

    assert c.path.exists()
    assert len(report.skipped) == 1
    assert "dangerous" in report.skipped[0].error.lower()


def test_nonexistent_path_returns_failed(tmp_path):
    p = tmp_path / "nonexistent"
    c = Candidate(
        path=p,
        name="missing",
        category=Category.XCODE,
        risk=RiskLevel.SAFE,
        size_bytes=1024,
        reason="test",
    )

    report = clean_candidates([c], dry_run=False)
    assert len(report.failed) == 1


def test_partial_failure(tmp_path):
    good = make_candidate(tmp_path, "good", RiskLevel.SAFE)
    missing_path = tmp_path / "missing"
    bad = Candidate(
        path=missing_path,
        name="missing",
        category=Category.XCODE,
        risk=RiskLevel.SAFE,
        size_bytes=1024,
        reason="test",
    )

    report = clean_candidates([good, bad], dry_run=False)

    assert len(report.succeeded) == 1
    assert len(report.failed) == 1


def test_blocked_path_is_skipped():
    """Downloads should never be deleted."""
    from pathlib import Path
    downloads = Path.home() / "Downloads"
    c = Candidate(
        path=downloads,
        name="Downloads",
        category=Category.GENERAL,
        risk=RiskLevel.DANGEROUS,
        size_bytes=1024,
        reason="test",
    )

    report = clean_candidates([c], dry_run=False, allow_dangerous=True)
    # should still be skipped because guard blocks it
    assert len(report.skipped) == 1


def test_clean_report_summary(tmp_path):
    safe1 = make_candidate(tmp_path, "safe1", RiskLevel.SAFE)
    safe2 = make_candidate(tmp_path, "safe2", RiskLevel.SAFE)
    caution = make_candidate(tmp_path, "caution1", RiskLevel.CAUTION)

    report = clean_candidates([safe1, safe2, caution], dry_run=False, allow_caution=False)

    assert len(report.succeeded) == 2
    assert len(report.skipped) == 1
    assert report.total_reclaimed_bytes > 0


def test_clean_all_safe_excludes_caution_by_default(tmp_path):
    safe = make_candidate(tmp_path, "safe_default", RiskLevel.SAFE)
    caution = make_candidate(tmp_path, "caution_default", RiskLevel.CAUTION)

    summary = ScanSummary(
        disk=DiskSummary(total_bytes=1, used_bytes=1, free_bytes=0),
        categories=[CategorySummary(category=Category.XCODE, candidates=[safe, caution])],
    )

    with patch("storix.services.clean_service.run_scan", return_value=summary):
        report = clean_all_safe(dry_run=True)

    assert len(report.dry_run_items) == 1
    assert report.dry_run_items[0].candidate.name == "safe_default"
    assert len(report.skipped) == 0
    assert caution.path.exists()


def test_clean_all_safe_includes_caution_when_allowed(tmp_path):
    safe = make_candidate(tmp_path, "safe_with_caution", RiskLevel.SAFE)
    caution = make_candidate(tmp_path, "caution_with_caution", RiskLevel.CAUTION)

    summary = ScanSummary(
        disk=DiskSummary(total_bytes=1, used_bytes=1, free_bytes=0),
        categories=[CategorySummary(category=Category.XCODE, candidates=[safe, caution])],
    )

    with patch("storix.services.clean_service.run_scan", return_value=summary):
        report = clean_all_safe(dry_run=True, allow_caution=True)

    dry_run_names = {item.candidate.name for item in report.dry_run_items}
    assert dry_run_names == {"safe_with_caution", "caution_with_caution"}
    assert len(report.skipped) == 0
