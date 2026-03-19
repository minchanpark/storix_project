"""Android cleaner."""

from typing import List

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanReport
from storix.cleaners.base import clean_candidates
from storix.scanners.android_scanner import scan_android


def clean_android(
    dry_run: bool = False,
    allow_caution: bool = False,
    candidates: List[Candidate] | None = None,
) -> CleanReport:
    """Clean Android candidates."""
    if candidates is None:
        candidates = scan_android()
    return clean_candidates(candidates, dry_run=dry_run, allow_caution=allow_caution)
