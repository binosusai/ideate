## 1. Baseline Parent OpenSpec Structure

- [x] 1.1 Confirm parent change folder and required artifacts exist under `ideate/openspec/changes/ideate-governance/`.
- [x] 1.2 Confirm capability spec file exists under `specs/parent-openspec-governance/spec.md`.
- [x] 1.3 Validate artifact dependency order (proposal -> design/specs -> tasks).

## 2. Align Parent Governance With Current Implementation

- [x] 2.1 Document how current idea-level OpenSpec files are organized in `ideas/*/openspec/changes/*`.
- [x] 2.2 Document how ideate workflow stages currently produce and consume planning artifacts.
- [x] 2.3 Update parent requirements to match implemented runtime and workflow behavior.

## 3. Validation Workflow

- [x] 3.1 Run `openspec status --change ideate-governance` and ensure all artifacts are recognized.
- [x] 3.2 Run `openspec validate --strict ideate-governance` and resolve any schema issues.
- [x] 3.3 Capture validation output in change notes before implementation begins.

## 4. Next Additions (Spec-Driven Roadmap)

- [ ] 4.1 Define parent quality gates for proposal/design/spec/tasks completeness per idea.
- [ ] 4.2 Define parent traceability rules from requirements to idea artifacts and acceptance tests.
- [ ] 4.3 Define parent release-readiness checklist for paid distribution (security, observability, supportability, compliance).
- [ ] 4.4 Propose automation for drift detection between parent governance and child OpenSpec changes.

## 5. Parallel Venture Trials (Unique Pitch)

- [ ] 5.1 Add a new deterministic trial mode that forks one approved idea into 3 variants: speed-to-revenue, defensibility, and low-burn simplicity.
- [ ] 5.2 Extend planning output to generate a variant brief for each fork with ICP, offer, pricing hypothesis, and success metric.
- [ ] 5.3 Add trial-specific artifact files: `variant_a.md`, `variant_b.md`, `variant_c.md`, and `winner_selection.md`.
- [ ] 5.4 Generate lightweight POC stubs and landing-page copy per variant under the external `pocs/` workspace.
- [ ] 5.5 Add deterministic winner-scoring (evidence-weighted rubric) and produce a ranked recommendation with rationale.
- [ ] 5.6 Add CLI command support for trial runs and winner selection without breaking existing default workflow.
- [ ] 5.7 Add acceptance tests for variant generation, scoring stability, and winner artifact integrity.

## 6. Continuous Functionality Audit Loop

- [ ] 6.1 Add a repeatable audit command/workflow that inspects core stages for regressions, missing artifacts, and stage-state inconsistencies.
- [ ] 6.2 Add audit report output file per run: `audit_report.md` with severity labels, impacted files, and fix recommendations.
- [ ] 6.3 Add bug triage categories in audit output: reliability, artifact integrity, UX/CLI clarity, and security hygiene.
- [ ] 6.4 Add feature-opportunity section in audit output: quick wins, differentiators, and paid-tier candidates.
- [ ] 6.5 Add tests validating that audit output is generated and includes at least one actionable recommendation format.

## 7. Implementation Progress Snapshot (2026-05-05)

- [x] 7.1 Completed functionality audit pass and documented prioritized bug/feature recommendations.
- [x] 7.2 Implemented lifecycle status transition validation for SQLite and Postgres stores.
- [x] 7.3 Added regression tests for valid/invalid status transitions.
- [x] 7.4 Added board-setup fail-fast preflight (repo/token/connectivity) and strict sync path.
- [x] 7.5 Added strict iteration-context validation mode with missing-artifact detection.
- [x] 7.6 Added safer POC repo initialization behavior with partial-state cleanup/warnings.
- [ ] 7.7 Implement CLI/user-facing archive command (`idea archive`) for lifecycle hygiene.
- [ ] 7.8 Implement first slice of Parallel Venture Trials (`trial` command + variant artifacts).
- [ ] 7.9 Add audit command that emits `audit_report.md` from deterministic checks.
- [x] 7.10 Start POC-focused improvement cycle (quality rubric + generated POC evaluation loop).

## 8. POC Quality Cycle Status

- [x] 8.1 Generate `poc_quality_rubric.md` in idea artifacts during `idea poc`.
- [x] 8.2 Generate deterministic `poc_quality_score.md` based on file-evidence checks.
- [x] 8.3 Generate `poc_improvement_loop.md` with recommended next actions per weak section.
- [x] 8.4 Validate quality-cycle artifacts in workflow tests for both feasible and skipped POC paths.
- [x] 8.5 Add SMTP email notifications for quality score + improvement loop outputs.
- [x] 8.6 Add `idea score <id>` to re-score existing POC state without regeneration.
- [x] 8.7 Add `idea poc-patch <id>` for targeted missing-file patching on existing POCs.
- [x] 8.8 Add manual feedback workflow (`poc-improve.yml`) with before/after score visibility.
- [x] 8.9 Add push/manual re-score workflow (`poc-rescore.yml`) for continuous score updates.
- [ ] 8.10 Add iterative scoring history (`poc_quality_history.md`) to track score deltas per iteration.
- [ ] 8.11 Add stricter quality thresholds for handoff gating (optional strict mode).
- [ ] 8.12 Extend scoring to include runtime smoke checks (endpoint health, basic UI assertions).