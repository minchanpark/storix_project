"""Tests for TUI state logic (without launching the full app)."""

import pytest
from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.presenters.tui_adapter import candidate_to_row, format_detail
from storix.utils.size import format_size


def make_candidate(
    name: str = "TestItem",
    category: Category = Category.XCODE,
    risk: RiskLevel = RiskLevel.SAFE,
    size: int = 1024 * 1024 * 500,
    path: Path = Path("/tmp/test"),
    warning: str = "",
    description: str = "A test item",
) -> Candidate:
    return Candidate(
        path=path,
        name=name,
        category=category,
        risk=risk,
        size_bytes=size,
        reason="test reason",
        regenerable=True,
        warning=warning,
        description=description,
    )


def test_candidate_to_row_safe():
    c = make_candidate(risk=RiskLevel.SAFE)
    name, size, label, color = candidate_to_row(c)
    assert name == "TestItem"
    assert "safe" in label
    assert color == "green"


def test_candidate_to_row_caution():
    c = make_candidate(risk=RiskLevel.CAUTION)
    _, _, label, color = candidate_to_row(c)
    assert "caution" in label
    assert color == "yellow"


def test_candidate_to_row_dangerous():
    c = make_candidate(risk=RiskLevel.DANGEROUS)
    _, _, label, color = candidate_to_row(c)
    assert "dangerous" in label
    assert color == "red"


def test_format_detail_contains_key_info():
    c = make_candidate(
        name="Xcode DerivedData",
        risk=RiskLevel.SAFE,
        warning="",
        description="Build intermediates",
    )
    detail = format_detail(c)
    assert "Xcode DerivedData" in detail
    assert "safe" in detail.lower()
    assert "Build intermediates" in detail


def test_format_detail_shows_warning():
    c = make_candidate(
        warning="Careful with this one",
        risk=RiskLevel.CAUTION,
    )
    detail = format_detail(c)
    assert "Careful with this one" in detail


def test_format_detail_no_warning_omits_warning_section():
    c = make_candidate(warning="", risk=RiskLevel.SAFE)
    detail = format_detail(c)
    assert "Warning" not in detail


def test_candidate_selected_default_false():
    c = make_candidate()
    assert c.selected is False


def test_candidate_toggle_selected():
    c = make_candidate()
    c.selected = True
    assert c.selected is True
    c.selected = False
    assert c.selected is False


def test_size_format_in_row():
    c = make_candidate(size=5 * 1024**3)  # 5 GB
    _, size_str, _, _ = candidate_to_row(c)
    assert "GB" in size_str
