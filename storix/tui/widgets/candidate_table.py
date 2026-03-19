"""Candidate table widget for the TUI center panel."""

from typing import List

from textual.widgets import DataTable
from textual.app import ComposeResult
from rich.text import Text

from storix.models.candidate import Candidate
from storix.models.enums import RiskLevel
from storix.utils.size import format_size

RISK_COLOR = {
    RiskLevel.SAFE: "green",
    RiskLevel.CAUTION: "yellow",
    RiskLevel.DANGEROUS: "red",
}

RISK_ICON = {
    RiskLevel.SAFE: "✓",
    RiskLevel.CAUTION: "⚠",
    RiskLevel.DANGEROUS: "✗",
}


class CandidateTable(DataTable):
    """Center panel candidate table."""

    DEFAULT_CSS = """
    CandidateTable {
        height: 100%;
    }
    """

    def __init__(self, candidates: List[Candidate] | None = None, **kwargs):
        super().__init__(**kwargs)
        self._candidates: List[Candidate] = candidates or []

    def on_mount(self) -> None:
        self.add_columns("", "Name", "Size", "Risk")
        self.cursor_type = "row"
        self.refresh_rows()

    def refresh_rows(self) -> None:
        self.clear()
        for c in self._candidates:
            icon = RISK_ICON[c.risk]
            color = RISK_COLOR[c.risk]
            checkbox = "☑" if c.selected else "☐"
            risk_text = Text(f"{icon} {c.risk.value}", style=color)
            self.add_row(checkbox, c.name, format_size(c.size_bytes), risk_text, key=str(c.path))

    def update_candidates(self, candidates: List[Candidate]) -> None:
        self._candidates = candidates
        self.refresh_rows()

    def toggle_selected(self, row_key: str) -> None:
        for c in self._candidates:
            if str(c.path) == row_key:
                c.selected = not c.selected
                break
        self.refresh_rows()

    def select_all(self) -> None:
        for c in self._candidates:
            c.selected = True
        self.refresh_rows()

    def deselect_all(self) -> None:
        for c in self._candidates:
            c.selected = False
        self.refresh_rows()

    @property
    def selected_candidates(self) -> List[Candidate]:
        return [c for c in self._candidates if c.selected]

    @property
    def current_candidate(self) -> Candidate | None:
        if not self._candidates or self.cursor_row < 0:
            return None
        if self.cursor_row >= len(self._candidates):
            return None
        return self._candidates[self.cursor_row]
