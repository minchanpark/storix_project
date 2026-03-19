"""Android cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size


def scan_android() -> List[Candidate]:
    """Scan for Android-related cleanup candidates."""
    candidates: List[Candidate] = []

    # AVD
    avd = expand_path("~/.android/avd")
    if path_exists(avd):
        size = dir_size(avd)
        if size > 0:
            candidates.append(Candidate(
                path=avd,
                name="Android AVD",
                category=Category.ANDROID,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Android virtual devices; can be recreated in AVD Manager",
                regenerable=True,
                description="Android emulator device definitions and data. Recreatable via Android Studio AVD Manager.",
                warning="Deleting removes all emulator app data and configurations.",
            ))

    # Gradle caches
    gradle_caches = expand_path("~/.gradle/caches")
    if path_exists(gradle_caches):
        size = dir_size(gradle_caches)
        if size > 0:
            candidates.append(Candidate(
                path=gradle_caches,
                name="Gradle Caches",
                category=Category.ANDROID,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Gradle build caches; re-downloaded on next build",
                regenerable=True,
                description="Gradle dependency and build caches. Re-downloaded on next build.",
                warning="",
            ))

    # Android SDK system-images
    system_images = expand_path("~/Library/Android/sdk/system-images")
    if path_exists(system_images):
        size = dir_size(system_images)
        if size > 0:
            candidates.append(Candidate(
                path=system_images,
                name="Android SDK System Images",
                category=Category.ANDROID,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Android emulator system images; re-downloadable via SDK Manager",
                regenerable=True,
                description="Android emulator system images. Very large; re-downloadable via SDK Manager.",
                warning="Deleting requires re-downloading to use those API levels in the emulator.",
            ))

    return candidates
