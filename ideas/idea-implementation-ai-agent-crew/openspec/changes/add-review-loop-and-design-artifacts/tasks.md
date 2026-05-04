# Tasks: Add Review Loop And Design Artifacts

## Review Loop — ✅ Done
- [x] Add idea-store fields for `tinkered`, `review_status`, `review_feedback`, `last_reviewed_at`, and `iteration_count`.
- [x] Update idea-picking logic so `approved` and `pending_review` ideas are not re-selected automatically.
	- Note: `tinkered` column now exists in both SQLite and Neon Postgres (via `ALTER TABLE … ADD COLUMN IF NOT EXISTS`). The auto-pick SQL in the pipeline filters `COALESCE(tinkered, FALSE) = FALSE AND COALESCE(review_status, 'new') <> 'pending_review'`.
- [x] Add a post-POC pipeline review stage with environment approval (`poc-review` environment gate).
- [x] Define the approval action that flips `tinkered = true`.
- [x] Define the revision action that stores feedback without flipping `tinkered`.
- [x] Add a simple feedback input path that is auditable and attached to the idea.

## Iteration Memory — ✅ Done
- [x] Load prior research, debate, implementation plan, review decision, and review feedback into the next research run.
- [x] Load the same iteration context into the next debate run.
- [x] Persist enough history so a revision request does not lose earlier reasoning.
- [x] Add tests for approved, pending review, and revise selection behavior.

## Board Visibility — ✅ Done (new scope, May 2026)
- [x] Add `task:todo` label and open-issue state for pre-run task visibility in `board_sync.py`.
- [x] Add `idea board-setup <id> --stages <stages>` CLI command that pre-creates TODO issues before any agent runs.
	- Flow: `board-setup` (todo) → research/debate/plan run (in-progress → done) → `poc-approval` gate → poc run → `poc-review` gate.
	- The `poc-approval` environment gate is where you approve the todo task board (seeing all planned agent tasks before work starts).
- [x] Add `Create task board todos` step to pipeline before `Research`, so todos are visible at the `poc-approval` gate.

## Project Naming — ✅ Done (new scope, May 2026)
- [x] Replace random prefix/stem codename generator in `poc_name()` with slug-derived words.
	- Example: "unified-api-key-gateway-…" → `unifiedapioq`, "medium-article-writer-…" → `mediumarticlelw`.
	- Two-char deterministic hash suffix retained for GitHub collision avoidance.

## Crew Expansion — ⏳ Deferred
- [ ] Add a `Designer` role to the crew.
- [ ] Add a `Software Architect` role to the crew.
- [ ] Define the exact output contract for both roles.
- [ ] Include those outputs in planning artifacts used by POC generation.

## Documentation Artifacts — ✅ Done (May 2026)
- [x] Generate a Mermaid component diagram for each POC.
- [x] Embed the Mermaid diagram in the generated README.
- [x] Add the same or richer architecture view in `docs/architecture.md`.
- [x] Add tests or fixture checks for Mermaid inclusion in generated output.

## Future Hosted Verification — ⏳ Deferred
- [ ] Compare free-tier or near-free options for frontend hosting.
- [ ] Compare free-tier or near-free options for backend/API hosting.
- [ ] Document a recommended hosted verification path with tradeoffs.
- [ ] Decide whether hosted verification should stay manual, become optional automation, or be promoted to a pipeline stage later.