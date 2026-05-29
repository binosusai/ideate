## Why

Ideate already captures structured ideas, syncs example YAML into the database, runs research/debate/planning crews, generates OpenSpec proposals, creates POCs, and records review outcomes. The missing product layer is a public-facing intake experience where a user can submit a one-line idea, have AI expand it into a durable blueprint, review that blueprint, and then let Ideate run the workflow with full context.

This change turns Ideate from an operator CLI/dashboard into the first phase of an idea-to-execution product. Minions remains the later execution phase after a user accepts a POC.

## What Changes

- Add a user-facing idea intake UI for one-line or fully baked idea submission.
- Add an AI blueprint-generation step that converts rough input into the canonical YAML-style idea schema.
- Store generated blueprints in the active database before research/debate/planning runs.
- Add a review/edit gate so the user can approve the blueprint before Ideate agents act on it.
- Run the existing Ideate workflow from the approved blueprint through proposal, POC, and review loop.
- Keep Phase 1 scoped to the operator's configured GitHub/email context; defer per-user GitHub/email authorization to Phase 2.
- Prepare, but do not implement, a later Minions handoff after POC acceptance.

## Capabilities

### New Capabilities

- `public-blueprint-intake`: Users can submit a rough idea and review an AI-generated structured blueprint.
- `blueprint-backed-ideate-workflow`: Ideate agents use the approved blueprint as the source of truth for research, debate, planning, proposals, and POCs.
- `phase-one-operator-context`: The hosted workflow can run under the configured operator GitHub/email identity while public user identity is still limited.

### Modified Capabilities

- The dashboard evolves from an operator review surface into a product intake and review experience.
- Existing examples/YAML sync remains compatible and becomes the canonical blueprint persistence path.

## Impact

- Requires an AI model call or service boundary for blueprint generation.
- Requires durable storage for draft blueprints, approved blueprints, workflow state, and generated artifacts.
- Requires stronger auth/abuse limits before public exposure, even while the product is free.
- Requires a job runner or workflow dispatch path so long-running Ideate stages do not block HTTP requests.
- Does not commercialize Minions in this change; it only defines the future handoff point.
