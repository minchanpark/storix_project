"""Tests for guard rules."""

import pytest
from pathlib import Path

from storix.utils.guard import is_blocked, assert_safe, HOME


def test_home_is_blocked():
    blocked, reason = is_blocked(HOME)
    assert blocked
    assert "protected" in reason.lower() or "Protected" in reason


def test_downloads_is_blocked():
    blocked, _ = is_blocked(HOME / "Downloads")
    assert blocked


def test_desktop_is_blocked():
    blocked, _ = is_blocked(HOME / "Desktop")
    assert blocked


def test_documents_is_blocked():
    blocked, _ = is_blocked(HOME / "Documents")
    assert blocked


def test_root_is_blocked():
    blocked, _ = is_blocked(Path("/"))
    assert blocked


def test_system_is_blocked():
    blocked, _ = is_blocked(Path("/System"))
    assert blocked


def test_shallow_path_is_blocked():
    # /tmp is shallow (depth 2) - might or might not be blocked depending on resolve
    # Instead test a clearly shallow path
    blocked, _ = is_blocked(Path("/usr"))
    assert blocked


def test_deep_cache_path_is_not_blocked(tmp_path):
    # A deep temp path should not be blocked
    deep = tmp_path / "a" / "b" / "cache"
    deep.mkdir(parents=True)
    blocked, _ = is_blocked(deep)
    assert not blocked


def test_assert_safe_raises_for_blocked():
    with pytest.raises(ValueError, match="blocked"):
        assert_safe(HOME / "Downloads")


def test_assert_safe_passes_for_deep_path(tmp_path):
    deep = tmp_path / "a" / "b" / "cache"
    deep.mkdir(parents=True)
    # Should not raise
    assert_safe(deep)
