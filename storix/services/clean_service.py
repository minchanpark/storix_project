"""Clean service: orchestrates cleanup across categories."""

from typing import List, Optional

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanReport
from storix.models.enums import Category, RiskLevel
from storix.cleaners.base import clean_candidates
from storix.services.scan_service import run_scan


def clean_all_safe(dry_run: bool = False, allow_caution: bool = False) -> CleanReport:
    """Clean all safe candidates, and optionally caution candidates, across all categories."""
    summary = run_scan()
    eligible_risks = {RiskLevel.SAFE}
    if allow_caution:
        eligible_risks.add(RiskLevel.CAUTION)

    eligible_candidates = [
        c for c in summary.all_candidates if c.risk in eligible_risks
    ]
    return clean_candidates(
        eligible_candidates,
        dry_run=dry_run,
        allow_caution=allow_caution,
    )


def clean_by_category(
    category: Category,
    dry_run: bool = False,
    allow_caution: bool = False,
) -> CleanReport:
    """Clean all candidates in a specific category."""
    summary = run_scan(categories=[category])
    cat_summary = summary.get_category(category)
    if cat_summary is None:
        return CleanReport(results=[], dry_run=dry_run)
    return clean_candidates(
        cat_summary.candidates,
        dry_run=dry_run,
        allow_caution=allow_caution,
    )


def clean_selected(
    candidates: List[Candidate],
    dry_run: bool = False,
    allow_caution: bool = True,
    allow_dangerous: bool = False,
) -> CleanReport:
    """Clean a specific list of candidates (used from TUI)."""
    return clean_candidates(
        candidates,
        dry_run=dry_run,
        allow_caution=allow_caution,
        allow_dangerous=allow_dangerous,
    )
