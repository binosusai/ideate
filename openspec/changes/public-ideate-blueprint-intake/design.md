## Context

The desired product flow is:

```text
User idea
  -> AI-generated blueprint
  -> user review/edit
  -> Ideate research/debate/plan
  -> proposal
  -> POC
  -> review loop
  -> accepted POC
  -> later Minions execution handoff
```

The current system already has most of the backend primitives:

- YAML idea schema in `examples/idea*.yaml`
- `details_json` persistence in SQLite/Postgres
- `examples-sync` for pushing YAML context into the active database
- research/debate/planning crews
- OpenSpec proposal generation
- POC generation and review status
- dashboard APIs for idea listing, details, approvals, and reviews

The product work should therefore harden the input, persistence, workflow orchestration, and user review surfaces before adding Minions.

## Goals / Non-Goals

**Goals:**

- Make one-line idea intake feel simple and polished.
- Produce structured, editable blueprints that match the existing YAML idea shape.
- Ensure all Ideate agents operate on the full approved blueprint context.
- Keep a human approval gate before expensive or state-changing work.
- Support a free Phase 1 release using the operator's configured GitHub/email.
- Keep future user-owned GitHub/email and Minions handoff cleanly separable.

**Non-Goals:**

- Do not implement Minions execution in Phase 1.
- Do not implement per-user GitHub OAuth scopes for workflow execution in Phase 1.
- Do not expose arbitrary prompt controls or raw database access.
- Do not require paid external services for user-generated POCs by default.
- Do not remove the CLI workflow; the UI should orchestrate the same durable state transitions.

## Canonical Blueprint

The blueprint remains a YAML-compatible object:

```yaml
title: string
category: money|personal
why: string
details:
  domain: string
  problem: object|string|list
  target_users: list
  use_cases: list
  technology: object
  constraints: list
  mvp: object
  acceptance_criteria: list
  success_metrics: object|list
  monetization: object
  differentiation: list
  risks: list
  open_questions: list
```

The database source of truth is still the `ideas` row plus `details_json`. YAML files may remain useful as fixtures, exports, and operator-authored seeds.

## Proposed Architecture

```text
Browser
  |
  | submit one-line idea
  v
Dashboard API
  |
  | generate blueprint via model
  v
Blueprint draft row / idea draft state
  |
  | user edits and approves blueprint
  v
Idea row with full why + details_json
  |
  | background job or workflow dispatch
  v
Ideate stages: research -> debate -> plan -> proposal -> approve -> POC -> review
  |
  | accepted POC
  v
Future Minions handoff
```

## Delivery Chunks

### Chunk 1: Blueprint Contract And Validation

Create a formal blueprint schema and validation layer.

- Define required and optional fields.
- Normalize categories to Ideate's supported set.
- Preserve unsupported or extra fields in `details_json`.
- Add deterministic tests for valid, partial, and malformed blueprint payloads.

This chunk makes the product data contract reliable before UI or AI calls.

### Chunk 2: Manual Blueprint Intake UI

Build a simple dashboard intake surface that accepts a full YAML/JSON blueprint and saves it to the active database.

- Add "New Idea" UI.
- Accept structured text.
- Validate and preview normalized blueprint.
- Save as a captured idea.
- Show the idea in the existing queue/detail views.

This gives a usable end-to-end path without model variability.

### Chunk 3: AI Blueprint Generation

Add the model-backed one-liner expansion.

- User enters a gist/one-liner.
- API asks the model for strict structured JSON/YAML matching the blueprint schema.
- Validate model output.
- Show editable draft to user.
- Persist only after user approval.

The UI should make the AI output feel like a draft the user owns, not an irreversible action.

### Chunk 4: Workflow Orchestration

Run Ideate stages from approved blueprints without blocking HTTP requests.

- Add an explicit "Run Ideate" action.
- Dispatch research/debate/plan as a background job or GitHub workflow.
- Persist stage status and errors.
- Display progress in the dashboard.
- Ensure proposals include `details_json` and latest artifacts.

Phase 1 may use the operator's configured GitHub/email identity.

### Chunk 5: Proposal And POC Review Loop

Polish the user-facing proposal/POC loop.

- Show proposal, research, debate, and plan in a readable detail view.
- Allow approve/revise on proposal.
- Allow POC generation after approval.
- Show POC report, quality score, and improvement loop.
- Allow accept/revise on POC.

This chunk completes the hardening of Ideate as a standalone product phase.

### Chunk 6: Public-Free Readiness

Add minimum safeguards for exposing the system for free.

- Authenticated sessions.
- Rate limits or quota counters for blueprint generation and workflows.
- Abuse-safe model prompt boundaries.
- Secret-safe artifact rendering.
- Clear user-facing status/error messages.
- Basic operational telemetry that avoids storing secrets.

### Chunk 7: Minions Handoff Preparation

Define the handoff contract without building the Minions integration yet.

- Add an accepted-POC event/state.
- Export a Minions-ready package: blueprint, proposal, POC path, artifacts, decisions, and next tasks.
- Document the future transition to Minions sprint planning and agent roster views.

## Phase 1 Scope Recommendation

Phase 1 should include Chunks 1 through 5, plus only the minimum parts of Chunk 6 needed to safely test with real users. Chunk 7 can be a spec-only bridge unless the POC acceptance path is already stable.

## POC Launchpad Direction

The public product should feel less like an agent transcript viewer and more like a POC Launchpad. The useful, shiny artifact is a **POC Capsule**:

- a canonical blueprint
- proposal/research/debate/plan artifacts
- runnable local POC code
- one-command local runner
- smoke check
- deployment targets
- ecosystem profile
- quality score
- review and next-step loop

The user-facing promise is:

```text
Give Ideate an idea. It returns a blueprint, a proposal, a runnable local POC, and a deployment path.
```

### POC Capsule Standard

Every generated POC should include:

- `poc.capsule.json`: machine-readable capsule contract
- `ecosystem.profile.yaml`: stack preferences such as frontend, backend, database, auth, deploy targets, repo, and project management
- `deploy.targets.json`: local and cloud deployment targets
- `run-local.sh`: one-command localhost runner
- `scripts/smoke_check.py`: localhost health check
- `.env.example`: placeholder-only configuration
- `README.md`: run, smoke, diagram, and artifact overview
- `docs/local_setup.md`: local setup and secrets posture
- `docs/deployment.md`: Vercel/AWS/Neon or equivalent deploy path
- `docs/poc_capsule.md`: capsule contract and Minions handoff notes
- `infra/terraform/main.tf`: deploy entrypoint using shared platform modules
- `.github/workflows/poc-ci.yml`: minimal CI/smoke validation

### Ecosystem Profile

Ideate should let users bring their own ecosystem over time:

```yaml
frontend: nextjs
backend: fastapi
database: neon
auth: clerk
deploy:
  frontend: vercel
  backend: render
  database: neon-postgres
repo: github
project_management: github-projects
```

Phase 1 can start with generated defaults. Later, the UI can expose these as stack preferences before POC generation.

### Quality Score Surface

The quality score should be product-facing, not just an internal report:

- local runnable: yes/no
- smoke check: yes/no
- UI included: yes/no
- API included: yes/no
- persistence included: yes/no
- deploy path included: yes/no
- ecosystem profile included: yes/no
- docs included: yes/no
- next gaps: top 1-3 actions

This makes the system feel alive and useful because the user sees exactly what they can run, what is deployment-ready, and what still needs work.

## Data Model Notes

Potential new concepts:

- `blueprint_status`: `draft`, `approved`, `rejected`
- `blueprint_source`: `manual`, `ai_generated`, `example_yaml`
- `blueprint_prompt`: optional sanitized original one-liner
- `workflow_status`: `idle`, `queued`, `running`, `failed`, `complete`
- `workflow_last_error`: sanitized error text

These can be columns on `ideas` for simplicity, or a separate `blueprints` table if multiple drafts per idea need to be preserved.

Recommendation: start with one approved blueprint per idea, plus artifact rows for generated drafts if auditability is needed.

## AI Generation Boundary

The blueprint-generation API should:

- Accept only the user's idea text and optional lightweight preferences.
- Use a strict schema response format when available.
- Reject or repair outputs that fail validation.
- Preserve user language in `why` while expanding `details`.
- Avoid promising integrations, paid services, or automatic publication.
- Mark uncertain fields as `open_questions` rather than inventing confidence.

## Workflow Execution

Avoid long-running work inside dashboard request handlers. Use one of:

- GitHub Actions `workflow_dispatch` with idea id.
- A hosted worker process.
- A queue table polled by a worker.

Recommendation for Phase 1: use GitHub Actions or the existing operator environment first, because the project already has GitHub task sync and deployment assumptions.

## Phase 2 Boundary

Phase 2 adds:

- Per-user GitHub account authorization.
- Per-user email settings.
- Minions organization creation.
- Sprint planning, agent rosters, agile ceremonies, and execution views.
- Paid tiers and commercial controls.

Ideate should hand Minions a stable package, not leak its internal stage implementation as the Minions contract.

## Risks / Trade-offs

- [Risk] Model-generated blueprints overstate feasibility.
  - Mitigation: require user review and keep `open_questions`.
- [Risk] Public free usage can burn model or GitHub quota.
  - Mitigation: quota free users and separate blueprint generation from POC generation.
- [Risk] Workflow jobs become hard to debug.
  - Mitigation: persist stage status, artifacts, decisions, and sanitized errors.
- [Risk] Minions scope distracts from Ideate hardening.
  - Mitigation: define only the handoff contract in Phase 1.
- [Risk] User ideas contain sensitive business context.
  - Mitigation: protect all routes, avoid public sharing by default, and maintain secret-safe rendering.

## Open Questions

- Should Phase 1 store multiple blueprint drafts per idea or only the approved blueprint?
- Should free users get POC generation, or only blueprint + proposal?
- Should proposal approval automatically trigger POC generation, or remain a separate explicit action?
- Should GitHub workflow dispatch be the first background runner?
- What exact Minions input package does the future integration need?
