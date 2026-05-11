## Why

Ideate can already generate idea artifacts, GitHub task-board issues, POCs, and review states, but the human approval loop still lives mostly in CLI commands and GitHub Actions environment gates. That makes the workflow awkward when the operator wants an always-on view of pending proposals and POCs without restarting a local server.

Adding Neon-backed dashboard pages turns the existing static dashboard into a lightweight control plane for reviewing idea progress, approving plans, and sending POCs back for revision from Vercel.

## What Changes

- Add read-only Neon-backed dashboard APIs for ideas, idea detail, artifacts, decisions, and pending review queues.
- Add protected dashboard actions for approving an idea and recording POC review outcomes.
- Add dashboard pages/views for:
  - idea queue
  - idea detail
  - pending POC reviews
  - approval/revision actions
- Reuse existing store semantics so dashboard actions call the same state transitions as CLI commands.
- Keep GitHub Actions environment gates as a fallback/automation layer, not the only approval surface.

## Capabilities

### New Capabilities

- `dashboard-approval-control-plane`: Vercel dashboard can read Neon-backed idea state and write protected approval/review decisions.

### Modified Capabilities

- Existing idea lifecycle remains unchanged, but approvals may originate from the dashboard as well as CLI/GitHub Actions.

## Impact

- Adds Vercel serverless API routes that require `DATABASE_URL` and an admin auth mechanism.
- Adds UI for operational decision-making rather than only presentation.
- Introduces a stronger need for dashboard authorization because approval buttons mutate Neon state.
- Does not require running a local server for day-to-day review/approval.
