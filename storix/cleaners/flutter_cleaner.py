"""Flutter/Dart cleaner."""

from typing import List

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanReport
from storix.cleaners.base import clean_candidates
from storix.scanners.flutter_scanner import scan_flutter


def clean_flutter(
    dry_run: bool = False,
    allow_caution: bool = False,
    candidates: List[Candidate] | None = None,
) -> CleanReport:
    """Clean Flutter/Dart candidates."""
    if candidates is None:
        candidates = scan_flutter()
    return clean_candidates(candidates, dry_run=dry_run, allow_caution=allow_caution)
