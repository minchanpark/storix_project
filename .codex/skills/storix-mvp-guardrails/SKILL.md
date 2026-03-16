---
name: storix-mvp-guardrails
description: Use when planning, scoping, or implementing Storix features so work stays aligned with the PRD/TDD, MVP boundaries, macOS focus, CLI plus TUI goals, and shared service architecture. Trigger on feature proposals, refactors, roadmap questions, or requirement interpretation.
---

# Storix MVP Guardrails

Use this skill when a task needs product or architecture judgment before code is written.

Typical triggers:

- "이 기능 MVP에 넣어도 돼?"
- "doctor/scan/tui 구조를 어떻게 잡아야 해?"
- "리팩터링 방향이 PRD/TDD와 맞는지 봐줘"

## Read first

Open only the relevant parts of these files:

- `../../../AGENTS.md`
- `../../../dev/storix_prd.md`
- `../../../dev/storix_tdd.md`

## Workflow

1. Restate the task in Storix terms: scan, analyze, classify, dry-run, clean, report, or TUI.
2. Check whether the request stays inside MVP v1.0.
3. Map the change to the shared architecture before touching CLI or TUI.
4. Call out any scope expansion or product-risk tradeoff before implementing it.
5. End with a short implementation plan that names the affected layers and expected tests.

## Non-negotiable guardrails

- Storix is macOS-first. Do not generalize to Linux or GUI unless explicitly requested.
- CLI and TUI must reuse the same service logic.
- Show first, delete later. Safety beats convenience.
- Keep known-path scanning and reclaimable-size estimation central to the user experience.
- Prefer the MVP command surface: `scan`, `top`, `doctor`, `clean`, `projects scan`, `report`, `tui`.

## Out of scope by default

Do not silently expand MVP with:

- Trash move workflows
- Duplicate-file detection
- Scheduler integration
- iCloud-local-occupancy handling
- Linux support
- Full GUI app plans

If a user asks for one of these, state that it is beyond the current MVP and either:

- implement it as an explicit deviation, or
- propose the closest in-scope alternative first

## Output format

When this skill is used, make the decision explicit:

- In scope or out of scope
- Affected product areas
- Affected code layers
- Main safety or UX risk
- Tests that should move with the change
