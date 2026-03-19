"""Summary bar widget showing selected size."""

from textual.widgets import Static

from storix.utils.size import format_size


class SummaryBar(Static):
    """Status bar showing scan summary and selected size."""

    DEFAULT_CSS = """
    SummaryBar {
        height: 1;
        background: $primary-darken-2;
        color: $text;
        padding: 0 1;
    }
    """

    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self._selected_bytes = 0
        self._total_bytes = 0
        self._status = ""

    def update_selection(self, selected_bytes: int, total_bytes: int) -> None:
        self._selected_bytes = selected_bytes
        self._total_bytes = total_bytes
        self._refresh_text()

    def set_status(self, status: str) -> None:
        self._status = status
        self._refresh_text()

    def _refresh_text(self) -> None:
        parts = []
        if self._total_bytes > 0:
            parts.append(f"Total reclaimable: {format_size(self._total_bytes)}")
        if self._selected_bytes > 0:
            parts.append(f"Selected: [bold cyan]{format_size(self._selected_bytes)}[/bold cyan]")
        if self._status:
            parts.append(self._status)
        self.update("  ".join(parts) if parts else "")
