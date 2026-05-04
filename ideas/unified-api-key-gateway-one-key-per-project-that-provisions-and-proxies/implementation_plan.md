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
- Product Planner: MVP Workflow for Unified API Key Gateway:

1. Scope Minimal Integrations: Select 2–3 popular APIs (e.g., Stripe, SendGrid, Segment) to support initially, covering payment, messaging, and analytics.

2. CLI-First & Local-First: Build a CLI tool that developers run locally, storing config and keys in encrypted local files (e.g., JSON + AES encryption). This avoids early cloud infra and paid services.

3. Single Unified Key: Generate one project-level API key that the CLI uses to proxy requests to third-party APIs. Proxy logic translates calls and injects underlying keys.

4. Proxy Server: Implement a lightweight local proxy server (Node.js or Go) that the CLI spins up on demand, forwarding requests to third-party APIs using stored keys.

5. Onboarding Flow: CLI command to add a new third-party API integration with minimal prompts, storing credentials securely and updating proxy config.

6. Demo Script: Provide a scripted demo showing onboarding a new API and making proxied calls via the unified key.

Tradeoffs:
- Security: Local encrypted storage limits risk but no multi-user sync yet.
- Scale: No multi-user/team management initially; focus on solo devs or small teams.
- Features: No UI or dashboard in MVP; CLI-only to maximize speed.

Deliverables:
- CLI tool repo with onboarding and proxy commands
- README with setup and demo instructions
- Basic test coverage for proxy and key management

This MVP enables rapid validation of core value with minimal dependencies and cost.
- POC Coder: Smallest working POC plan:

1. CLI tool (Node.js or Python) that:
  - Accepts a “project key” (UUID or random token) as input.
  - Stores minimal config in a local JSON file mapping project key → 2–3 hardcoded third-party API keys (e.g., Stripe test key, SendGrid test key).
  - Proxies requests from user to these APIs by rewriting Authorization headers with stored keys.

2. Minimal HTTP proxy server (Express or Flask):
  - Listens locally.
  - Routes incoming requests with project key header to corresponding third-party API.
  - Returns proxied responses transparently.

3. Demo flow:
  - User runs CLI to generate project key and config file.
  - User sends API calls to local proxy with project key.
  - Proxy injects correct third-party key and forwards request.

Tradeoffs:
- No real provisioning UI or onboarding automation (manual config edits).
- No multi-user or security hardening (local-only, no encryption).
- Only 2–3 APIs hardcoded, no dynamic integration.
- No billing or analytics.

This POC proves unified key usage and proxying concept in <1 day, requires no paid services or deployment, and produces artifacts for next-stage automation.
- Frontend Engineer: POC Interface Plan:

1. **Project Dashboard (Web UI)**  
- Lists projects with unified API key status (e.g., active, pending).  
- Action: “Create Project” button launches minimal form (name, description).  

2. **Project Detail View**  
- Shows a single unified API key for the project.  
- Lists integrated third-party tools (start with Stripe, SendGrid).  
- “Add Integration” button triggers OAuth or API key input flow for that tool.  

3. **Unified Key Usage Example**  
- Show sample request snippet using the unified key to proxy calls.  

4. **Key Rotation & Revocation**  
- Simple “Rotate Key” and “Revoke Key” buttons per project.  

Tradeoffs:  
- Start web-first for demo clarity; CLI local-first can follow.  
- Limit integrations to 2–3 popular APIs to reduce scope and dependencies.  
- Proxying real API calls can be mocked or stubbed to avoid paid services.  
- Minimal UI avoids complex auth flows initially; OAuth can be faked or simplified.  

Actionable next step: Build React components for Project Dashboard and Detail View with static data, then wire up stubbed API calls to simulate provisioning and proxying.
- Backend Engineer: API Definition:
- POST /projects/{projectId}/unified-key: Create or retrieve the unified API key for a project.
- POST /projects/{projectId}/integrations: Add a third-party API integration by securely storing its credentials.
- GET /projects/{projectId}/proxy/{integrationName}/**: Proxy requests to the third-party API using stored keys.
- DELETE /projects/{projectId}/integrations/{integrationName}: Remove an integration and revoke keys.

Local Persistence:
- File-backed JSON/YAML config per project storing:
  - Unified API key (UUID or JWT)
  - List of integrations with encrypted third-party API keys
  - Proxy routing rules
- Use local encryption (e.g., libsodium) to secure stored keys.

Tradeoffs:
- CLI-first, local file persistence enables rapid POC without external dependencies but limits multi-user sync and real-time revocation.
- Proxying via backend simplifies client security but adds latency and complexity; POC should proxy only 2–3 APIs (Stripe, SendGrid).
- Avoid paid services or cloud secrets managers to keep POC lightweight and self-contained.
- Use simple authentication (API key header) for unified key to minimize complexity.

Action:
- Implement CLI tool to generate/store unified key and integrations file.
- Build minimal HTTP proxy server reading local config to forward requests.
- Demo onboarding flow: one command adds integration, one key used for all proxied calls.
- Auth Engineer: For local POC: Use a CLI-first, file-backed auth posture with a single unified API key per project stored encrypted locally (e.g., AES-256). The CLI proxies requests to third-party APIs using stored keys fetched from config files. No external dependencies or paid services. This keeps the POC lightweight, fast to build, and easy to demo. Tradeoff: limited multi-user support and no centralized audit.

For production handoff: Move to a centralized API gateway with per-project API keys issued by your system, backed by a secure secrets manager (e.g., HashiCorp Vault or AWS Secrets Manager). The gateway proxies all third-party API calls, injecting credentials dynamically. Add RBAC and audit logging for security and compliance. Tradeoff: higher complexity and cost, but essential for multi-user teams, rotation, and compliance.

Action steps:
1. Build local CLI POC with encrypted local config and proxy logic.
2. Design production gateway API key issuance and proxy flow.
3. Integrate secrets manager and audit logging for production.
4. Validate security posture with threat modeling before rollout.

This staged approach balances speed and security, enabling quick validation and smooth scaling.
- Database Engineer: For the Unified API Key Gateway POC, choose a local-first, file-backed embedded database to maximize speed, simplicity, and offline capability:

**Recommendation:** Use SQLite as the default database.

**Implementation details:**
- Store API key metadata, provisioning state, and proxy configs in a single `.db` file per project.
- Use SQLite’s ACID transactions to ensure consistency during key rotations and provisioning.
- Bundle SQLite with the CLI tool—no external dependencies or servers.
- Schema: tables for projects, third-party APIs, keys, usage logs.
- Access via lightweight ORM or direct SQL queries in the CLI.

**Tradeoffs:**
- Pros: Zero-config, cross-platform, fast reads/writes, easy backup/restore, no network latency.
- Cons: Limited concurrent writes (acceptable for single-user CLI), no built-in multi-node sync (out of scope for POC).
- Avoid heavier DBs (Postgres, Mongo) to keep POC deployable and simple.
- Avoid in-memory DBs (e.g., SQLite in-memory mode) to persist state across CLI sessions.

This approach enables a minimal, deployable POC that can be extended later with remote sync or multi-user support.
- Infra Engineer: Deploy a minimal viable unified API key gateway on AWS with Terraform and Vercel:

1. **AWS Infra (Terraform):**  
- Use AWS Lambda + API Gateway for proxying third-party APIs.  
- Store third-party API keys securely in AWS Secrets Manager, scoped per project.  
- Use DynamoDB for lightweight metadata (projects, keys, usage).  
- Terraform manages all infra as code for repeatability and auditability.

2. **Vercel Frontend:**  
- Deploy a React-based dashboard on Vercel for project/key management and onboarding flows.  
- Use serverless functions (Vercel Edge Functions) to call AWS APIs securely.

3. **Security & Tradeoffs:**  
- Lambda proxy avoids exposing keys client-side, improving security.  
- Secrets Manager adds cost but ensures secure key storage and rotation.  
- DynamoDB is low-latency but may add complexity vs. simpler file-backed POC.  
- Vercel accelerates frontend deployment but adds cross-cloud complexity.

4. **Actionable Next Steps:**  
- Define Terraform modules for Lambda, API Gateway, Secrets Manager, DynamoDB.  
- Build minimal Lambda proxy for 2–3 APIs (Stripe, SendGrid).  
- Create Vercel dashboard with project/key CRUD and onboarding button.  
- Validate with internal dev team in 1 week.

This shape balances rapid POC speed, security, and extensibility for commercial validation.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions to automate CI/CD.
- On PR: run lint, unit tests, and security scans (e.g., secret scanning, dependency checks).
- On merge to main: run integration tests and build the CLI-first POC artifact.
- Use branch protection rules requiring passing checks before merge.

Deployment Notes:
- Deploy CLI-first POC as a versioned release artifact (GitHub Releases).
- Keep deployment local-first and file-backed; no external services initially.
- Document setup steps for local usage and artifact consumption by other teams.
- Use semantic versioning to track POC iterations.

Tradeoffs:
- No paid services or external deployment reduces complexity and cost but limits real-time multi-user testing.
- CLI-first and file-backed approach accelerates MVP but delays cloud-native scalability.
- Focus on 2–3 popular APIs for POC limits scope but validates core value quickly.

Action:
1. Define GitHub Actions workflows for lint, test, and build.
2. Configure branch protections.
3. Prepare release pipeline for CLI artifact.
4. Document local usage and integration points for next-phase teams.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that manages a unified API key per project.
2. File-backed storage of project config and provisioned keys (e.g., JSON/YAML).
3. Support provisioning and proxying for 2–3 popular APIs (e.g., Stripe, SendGrid, Segment).
4. Proxy requests from user code through the gateway using the unified key.
5. Single-click onboarding flow for adding new third-party APIs.
6. Minimal dependencies; no paid services or external deployments for POC.
7. Logging and error handling for key provisioning and proxying.
8. Extensible architecture for adding more APIs later.

Acceptance Criteria:
- User can create a project and generate one unified API key.
- User can onboard at least two third-party APIs via CLI with a single command.
- Requests to third-party APIs are proxied correctly using provisioned keys.
- Local config files reflect current key mappings and project state.
- No external paid services or fragile integrations are required.
- Demo shows reduced manual key management steps compared to baseline.

Tradeoffs:
- Limited API coverage initially to ensure quick POC delivery.
- Local-first approach may limit multi-user collaboration but accelerates iteration.
- Proxying adds latency but centralizes key management and auditing.
- Avoiding external services reduces complexity but may limit scalability.

Next Steps:
- Define minimal API integrations and CLI commands.
- Build local config schema and proxy server.
- Develop onboarding CLI flow.
- Validate with target users ASAP.
