"""Tests for project_scanner."""

import pytest
from pathlib import Path

from storix.scanners.project_scanner import (
    detect_project_type,
    scan_project,
    scan_projects,
)
from storix.models.enums import RiskLevel, Category


def make_flutter_project(root: Path) -> Path:
    root.mkdir(parents=True)
    (root / "pubspec.yaml").write_text("name: myapp\n")
    build = root / "build"
    build.mkdir()
    (build / "output.bin").write_bytes(b"x" * (2 * 1024 * 1024))  # 2 MB
    dart_tool = root / ".dart_tool"
    dart_tool.mkdir()
    (dart_tool / "cache.json").write_text("{}")
    return root


def make_node_project(root: Path) -> Path:
    root.mkdir(parents=True)
    (root / "package.json").write_text('{"name": "myapp"}')
    node_modules = root / "node_modules"
    node_modules.mkdir()
    (node_modules / "lib.js").write_bytes(b"x" * (5 * 1024 * 1024))  # 5 MB
    return root


def make_python_project(root: Path) -> Path:
    root.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'myapp'\n")
    pycache = root / "__pycache__"
    pycache.mkdir()
    (pycache / "mod.pyc").write_bytes(b"x" * 1024)
    return root


def test_detect_flutter_project(tmp_path):
    p = tmp_path / "flutter_app"
    p.mkdir()
    (p / "pubspec.yaml").touch()
    assert detect_project_type(p) == "flutter"


def test_detect_node_project(tmp_path):
    p = tmp_path / "node_app"
    p.mkdir()
    (p / "package.json").touch()
    assert detect_project_type(p) == "node"


def test_detect_python_project(tmp_path):
    p = tmp_path / "py_app"
    p.mkdir()
    (p / "pyproject.toml").touch()
    assert detect_project_type(p) == "python"


def test_detect_unknown_project(tmp_path):
    p = tmp_path / "unknown"
    p.mkdir()
    assert detect_project_type(p) is None


def test_scan_flutter_project(tmp_path):
    proj = make_flutter_project(tmp_path / "flutter_app")
    candidates = scan_project(proj)

    names = [c.name for c in candidates]
    assert any("build" in n for n in names)
    assert any(".dart_tool" in n for n in names)


def test_scan_flutter_build_is_safe(tmp_path):
    proj = make_flutter_project(tmp_path / "flutter_app")
    candidates = scan_project(proj)
    build_candidates = [c for c in candidates if "build" in c.name]
    assert all(c.risk == RiskLevel.SAFE for c in build_candidates)


def test_scan_node_project(tmp_path):
    proj = make_node_project(tmp_path / "node_app")
    candidates = scan_project(proj)
    names = [c.name for c in candidates]
    assert any("node_modules" in n for n in names)


def test_scan_node_modules_is_caution(tmp_path):
    proj = make_node_project(tmp_path / "node_app")
    candidates = scan_project(proj)
    nm = [c for c in candidates if "node_modules" in c.name]
    assert all(c.risk == RiskLevel.CAUTION for c in nm)


def test_scan_python_project(tmp_path):
    proj = make_python_project(tmp_path / "py_app")
    candidates = scan_project(proj)
    names = [c.name for c in candidates]
    assert any("__pycache__" in n for n in names)


def test_scan_projects_multi_root(tmp_path):
    root1 = tmp_path / "root1"
    root2 = tmp_path / "root2"
    make_flutter_project(root1 / "app1")
    make_node_project(root2 / "app2")

    candidates = scan_projects([root1, root2])
    categories = {c.category for c in candidates}
    assert Category.FLUTTER in categories
    assert Category.NODE in categories


def test_scan_projects_missing_root(tmp_path):
    missing = tmp_path / "does_not_exist"
    candidates = scan_projects([missing])
    assert candidates == []


def test_scan_project_unknown_type_returns_empty(tmp_path):
    unknown = tmp_path / "unknown"
    unknown.mkdir()
    candidates = scan_project(unknown)
    assert candidates == []
