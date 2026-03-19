"""Candidate model - a detected cleanup target."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from storix.models.enums import RiskLevel, Category


@dataclass
class Candidate:
    """A detected item that could be cleaned up."""

    path: Path
    name: str
    category: Category
    risk: RiskLevel
    size_bytes: int
    reason: str
    regenerable: bool = True
    warning: str = ""
    description: str = ""
    selected: bool = False

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)

    @property
    def size_gb(self) -> float:
        return self.size_bytes / (1024 * 1024 * 1024)

    def to_dict(self) -> dict:
        return {
            "path": str(self.path),
            "name": self.name,
            "category": str(self.category),
            "risk": str(self.risk),
            "size_bytes": self.size_bytes,
            "reason": self.reason,
            "regenerable": self.regenerable,
            "warning": self.warning,
            "description": self.description,
        }
