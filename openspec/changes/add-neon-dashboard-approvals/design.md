## Context

The current dashboard is static presentation plus a GitHub issue proxy. Ideate already has:

- Postgres-backed `PgStore` selected by `DATABASE_URL`
- lifecycle transitions in `Store`/`PgStore`
- CLI commands:
  - `idea approve <id>`
  - `idea review <id> --decision approve|revise --feedback ...`
- GitHub issue task-board sync
- GitHub Actions environment gates `poc-approval` and `poc-review`

The missing layer is a deployed web surface that can inspect Neon state and trigger those same decisions.

## Goals / Non-Goals

**Goals:**

- Provide an always-on Vercel dashboard for idea review and approval.
- Use Neon as the source of truth.
- Keep dashboard mutations narrow and auditable.
- Avoid exposing raw database credentials to the browser.
- Make approval/revision actions idempotent enough for repeated button clicks or retries.

**Non-Goals:**

- Do not replace GitHub Projects as the sprint board in this change.
- Do not build a full admin console or arbitrary SQL editor.
- Do not add public user signup.
- Do not store or read `.env` files.
- Do not bypass existing lifecycle rules in `db.py`.

## Proposed Architecture

```text
Browser
  |
  | GET /api/ideas
  | GET /api/ideas/:id
  | GET /api/reviews/pending
  | POST /api/ideas/:id/approve
  | POST /api/ideas/:id/review
  v
Vercel Serverless Functions
  |
  | server-side DATABASE_URL
  | server-side auth check
  v
Neon Postgres
```

## Authentication

Use a narrow admin gate for the first implementation:

- Option A: `IDEATE_DASHBOARD_ADMIN_TOKEN` header/cookie check.
- Option B: GitHub OAuth cookie plus allowed-login allowlist.

Recommendation for first slice:

- Add `IDEATE_DASHBOARD_ADMIN_TOKEN`.
- Browser stores no DB credential.
- Mutating API routes require `Authorization: Bearer <token>` or an HTTP-only admin session cookie.
- Read APIs may start protected too, because idea details can contain private business context.

GitHub OAuth can be layered later using the existing dashboard auth files.

## API Routes

### `GET /api/ideas`

Returns a compact list:

- `id`
- `title`
- `slug`
- `category`
- `status`
- `score`
- `review_status`
- `tinkered`
- `hardened`
- `iteration_count`
- `created_at`
- `updated_at`
- selected `details_json` summaries such as `domain`, `target_users`, `source_category`

Filters:

- `status`
- `review_status`
- `q`
- `limit`

### `GET /api/ideas/:id`

Returns full idea detail plus latest artifacts and decisions:

- idea row including `details_json`
- latest `research`
- latest `debate`
- latest `plan`
- latest `poc_quality_score`
- latest `poc_improvement_loop`
- recent decisions

### `GET /api/reviews/pending`

Returns ideas where:

```sql
review_status = 'pending_review'
```

Include enough data to review the generated POC and quality score quickly.

### `POST /api/ideas/:id/approve`

Approves an idea for POC generation.

Behavior:

- Check auth.
- Load current idea.
- Call the same lifecycle validation as `idea approve`.
- Add decision `approved`.
- Return updated idea.

### `POST /api/ideas/:id/review`

Records generated POC review outcome.

Body:

```json
{
  "decision": "approve",
  "feedback": "Looks good"
}
```

or

```json
{
  "decision": "revise",
  "feedback": "Add auth and deploy docs before handoff"
}
```

Behavior:

- Check auth.
- For `approve`: set `review_status=approved`, `tinkered=true`.
- For `revise`: set `review_status=revise`, keep `tinkered=false`, store feedback.
- Add a matching decision row.
- Return updated idea.

## UI Views

### Idea Queue

Dense table for scanning:

- title
- status
- score
- review state
- domain/source category
- iteration count
- next action

Primary actions:

- Open detail
- Approve plan when status is `planned`
- Open pending review when `review_status=pending_review`

### Idea Detail

Shows:

- problem/domain/details summary
- lifecycle status
- latest research/debate/plan
- POC quality score and recommended actions
- decision history

Actions:

- Approve idea
- Record POC approval
- Send POC back for revision with feedback

### Pending Reviews

Focused page for POCs awaiting human review:

- POC status
- score
- improvement loop
- feedback textarea
- Approve button
- Revise button

## Data Access

Avoid importing the Python store into Vercel. The dashboard runtime is Node serverless, so use a small JS Postgres helper:

- dependency: `pg`
- helper: `dashboard/api/_db.js`
- environment: `DATABASE_URL`
- SQL queries should be parameterized.

Keep mutation logic equivalent to Python `PgStore` behavior. If duplication becomes risky, future work can expose a Python HTTP service or package shared lifecycle rules.

## Auditability

Every mutating dashboard action SHALL insert a row into `decisions`.

Decision values:

- `dashboard-approved`
- `dashboard-poc-approved`
- `dashboard-poc-revise`

Rationale stores feedback or a default dashboard action message.

## Risks / Trade-offs

- [Risk] Dashboard mutation logic drifts from CLI lifecycle behavior.
  - Mitigation: duplicate only narrow approve/review transitions and add tests.
- [Risk] Exposing idea details on Vercel leaks private business context.
  - Mitigation: protect all Neon-backed APIs with admin auth.
- [Risk] Serverless DB connection handling causes connection churn.
  - Mitigation: use a small pooled helper compatible with Vercel/Neon or Neon serverless driver later.
- [Risk] Approval buttons trigger state changes but not downstream GitHub Actions.
  - Mitigation: first slice records state only; follow-up can dispatch workflows via GitHub API.

## Open Questions

- Should dashboard approval also trigger the POC workflow immediately via `workflow_dispatch`?
- Should read-only views require the same admin auth as mutation routes?
- Should GitHub OAuth allowlist replace admin-token auth before deployment?
- Should dashboard actions sync GitHub task-board issues immediately?
