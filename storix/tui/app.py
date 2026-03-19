"""Storix TUI application."""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding

from storix.services.scan_service import run_scan


class StorixApp(App):
    """Storix terminal user interface."""

    TITLE = "Storix — Storage Analyzer"
    CSS_PATH = Path(__file__).parent / "storix.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
    ]

    def on_mount(self) -> None:
        from storix.tui.screens.main_screen import MainScreen
        summary = run_scan()
        self.push_screen(MainScreen(scan_summary=summary))


def run_tui() -> None:
    """Entry point for the TUI."""
    app = StorixApp()
    app.run()
