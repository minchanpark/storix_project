---
name: storix-cli-tui-delivery
description: Use when building or refining Storix CLI commands, Rich output, Textual TUI screens, presenters, or reports. Trigger on scan and doctor output, clean confirmations, TUI layout, command options, report formatting, and shared service to UI wiring.
---

# Storix CLI and TUI Delivery

Use this skill when the task is user-visible and touches command behavior or terminal UI.

Typical triggers:

- "scan/doctor 출력 포맷을 다듬어줘"
- "Typer 명령을 추가해줘"
- "Textual TUI 메인 화면을 설계해줘"
- "JSON/Markdown 리포트를 연결해줘"

## Read first

Open only the relevant parts of:

- `../../../AGENTS.md`
- `../../../dev/storix_prd.md` sections on interface strategy, TUI UX, and command examples
- `../../../dev/storix_tdd.md` module layout for CLI, presenters, and TUI

## Delivery workflow

1. Start from the shared service or presenter that should own the behavior.
2. Keep CLI script-friendly and TUI human-friendly without duplicating business logic.
3. Preserve command naming and option consistency from the PRD.
4. Make risk, reclaimable size, and reasoning visible in the UI.
5. If TUI state changes, update TUI state tests with the implementation.

## CLI rules

- Prefer `Typer` for command surface and `Rich` for readable output.
- Keep machine-readable output stable for `--json` and `--markdown`.
- Support the expected flows for `scan`, `doctor`, `clean`, `projects scan`, `report`, and `tui`.
- Preserve automation-friendly behavior for `clean all-safe --yes`.

## TUI rules

- Keep the three-panel structure: category list, candidate list, detail panel.
- Preserve a bottom area for status, keybinds, and total selected reclaimable size.
- Distinguish dry-run from real clean clearly.
- Require a confirmation flow before destructive actions.
- Keep the expected keybind vocabulary when possible: `↑/↓`, `←/→`, `space`, `a`, `d`, `c`, `r`, `f`, `q`.

## Output checklist

- path
- size
- risk
- detection reason
- regenerability
- warning notes
- expected reclaimable total
