"""Summary models for scan results."""

from dataclasses import dataclass, field
from typing import List

from storix.models.enums import Category, RiskLevel
from storix.models.candidate import Candidate


@dataclass
class DiskSummary:
    """macOS disk usage overview."""

    total_bytes: int
    used_bytes: int
    free_bytes: int
    volume: str = "/"

    @property
    def used_gb(self) -> float:
        return self.used_bytes / (1024 ** 3)

    @property
    def free_gb(self) -> float:
        return self.free_bytes / (1024 ** 3)

    @property
    def total_gb(self) -> float:
        return self.total_bytes / (1024 ** 3)

    @property
    def used_pct(self) -> float:
        if self.total_bytes == 0:
            return 0.0
        return (self.used_bytes / self.total_bytes) * 100

    def to_dict(self) -> dict:
        return {
            "volume": self.volume,
            "total_bytes": self.total_bytes,
            "used_bytes": self.used_bytes,
            "free_bytes": self.free_bytes,
            "total_gb": round(self.total_gb, 2),
            "used_gb": round(self.used_gb, 2),
            "free_gb": round(self.free_gb, 2),
            "used_pct": round(self.used_pct, 1),
        }


@dataclass
class CategorySummary:
    """Aggregated summary for a single category."""

    category: Category
    candidates: List[Candidate] = field(default_factory=list)

    @property
    def total_size_bytes(self) -> int:
        return sum(c.size_bytes for c in self.candidates)

    @property
    def safe_size_bytes(self) -> int:
        return sum(c.size_bytes for c in self.candidates if c.risk == RiskLevel.SAFE)

    @property
    def caution_size_bytes(self) -> int:
        return sum(c.size_bytes for c in self.candidates if c.risk == RiskLevel.CAUTION)

    @property
    def dangerous_size_bytes(self) -> int:
        return sum(c.size_bytes for c in self.candidates if c.risk == RiskLevel.DANGEROUS)

    @property
    def safe_count(self) -> int:
        return sum(1 for c in self.candidates if c.risk == RiskLevel.SAFE)

    @property
    def caution_count(self) -> int:
        return sum(1 for c in self.candidates if c.risk == RiskLevel.CAUTION)

    @property
    def candidate_count(self) -> int:
        return len(self.candidates)

    def to_dict(self) -> dict:
        return {
            "category": str(self.category),
            "candidate_count": self.candidate_count,
            "total_size_bytes": self.total_size_bytes,
            "safe_size_bytes": self.safe_size_bytes,
            "caution_size_bytes": self.caution_size_bytes,
            "dangerous_size_bytes": self.dangerous_size_bytes,
            "candidates": [c.to_dict() for c in self.candidates],
        }


@dataclass
class ScanSummary:
    """Full scan result."""

    disk: DiskSummary
    categories: List[CategorySummary] = field(default_factory=list)

    @property
    def all_candidates(self) -> List[Candidate]:
        result = []
        for cat in self.categories:
            result.extend(cat.candidates)
        return result

    @property
    def total_reclaimable_bytes(self) -> int:
        return sum(c.total_size_bytes for c in self.categories)

    @property
    def safe_reclaimable_bytes(self) -> int:
        return sum(c.safe_size_bytes for c in self.categories)

    def get_category(self, category: Category) -> CategorySummary | None:
        for cat in self.categories:
            if cat.category == category:
                return cat
        return None

    def to_dict(self) -> dict:
        return {
            "disk": self.disk.to_dict(),
            "total_reclaimable_bytes": self.total_reclaimable_bytes,
            "safe_reclaimable_bytes": self.safe_reclaimable_bytes,
            "categories": [c.to_dict() for c in self.categories],
        }
