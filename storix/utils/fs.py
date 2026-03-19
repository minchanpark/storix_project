"""File system utilities."""

import shutil
from pathlib import Path
from typing import Iterator, List, Optional

from storix.utils.guard import assert_safe, is_blocked


def expand_path(path: str | Path) -> Path:
    """Expand ~ and environment variables, return absolute Path."""
    return Path(str(path)).expanduser().resolve()


def safe_delete(path: Path, dry_run: bool = False) -> tuple[bool, str]:
    """
    Delete a path (file or directory) safely.

    Returns (success: bool, error_message: str).
    """
    try:
        assert_safe(path)
    except ValueError as e:
        return False, str(e)

    if not path.exists():
        return False, f"Path does not exist: {path}"

    if dry_run:
        return True, ""

    try:
        if path.is_file() or path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        return True, ""
    except PermissionError as e:
        return False, f"Permission denied: {e}"
    except OSError as e:
        return False, f"OS error: {e}"


def find_dirs(root: Path, name: str, max_depth: int = 5) -> Iterator[Path]:
    """Recursively find directories matching name under root, up to max_depth."""
    if not root.exists() or not root.is_dir():
        return

    try:
        for entry in root.iterdir():
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if entry.name == name:
                    yield entry
                elif max_depth > 1:
                    yield from find_dirs(entry, name, max_depth - 1)
    except (PermissionError, OSError):
        return


def find_files_with_extension(root: Path, extension: str, max_depth: int = 5) -> Iterator[Path]:
    """Find files with a given extension under root."""
    if not root.exists() or not root.is_dir():
        return
    try:
        for entry in root.iterdir():
            if entry.is_symlink():
                continue
            if entry.is_file() and entry.suffix == extension:
                yield entry
            elif entry.is_dir() and max_depth > 1:
                yield from find_files_with_extension(entry, extension, max_depth - 1)
    except (PermissionError, OSError):
        return


def path_exists(path: Path) -> bool:
    """Check if path exists (handles symlinks and permission errors)."""
    try:
        return path.exists()
    except (PermissionError, OSError):
        return False
