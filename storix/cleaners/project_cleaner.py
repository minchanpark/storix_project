"""Project artifact cleaner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanReport
from storix.cleaners.base import clean_candidates
from storix.scanners.project_scanner import scan_projects


def clean_projects(
    roots: List[Path],
    dry_run: bool = False,
    allow_caution: bool = False,
    candidates: List[Candidate] | None = None,
) -> CleanReport:
    """Clean project artifacts in given root directories."""
    if candidates is None:
        candidates = scan_projects(roots)
    return clean_candidates(candidates, dry_run=dry_run, allow_caution=allow_caution)
