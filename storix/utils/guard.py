"""Guard rules: protect dangerous paths from accidental deletion."""

import os
from pathlib import Path
from typing import Set

HOME = Path.home()

# Paths that must never be deleted automatically
HARD_BLOCKED: Set[Path] = {
    HOME,
    HOME / "Desktop",
    HOME / "Documents",
    HOME / "Downloads",
    HOME / "Movies",
    HOME / "Music",
    HOME / "Pictures",
    HOME / "Public",
    HOME / ".Trash",
    Path("/"),
    Path("/System"),
    Path("/usr"),
    Path("/bin"),
    Path("/sbin"),
    Path("/etc"),
    Path("/var"),
    Path("/private"),
    Path("/Library"),
    Path("/Applications"),
    Path("/Users"),
    Path("/Volumes"),
}

# Maximum path depth allowed for deletion (safety: don't delete very shallow paths)
MIN_PATH_DEPTH = 3


def is_blocked(path: Path) -> tuple[bool, str]:
    """
    Check whether a path is blocked from deletion.

    Returns (blocked: bool, reason: str).
    """
    try:
        resolved = path.resolve()
    except (OSError, RuntimeError):
        return True, "Cannot resolve path"

    # Hard blocked exact matches
    if resolved in HARD_BLOCKED:
        return True, f"Protected system/user path: {resolved}"

    # Hard blocked parent check
    for blocked in HARD_BLOCKED:
        try:
            resolved.relative_to(blocked)
            # The path is inside a blocked dir — only safe if it's deep enough
            depth = len(resolved.parts) - len(blocked.parts)
            if depth < 2:
                return True, f"Too close to protected path: {blocked}"
        except ValueError:
            continue

    # Depth check
    if len(resolved.parts) < MIN_PATH_DEPTH:
        return True, f"Path too shallow (depth {len(resolved.parts)})"

    # Check if it's the home directory itself
    try:
        if resolved == HOME.resolve():
            return True, "Home directory is protected"
    except (OSError, RuntimeError):
        pass

    return False, ""


def assert_safe(path: Path) -> None:
    """Raise ValueError if path is blocked."""
    blocked, reason = is_blocked(path)
    if blocked:
        raise ValueError(f"Path is blocked: {path} — {reason}")
