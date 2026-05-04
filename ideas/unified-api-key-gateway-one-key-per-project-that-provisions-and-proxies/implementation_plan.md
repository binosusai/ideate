# Implementation Plan: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Goal
Create a working proof of concept that demonstrates the core value of `Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys` with the smallest credible interface.

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
`unified-api-key-gateway-one-key-per-project-that-provisions-and-proxies`

## Debate Context Used
Founder Board debate exists and was considered.

## Crew Implementation Notes
- Product Planner: MVP Workflow for Unified API Key Gateway

1. CLI-First Setup (Day 1)
- Build a local CLI tool to create a project and generate one unified API key.
- Store third-party API keys in a local encrypted JSON file (file-backed, no external DB).
- Support 2–3 popular APIs (e.g., Stripe, SendGrid, Auth0) with hardcoded minimal provisioning flows (e.g., OAuth token exchange or manual input).

2. Proxy Server (Day 2–3)
- Implement a lightweight local proxy server that accepts requests authenticated by the unified key.
- Proxy requests to the appropriate third-party API using stored keys.
- Log requests/responses for debugging.

3. Demo Integration (Day 4)
- Provide sample code snippets showing how a developer uses the unified key to call multiple APIs via the proxy.
- Include onboarding CLI commands for adding/removing APIs.

4. Pilot Testing (Day 5)
- Onboard 2–3 early-stage SaaS startups via Slack groups.
- Offer concierge onboarding to migrate existing keys.
- Collect feedback on setup time, security concerns, and usability.

Tradeoffs:
- Local-first and file-backed limits scalability but accelerates MVP delivery and reduces security risk.
- Hardcoded APIs limit breadth but prove core concept.
- No paid services or external deployment reduces cost and complexity but requires manual pilot coordination.

Outcome:
A working POC within one week that validates demand, usability, and security assumptions before full engineering investment.
- POC Coder: POC Plan: CLI-first local proxy for unified API key gateway

Scope:
- Support 2–3 popular APIs (e.g., Stripe, SendGrid, Auth0) with hardcoded minimal proxy logic
- Single project context with one unified key (e.g., UUID)
- Local CLI tool that:
  1. Accepts unified key input
  2. Maps unified key to stored third-party keys in a local JSON file (file-backed for persistence)
  3. Proxies HTTP requests to third-party APIs by rewriting auth headers with stored keys
- No external deployment or paid services; all local and ephemeral
- No user auth or multi-user support (out of scope for POC)
- Simple logging to show request flow and key substitution

Tradeoffs:
- Security: Local file storage only, no encryption (acceptable for demo, not production)
- Scalability: Single user, single project only
- API coverage: Minimal, no full API surface or error handling
- UX: CLI-only, no UI or onboarding automation yet

Deliverables:
- CLI tool (Node.js or Python) with commands: `init`, `add-key`, `proxy-request`
- README with usage and demo script calling Stripe/SendGrid/Auth0 endpoints via proxy
- Demo script showing unified key usage reduces setup friction

This POC proves core value: one key per project proxies multiple APIs, easing onboarding friction. It’s actionable within 1–2 days by a single dev.
- Frontend Engineer: POC Interface Plan: Unified API Key Gateway Dashboard (Web + CLI)

1. Web UI (React):
- Project list: Create/view projects (1 unified key each)
- Inside project: Add/remove 3rd-party tools (Stripe, SendGrid, Auth0)
- For each tool: Input API key once, stored encrypted locally (POC: in-memory/sessionStorage)
- Show unified project API key (proxy key) for client usage
- Button: “Test API call” per tool via proxy, showing success/failure
- Minimal auth: local password or token for demo

Tradeoffs:
- Web UI enables quick demo, visual validation, and user feedback
- In-memory storage limits persistence but simplifies POC, no backend needed
- Supports only 3 APIs to reduce scope and complexity

2. CLI (Node.js):
- Commands: create-project, add-tool, list-projects, get-unified-key, test-call
- Local JSON file storage for demo persistence
- Output unified key and proxy call results

Tradeoffs:
- CLI-first aligns with Builder’s recommendation and developer workflows
- File-backed storage avoids external deps, easy to share/demo
- Limited API support and no multi-user support for MVP speed

Action:
- Build minimal React dashboard + CLI with above features
- Use mock API proxy layer to simulate key proxying
- Demo with 2–3 startups to validate UX and value proposition within 1 week
- Backend Engineer: API Design for POC:

1. **POST /projects**  
- Create a project and generate a unified API key (UUID).  
- Request: { "project_name": string }  
- Response: { "project_id": string, "unified_key": string }

2. **POST /projects/{project_id}/third_party_keys**  
- Add third-party API keys to a project (store encrypted locally).  
- Request: { "service": enum("stripe","sendgrid","auth0"), "api_key": string }  
- Response: 201 Created

3. **GET /projects/{project_id}/proxy/{service}/**  
- Proxy endpoint that forwards requests to the third-party API using stored keys.  
- Auth: unified_key in header  
- Proxy transparently injects the stored third-party key.

Local Persistence:

- File-backed JSON or SQLite DB per user, storing:  
  - Projects: { id, name, unified_key }  
  - Third-party keys encrypted at rest (AES-256) linked to projects  
- CLI tool reads/writes this local store.

Tradeoffs:

- **Security:** Local encrypted storage avoids cloud risks but requires user trust in local device security.  
- **Simplicity:** File-backed storage and minimal API surface enable rapid POC delivery without external dependencies.  
- **Scope:** Proxy limited to 2–3 services and basic forwarding reduces complexity but may limit demo breadth.  
- **No multi-user support** in POC; focus on single dev/project to prove concept fast.

Action: Implement minimal CLI + local store + lightweight HTTP proxy with above API within 1 week.
- Auth Engineer: For the local POC, adopt a **CLI-first, local-first, file-backed auth posture**:

- Generate one unified API key per project locally.
- Store third-party API keys encrypted in a local config file (e.g., JSON with AES encryption).
- Proxy API requests through a local lightweight server that injects the correct third-party keys.
- No external dependencies or paid services.
- Support 2–3 key integrations (Stripe, SendGrid, Auth0) hardcoded for MVP speed.
- CLI commands to create, list, and revoke unified keys.
- Logs and telemetry local only, no network calls.

**Tradeoffs:**  
+ Fast iteration, no cloud infra needed, easy to demo and debug.  
- No multi-user or team sync, no high availability, no hardened security beyond local encryption.

For production handoff, evolve to a **cloud-hosted, multi-tenant API gateway with secure vault-backed key storage**:

- Use a managed secrets manager (AWS Secrets Manager, HashiCorp Vault) for encrypted storage.  
- Authenticate clients with OAuth2 or JWT tokens scoped per project.  
- Proxy API calls with rate limiting, monitoring, and audit logs.  
- Provide a web dashboard for key lifecycle management and onboarding.  
- Implement strict RBAC and compliance controls.

**Tradeoffs:**  
+ Scalable, secure, multi-user, enterprise-ready.  
- Higher complexity, cost, and longer build time.

This staged approach balances rapid POC validation with a clear path to production-grade security and usability.
- Database Engineer: For the Unified API Key Gateway POC, choose a local, deployable database that is zero-config, file-backed, and embeddable to maximize simplicity, speed, and developer trust:

**Recommendation:** SQLite (v3) with WAL mode  
- **Why:**  
  - Single-file DB, no server needed, perfect for CLI-first local-first approach  
  - ACID compliant, reliable for credential storage  
  - Widely supported, easy to integrate in Node.js/Python/Go  
  - WAL mode enables concurrent reads/writes, good for proxying keys  
  - No external dependencies or paid services required  
- **Tradeoffs:**  
  - Not designed for multi-node scaling (acceptable for POC)  
  - Limited built-in encryption; encrypt sensitive fields at app layer or use OS-level encryption  
  - File-based means backup/restoration must be manual or scripted  

**Implementation notes:**  
- Store API keys encrypted at rest using a master key derived from user passphrase or environment variable  
- Use a simple schema: projects table, third_party_keys table linked by project_id  
- Keep DB file in user’s home directory or project folder for easy access and portability  
- For demo, keep all state local; later consider syncing or server-backed DB if scaling  

This approach delivers a secure, local, deployable DB that aligns with MVP speed, CLI-first, and no external dependency goals.
- Infra Engineer: Deploy a minimal POC on AWS + Vercel with Terraform for rapid iteration:

1. **AWS Infra**  
- Use AWS Lambda (Node.js) behind API Gateway for proxying unified keys to 2–3 third-party APIs (Stripe, SendGrid, Auth0).  
- Store API keys encrypted in AWS Secrets Manager scoped per project.  
- Use DynamoDB for lightweight metadata (project, key mappings).  
- IAM roles tightly scoped to Lambda and Secrets Manager access.  

2. **Vercel Frontend**  
- CLI-first React app deployed on Vercel for onboarding and key management UI.  
- Use Vercel Serverless Functions for auth and proxy fallback if needed.  

3. **Terraform**  
- Manage all infra as code: API Gateway, Lambda, Secrets Manager, DynamoDB, Vercel project config.  
- Enable easy environment replication and rollback.  

**Tradeoffs:**  
- AWS Lambda + API Gateway adds latency but offers zero-maintenance scaling and security.  
- Secrets Manager costs scale with usage but ensures secure key storage and rotation.  
- Vercel frontend accelerates developer UX but adds cross-cloud complexity.  
- Terraform upfront cost pays off in reproducibility and team onboarding speed.  

This shape enables a one-week POC proving unified key proxying and onboarding with minimal ops overhead and clear security boundaries.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions for CI/CD with workflows triggered on PRs and merges to main.
- Checks: Linting, unit tests, and security scans (e.g., secret scanning, dependency vulnerability).
- Add a workflow to run the POC CLI tool against a sample project to validate provisioning and proxying.
- Automate semantic versioning and changelog generation on merges.

Deployment Notes:
- POC deploys as a CLI-first, local-first tool with file-backed config (no external paid services).
- Use GitHub Releases to distribute CLI binaries.
- Document onboarding steps for pilot startups, including how to run the CLI and connect 2–3 third-party APIs.
- Include a rollback plan: users keep existing API keys until migration is verified.
- Monitor usage and errors via optional telemetry (opt-in).

Tradeoffs:
- CLI-first limits immediate cloud scalability but accelerates MVP delivery and reduces security risks.
- No external deployment avoids fragile integrations but delays SaaS platform rollout.
- Focus on 2–3 APIs reduces scope but enables rapid, visible demo.
- In-memory or file-backed storage simplifies POC but requires redesign for production secrets management.

Action:
- Define GitHub Actions workflows for CI, tests, and POC validation.
- Prepare release pipeline for CLI.
- Write deployment and pilot onboarding docs.
- Schedule pilot with 2–3 YC startups for feedback within one week.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that manages a single unified API key per project.
2. Support provisioning, storing, and proxying keys for 2–3 popular third-party APIs (e.g., Stripe, SendGrid, Auth0).
3. Use in-memory or local file-backed storage to avoid external dependencies.
4. Provide a simple proxy server that relays requests authenticated by the unified key to the respective third-party APIs.
5. Enable single-click onboarding flow for adding new third-party APIs within the project.
6. Produce artifacts (config files, logs) readable by other teams for handoff.
7. Include basic security measures (e.g., encrypted local storage, scoped keys).
8. No paid services or external deployments required for POC.

Acceptance Criteria:
- Developer can create one unified API key for a project via CLI.
- Developer can onboard at least 2 third-party APIs with a single command.
- Proxy server correctly routes requests authenticated by the unified key to the appropriate third-party API.
- Local storage persists keys securely between sessions.
- Demo onboarding reduces setup time from hours to minutes in a test scenario.
- Pilot with 2–3 early-stage SaaS startups confirms usability and identifies adoption blockers.

Tradeoffs:
- Limited API coverage and language support to reduce scope and risk.
- Local storage only, no cloud sync, to avoid security and deployment complexity.
- Minimal security for POC; full compliance and hardened security deferred to later stages.
