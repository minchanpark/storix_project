"""Markdown presenter."""

from storix.models.report import Report
from storix.services.report_service import to_markdown


def report_to_markdown(report: Report) -> str:
    return to_markdown(report)
