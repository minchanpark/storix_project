"""Confirmation screen for destructive actions."""

from typing import List

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from textual.containers import Vertical, Horizontal

from storix.models.candidate import Candidate
from storix.utils.size import format_size


class ConfirmScreen(ModalScreen[bool]):
    """Modal confirmation dialog before clean."""

    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }
    ConfirmScreen > Vertical {
        width: 60;
        max-height: 20;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    ConfirmScreen Label {
        margin-bottom: 1;
    }
    ConfirmScreen Horizontal {
        align: center middle;
        margin-top: 1;
    }
    ConfirmScreen Button {
        margin: 0 1;
    }
    """

    def __init__(self, candidates: List[Candidate], dry_run: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._candidates = candidates
        self._dry_run = dry_run

    def compose(self) -> ComposeResult:
        total = sum(c.size_bytes for c in self._candidates)
        mode = "DRY RUN" if self._dry_run else "DELETE"

        with Vertical():
            yield Label(f"[bold red]Confirm {mode}[/bold red]")
            yield Label(
                f"[bold]{len(self._candidates)}[/bold] items selected  "
                f"([cyan]{format_size(total)}[/cyan])"
            )
            if not self._dry_run:
                yield Static("[yellow]⚠ This will permanently delete the selected items.[/yellow]")
            with Horizontal():
                yield Button("Cancel", id="cancel", variant="default")
                yield Button(
                    f"Run {mode}" if self._dry_run else "Delete",
                    id="confirm",
                    variant="error" if not self._dry_run else "primary",
                )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm")
