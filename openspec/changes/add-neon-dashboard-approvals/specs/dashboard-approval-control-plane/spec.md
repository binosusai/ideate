## ADDED Requirements

### Requirement: Dashboard Reads Neon Idea State
The dashboard SHALL provide protected server-side API routes that read idea lifecycle state from Neon Postgres.

#### Scenario: Operator lists ideas
- **WHEN** an authenticated operator opens the idea queue
- **THEN** the dashboard displays ideas from Neon with status, score, review status, and updated timestamp
- **AND** the browser never receives the database connection string

#### Scenario: Operator opens idea detail
- **WHEN** an authenticated operator opens an idea detail view
- **THEN** the dashboard displays the idea details, latest core artifacts, and recent decisions

### Requirement: Dashboard Shows Pending POC Reviews
The dashboard SHALL provide a focused pending-review view for generated POCs awaiting human review.

#### Scenario: POC awaits review
- **WHEN** an idea has `review_status = 'pending_review'`
- **THEN** the pending-review view includes that idea
- **AND** it shows available POC quality score and improvement-loop context when present

### Requirement: Dashboard Approves Planned Ideas
The dashboard SHALL allow an authenticated operator to approve a planned idea for POC generation.

#### Scenario: Planned idea is approved
- **WHEN** an authenticated operator approves an idea with status `planned`
- **THEN** the idea status becomes `approved`
- **AND** a decision row records the dashboard approval

#### Scenario: Invalid approval is rejected
- **WHEN** an authenticated operator attempts an invalid approval transition
- **THEN** the API returns a clear conflict response
- **AND** the idea state remains unchanged

### Requirement: Dashboard Records POC Review Decisions
The dashboard SHALL allow an authenticated operator to approve or request revision for a generated POC.

#### Scenario: POC is approved
- **WHEN** an authenticated operator records review decision `approve`
- **THEN** the idea review status becomes `approved`
- **AND** `tinkered` becomes true
- **AND** a decision row records the dashboard POC approval

#### Scenario: POC needs revision
- **WHEN** an authenticated operator records review decision `revise` with feedback
- **THEN** the idea review status becomes `revise`
- **AND** `tinkered` remains false
- **AND** review feedback is saved for the next iteration
- **AND** a decision row records the dashboard revision request

### Requirement: Dashboard Mutations Are Protected
All dashboard routes that mutate Neon state SHALL require server-side authorization.

#### Scenario: Missing authorization
- **WHEN** a request without valid dashboard authorization calls an approval or review mutation route
- **THEN** the route returns an unauthorized response
- **AND** no idea, decision, or artifact row is changed

### Requirement: Vercel Deployment Is Documented
The project SHALL document the environment variables and deployment steps required to run the Neon-backed dashboard on Vercel.

#### Scenario: Operator deploys dashboard
- **WHEN** an operator follows the deployment checklist
- **THEN** Vercel has the required `DATABASE_URL` and dashboard authorization secret
- **AND** the deployed dashboard can list ideas without a local server
