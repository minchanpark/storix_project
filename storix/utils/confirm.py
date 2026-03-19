"""User confirmation utilities."""

import sys


def confirm(prompt: str, default: bool = False) -> bool:
    """
    Prompt the user for yes/no confirmation.
    Returns True if confirmed, False otherwise.
    """
    suffix = " [Y/n] " if default else " [y/N] "
    try:
        answer = input(prompt + suffix).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False

    if answer == "":
        return default
    return answer in ("y", "yes")
