"""Tests for the Storix script entrypoint."""

import os
import subprocess
import sys
from pathlib import Path

from storix import __version__

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = PROJECT_ROOT / "storix" / "main.py"


def test_main_py_supports_direct_execution(tmp_path):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [sys.executable, str(MAIN_PATH), "--version"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    assert f"storix {__version__}" in result.stdout


def test_main_py_without_args_shows_help(tmp_path):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [sys.executable, str(MAIN_PATH)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )

    combined_output = result.stdout + result.stderr

    assert result.returncode == 0, combined_output
    assert "Usage:" in combined_output
    assert "Missing command" not in combined_output
