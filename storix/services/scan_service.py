"""Scan service: orchestrates all category scanners."""

from typing import List, Optional

from storix.models.enums import Category
from storix.models.summary import CategorySummary, ScanSummary
from storix.scanners import disk_scanner, xcode_scanner, android_scanner
from storix.scanners import flutter_scanner, node_scanner, python_scanner
from storix.scanners import vscode_scanner, general_scanner

ALL_CATEGORIES = [
    Category.XCODE,
    Category.ANDROID,
    Category.FLUTTER,
    Category.NODE,
    Category.PYTHON,
    Category.VSCODE,
    Category.GENERAL,
]


def _get_scanner(cat: Category):
    """Return the scanner function for the given category (looked up at call time)."""
    return {
        Category.XCODE: xcode_scanner.scan_xcode,
        Category.ANDROID: android_scanner.scan_android,
        Category.FLUTTER: flutter_scanner.scan_flutter,
        Category.NODE: node_scanner.scan_node,
        Category.PYTHON: python_scanner.scan_python,
        Category.VSCODE: vscode_scanner.scan_vscode,
        Category.GENERAL: general_scanner.scan_general,
    }.get(cat)


def run_scan(
    categories: Optional[List[Category]] = None,
    volume: str = "/",
) -> ScanSummary:
    """
    Run a full scan across selected categories.

    If categories is None, all categories are scanned.
    """
    if categories is None:
        categories = ALL_CATEGORIES

    disk = disk_scanner.scan_disk(volume)
    category_summaries: List[CategorySummary] = []

    for cat in categories:
        scanner = _get_scanner(cat)
        if scanner is None:
            continue
        try:
            candidates = scanner()
        except Exception:
            candidates = []

        if candidates:
            category_summaries.append(CategorySummary(
                category=cat,
                candidates=candidates,
            ))

    return ScanSummary(disk=disk, categories=category_summaries)
