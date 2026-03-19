"""Disk usage scanner."""

from storix.models.summary import DiskSummary
from storix.utils.size import disk_usage


def scan_disk(volume: str = "/") -> DiskSummary:
    """Return disk usage summary for the given volume."""
    total, used, free = disk_usage(volume)
    return DiskSummary(
        total_bytes=total,
        used_bytes=used,
        free_bytes=free,
        volume=volume,
    )
