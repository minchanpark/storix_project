"""Doctor service: summarize cleanup opportunities by category."""

from typing import Optional, List

from storix.models.enums import Category, RiskLevel
from storix.models.summary import ScanSummary, CategorySummary
from storix.services.scan_service import run_scan


def run_doctor(categories: Optional[List[Category]] = None) -> ScanSummary:
    """
    Run a doctor scan: same as scan_service but intended for advisory output.

    Returns a ScanSummary with all candidates ranked by size.
    """
    summary = run_scan(categories=categories)

    # Sort candidates within each category by size desc
    for cat_summary in summary.categories:
        cat_summary.candidates.sort(key=lambda c: c.size_bytes, reverse=True)

    # Sort categories by total size desc
    summary.categories.sort(key=lambda c: c.total_size_bytes, reverse=True)

    return summary
