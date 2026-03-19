"""Report service: generate JSON/Markdown reports."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from storix.models.report import Report
from storix.models.summary import ScanSummary
from storix.models.clean_result import CleanReport
from storix.utils.size import format_size


def build_report(
    scan: Optional[ScanSummary] = None,
    clean: Optional[CleanReport] = None,
) -> Report:
    """Build a Report from scan and/or clean results."""
    return Report(
        generated_at=datetime.now(),
        scan=scan,
        clean=clean,
    )


def to_json(report: Report, indent: int = 2) -> str:
    """Serialize report to JSON string."""
    return json.dumps(report.to_dict(), indent=indent, ensure_ascii=False)


def to_markdown(report: Report) -> str:
    """Serialize report to Markdown string."""
    lines = []
    lines.append("# Storix Report")
    lines.append(f"\nGenerated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")

    if report.scan:
        scan = report.scan
        disk = scan.disk
        lines.append("\n## Disk Usage")
        lines.append(f"- Total: {format_size(disk.total_bytes)}")
        lines.append(f"- Used: {format_size(disk.used_bytes)} ({disk.used_pct:.1f}%)")
        lines.append(f"- Free: {format_size(disk.free_bytes)}")
        lines.append(f"- Total reclaimable: **{format_size(scan.total_reclaimable_bytes)}**")
        lines.append(f"- Safe reclaimable: **{format_size(scan.safe_reclaimable_bytes)}**")

        lines.append("\n## Cleanup Candidates")
        for cat in scan.categories:
            lines.append(f"\n### {cat.category.value.title()} ({format_size(cat.total_size_bytes)})")
            for c in cat.candidates:
                risk_icon = {"safe": "✓", "caution": "⚠", "dangerous": "✗"}.get(str(c.risk), "?")
                lines.append(f"- [{risk_icon}] **{c.name}** — {format_size(c.size_bytes)}")
                lines.append(f"  - Path: `{c.path}`")
                lines.append(f"  - Risk: {c.risk}")
                lines.append(f"  - Reason: {c.reason}")
                if c.warning:
                    lines.append(f"  - ⚠ Warning: {c.warning}")

    if report.clean:
        clean = report.clean
        lines.append("\n## Clean Results")
        lines.append(f"- Dry run: {'Yes' if clean.dry_run else 'No'}")
        lines.append(f"- Reclaimed: **{format_size(clean.total_reclaimed_bytes)}**")
        lines.append(f"- Succeeded: {len(clean.succeeded)}")
        lines.append(f"- Skipped: {len(clean.skipped)}")
        lines.append(f"- Failed: {len(clean.failed)}")

        if clean.failed:
            lines.append("\n### Failures")
            for r in clean.failed:
                lines.append(f"- `{r.candidate.path}`: {r.error}")

    return "\n".join(lines)


def save_report(report: Report, path: Path, fmt: str = "json") -> None:
    """Save a report to a file."""
    if fmt == "json":
        path.write_text(to_json(report), encoding="utf-8")
    elif fmt == "markdown":
        path.write_text(to_markdown(report), encoding="utf-8")
    else:
        raise ValueError(f"Unknown format: {fmt}")
