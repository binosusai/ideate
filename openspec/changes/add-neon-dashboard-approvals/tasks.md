## 1. API Foundation

- [x] 1.1 Add dashboard Postgres dependency and serverless DB helper.
- [x] 1.2 Add shared dashboard auth helper using `IDEATE_DASHBOARD_ADMIN_TOKEN`.
- [x] 1.3 Add parameterized query helpers for ideas, artifacts, and decisions.
- [x] 1.4 Add API error handling that never leaks `DATABASE_URL` or raw connection strings.

## 2. Read APIs

- [x] 2.1 Add `GET /api/ideas` with status/review filters.
- [x] 2.2 Add `GET /api/ideas/:id` with details, latest artifacts, and recent decisions.
- [x] 2.3 Add `GET /api/reviews/pending` for `review_status='pending_review'`.
- [ ] 2.4 Add tests or fixture-driven checks for query output shape.

## 3. Mutation APIs

- [x] 3.1 Add `POST /api/ideas/:id/approve`.
- [x] 3.2 Add `POST /api/ideas/:id/review`.
- [x] 3.3 Ensure dashboard approvals insert decision rows.
- [x] 3.4 Ensure invalid lifecycle transitions return clear 409-style errors.
- [x] 3.5 Ensure unauthenticated mutation attempts return 401/403.

## 4. Dashboard UI

- [x] 4.1 Add idea queue view with lifecycle and review-state columns.
- [x] 4.2 Add idea detail panel/page.
- [x] 4.3 Add pending reviews view.
- [x] 4.4 Add approval and revision controls with loading/error states.
- [x] 4.5 Add feedback textarea for revision decisions.
- [x] 4.6 Preserve the existing agent hierarchy presentation as a separate overview section.

## 5. Deployment

- [ ] 5.1 Document required Vercel environment variables.
- [ ] 5.2 Document Neon connection requirements and least-privilege DB role guidance.
- [ ] 5.3 Add a deploy checklist for Vercel.
- [x] 5.4 Confirm static dashboard still builds with `npm run build`.

## 6. Validation

- [ ] 6.1 Add unit-level tests for API helper behavior where feasible.
- [ ] 6.2 Add manual smoke-test checklist for Vercel:
  - list ideas
  - open idea detail
  - approve planned idea
  - approve pending POC
  - revise pending POC with feedback
- [ ] 6.3 Verify decisions table records every dashboard mutation.
