"""Base cleaner: shared logic for all category cleaners."""

from typing import List

from storix.models.candidate import Candidate
from storix.models.clean_result import CleanResult, CleanReport
from storix.models.enums import CleanStatus, RiskLevel
from storix.utils.fs import safe_delete
from storix.utils.size import dir_size
from storix.utils.guard import is_blocked


def clean_candidates(
    candidates: List[Candidate],
    dry_run: bool = False,
    allow_caution: bool = False,
    allow_dangerous: bool = False,
) -> CleanReport:
    """
    Clean a list of candidates.

    - dangerous items are always skipped unless allow_dangerous=True
    - caution items are skipped unless allow_caution=True
    - dry_run=True shows what would be deleted without deleting
    """
    results: List[CleanResult] = []

    for candidate in candidates:
        # Skip dangerous by default
        if candidate.risk == RiskLevel.DANGEROUS and not allow_dangerous:
            results.append(CleanResult(
                candidate=candidate,
                status=CleanStatus.SKIPPED,
                reclaimed_bytes=0,
                error="dangerous items are excluded from default cleanup",
            ))
            continue

        # Skip caution unless allowed
        if candidate.risk == RiskLevel.CAUTION and not allow_caution:
            results.append(CleanResult(
                candidate=candidate,
                status=CleanStatus.SKIPPED,
                reclaimed_bytes=0,
                error="caution items require explicit --caution flag",
            ))
            continue

        # Guard check
        blocked, reason = is_blocked(candidate.path)
        if blocked:
            results.append(CleanResult(
                candidate=candidate,
                status=CleanStatus.SKIPPED,
                reclaimed_bytes=0,
                error=f"path blocked: {reason}",
            ))
            continue

        if dry_run:
            results.append(CleanResult(
                candidate=candidate,
                status=CleanStatus.DRY_RUN,
                reclaimed_bytes=candidate.size_bytes,
            ))
            continue

        # Perform deletion
        size_before = dir_size(candidate.path)
        success, error = safe_delete(candidate.path, dry_run=False)

        if success:
            results.append(CleanResult(
                candidate=candidate,
                status=CleanStatus.SUCCESS,
                reclaimed_bytes=size_before,
            ))
        else:
            results.append(CleanResult(
                candidate=candidate,
                status=CleanStatus.FAILED,
                reclaimed_bytes=0,
                error=error,
            ))

    return CleanReport(results=results, dry_run=dry_run)
