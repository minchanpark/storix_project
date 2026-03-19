"""Python cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size


def scan_python() -> List[Candidate]:
    """Scan for Python-related cleanup candidates."""
    candidates: List[Candidate] = []

    # pip cache
    pip_cache = expand_path("~/Library/Caches/pip")
    if path_exists(pip_cache):
        size = dir_size(pip_cache)
        if size > 0:
            candidates.append(Candidate(
                path=pip_cache,
                name="pip Cache",
                category=Category.PYTHON,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="pip wheel and package cache",
                regenerable=True,
                description="pip download and wheel cache. Safe to clear.",
                warning="",
            ))

    # uv cache
    uv_cache = expand_path("~/.cache/uv")
    if path_exists(uv_cache):
        size = dir_size(uv_cache)
        if size > 0:
            candidates.append(Candidate(
                path=uv_cache,
                name="uv Cache",
                category=Category.PYTHON,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="uv package manager cache",
                regenerable=True,
                description="uv package manager download cache.",
                warning="",
            ))

    # poetry cache
    poetry_cache = expand_path("~/Library/Caches/pypoetry")
    if path_exists(poetry_cache):
        size = dir_size(poetry_cache)
        if size > 0:
            candidates.append(Candidate(
                path=poetry_cache,
                name="Poetry Cache",
                category=Category.PYTHON,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Poetry virtual environments and download cache",
                regenerable=True,
                description="Poetry package and virtualenv cache.",
                warning="",
            ))

    return candidates
