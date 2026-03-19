"""Project service: scan project directories for artifacts."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanReport
from storix.models.summary import CategorySummary, ScanSummary
from storix.models.enums import Category
from storix.scanners.project_scanner import scan_projects
from storix.scanners.disk_scanner import scan_disk
from storix.cleaners.base import clean_candidates


def run_project_scan(roots: List[Path]) -> ScanSummary:
    """Scan project directories and return a ScanSummary."""
    disk = scan_disk()
    candidates = scan_projects(roots)

    # Group candidates by category
    category_map: dict[Category, List[Candidate]] = {}
    for c in candidates:
        category_map.setdefault(c.category, []).append(c)

    categories = [
        CategorySummary(category=cat, candidates=cands)
        for cat, cands in category_map.items()
    ]
    categories.sort(key=lambda c: c.total_size_bytes, reverse=True)

    return ScanSummary(disk=disk, categories=categories)


def clean_project_artifacts(
    roots: List[Path],
    dry_run: bool = False,
    allow_caution: bool = False,
) -> CleanReport:
    """Clean project artifacts in given directories."""
    candidates = scan_projects(roots)
    return clean_candidates(candidates, dry_run=dry_run, allow_caution=allow_caution)
