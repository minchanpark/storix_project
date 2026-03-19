"""File system size utilities."""

import os
import shutil
from pathlib import Path
from typing import Optional


def dir_size(path: Path) -> int:
    """Return total size of a directory in bytes. Returns 0 if path doesn't exist or is inaccessible."""
    if not path.exists():
        return 0
    if path.is_file():
        try:
            return path.stat().st_size
        except (PermissionError, OSError):
            return 0

    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_symlink():
                    continue
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += dir_size(Path(entry.path))
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError):
        pass
    return total


def format_size(size_bytes: int) -> str:
    """Human-readable file size."""
    if size_bytes < 0:
        return "0 B"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / 1024 ** 2:.1f} MB"
    else:
        return f"{size_bytes / 1024 ** 3:.2f} GB"


def disk_usage(path: str = "/") -> tuple[int, int, int]:
    """Return (total, used, free) bytes for the given mount point."""
    usage = shutil.disk_usage(path)
    return usage.total, usage.used, usage.free
