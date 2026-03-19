"""Flutter/Dart cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size


def scan_flutter() -> List[Candidate]:
    """Scan for Flutter/Dart-related cleanup candidates."""
    candidates: List[Candidate] = []

    # pub cache
    pub_cache = expand_path("~/.pub-cache")
    if path_exists(pub_cache):
        size = dir_size(pub_cache)
        if size > 0:
            candidates.append(Candidate(
                path=pub_cache,
                name="Dart/Flutter Pub Cache",
                category=Category.FLUTTER,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Dart package cache; re-downloaded on next pub get/flutter pub get",
                regenerable=True,
                description="Cached Dart packages. Re-fetched automatically on next `flutter pub get`.",
                warning="",
            ))

    return candidates
