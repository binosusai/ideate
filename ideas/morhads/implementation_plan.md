# Implementation Plan: AI OSS Good-First-Issue Discovery and Guided Resolution Assistant

## Goal
Create a working proof of concept that demonstrates the core value of `AI OSS Good-First-Issue Discovery and Guided Resolution Assistant` with the smallest credible interface.

## MVP
- Represent the idea as a concrete user workflow.
- Create one runnable local draft project.
- Include acceptance tests or manual verification steps.
- Document what the larger engineering crew should improve next.

## Approval Gate
Ask before spending money, publishing, deleting substantial work, or handing this to the 47-agent crew.

## POC Feasibility
Feasible if it can run locally using standard tooling and sample data.

## OpenSpec Change ID
`morhads`

## Debate Context Used
Founder Board debate exists and was considered.

## Crew Implementation Notes
- Product Planner: MVP Workflow for AI OSS Good-First-Issue Discovery & Guided Resolution Assistant:

1. **GitHub API Integration**  
- Implement a backend service to fetch "good first issues" from popular OSS repos via GitHub API.  
- Normalize issue data (title, labels, repo metadata).  
*Tradeoff:* Start with a curated repo list to limit API calls and complexity.

2. **Competency & Language Preference Model**  
- Simple user profile form capturing skill level (beginner/intermediate) and preferred languages.  
- Use rule-based filters to match issues by language and label difficulty.  
*Tradeoff:* Avoid complex ML ranking initially; use heuristic sorting.

3. **Web UI**  
- Display filtered issues with ranking labels (easy, intermediate, hard).  
- Allow users to filter by language and difficulty.  
- Highlight the easiest issue prominently.

4. **Engineer AI Agent for TODO Generation**  
- On selecting the easiest issue, call a lightweight AI prompt (e.g., GPT-4) to generate a step-by-step TODO checklist.  
*Tradeoff:* Use prompt engineering over fine-tuned models to reduce cost and complexity.

5. **Email Workflow**  
- Compose an email with issue title as subject, body containing repo metadata and AI-generated TODOs.  
- Send email to user’s registered address.

6. **Success Metrics Logging**  
- Track issue views, selections, email opens/clicks, and self-reported completion via simple feedback form.

**Tradeoffs & Risks:**  
- MVP avoids paid AI APIs by limiting usage or using open-source LLMs.  
- Single easiest issue email avoids complex multi-issue workflows.  
- Focus on usability and measurable engagement before expanding AI sophistication or revenue models.

Deliverables: GitHub ingestion backend, React UI, AI prompt service, email sender, basic analytics dashboard.
- POC Coder: POC Plan: CLI-first, local, file-backed AI OSS Good-First-Issue Assistant

1. GitHub API Integration (Python script):
   - Query 1-2 popular OSS repos for open issues labeled "good first issue".
   - Normalize issue data: title, body, labels, repo metadata.
   - Store results in a local JSON file.

2. Simple Ranking:
   - Hardcode user language preference (e.g., Python).
   - Filter issues by language label or repo language.
   - Rank by issue creation date (newest easiest proxy).

3. AI TODO Generation (local LLM or OpenAI API if allowed):
   - For the top-ranked issue, generate a step-by-step TODO list based on issue title/body.
   - Save TODOs as a markdown checklist in a local file.

4. Email Workflow (mocked):
   - Compose an email text file with:
     - Subject: issue title
     - Body: repo metadata + issue metadata + TODO checklist
   - Print email content to console or save locally (no real sending).

5. CLI UI:
   - List issues with rank and language filter.
   - Allow user to select top easiest issue.
   - Trigger TODO generation and email composition.

Tradeoffs:
- No real email sending avoids complexity and privacy issues.
- Ranking is heuristic, not ML-based, to save time.
- AI TODO generation may be simplistic but proves concept.
- Local files enable easy inspection and iteration.

Outcome:
- Demonstrates end-to-end flow: discovery → ranking → guided TODO → "email".
- Validates user interest and AI TODO value before scaling or UI polish.
- Frontend Engineer: POC Interface Plan:

1. **Landing Page:**
- Header: "Discover Your Next OSS Good-First-Issue"
- Skill & Language Filters: dropdowns (e.g., JavaScript, Python), multi-select
- "Find Issues" button triggers GitHub API fetch and ranking

2. **Issue List View:**
- Table/List showing: Issue Title (link to GitHub), Repo Name, Difficulty Label (Easy/Intermediate/Hard), Language, Short Description snippet
- Sort by Difficulty ascending by default
- Pagination or infinite scroll for ~20 issues max

3. **Issue Selection:**
- Radio button or "Select" button per issue for single selection
- Once selected, show "Generate TODOs & Send Email" button

4. **TODO Generation & Email Preview:**
- On click, call AI agent to generate step-by-step TODO checklist below selected issue
- Display editable TODO checklist and email preview (subject = issue title; body = repo metadata + TODOs)
- Confirm button to send email

**Tradeoffs:**
- MVP UI is minimal: no user accounts, no saved preferences (tradeoff: faster dev vs. personalization)
- Email workflow is one-step with preview to reduce errors but no scheduling or multiple issue emails
- Filtering limited to skill/language to keep UI simple; advanced filters deferred

**Actionables:**
- Build React app with GitHub API integration for issues & metadata
- Implement ranking labels client-side based on fetched data
- Integrate AI TODO generation as async call after issue selection
- Use simple email API (e.g., SendGrid sandbox) for demo sending
- Ensure mobile-friendly layout but focus desktop-first for dev speed
- Backend Engineer: API Design:

1. GET /issues?skills=&languages=&competency= - Fetch normalized GitHub issues filtered by user skills, language prefs, ranked by difficulty. Returns paginated list with metadata and ranking labels.

2. POST /issue/{id}/todo - Calls engineer AI agent to generate step-by-step TODOs for selected issue. Returns TODO checklist.

3. POST /email/send - Sends email to user with issue title as subject, body includes repo metadata, OSS project info, and TODO checklist.

Local Persistence:

- Store fetched issues JSON locally (file-based DB like SQLite or JSON files) with indexing on skills, languages, competency for quick filtering offline.

- Cache generated TODOs per issue to avoid repeated AI calls.

- Persist sent email logs with timestamps and user info for metrics.

Tradeoffs:

- Local file-backed persistence ensures CLI-first, offline usability, and quick iteration but limits real-time multi-user sync.

- Using GitHub API directly in backend simplifies ingestion but requires token management and rate-limit handling.

- AI TODO generation is async; caching reduces latency but may serve stale plans if issues update.

Actionables:

- Define JSON schema for normalized issues including ranking and metadata.

- Implement SQLite schema for issues, TODOs, and email logs.

- Build API endpoints with authentication and rate-limit safeguards.

- Design email template including dynamic TODO checklist insertion.

- Plan CLI tool to sync issues locally, trigger TODO generation, and send emails.

This minimal API and local persistence plan enables a runnable POC without external paid services or fragile integrations.
- Auth Engineer: For local POC (CLI-first, local-first, file-backed):

- Use OAuth Device Flow or GitHub Personal Access Token (PAT) for GitHub API auth to avoid complex web flows.
- Store tokens encrypted locally (e.g., OS keychain or encrypted file).
- No user accounts or backend session management needed.
- Email sending can use local SMTP config or a simple API key stored locally.
- Keep auth minimal to enable quick iteration and offline dev.

Tradeoffs:
- Local PAT or device flow is simple but less scalable and secure than full OAuth with backend.
- No centralized user management or token revocation.
- Email sending depends on user-configured SMTP or lightweight API keys, limiting reliability.

For production handoff:

- Implement full OAuth 2.0 with GitHub for user login and token management.
- Backend stores tokens securely with refresh tokens if applicable.
- Use a dedicated email service (e.g., SendGrid, SES) with API keys stored in secrets manager.
- Add RBAC and rate limiting to protect APIs.
- Support token revocation and audit logs.

Tradeoffs:
- More complex infrastructure and dev time.
- Requires secure backend and compliance with data protection.
- Enables multi-user, scalable, and secure operation.

Action:
1. Start POC with local PAT/device flow and file-backed token storage.
2. Design auth interfaces to be replaceable with OAuth backend later.
3. Plan production backend with OAuth, secure token storage, and managed email service.
- Database Engineer: For a local-first, deployable MVP of the AI OSS Good-First-Issue Discovery assistant, choose SQLite as the default database:

- **Why SQLite?**  
  - Zero-configuration, file-based, no server needed → fits CLI-first, local-first approach.  
  - Lightweight but supports complex queries for issue ranking and filtering.  
  - Easy to backup, share, and inspect artifacts (DB file) by other agents or users.  
  - Mature ecosystem with Python/Node.js/Go bindings for rapid MVP development.

- **Schema suggestions:**  
  - Tables: `repositories`, `issues`, `users`, `competency_levels`, `issue_rankings`, `todo_plans`.  
  - Index on issue difficulty, language, and user preferences for fast filtering.

- **Tradeoffs:**  
  - Not suited for high concurrency or massive scale, but MVP scope is single-user local usage.  
  - Limited built-in full-text search; consider SQLite FTS5 extension if needed for issue text search.  
  - No built-in replication or clustering, but not required here.

- **Action:**  
  - Implement DB schema in SQLite.  
  - Store GitHub API ingested data locally.  
  - Use DB to power UI filters and ranking engine.  
  - Persist generated TODO plans for email workflow.

This choice maximizes simplicity, portability, and developer accessibility while minimizing infrastructure overhead.
- Infra Engineer: **Deployment Shape Recommendation for AI OSS Good-First-Issue Discovery and Guided Resolution Assistant**

1. **AWS Core Services:**
   - **API & Backend:** Use AWS Lambda (serverless) for GitHub API ingestion, ranking engine, and AI TODO generation calls. Lambda scales automatically and reduces ops overhead.
   - **Data Storage:** DynamoDB for normalized issues, user preferences, and ranking metadata (low-latency, scalable NoSQL).
   - **Email Delivery:** Amazon SES for reliable, cost-effective email sending.
   - **Web UI Hosting:** Deploy static React app on Vercel for fast global CDN and developer experience.
   - **Authentication:** AWS Cognito for user management and secure access to UI and APIs.

2. **Terraform:**
   - Manage AWS infrastructure (Lambda, DynamoDB, SES, Cognito) as code for repeatability and environment parity.
   - Use Vercel Terraform provider or CLI automation for UI deployment.

3. **Tradeoffs:**
   - **Serverless vs. Containers:** Lambda reduces operational burden but has cold start latency; acceptable for this use case.
   - **Vercel for UI:** Simplifies frontend deployment and CDN; less control than AWS Amplify but faster iteration.
   - **SES Email Limits:** SES free tier is limited; monitor usage and request quota increases if scaling.
   - **Data Model:** DynamoDB is schemaless, flexible but requires careful design for query efficiency.

**Actionable Next Steps:**
- Define Terraform modules for AWS Lambda functions, DynamoDB tables, SES setup, and Cognito user pool.
- Develop CI/CD pipelines integrating Terraform apply and Vercel deploy.
- Prototype Lambda GitHub ingestion + SES email workflow.
- Build minimal React UI on Vercel with API integration.
- Monitor costs and performance; iterate on scaling and UX.
- DevOps Engineer: **GitHub Automation & Checks:**

- Use GitHub Actions triggered on schedule (e.g., daily) to:
  - Query GitHub API for "good first issues" across target repos.
  - Normalize and store issues in a DB or JSON artifact.
  - Run ranking engine (easy→hard) based on competency & language prefs.
- On user selection (via UI or API), trigger an action to:
  - Call engineer AI agent to generate step-by-step TODOs.
  - Compose and send email with issue metadata + TODO checklist.
- Implement checks:
  - Validate GitHub API rate limits and handle errors gracefully.
  - Lint and test AI-generated TODO format for consistency.
  - Monitor email delivery success and bounce rates.

**Deployment Notes:**

- Deploy backend as containerized microservice with environment variables for GitHub tokens, AI API keys, and SMTP credentials.
- Use secrets management for sensitive keys.
- Schedule GitHub Actions workflows in `.github/workflows/` with clear concurrency limits.
- Log all automation runs with metrics for success/failure and timing.
- Tradeoffs:
  - GitHub Actions ease integration but have runtime limits; heavy AI calls may require external serverless functions.
  - Email delivery via SMTP is simple but may need scaling to transactional email services if volume grows.
  - Storing issues locally vs DB: DB enables richer querying but adds complexity.

This setup ensures repeatable, observable automation with clear failure points and scalability paths.
- OpenSpec Writer: Implementation Requirements:

1. GitHub API Integration  
- Authenticate and query repositories for issues labeled "good first issue" or similar.  
- Normalize issue data (title, body, labels, repo metadata).  
- Refresh data periodically (e.g., daily) to keep issue list current.

2. Competency & Language Preference Model  
- Allow users to input skill level and preferred languages.  
- Map issues to competency tiers (easy, intermediate, hard) based on heuristics (e.g., label presence, issue complexity).  
- Filter and rank issues accordingly.

3. Web UI  
- Display issues with filters (language, difficulty).  
- Show ranking labels and brief metadata.  
- Allow user selection of an issue.

4. Engineer AI Agent for TODO Generation  
- On issue selection, call AI agent to generate a step-by-step implementation checklist.  
- Ensure output is actionable, concise, and context-aware.

5. Email Workflow  
- Compose email with subject = issue title.  
- Body includes repo metadata, issue details, and AI-generated TODOs.  
- Send email to user with tracking for open and click-through rates.

Acceptance Criteria:

- Issues are ingested and normalized with >95% accuracy.  
- UI filters and ranks issues correctly per user preferences.  
- AI-generated TODOs are relevant and actionable (validated by sample user testing).  
- Email is sent within 1 minute of issue selection with correct content.  
- Metrics for email open rate and contributor completion are tracked.

Tradeoffs:

- MVP uses GitHub API only; no multi-platform support initially.  
- AI agent runs synchronously to minimize latency but may limit complexity.  
- Email is single-issue focused to reduce scope; batch workflows deferred.  
- Web UI prioritized over CLI for user engagement despite higher dev cost.

Action: Begin GitHub API integration and UI prototyping in parallel; design AI prompt templates for TODO generation; implement email service with tracking hooks.
