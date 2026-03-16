---
name: storix-clean-safety
description: Use when implementing or reviewing Storix scan, doctor, clean, risk classification, guard rules, path handling, reclaimable-size logic, or any filesystem deletion flow. Trigger on cleanup policies, deletion safety, category classification, and dry-run behavior.
---

# Storix Clean Safety

Use this skill for any task that can change what Storix detects, recommends, or deletes.

Typical triggers:

- "safe/caution/dangerous 분류를 추가해줘"
- "clean 로직 구현해줘"
- "guard path 규칙 검토해줘"
- "dry-run과 실제 삭제 흐름을 분리해줘"

## Read first

Open only what you need:

- `../../../AGENTS.md`
- `../../../dev/storix_prd.md` sections on risk policy and clean behavior
- `../../../dev/storix_tdd.md` sections on architecture and guard reuse

## Safety workflow

1. Identify the candidate type and category.
2. Assign `safe`, `caution`, or `dangerous` using the PRD examples.
3. Route deletion through shared service and guard logic, not ad-hoc shell commands.
4. Provide dry-run output before destructive execution.
5. Show expected reclaimable size, path, reason, and warning text.
6. Allow partial failure and summarize successes and failures separately.

## Risk policy

`safe`

- Rebuildable caches and build outputs
- Examples: `DerivedData`, `build`, `.dart_tool`, VS Code cache, `workspaceStorage`

`caution`

- Rebuildable, but costly or disruptive to restore
- Examples: Xcode Archives, Android `system-images`, AVD, pub cache, Gradle cache, CocoaPods cache, `ios/Pods`

`dangerous`

- User data or source artifacts may be mixed in
- Examples: `Downloads`, `Desktop`, `Documents`, `Movies`, project roots, original user files

## Hard rules

- `dangerous` must be excluded from default cleanup.
- `dangerous` must never be auto-deleted.
- `caution` requires explicit confirmation and visible explanation.
- Every clean flow must support dry-run.
- Never bypass central guard checks.
- Never assume root access or unrestricted system visibility.

## Implementation checklist

- Candidate data includes path, size, risk, reason, regenerability, and warning note.
- Known-path scanning comes before expensive recursive scans.
- Missing paths and permission errors do not crash the whole run.
- Cleanup reports show reclaimed, skipped, and failed items separately.

## Test checklist

- risk classification
- dry-run parity with real selection
- guard rejection for dangerous paths
- confirmation requirements for caution
- partial failure handling
- missing path and permission error handling
