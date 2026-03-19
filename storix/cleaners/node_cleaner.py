"""Node/Web cleaner."""

from typing import List

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanReport
from storix.cleaners.base import clean_candidates
from storix.scanners.node_scanner import scan_node


def clean_node(
    dry_run: bool = False,
    allow_caution: bool = False,
    candidates: List[Candidate] | None = None,
) -> CleanReport:
    """Clean Node/Web candidates."""
    if candidates is None:
        candidates = scan_node()
    return clean_candidates(candidates, dry_run=dry_run, allow_caution=allow_caution)
