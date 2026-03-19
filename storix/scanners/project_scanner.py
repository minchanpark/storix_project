"""Project artifact scanner - detects build outputs in project directories."""

from pathlib import Path
from typing import List, Optional
import fnmatch

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import path_exists
from storix.utils.size import dir_size


# Project type detection: marker files → category
PROJECT_MARKERS: dict[str, list[str]] = {
    "flutter": ["pubspec.yaml"],
    "node": ["package.json"],
    "python": ["pyproject.toml", "setup.py", "setup.cfg"],
    "android": ["build.gradle", "build.gradle.kts"],
}

# Artifacts to look for per project type
PROJECT_ARTIFACTS: dict[str, list[dict]] = {
    "flutter": [
        {"path": "build", "risk": RiskLevel.SAFE, "reason": "Flutter build output"},
        {"path": ".dart_tool", "risk": RiskLevel.SAFE, "reason": "Dart tool cache"},
        {"path": "ios/Pods", "risk": RiskLevel.CAUTION, "reason": "CocoaPods deps; run pod install to restore"},
    ],
    "node": [
        {"path": "node_modules", "risk": RiskLevel.CAUTION, "reason": "Dependencies; run npm/yarn install to restore"},
        {"path": ".next", "risk": RiskLevel.SAFE, "reason": "Next.js build output"},
        {"path": "dist", "risk": RiskLevel.SAFE, "reason": "Build output"},
        {"path": "build", "risk": RiskLevel.SAFE, "reason": "Build output"},
        {"path": ".cache", "risk": RiskLevel.SAFE, "reason": "Build cache"},
        {"path": "coverage", "risk": RiskLevel.SAFE, "reason": "Test coverage output"},
        {"path": "out", "risk": RiskLevel.SAFE, "reason": "Build output"},
    ],
    "python": [
        {"path": "__pycache__", "risk": RiskLevel.SAFE, "reason": "Python bytecode cache"},
        {"path": ".pytest_cache", "risk": RiskLevel.SAFE, "reason": "pytest cache"},
        {"path": "dist", "risk": RiskLevel.SAFE, "reason": "Python distribution build"},
        {"path": "build", "risk": RiskLevel.SAFE, "reason": "Build output"},
        {"path": ".venv", "risk": RiskLevel.CAUTION, "reason": "Virtual environment; recreatable with pip install"},
        {"path": "venv", "risk": RiskLevel.CAUTION, "reason": "Virtual environment; recreatable with pip install"},
    ],
    "android": [
        {"path": "build", "risk": RiskLevel.SAFE, "reason": "Android build output"},
        {"path": ".gradle", "risk": RiskLevel.SAFE, "reason": "Gradle build cache"},
    ],
}

CATEGORY_MAP: dict[str, Category] = {
    "flutter": Category.FLUTTER,
    "node": Category.NODE,
    "python": Category.PYTHON,
    "android": Category.ANDROID,
}


def detect_project_type(project_root: Path) -> Optional[str]:
    """Return the project type string, or None if unrecognized."""
    for ptype, markers in PROJECT_MARKERS.items():
        for marker in markers:
            if (project_root / marker).exists():
                return ptype
    return None


def scan_project(project_root: Path) -> List[Candidate]:
    """Scan a single project directory for cleanup artifacts."""
    candidates: List[Candidate] = []

    ptype = detect_project_type(project_root)
    if ptype is None:
        return candidates

    category = CATEGORY_MAP.get(ptype, Category.GENERAL)

    for artifact in PROJECT_ARTIFACTS.get(ptype, []):
        artifact_path = project_root / artifact["path"]
        if path_exists(artifact_path):
            size = dir_size(artifact_path)
            if size > 0:
                candidates.append(Candidate(
                    path=artifact_path,
                    name=f"{artifact_path.name} ({project_root.name})",
                    category=category,
                    risk=artifact["risk"],
                    size_bytes=size,
                    reason=artifact["reason"],
                    regenerable=True,
                    description=f"Project artifact in {project_root}",
                    warning="",
                ))

    return candidates


def scan_projects(roots: List[Path], max_depth: int = 4) -> List[Candidate]:
    """Scan multiple root directories for project artifacts."""
    candidates: List[Candidate] = []
    visited: set[Path] = set()

    def _recurse(directory: Path, depth: int) -> None:
        if depth == 0 or directory in visited:
            return
        visited.add(directory)

        if not path_exists(directory):
            return

        # Check if this is a project root
        ptype = detect_project_type(directory)
        if ptype is not None:
            candidates.extend(scan_project(directory))
            return  # Don't descend into sub-projects

        # Recurse
        try:
            for entry in directory.iterdir():
                if entry.is_symlink():
                    continue
                if entry.is_dir() and not entry.name.startswith("."):
                    _recurse(entry, depth - 1)
        except (PermissionError, OSError):
            pass

    for root in roots:
        _recurse(root, max_depth)

    return candidates
