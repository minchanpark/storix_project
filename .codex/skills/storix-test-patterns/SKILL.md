---
name: storix-test-patterns
description: Use when adding or updating Storix tests for services, scanners, cleaners, guard rules, project scanning, or TUI state. Trigger on pytest coverage, tmp_path fixture design, destructive-flow validation, and regression testing for scan and clean behavior.
---

# Storix Test Patterns

Use this skill whenever a Storix change needs tests or a review of test coverage.

Typical triggers:

- "이 기능 테스트도 추가해줘"
- "scan/clean 회귀 테스트를 짜줘"
- "tmp_path로 파일시스템 fixture 만들어줘"
- "TUI 상태 테스트를 어떻게 잡아야 해?"

## Read first

Open only what you need:

- `../../../AGENTS.md`
- `../../../dev/storix_prd.md` sections on risk policy and functional expectations
- `../../../dev/storix_tdd.md` target test layout

## Testing workflow

1. Start at the service layer unless the change is purely presentational.
2. Use `pytest` and `tmp_path` for filesystem-heavy behavior.
3. Model destructive cases with temporary directories, never real user folders.
4. Add focused TUI state tests when selection, filters, or confirmation flows change.
5. Report any untested residual risk if a full test cannot be run.

## Minimum regression matrix

- category scan result correctness
- reclaimable-size calculation
- risk classification
- dry-run behavior
- clean success path
- clean partial failure path
- guard enforcement
- project scan detection

## Edge cases to prefer

- missing path
- empty directory
- permission denied
- skipped dangerous item
- caution item requiring confirmation
- absent optional tooling or category paths

## Good patterns

- keep fixtures small and explicit
- assert both human-facing and structured outputs when behavior changes
- test behavior, not implementation details
- isolate TUI state transitions from unrelated rendering concerns
