## Context

The repository already uses idea-scoped OpenSpec artifacts in `ideas/*/openspec/changes/*` with `proposal.md`, `design.md`, `tasks.md`, and `specs/*/spec.md`. This parent change now governs both process artifacts and implementation-grounded quality controls so governance remains coupled to real behavior.

## Goals / Non-Goals

**Goals:**
- Define parent-level OpenSpec guidance and requirements for ideate.
- Keep parent artifacts aligned with current implementation behavior.
- Provide implementation tasks for spec-driven improvements that can be executed incrementally.
- Preserve current idea-level workflows and avoid runtime regressions.
- Add deterministic quality-loop mechanics that make improvement progress measurable.

**Non-Goals:**
- Do not redesign the core stage order (`capture -> research -> debate -> plan -> approve -> poc -> review -> handoff`).
- Do not add external paid services beyond optional SMTP notifications and existing provider integrations.
- Do not introduce deployment or billing infrastructure changes in this change set.

## Decisions

- Use `ideate/openspec/changes/add-parent-ideate-openspec/` as the parent change root.
  - Rationale: consistent with OpenSpec change workflow and repository naming conventions.
  - Alternative considered: placing governance docs outside `openspec/`; rejected to preserve standard OpenSpec tooling compatibility.

- Define one new capability `parent-openspec-governance`.
  - Rationale: keeps requirements cohesive and avoids over-fragmented specs in the first parent change.
  - Alternative considered: splitting into multiple capabilities immediately; rejected to keep initial adoption lightweight.

- Keep tasks implementation-grounded against existing behavior in:
  - `src/ideate/projects.py` (OpenSpec generation and copy behavior)
  - `src/ideate/cli.py` (stage command orchestration, `score`, `poc-patch`)
  - `src/ideate/db.py` (status transition validation)
  - `src/ideate/board_sync.py` (board preflight fail-fast)
  - `tests/test_workflow.py` (workflow expectations)
  - Rationale: process specs must match what exists today to stay actionable.

- Add a deterministic POC quality loop:
  - Generate rubric + score + improvement docs during `idea poc`.
  - Allow re-score against current disk state using `idea score`.
  - Allow targeted patching of missing POC files using `idea poc-patch`.
  - Wire CI workflows for manual improvement (`poc-improve.yml`) and push-triggered re-score (`poc-rescore.yml`).
  - Rationale: governance is stronger when quality is observable and iterative.

## Risks / Trade-offs

- [Risk] Parent artifacts drift from idea-level reality over time. -> Mitigation: include periodic parent OpenSpec refresh and validation tasks.
- [Risk] Team treats parent OpenSpec as documentation-only and skips task execution. -> Mitigation: include explicit tracked checklist tasks with ownership.
- [Risk] Lack of automation for parent checks can reduce consistency. -> Mitigation: define future tasks for validation tooling as a follow-up capability.
- [Risk] File-existence scoring can overestimate true runtime readiness. -> Mitigation: roadmap includes smoke checks and stricter handoff thresholds.
- [Risk] Iterative patching may leave inconsistent content quality in existing files. -> Mitigation: `poc-patch` only fills missing files and preserves authored content; follow-up human review remains required.

## Migration Plan

1. Keep current idea-level OpenSpec process unchanged.
2. Adopt parent-level OpenSpec review in planning workflow.
3. Apply runtime hardening and quality-loop tasks tracked in this change.
4. Execute parent tasks incrementally and record completion in `tasks.md`.
5. Validate change with `openspec validate --strict` before archive.

Rollback strategy:
- If parent flow creates friction, stop using this parent change operationally while keeping existing idea-level OpenSpec process unchanged.

## Open Questions

- Should parent OpenSpec checks eventually be required in CI for all ideas?
- Should parent governance be split into separate capabilities (governance, validation, release-readiness) after this baseline?
- What review cadence should be used to keep parent artifacts synchronized with new idea changes?