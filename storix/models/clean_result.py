"""Clean result models."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from storix.models.enums import CleanStatus
from storix.models.candidate import Candidate


@dataclass
class CleanResult:
    """Result of cleaning a single candidate."""

    candidate: Candidate
    status: CleanStatus
    reclaimed_bytes: int = 0
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "path": str(self.candidate.path),
            "name": self.candidate.name,
            "category": str(self.candidate.category),
            "risk": str(self.candidate.risk),
            "status": str(self.status),
            "reclaimed_bytes": self.reclaimed_bytes,
            "error": self.error,
        }


@dataclass
class CleanReport:
    """Aggregate report after a clean run."""

    results: List[CleanResult] = field(default_factory=list)
    dry_run: bool = False

    @property
    def succeeded(self) -> List[CleanResult]:
        return [r for r in self.results if r.status == CleanStatus.SUCCESS]

    @property
    def skipped(self) -> List[CleanResult]:
        return [r for r in self.results if r.status == CleanStatus.SKIPPED]

    @property
    def failed(self) -> List[CleanResult]:
        return [r for r in self.results if r.status == CleanStatus.FAILED]

    @property
    def dry_run_items(self) -> List[CleanResult]:
        return [r for r in self.results if r.status == CleanStatus.DRY_RUN]

    @property
    def total_reclaimed_bytes(self) -> int:
        return sum(r.reclaimed_bytes for r in self.succeeded)

    @property
    def total_estimated_bytes(self) -> int:
        return sum(r.candidate.size_bytes for r in self.results if r.status in (CleanStatus.DRY_RUN, CleanStatus.SUCCESS))

    def to_dict(self) -> dict:
        return {
            "dry_run": self.dry_run,
            "total_reclaimed_bytes": self.total_reclaimed_bytes,
            "total_estimated_bytes": self.total_estimated_bytes,
            "succeeded_count": len(self.succeeded),
            "skipped_count": len(self.skipped),
            "failed_count": len(self.failed),
            "results": [r.to_dict() for r in self.results],
        }
