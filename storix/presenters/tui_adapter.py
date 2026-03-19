"""TUI adapter: converts domain models to TUI-friendly data structures."""

from typing import List

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


def candidate_to_row(c: Candidate) -> tuple[str, str, str, str]:
    """Convert candidate to (name, size, risk_label, risk_color)."""
    icon = RISK_ICON[c.risk]
    label = f"{icon} {c.risk.value}"
    color = RISK_COLOR[c.risk]
    return (c.name, format_size(c.size_bytes), label, color)


def format_detail(c: Candidate) -> str:
    """Format candidate detail text for the TUI detail panel."""
    lines = [
        f"[bold]{c.name}[/bold]",
        f"",
        f"[bold]Path:[/bold] {c.path}",
        f"[bold]Size:[/bold] {format_size(c.size_bytes)}",
        f"[bold]Category:[/bold] {c.category.value.title()}",
        f"[bold]Risk:[/bold] [{RISK_COLOR[c.risk]}]{c.risk.value}[/{RISK_COLOR[c.risk]}]",
        f"",
        f"[bold]Description:[/bold]",
        f"{c.description or c.reason}",
        f"",
        f"[bold]Regenerable:[/bold] {'Yes' if c.regenerable else 'No'}",
    ]
    if c.warning:
        lines += ["", f"[yellow bold]⚠ Warning:[/yellow bold]", f"[yellow]{c.warning}[/yellow]"]
    return "\n".join(lines)
