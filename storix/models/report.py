"""Report model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from storix.models.summary import ScanSummary
from storix.models.clean_result import CleanReport


@dataclass
class Report:
    """Full Storix run report."""

    generated_at: datetime = field(default_factory=datetime.now)
    scan: Optional[ScanSummary] = None
    clean: Optional[CleanReport] = None
    version: str = "0.1.0"

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "generated_at": self.generated_at.isoformat(),
            "scan": self.scan.to_dict() if self.scan else None,
            "clean": self.clean.to_dict() if self.clean else None,
        }
