"""Detail panel widget for the TUI right panel."""

from textual.widgets import Static
from textual.app import ComposeResult

from storix.models.candidate import Candidate
from storix.presenters.tui_adapter import format_detail


class DetailPanel(Static):
    """Right panel showing candidate details."""

    DEFAULT_CSS = """
    DetailPanel {
        width: 30;
        height: 100%;
        border-left: solid $primary;
        padding: 1;
        overflow-y: auto;
    }
    """

    def __init__(self, **kwargs):
        super().__init__("", **kwargs)

    def show_candidate(self, candidate: Candidate | None) -> None:
        if candidate is None:
            self.update("[dim]Select an item to see details.[/dim]")
        else:
            self.update(format_detail(candidate))
