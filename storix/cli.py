"""Storix CLI entry point."""

import json
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from storix import __version__

app = typer.Typer(
    name="storix",
    help="macOS storage analyzer and cleaner for developers.",
    add_completion=False,
    rich_markup_mode="rich",
)
projects_app = typer.Typer(help="Project artifact scanning commands.")
app.add_typer(projects_app, name="projects")

console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"storix {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version."
    ),
) -> None:
    pass


# ─── scan ─────────────────────────────────────────────────────────────────────

@app.command()
def scan(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
    markdown: bool = typer.Option(False, "--markdown", help="Output as Markdown."),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category."),
) -> None:
    """Scan local storage and show cleanup candidates."""
    from storix.services.scan_service import run_scan
    from storix.models.enums import Category
    from storix.presenters.console_presenter import print_scan_summary
    from storix.presenters.json_presenter import scan_to_json
    from storix.services.report_service import to_markdown, build_report

    cats = None
    if category:
        try:
            cats = [Category(category.lower())]
        except ValueError:
            console.print(f"[red]Unknown category: {category}[/red]")
            raise typer.Exit(1)

    with console.status("[bold green]Scanning..."):
        summary = run_scan(categories=cats)

    if json_output:
        console.print(scan_to_json(summary))
    elif markdown:
        report = build_report(scan=summary)
        console.print(to_markdown(report))
    else:
        print_scan_summary(summary)


# ─── top ──────────────────────────────────────────────────────────────────────

@app.command()
def top(
    count: int = typer.Option(10, "--count", "-n", help="Number of top items to show."),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
) -> None:
    """Show top N largest cleanup candidates."""
    from storix.services.scan_service import run_scan
    from storix.presenters.console_presenter import print_category_summary
    from storix.models.summary import CategorySummary
    from storix.models.enums import Category

    with console.status("[bold green]Scanning..."):
        summary = run_scan()

    all_candidates = sorted(summary.all_candidates, key=lambda c: c.size_bytes, reverse=True)[:count]

    if json_output:
        console.print(json.dumps([c.to_dict() for c in all_candidates], indent=2))
    else:
        from rich.table import Table
        from rich import box
        from storix.utils.size import format_size
        from storix.presenters.console_presenter import _risk_text

        table = Table(
            title=f"Top {count} Cleanup Candidates",
            box=box.ROUNDED,
            header_style="bold magenta",
        )
        table.add_column("Name", style="white")
        table.add_column("Category", style="dim")
        table.add_column("Size", justify="right", style="cyan")
        table.add_column("Risk", justify="center")

        for c in all_candidates:
            table.add_row(c.name, c.category.value, format_size(c.size_bytes), _risk_text(c.risk))

        console.print(table)


# ─── doctor ───────────────────────────────────────────────────────────────────

@app.command()
def doctor(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
    markdown: bool = typer.Option(False, "--markdown", help="Output as Markdown."),
) -> None:
    """Show categorized cleanup summary and recommendations."""
    from storix.services.doctor_service import run_doctor
    from storix.presenters.console_presenter import print_doctor_summary
    from storix.presenters.json_presenter import scan_to_json
    from storix.services.report_service import to_markdown, build_report

    with console.status("[bold green]Analyzing..."):
        summary = run_doctor()

    if json_output:
        console.print(scan_to_json(summary))
    elif markdown:
        report = build_report(scan=summary)
        console.print(to_markdown(report))
    else:
        print_doctor_summary(summary)


# ─── clean ────────────────────────────────────────────────────────────────────

clean_app = typer.Typer(help="Clean storage by category or risk level.")
app.add_typer(clean_app, name="clean")


@clean_app.command("all-safe")
def clean_all_safe(
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without deleting."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation."),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
) -> None:
    """Clean all safe candidates across all categories."""
    from storix.services.clean_service import clean_all_safe as _clean_all_safe
    from storix.presenters.console_presenter import print_clean_report
    from storix.presenters.json_presenter import clean_to_json
    from storix.utils.confirm import confirm

    if not dry_run and not yes:
        if not confirm("Clean all safe items?", default=False):
            console.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(0)

    with console.status("[bold green]Cleaning..."):
        report = _clean_all_safe(dry_run=dry_run)

    if json_output:
        console.print(clean_to_json(report))
    else:
        print_clean_report(report)


@clean_app.command("xcode")
def clean_xcode(
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without deleting."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation."),
    caution: bool = typer.Option(False, "--caution", help="Include caution items."),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
) -> None:
    """Clean Xcode build artifacts."""
    _run_category_clean("xcode", dry_run, yes, caution, json_output)


@clean_app.command("android")
def clean_android(
    dry_run: bool = typer.Option(False, "--dry-run"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    caution: bool = typer.Option(False, "--caution"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Clean Android build artifacts."""
    _run_category_clean("android", dry_run, yes, caution, json_output)


@clean_app.command("flutter")
def clean_flutter(
    dry_run: bool = typer.Option(False, "--dry-run"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    caution: bool = typer.Option(False, "--caution"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Clean Flutter/Dart artifacts."""
    _run_category_clean("flutter", dry_run, yes, caution, json_output)


@clean_app.command("node")
def clean_node(
    dry_run: bool = typer.Option(False, "--dry-run"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    caution: bool = typer.Option(False, "--caution"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Clean Node/Web artifacts."""
    _run_category_clean("node", dry_run, yes, caution, json_output)


@clean_app.command("python")
def clean_python(
    dry_run: bool = typer.Option(False, "--dry-run"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    caution: bool = typer.Option(False, "--caution"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Clean Python artifacts."""
    _run_category_clean("python", dry_run, yes, caution, json_output)


@clean_app.command("vscode")
def clean_vscode(
    dry_run: bool = typer.Option(False, "--dry-run"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    caution: bool = typer.Option(False, "--caution"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Clean VS Code artifacts."""
    _run_category_clean("vscode", dry_run, yes, caution, json_output)


def _run_category_clean(
    category: str,
    dry_run: bool,
    yes: bool,
    allow_caution: bool,
    json_output: bool,
) -> None:
    from storix.services.clean_service import clean_by_category
    from storix.models.enums import Category
    from storix.presenters.console_presenter import print_clean_report
    from storix.presenters.json_presenter import clean_to_json
    from storix.utils.confirm import confirm

    try:
        cat = Category(category)
    except ValueError:
        console.print(f"[red]Unknown category: {category}[/red]")
        raise typer.Exit(1)

    if not dry_run and not yes:
        if not confirm(f"Clean {category} items?", default=False):
            console.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(0)

    with console.status(f"[bold green]Cleaning {category}..."):
        report = clean_by_category(cat, dry_run=dry_run, allow_caution=allow_caution)

    if json_output:
        console.print(clean_to_json(report))
    else:
        print_clean_report(report)


# ─── projects scan ────────────────────────────────────────────────────────────

@projects_app.command("scan")
def projects_scan(
    paths: List[Path] = typer.Argument(..., help="Project root directories to scan."),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
    markdown: bool = typer.Option(False, "--markdown", help="Output as Markdown."),
    clean: bool = typer.Option(False, "--clean", help="Clean found artifacts."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without deleting."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation."),
    caution: bool = typer.Option(False, "--caution", help="Include caution items."),
) -> None:
    """Scan project directories for build artifacts."""
    from storix.services.project_service import run_project_scan, clean_project_artifacts
    from storix.presenters.console_presenter import print_scan_summary, print_clean_report
    from storix.presenters.json_presenter import scan_to_json, clean_to_json
    from storix.services.report_service import to_markdown, build_report
    from storix.utils.confirm import confirm

    expanded = [p.expanduser().resolve() for p in paths]

    with console.status("[bold green]Scanning projects..."):
        summary = run_project_scan(expanded)

    if json_output:
        console.print(scan_to_json(summary))
    elif markdown:
        report = build_report(scan=summary)
        console.print(to_markdown(report))
    else:
        print_scan_summary(summary)

    if clean:
        if not dry_run and not yes:
            if not confirm("Clean found artifacts?", default=False):
                console.print("[yellow]Aborted.[/yellow]")
                raise typer.Exit(0)

        with console.status("[bold green]Cleaning..."):
            clean_report = clean_project_artifacts(expanded, dry_run=dry_run, allow_caution=caution)

        if json_output:
            console.print(clean_to_json(clean_report))
        else:
            print_clean_report(clean_report)


# ─── report ───────────────────────────────────────────────────────────────────

@app.command()
def report(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path."),
    fmt: str = typer.Option("json", "--format", "-f", help="Output format: json or markdown."),
) -> None:
    """Generate a full report from a fresh scan."""
    from storix.services.scan_service import run_scan
    from storix.services.report_service import build_report, to_json, to_markdown, save_report

    with console.status("[bold green]Scanning..."):
        summary = run_scan()

    rep = build_report(scan=summary)

    if output:
        save_report(rep, output, fmt=fmt)
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        if fmt == "json":
            console.print(to_json(rep))
        else:
            console.print(to_markdown(rep))


# ─── tui ──────────────────────────────────────────────────────────────────────

@app.command()
def tui() -> None:
    """Launch the interactive TUI."""
    from storix.tui.app import run_tui
    run_tui()
