"""Main TUI screen."""

from typing import List

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.models.summary import ScanSummary
from storix.tui.widgets.category_list import CategoryList
from storix.tui.widgets.candidate_table import CandidateTable
from storix.tui.widgets.detail_panel import DetailPanel
from storix.tui.widgets.summary_bar import SummaryBar
from storix.tui.widgets.footer_bar import FooterBar


class MainScreen(Screen):
    """Main TUI screen with 3-panel layout."""

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("space", "toggle_select", "Select/Deselect"),
        Binding("a", "select_all", "Select All"),
        Binding("d", "dry_run", "Dry Run"),
        Binding("c", "clean", "Clean"),
        Binding("r", "rescan", "Rescan"),
        Binding("f", "filter_risk", "Filter Risk"),
        Binding("left,right", "switch_panel", "Switch Panel"),
    ]

    def __init__(self, scan_summary: ScanSummary, **kwargs):
        super().__init__(**kwargs)
        self._scan_summary = scan_summary
        self._current_category: Category = Category.ALL
        self._risk_filter: RiskLevel | None = None
        self._all_candidates: List[Candidate] = scan_summary.all_candidates

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        category_sizes = {
            cat.category: cat.total_size_bytes
            for cat in self._scan_summary.categories
        }

        with Horizontal():
            yield CategoryList(category_sizes=category_sizes, id="category-list")
            yield CandidateTable(candidates=self._all_candidates, id="candidate-table")
            yield DetailPanel(id="detail-panel")

        yield SummaryBar(id="summary-bar")
        yield FooterBar()

    def on_mount(self) -> None:
        self._update_summary_bar()

    def on_list_view_selected(self, event) -> None:
        """Handle category selection."""
        if event.item.id and event.item.id.startswith("cat-"):
            cat_value = event.item.id[4:]
            try:
                self._current_category = Category(cat_value)
            except ValueError:
                return
            self._filter_candidates()

    def on_data_table_cursor_moved(self, event) -> None:
        """Update detail panel when cursor moves."""
        table = self.query_one("#candidate-table", CandidateTable)
        candidate = table.current_candidate
        detail = self.query_one("#detail-panel", DetailPanel)
        detail.show_candidate(candidate)

    def action_toggle_select(self) -> None:
        table = self.query_one("#candidate-table", CandidateTable)
        candidate = table.current_candidate
        if candidate:
            table.toggle_selected(str(candidate.path))
            self._update_summary_bar()

    def action_select_all(self) -> None:
        table = self.query_one("#candidate-table", CandidateTable)
        if all(c.selected for c in table._candidates):
            table.deselect_all()
        else:
            table.select_all()
        self._update_summary_bar()

    def action_dry_run(self) -> None:
        from storix.tui.screens.confirm_screen import ConfirmScreen
        table = self.query_one("#candidate-table", CandidateTable)
        selected = table.selected_candidates
        if not selected:
            self.query_one("#summary-bar", SummaryBar).set_status(
                "[yellow]No items selected.[/yellow]"
            )
            return

        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                self._run_clean(selected, dry_run=True)

        self.app.push_screen(ConfirmScreen(selected, dry_run=True), _on_confirm)

    def action_clean(self) -> None:
        from storix.tui.screens.confirm_screen import ConfirmScreen
        table = self.query_one("#candidate-table", CandidateTable)
        selected = table.selected_candidates
        if not selected:
            self.query_one("#summary-bar", SummaryBar).set_status(
                "[yellow]No items selected.[/yellow]"
            )
            return

        def _on_confirm(confirmed: bool) -> None:
            if confirmed:
                self._run_clean(selected, dry_run=False)

        self.app.push_screen(ConfirmScreen(selected, dry_run=False), _on_confirm)

    def _run_clean(self, candidates: List[Candidate], dry_run: bool) -> None:
        from storix.services.clean_service import clean_selected
        from storix.tui.screens.result_screen import ResultScreen
        report = clean_selected(candidates, dry_run=dry_run, allow_caution=True)
        self.app.push_screen(ResultScreen(report))
        if not dry_run:
            self.action_rescan()

    def action_rescan(self) -> None:
        from storix.services.scan_service import run_scan
        summary = run_scan()
        self._scan_summary = summary
        self._all_candidates = summary.all_candidates
        self._filter_candidates()

    def action_filter_risk(self) -> None:
        """Cycle through risk filters: None → safe → caution → dangerous → None."""
        cycle = [None, RiskLevel.SAFE, RiskLevel.CAUTION, RiskLevel.DANGEROUS]
        idx = cycle.index(self._risk_filter)
        self._risk_filter = cycle[(idx + 1) % len(cycle)]
        self._filter_candidates()

        label = f"Filter: {self._risk_filter.value}" if self._risk_filter else "Filter: all"
        self.query_one("#summary-bar", SummaryBar).set_status(f"[cyan]{label}[/cyan]")

    def _filter_candidates(self) -> None:
        candidates = self._all_candidates

        if self._current_category != Category.ALL:
            candidates = [c for c in candidates if c.category == self._current_category]

        if self._risk_filter is not None:
            candidates = [c for c in candidates if c.risk == self._risk_filter]

        table = self.query_one("#candidate-table", CandidateTable)
        table.update_candidates(candidates)
        self._update_summary_bar()

    def _update_summary_bar(self) -> None:
        table = self.query_one("#candidate-table", CandidateTable)
        selected_bytes = sum(c.size_bytes for c in table.selected_candidates)
        total_bytes = self._scan_summary.total_reclaimable_bytes
        self.query_one("#summary-bar", SummaryBar).update_selection(selected_bytes, total_bytes)
