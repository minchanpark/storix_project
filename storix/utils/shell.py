"""Shell command utilities."""

import subprocess
from typing import Optional


def run(cmd: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """
    Run a shell command and return (returncode, stdout, stderr).
    Never raises on non-zero exit.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"
    except OSError as e:
        return -1, "", str(e)


def command_exists(name: str) -> bool:
    """Check if a shell command is available."""
    code, _, _ = run(["which", name], timeout=5)
    return code == 0
