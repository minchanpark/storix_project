"""VS Code cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size


def scan_vscode() -> List[Candidate]:
    """Scan for VS Code-related cleanup candidates."""
    candidates: List[Candidate] = []

    targets = [
        (
            "~/Library/Application Support/Code/Cache",
            "VS Code Cache",
            RiskLevel.SAFE,
            "VS Code UI cache; recreated automatically",
            "VS Code Electron cache.",
            "",
        ),
        (
            "~/Library/Application Support/Code/CachedData",
            "VS Code CachedData",
            RiskLevel.SAFE,
            "VS Code compiled extension data; recreated",
            "Compiled VS Code extension data. Recreated on next launch.",
            "",
        ),
        (
            "~/Library/Application Support/Code/User/workspaceStorage",
            "VS Code Workspace Storage",
            RiskLevel.SAFE,
            "Per-workspace extension data; safely removable for old workspaces",
            "Per-workspace state stored by extensions. Old/unused workspace entries can be safely removed.",
            "",
        ),
        (
            "~/Library/Application Support/Code/logs",
            "VS Code Logs",
            RiskLevel.SAFE,
            "VS Code log files",
            "VS Code diagnostic log files.",
            "",
        ),
    ]

    for path_str, name, risk, reason, description, warning in targets:
        path = expand_path(path_str)
        if path_exists(path):
            size = dir_size(path)
            if size > 0:
                candidates.append(Candidate(
                    path=path,
                    name=name,
                    category=Category.VSCODE,
                    risk=risk,
                    size_bytes=size,
                    reason=reason,
                    regenerable=True,
                    description=description,
                    warning=warning,
                ))

    return candidates
