## 1. Blueprint Contract

- [ ] 1.1 Define a canonical blueprint schema for one-line and structured idea intake.
- [ ] 1.2 Add validation/normalization helpers for title, category, why, and details.
- [ ] 1.3 Preserve unknown structured fields in `details_json`.
- [ ] 1.4 Add tests for valid blueprint, partial blueprint, invalid payload, and category normalization.
- [ ] 1.5 Document the blueprint contract with examples.

## 2. Manual Intake

- [ ] 2.1 Add a protected `POST /api/blueprints/validate` route.
- [ ] 2.2 Add a protected `POST /api/ideas` route that creates an idea from an approved blueprint.
- [ ] 2.3 Add a dashboard "New Idea" view.
- [ ] 2.4 Add YAML/JSON input mode with validation errors and normalized preview.
- [ ] 2.5 Ensure saved ideas appear in the existing idea queue and detail views.

## 3. AI Blueprint Generation

- [ ] 3.1 Add a server-side model client for blueprint generation using exported environment variables only.
- [ ] 3.2 Add `POST /api/blueprints/generate` for one-line idea expansion.
- [ ] 3.3 Enforce structured output validation before returning a draft to the browser.
- [ ] 3.4 Add editable blueprint preview before persistence.
- [ ] 3.5 Add tests or recorded fixtures for model-output validation and repair failures.

## 4. Workflow Orchestration

- [ ] 4.1 Add an explicit "Run Ideate" dashboard action for approved blueprints.
- [ ] 4.2 Choose and implement the first background runner: GitHub Actions dispatch, hosted worker, or queue table.
- [ ] 4.3 Persist workflow stage status and sanitized errors.
- [ ] 4.4 Display research/debate/planning progress in the idea detail view.
- [ ] 4.5 Ensure research, debate, plan, and OpenSpec proposal use the approved blueprint details.

## 5. Proposal And POC Review

- [ ] 5.1 Polish proposal display for user review.
- [ ] 5.2 Add proposal approve/revise controls with feedback.
- [ ] 5.3 Add POC generation trigger after proposal approval.
- [x] 5.4 Display/generate POC report, quality score, and improvement loop artifacts.
- [ ] 5.5 Add POC accept/revise controls with feedback.
- [ ] 5.6 Ensure accepted POCs are not automatically selected for more Ideate iterations.

## 5A. POC Launchpad And Capsule Quality

- [x] 5A.1 Define the POC Capsule standard in this OpenSpec change.
- [x] 5A.2 Generate `poc.capsule.json` for every generated POC.
- [x] 5A.3 Generate `run-local.sh` for one-command localhost execution.
- [x] 5A.4 Generate `scripts/smoke_check.py` for local health verification.
- [x] 5A.5 Generate `ecosystem.profile.yaml` so future runs can adapt to user stack preferences.
- [x] 5A.6 Generate `deploy.targets.json` and deployment docs for local/cloud wiring.
- [x] 5A.7 Add capsule files to the deterministic POC quality scorer.
- [x] 5A.8 Surface capsule readiness as a Launchpad panel in the dashboard.
- [x] 5A.9 Allow users to edit ecosystem profile before POC generation.
- [x] 5A.10 Add integration smoke test that starts generated POC locally and runs `scripts/smoke_check.py`.

## 6. Public-Free Readiness

- [ ] 6.1 Add authenticated session requirements for all intake and workflow routes.
- [ ] 6.2 Add basic rate limits or quotas for blueprint generation and workflow runs.
- [ ] 6.3 Add secret-safe rendering checks for generated artifacts.
- [ ] 6.4 Add user-facing error states for model failures, validation failures, and workflow failures.
- [ ] 6.5 Add deployment checklist for the public free test.

## 7. Minions Handoff Preparation

- [ ] 7.1 Define the Minions-ready accepted-POC package.
- [ ] 7.2 Add an export artifact containing blueprint, proposal, POC metadata, decisions, and next tasks.
- [ ] 7.3 Add a placeholder dashboard state for "Ready for Minions".
- [ ] 7.4 Document Phase 2 requirements for user GitHub/email, Minions org creation, sprint planning, and agent roster views.

## 8. Validation

- [x] 8.1 Run Python workflow tests.
- [x] 8.2 Run dashboard build/tests.
- [ ] 8.3 Smoke test manual blueprint intake against local SQLite.
- [ ] 8.4 Smoke test example/blueprint sync against Neon with exported `DATABASE_URL`.
- [ ] 8.5 Smoke test full Phase 1 path: one-liner -> blueprint -> proposal -> POC -> accepted.
