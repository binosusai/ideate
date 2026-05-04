# Design: Add Review Loop And Design Artifacts

## Scope
This change affects idea selection, pipeline review flow, crew composition, generated documentation, and future hosted verification planning.

## Idea Lifecycle Model
The system should distinguish between these states:

- `new`: idea has not yet entered the POC review loop.
- `pending_review`: a POC has been generated and is awaiting user review.
- `approved`: the user accepted the POC; the idea is considered `tinkered` and should not be auto-selected again.
- `revise`: the user rejected or requested changes; the idea remains eligible for another iteration, but only with previous outputs and feedback in context.

At minimum, the database should store:

- `tinkered` boolean
- `review_status`
- `review_feedback`
- `last_reviewed_at`
- `iteration_count`

`tinkered = true` is the durable stop signal for auto-selection.

## Selection Rules
Idea selection should exclude:

- ideas with `tinkered = true`
- ideas with `review_status = pending_review`

Ideas with `review_status = revise` may be selected again, but only after prior artifacts and feedback are loaded into the next research and debate cycle.

## Pipeline Review Stage
After the existing POC stage, add a new approval-gated review stage in the same pipeline.

The stage should support two outcomes:

- `approve`: mark the idea as `tinkered = true`, set `review_status = approved`
- `revise`: keep `tinkered = false`, set `review_status = revise`, persist user feedback for the next iteration

## Feedback Capture
GitHub Actions environment approval can gate a stage, but approval alone is not enough to capture structured rejection feedback.

The implementation should therefore add one explicit feedback input surface, such as:

- a workflow input on a manual follow-up step
- a checked-in review artifact file for the idea
- a CLI command that writes review feedback back into the store

The first implementation should prefer the simplest auditable path and keep the feedback attached to the idea record.

## Cached Iteration Context
When an idea re-enters research or debate after a `revise` outcome, the agents should receive:

- latest research artifact
- latest debate artifact
- latest implementation plan
- last review decision
- latest review feedback
- previous POC location or repo link when available

This should be appended as explicit iteration context rather than replacing the base prompt.

## Crew Expansion
Add these crew roles:

- `Designer`: focuses on user flow, interaction quality, layout clarity, and the fastest useful first-run experience
- `Software Architect`: focuses on system boundaries, component responsibilities, data flow, deployment constraints, and failure points

Their outputs should be included in the research, debate, or planning artifacts in a stable format so downstream generation can use them.

## Mermaid Diagram Generation
Generated POCs should include a Mermaid component diagram in the README and optionally in `docs/architecture.md`.

The diagram should show at minimum:

- browser UI
- backend API
- local SQLite store
- external provider or mock provider boundary
- optional hosted deployment targets when relevant

## Hosted Verification Track
This is a future feature, not a required first implementation.

The system should document a path for optionally publishing:

- static frontend to Vercel or another no-cost static host
- backend API to a low-cost or free-tier-compatible host

The design should compare cost, cold-start, secret handling, observability, and teardown risk before automating deployment.