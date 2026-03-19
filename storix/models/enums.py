"""Storix enumerations."""

from enum import Enum


class RiskLevel(str, Enum):
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"

    def __str__(self) -> str:
        return self.value


class Category(str, Enum):
    ALL = "all"
    XCODE = "xcode"
    ANDROID = "android"
    FLUTTER = "flutter"
    NODE = "node"
    PYTHON = "python"
    VSCODE = "vscode"
    GENERAL = "general"

    def __str__(self) -> str:
        return self.value


class CleanStatus(str, Enum):
    SUCCESS = "success"
    SKIPPED = "skipped"
    FAILED = "failed"
    DRY_RUN = "dry_run"

    def __str__(self) -> str:
        return self.value
