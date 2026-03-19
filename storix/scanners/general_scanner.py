"""General user folder cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size

# Minimum size to report downloads items (100 MB)
DOWNLOADS_MIN_SIZE = 100 * 1024 * 1024


def scan_general() -> List[Candidate]:
    """Scan general user folders for cleanup candidates."""
    candidates: List[Candidate] = []

    # Trash
    trash = expand_path("~/.Trash")
    if path_exists(trash):
        size = dir_size(trash)
        if size > 0:
            candidates.append(Candidate(
                path=trash,
                name="Trash",
                category=Category.GENERAL,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="Items already moved to Trash",
                regenerable=False,
                description="Items in the macOS Trash. Empty the Trash to reclaim space.",
                warning="",
            ))

    # Downloads — mark dangerous, just show large items
    downloads = expand_path("~/Downloads")
    if path_exists(downloads):
        size = dir_size(downloads)
        if size >= DOWNLOADS_MIN_SIZE:
            candidates.append(Candidate(
                path=downloads,
                name="Downloads",
                category=Category.GENERAL,
                risk=RiskLevel.DANGEROUS,
                size_bytes=size,
                reason="Large Downloads folder; review manually",
                regenerable=False,
                description="Your Downloads folder. Contains files you downloaded. Review and delete manually.",
                warning="Never auto-deleted. Review contents before removing anything.",
            ))

    return candidates
