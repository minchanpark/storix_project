"""Console (Rich) presenter for CLI output."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

from storix.models.summary import ScanSummary, CategorySummary
from storix.models.clean_result import CleanReport
from storix.models.candidate import Candidate
from storix.models.enums import RiskLevel
from storix.utils.size import format_size

console = Console()

RISK_STYLE = {
    RiskLevel.SAFE: "green",
    RiskLevel.CAUTION: "yellow",
    RiskLevel.DANGEROUS: "red",
}

RISK_LABEL = {
    RiskLevel.SAFE: "safe",
    RiskLevel.CAUTION: "caution",
    RiskLevel.DANGEROUS: "dangerous",
}


def _risk_text(risk: RiskLevel) -> Text:
    style = RISK_STYLE[risk]
    label = RISK_LABEL[risk]
    icon = {"safe": "✓", "caution": "⚠", "dangerous": "✗"}[label]
    return Text(f"{icon} {label}", style=style)


def print_disk_summary(summary: ScanSummary) -> None:
    disk = summary.disk
    used_pct = disk.used_pct
    bar_width = 30
    filled = int(bar_width * used_pct / 100)
    bar = "[green]" + "█" * filled + "[/green]" + "░" * (bar_width - filled)

    panel = Panel(
        f"[bold]Volume:[/bold] {disk.volume}\n"
        f"[bold]Total:[/bold]  {format_size(disk.total_bytes)}\n"
        f"[bold]Used:[/bold]   {format_size(disk.used_bytes)} ({used_pct:.1f}%)\n"
        f"[bold]Free:[/bold]   {format_size(disk.free_bytes)}\n\n"
        f"{bar}",
        title="[bold blue]Disk Usage[/bold blue]",
        border_style="blue",
    )
    console.print(panel)


def print_scan_summary(summary: ScanSummary) -> None:
    print_disk_summary(summary)

    if not summary.categories:
        console.print("[yellow]No cleanup candidates found.[/yellow]")
        return

    total = summary.total_reclaimable_bytes
    safe = summary.safe_reclaimable_bytes
    console.print(
        f"\n[bold]Total reclaimable:[/bold] [cyan]{format_size(total)}[/cyan]  "
        f"([green]safe: {format_size(safe)}[/green])"
    )

    for cat_summary in summary.categories:
        print_category_summary(cat_summary)


def print_category_summary(cat: CategorySummary) -> None:
    if not cat.candidates:
        return

    table = Table(
        title=f"{cat.category.value.title()} — {format_size(cat.total_size_bytes)}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        expand=False,
    )
    table.add_column("Name", style="white", no_wrap=True)
    table.add_column("Size", justify="right", style="cyan")
    table.add_column("Risk", justify="center")
    table.add_column("Reason", style="dim")

    for c in sorted(cat.candidates, key=lambda x: x.size_bytes, reverse=True):
        risk_text = _risk_text(c.risk)
        table.add_row(c.name, format_size(c.size_bytes), risk_text, c.reason)

    console.print(table)


def print_doctor_summary(summary: ScanSummary) -> None:
    print_disk_summary(summary)

    if not summary.categories:
        console.print("[green]No cleanup candidates found. Your system looks clean![/green]")
        return

    total = summary.total_reclaimable_bytes
    safe = summary.safe_reclaimable_bytes

    console.print(f"\n[bold]Reclaimable storage:[/bold]")
    console.print(f"  Total:  [cyan]{format_size(total)}[/cyan]")
    console.print(f"  Safe:   [green]{format_size(safe)}[/green]")
    console.print(f"  Caution: [yellow]{format_size(total - safe)}[/yellow]")

    table = Table(
        title="Cleanup Candidates by Category",
        box=box.SIMPLE_HEAVY,
        header_style="bold",
        expand=False,
    )
    table.add_column("Category", style="bold white")
    table.add_column("Items", justify="right")
    table.add_column("Safe", justify="right", style="green")
    table.add_column("Caution", justify="right", style="yellow")
    table.add_column("Total", justify="right", style="cyan bold")

    for cat in summary.categories:
        table.add_row(
            cat.category.value.title(),
            str(cat.candidate_count),
            format_size(cat.safe_size_bytes),
            format_size(cat.caution_size_bytes),
            format_size(cat.total_size_bytes),
        )

    console.print(table)
    console.print("\n[dim]Run [bold]storix clean all-safe[/bold] to free up safe items.[/dim]")


def print_clean_report(report: CleanReport) -> None:
    prefix = "[dim](dry-run)[/dim] " if report.dry_run else ""

    if report.dry_run:
        console.print(
            f"\n{prefix}[bold]Estimated reclaimable:[/bold] "
            f"[cyan]{format_size(report.total_estimated_bytes)}[/cyan]"
        )
    else:
        console.print(
            f"\n[bold]Reclaimed:[/bold] [green]{format_size(report.total_reclaimed_bytes)}[/green]"
        )

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("Size", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Note", style="dim")

    for r in report.results:
        status_style = {
            "success": "green",
            "dry_run": "blue",
            "skipped": "yellow",
            "failed": "red",
        }.get(str(r.status), "white")
        status_text = Text(str(r.status), style=status_style)

        size_str = format_size(r.reclaimed_bytes or r.candidate.size_bytes)
        table.add_row(r.candidate.name, size_str, status_text, r.error)

    console.print(table)

    succeeded = len(report.succeeded)
    skipped = len(report.skipped)
    failed = len(report.failed)
    console.print(
        f"[green]✓ {succeeded} succeeded[/green]  "
        f"[yellow]~ {skipped} skipped[/yellow]  "
        f"[red]✗ {failed} failed[/red]"
    )
