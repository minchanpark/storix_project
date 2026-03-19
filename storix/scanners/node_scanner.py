"""Node/Web cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size


def scan_node() -> List[Candidate]:
    """Scan for Node/Web-related cleanup candidates."""
    candidates: List[Candidate] = []

    # npm cache
    npm_cache = expand_path("~/.npm")
    if path_exists(npm_cache):
        size = dir_size(npm_cache)
        if size > 0:
            candidates.append(Candidate(
                path=npm_cache,
                name="npm Cache",
                category=Category.NODE,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="npm package cache; automatically managed",
                regenerable=True,
                description="npm download cache. Safe to clear; npm will re-fetch packages as needed.",
                warning="",
            ))

    # yarn cache
    yarn_cache = expand_path("~/Library/Caches/yarn")
    if path_exists(yarn_cache):
        size = dir_size(yarn_cache)
        if size > 0:
            candidates.append(Candidate(
                path=yarn_cache,
                name="Yarn Cache",
                category=Category.NODE,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="Yarn package cache",
                regenerable=True,
                description="Yarn download cache.",
                warning="",
            ))

    # pnpm store
    pnpm_store = expand_path("~/Library/pnpm/store")
    if path_exists(pnpm_store):
        size = dir_size(pnpm_store)
        if size > 0:
            candidates.append(Candidate(
                path=pnpm_store,
                name="pnpm Store",
                category=Category.NODE,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="pnpm content-addressable store; shared across projects",
                regenerable=True,
                description="pnpm global content-addressable store. Deleting may break existing pnpm-linked projects.",
                warning="Shared across all pnpm projects. Run `pnpm store prune` for safer cleanup.",
            ))

    # bun cache
    bun_cache = expand_path("~/.bun/install/cache")
    if path_exists(bun_cache):
        size = dir_size(bun_cache)
        if size > 0:
            candidates.append(Candidate(
                path=bun_cache,
                name="Bun Cache",
                category=Category.NODE,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="Bun package cache",
                regenerable=True,
                description="Bun package download cache.",
                warning="",
            ))

    return candidates
