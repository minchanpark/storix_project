"""Storix global constants."""

from pathlib import Path

APP_NAME = "storix"
VERSION = "0.1.0"

# Home directory
HOME = Path.home()

# Standard macOS paths
LIBRARY = HOME / "Library"
CACHES = LIBRARY / "Caches"
APPLICATION_SUPPORT = LIBRARY / "Application Support"
DEVELOPER = LIBRARY / "Developer"
MOBILE_DEVICE = LIBRARY / "MobileDevice"

# Xcode
DERIVED_DATA = DEVELOPER / "Xcode" / "DerivedData"
XCODE_ARCHIVES = LIBRARY / "Developer" / "Xcode" / "Archives"
IOS_DEVICE_SUPPORT = MOBILE_DEVICE / "Provisioning Profiles"
XCODE_DEVICE_SUPPORT = DEVELOPER / "Xcode" / "iOS DeviceSupport"
WATCHOS_DEVICE_SUPPORT = DEVELOPER / "Xcode" / "watchOS DeviceSupport"
TVOS_DEVICE_SUPPORT = DEVELOPER / "Xcode" / "tvOS DeviceSupport"
SIMULATOR_DEVICES = LIBRARY / "Developer" / "CoreSimulator" / "Devices"
COCOAPODS_CACHE = CACHES / "CocoaPods"

# Android
ANDROID_HOME = HOME / "Library" / "Android" / "sdk"
ANDROID_AVD = HOME / ".android" / "avd"
GRADLE_CACHE = HOME / ".gradle" / "caches"
ANDROID_USER_SDK = HOME / ".android"

# Flutter / Dart
FLUTTER_PUB_CACHE = HOME / ".pub-cache"
DART_PUB_CACHE = HOME / ".pub-cache"

# Node / npm / yarn / pnpm
NPM_CACHE = HOME / ".npm"
YARN_CACHE = HOME / "Library" / "Caches" / "yarn"
PNPM_STORE = HOME / "Library" / "pnpm" / "store"
BUN_CACHE = HOME / ".bun" / "install" / "cache"

# Python
PIP_CACHE = HOME / "Library" / "Caches" / "pip"
PYENV_VERSIONS = HOME / ".pyenv" / "versions"
VIRTUALENV_CACHE = HOME / ".virtualenvs"
UV_CACHE = HOME / ".cache" / "uv"
POETRY_CACHE = HOME / "Library" / "Caches" / "pypoetry"

# VS Code
VSCODE_CACHE = HOME / "Library" / "Application Support" / "Code" / "Cache"
VSCODE_CACHED_DATA = HOME / "Library" / "Application Support" / "Code" / "CachedData"
VSCODE_WORKSPACE_STORAGE = HOME / "Library" / "Application Support" / "Code" / "User" / "workspaceStorage"
VSCODE_LOGS = HOME / "Library" / "Application Support" / "Code" / "logs"

# General / Downloads
DOWNLOADS = HOME / "Downloads"
DESKTOP = HOME / "Desktop"
DOCUMENTS = HOME / "Documents"
MOVIES = HOME / "Movies"
TRASH = HOME / ".Trash"

# Risk thresholds
RISK_COLOR = {
    "safe": "green",
    "caution": "yellow",
    "dangerous": "red",
}

RISK_EMOJI = {
    "safe": "[green]✓[/green]",
    "caution": "[yellow]⚠[/yellow]",
    "dangerous": "[red]✗[/red]",
}

# Size thresholds for reporting (bytes)
SIZE_MB = 1024 * 1024
SIZE_GB = 1024 * SIZE_MB

# Minimum size to report a candidate (1 MB)
MIN_CANDIDATE_SIZE = SIZE_MB
