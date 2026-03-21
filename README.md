# Storix

Storix is a macOS-first storage analyzer and cleanup CLI for developers and power users.

It helps answer three questions quickly:

- What is using the most disk space?
- What can I safely clean?
- How much space can I reclaim?

Storix ships as a CLI and TUI, with shared service logic behind both interfaces.

## Features

- Fast known-path scanning for common developer caches and build artifacts
- Risk classification with `safe`, `caution`, and `dangerous`
- Dry-run cleanup previews before deletion
- Safe-only cleanup flow for rebuildable artifacts
- Script-friendly JSON and Markdown output
- Interactive Textual TUI for browsing and cleaning candidates

## Supported Categories

- Xcode
- Android
- Flutter / Dart
- Node / Web
- Python
- VS Code
- General user folders

## Install

### From PyPI with `pipx`

```bash
pipx install storix-cli
```

After install, the command is still:

```bash
storix --help
```

### From GitHub with `pipx`

This is the most practical way to share the CLI before a public PyPI package name is finalized.

```bash
pipx install "git+https://github.com/minchanpark/storix_project.git"
```

After install, the command is still:

```bash
storix --help
```

### Local Development Install

```bash
python -m pip install -e ".[dev]"
storix --help
```

## Quick Start

```bash
storix scan
storix doctor
storix top
storix clean all-safe --dry-run
storix clean all-safe --caution --dry-run
storix clean all-safe --yes
storix tui
```

## Safety Model

- `safe`: rebuildable caches and build outputs
- `caution`: rebuildable, but time-consuming or disruptive to restore
- `dangerous`: user data or source artifacts that are excluded from default cleanup

Storix always supports dry-run flows and routes deletion through shared guard checks.

## Example Commands

```bash
storix scan --json
storix doctor --markdown
storix clean xcode --dry-run
storix clean all-safe --caution --yes
storix clean python --yes
storix projects scan ~/work/myapp ~/work/another-app
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
```

## Packaging Notes

- The PyPI package name is `storix-cli`
- The installed CLI command is `storix`
- The package currently targets Python 3.11+
- The project is designed for macOS workflows
