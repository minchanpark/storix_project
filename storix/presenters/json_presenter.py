"""JSON presenter."""

import json
from storix.models.summary import ScanSummary
from storix.models.clean_result import CleanReport
from storix.models.report import Report


def scan_to_json(summary: ScanSummary, indent: int = 2) -> str:
    return json.dumps(summary.to_dict(), indent=indent, ensure_ascii=False)


def clean_to_json(report: CleanReport, indent: int = 2) -> str:
    return json.dumps(report.to_dict(), indent=indent, ensure_ascii=False)


def report_to_json(report: Report, indent: int = 2) -> str:
    return json.dumps(report.to_dict(), indent=indent, ensure_ascii=False)
