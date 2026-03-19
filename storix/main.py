"""Storix main entry point.

Supports both package execution (`python -m storix.main`) and direct file
execution (`python storix/main.py`) without breaking package imports.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _load_app():
    if __package__ in {None, ""}:
        project_root = Path(__file__).resolve().parent.parent
        project_root_str = str(project_root)
        if project_root_str not in sys.path:
            sys.path.insert(0, project_root_str)
        from storix.cli import app as cli_app
    else:
        from .cli import app as cli_app

    return cli_app


app = _load_app()

if __name__ == "__main__":
    app()
