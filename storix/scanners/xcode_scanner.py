"""Xcode cleanup candidate scanner."""

from pathlib import Path
from typing import List

from storix.models.candidate import Candidate
from storix.models.enums import Category, RiskLevel
from storix.utils.fs import expand_path, path_exists
from storix.utils.size import dir_size

HOME = Path.home()


def scan_xcode() -> List[Candidate]:
    """Scan for Xcode-related cleanup candidates."""
    candidates: List[Candidate] = []

    # DerivedData
    derived_data = expand_path("~/Library/Developer/Xcode/DerivedData")
    if path_exists(derived_data):
        size = dir_size(derived_data)
        if size > 0:
            candidates.append(Candidate(
                path=derived_data,
                name="Xcode DerivedData",
                category=Category.XCODE,
                risk=RiskLevel.SAFE,
                size_bytes=size,
                reason="Build artifacts regenerated on next build",
                regenerable=True,
                description="Xcode build intermediates and products. Safe to delete; Xcode will rebuild on next build.",
                warning="",
            ))

    # Archives
    archives = expand_path("~/Library/Developer/Xcode/Archives")
    if path_exists(archives):
        size = dir_size(archives)
        if size > 0:
            candidates.append(Candidate(
                path=archives,
                name="Xcode Archives",
                category=Category.XCODE,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="App archives; may be needed to re-submit or symbolicate crash logs",
                regenerable=True,
                description="Xcode app archives. Can be recreated but you will lose the ability to symbolicate old crash reports.",
                warning="Deleting archives removes the ability to re-submit to App Store or symbolicate crash logs from released builds.",
            ))

    # iOS DeviceSupport
    ios_device_support = expand_path("~/Library/Developer/Xcode/iOS DeviceSupport")
    if path_exists(ios_device_support):
        size = dir_size(ios_device_support)
        if size > 0:
            candidates.append(Candidate(
                path=ios_device_support,
                name="iOS DeviceSupport",
                category=Category.XCODE,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Device debugging symbols; re-downloaded when device reconnects",
                regenerable=True,
                description="Per-iOS-version debugging support files. Re-downloaded automatically when device is connected.",
                warning="Remove only versions you no longer test against.",
            ))

    # watchOS DeviceSupport
    watchos_device_support = expand_path("~/Library/Developer/Xcode/watchOS DeviceSupport")
    if path_exists(watchos_device_support):
        size = dir_size(watchos_device_support)
        if size > 0:
            candidates.append(Candidate(
                path=watchos_device_support,
                name="watchOS DeviceSupport",
                category=Category.XCODE,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="watchOS device debugging symbols",
                regenerable=True,
                description="Per-watchOS-version debugging support files.",
                warning="Remove only versions you no longer test against.",
            ))

    # Simulator Devices
    simulator_devices = expand_path("~/Library/Developer/CoreSimulator/Devices")
    if path_exists(simulator_devices):
        size = dir_size(simulator_devices)
        if size > 0:
            candidates.append(Candidate(
                path=simulator_devices,
                name="Simulator Devices",
                category=Category.XCODE,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="iOS/watchOS simulator data; can be recreated via Xcode",
                regenerable=True,
                description="Simulator runtime data. Can be pruned with `xcrun simctl delete unavailable`.",
                warning="Deleting removes all simulator app data. Use 'xcrun simctl delete unavailable' for safer cleanup.",
            ))

    # CocoaPods cache
    cocoapods_cache = expand_path("~/Library/Caches/CocoaPods")
    if path_exists(cocoapods_cache):
        size = dir_size(cocoapods_cache)
        if size > 0:
            candidates.append(Candidate(
                path=cocoapods_cache,
                name="CocoaPods Cache",
                category=Category.XCODE,
                risk=RiskLevel.CAUTION,
                size_bytes=size,
                reason="Cached CocoaPods downloads; re-downloaded on next pod install",
                regenerable=True,
                description="CocoaPods download cache. Will be re-fetched on next `pod install`.",
                warning="",
            ))

    return candidates
