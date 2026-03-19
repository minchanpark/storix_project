"""Result screen shown after a clean operation."""

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, DataTable
from textual.containers import Vertical, Horizontal
from rich.text import Text

from storix.models.clean_result import CleanReport
from storix.models.enums import CleanStatus
from storix.utils.size import format_size


class ResultScreen(ModalScreen[None]):
    """Shows clean operation results."""

    DEFAULT_CSS = """
    ResultScreen {
        align: center middle;
    }
    ResultScreen > Vertical {
        width: 70;
        max-height: 30;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    ResultScreen DataTable {
        height: 15;
    }
    ResultScreen Horizontal {
        align: center middle;
        margin-top: 1;
    }
    """

    def __init__(self, report: CleanReport, **kwargs):
        super().__init__(**kwargs)
        self._report = report

    def compose(self) -> ComposeResult:
        report = self._report
        mode = "Dry Run Results" if report.dry_run else "Clean Results"

        with Vertical():
            yield Label(f"[bold]{mode}[/bold]")

            if report.dry_run:
                yield Label(f"Estimated: [cyan]{format_size(report.total_estimated_bytes)}[/cyan]")
            else:
                yield Label(f"Reclaimed: [green]{format_size(report.total_reclaimed_bytes)}[/green]")

            yield Label(
                f"[green]✓ {len(report.succeeded)}[/green]  "
                f"[yellow]~ {len(report.skipped)}[/yellow]  "
                f"[red]✗ {len(report.failed)}[/red]"
            )

            table = DataTable()
            table.add_columns("Name", "Size", "Status")
            for r in report.results:
                status_style = {
                    "success": "green",
                    "dry_run": "blue",
                    "skipped": "yellow",
                    "failed": "red",
                }.get(str(r.status), "white")
                status_text = Text(str(r.status), style=status_style)
                size = format_size(r.reclaimed_bytes or r.candidate.size_bytes)
                table.add_row(r.candidate.name, size, status_text)
            yield table

            with Horizontal():
                yield Button("Close", id="close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(None)
