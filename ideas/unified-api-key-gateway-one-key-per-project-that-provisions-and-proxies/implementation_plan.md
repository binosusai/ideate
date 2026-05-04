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

1. Scope: CLI-first, local-first, file-backed MVP proxying 2–3 popular APIs (e.g., Stripe, SendGrid, Google Analytics) to prove core value.

2. Project Setup: User runs CLI command to create a new project, generating one unified API key (UUID) stored locally in an encrypted JSON/YAML file.

3. API Key Provisioning: User inputs existing third-party API keys via CLI prompts, which are encrypted and stored in the project file. No external service dependency.

4. Proxy Server: Local lightweight HTTP proxy (Node.js/Go) runs per project, intercepting calls authenticated by the unified key, routing them to corresponding third-party APIs with stored keys.

5. Logging & Auditing: Proxy logs all proxied requests/responses locally with timestamps and API target for auditability.

6. Onboarding New APIs: CLI command adds new API keys and updates proxy routing config.

7. Security: Local encryption of keys; no cloud storage; CLI requires user authentication (e.g., OS user).

Tradeoffs:
- No cloud sync limits team collaboration but accelerates MVP speed and reduces risk.
- Local proxy limits scale but proves concept quickly.
- Supporting only 2–3 APIs reduces scope but validates core abstraction.

Next steps: Build CLI + local proxy + encrypted file storage in 1 week; demo with Stripe integration; collect early user feedback on setup time and security perception.
- POC Coder: Smallest working POC plan:

- Scope: CLI tool + local file storage, no external services.
- Support 1 project, proxy 1 third-party API (Stripe chosen for high developer value).
- Workflow:
  1. User runs CLI to create a unified project key (UUID).
  2. CLI stores Stripe API key encrypted in a local JSON/YAML file keyed by project key.
  3. CLI runs a local HTTP proxy server that:
     - Accepts requests with unified project key in header.
     - Maps to stored Stripe key.
     - Forwards request to Stripe API with correct Stripe key.
     - Logs request metadata (timestamp, endpoint).
     - Returns Stripe response transparently.
- Deliverables:
  - CLI commands: `init`, `add-key`, `start-proxy`.
  - Local encrypted config file storing third-party keys.
  - Proxy server logs requests for audit.
- Tradeoffs:
  - No multi-user or multi-project support yet.
  - No UI, no onboarding automation.
  - Local-only, no cloud deployment or scaling.
  - No key rotation or revocation.
- Why this works:
  - Proves unified key abstraction and proxying.
  - Demonstrates centralized credential management.
  - Enables quick user feedback on core value.
  - Minimal dependencies, fast build (<1 day).

This POC validates core thesis with minimal engineering risk and cost.
- Frontend Engineer: POC Interface Plan: CLI-first, minimal UI dashboard

1. CLI Commands (primary UX):
- `init-project [name]`: create project config file (YAML/JSON), local file-backed
- `add-api-key [provider] [key]`: securely store encrypted API key locally
- `list-apis`: show integrated APIs with masked keys
- `proxy-call [provider] [endpoint] [payload]`: route API request through unified key proxy, log request/response

2. Minimal Web Dashboard (optional, post-CLI MVP):
- Project overview: list APIs, usage stats, logs
- Add/remove API keys UI
- Audit trail: timestamped proxy logs

Tradeoffs:
- CLI-first enables quick iteration, no backend infra needed, easy artifact handoff to other teams
- Local file storage limits multi-user collaboration but accelerates POC delivery
- Proxy limited to 1–2 APIs (e.g. Stripe, SendGrid) to validate core abstraction without overbuilding
- Minimal UI avoids premature complexity; focus on core flows and data structures

Action:
- Define CLI commands and config schema this week
- Build proxy middleware for Stripe API with logging
- Deliver working CLI demo with local file storage and proxy call logs within 3–5 days
- Backend Engineer: API Definition for POC:

- POST /projects  
  Create a project with a unified API key (UUID). Returns project ID and unified key.

- POST /projects/{projectId}/integrations  
  Add a third-party API integration (e.g., Stripe) with its API key securely stored encrypted locally.

- GET /projects/{projectId}/proxy/{integrationName}/{*path}  
  Proxy endpoint that forwards requests to the third-party API using stored keys, logs calls, and returns responses.

Local Persistence:

- File-backed JSON/YAML config per project storing:  
  - Project metadata (ID, unified key)  
  - Encrypted integration credentials (AES-256 symmetric encryption with user passphrase)  
  - Proxy call logs (timestamp, endpoint, response status)

Tradeoffs:

- CLI-first, local file storage avoids early cloud complexity and paid services, enabling rapid POC delivery.  
- Encryption ensures credentials are secure at rest but requires user passphrase management.  
- Proxying only 1–2 popular APIs (Stripe, SendGrid) limits scope but proves core concept fast.  
- Logging calls locally enables auditability but lacks centralized monitoring—acceptable for POC.  
- No external deployment; users run CLI locally, simplifying compliance and iteration.

Action: Implement CLI tool with above APIs, local encrypted config, and proxy for Stripe integration first.
- Auth Engineer: For the local POC, adopt a **CLI-first, local-first, file-backed auth posture**:

- **Implementation**:  
  - Generate one unified project API key locally (e.g., UUID).  
  - Store third-party API keys encrypted in a local config file (e.g., JSON + AES encryption).  
  - Proxy requests via a local lightweight server that injects real keys and logs calls.  
  - No external dependencies or paid services.  
  - Support 1–2 popular APIs (e.g., Stripe) for demo.  

- **Tradeoffs**:  
  - Pros: Fast iteration, no cloud infra needed, easy to demo and debug, minimal security surface for POC.  
  - Cons: Not scalable or multi-user; local storage risks key leakage if machine compromised; no centralized audit or rotation yet.  

For production handoff, shift to a **cloud-hosted API gateway with centralized secrets management**:

- **Implementation**:  
  - Use a managed secrets vault (e.g., AWS Secrets Manager) for storing third-party keys.  
  - Deploy a secure API gateway that authenticates via the unified project key, proxies calls, injects keys, and logs usage.  
  - Implement RBAC, audit logs, and key rotation policies.  
  - Support multi-tenant, multi-user access with compliance controls.  

- **Tradeoffs**:  
  - Pros: Scalable, secure, compliant, supports team workflows and auditing.  
  - Cons: Higher complexity, cost, and deployment overhead. Requires cloud infrastructure and operational maturity.  

**Action**: Build the local CLI POC first to validate core concept rapidly. Plan production architecture in parallel to ensure smooth handoff once POC proves value.
- Database Engineer: For the POC of the unified API key gateway, choose a local-first, file-backed embedded database to maximize simplicity, speed, and deployability:

**Recommendation:** Use SQLite with SQLCipher (for encryption) as the default local database.

**Implementation details:**
- Store API key metadata, proxy logs, and project configs in a single encrypted SQLite file per project.
- SQLite requires zero setup, is cross-platform, and supports ACID transactions.
- SQLCipher adds transparent AES-256 encryption, addressing compliance and security needs.
- CLI tool reads/writes this file, enabling offline use and easy artifact sharing.
- Schema: tables for projects, third-party API keys, proxy logs with timestamps, and user audit info.
- Use a lightweight ORM or direct SQL for fast iteration.

**Tradeoffs:**
- Pros: No external dependencies, easy to version-control, portable, secure at rest.
- Cons: Limited concurrent writes (acceptable for single-user CLI POC), no built-in multi-node sync.
- Avoids complexity of server-based DBs or paid services, fitting the “local-first” and “no fragile integrations” mandate.

This approach enables a minimal viable demo within a day, proving core functionality and security without cloud reliance.
- Infra Engineer: **Deployment Shape for Unified API Key Gateway POC**

- **Cloud Provider:** AWS (mature, secure, cost-effective, rich IAM)
- **Compute:** Vercel for frontend/UI (fast iteration, serverless edge functions), AWS Lambda for backend proxy and key management (scalable, event-driven)
- **API Gateway:** AWS API Gateway to expose unified API key endpoints, handle throttling, and secure proxying
- **Secrets Management:** AWS Secrets Manager to store third-party API keys securely, with fine-grained access control
- **Infrastructure as Code:** Terraform to provision AWS resources and Vercel integration, enabling repeatable, versioned deployments
- **Data Storage:** DynamoDB for lightweight audit logs and usage tracking (serverless, low latency)
- **Security:** Use AWS IAM roles for Lambda, API Gateway authorizers for authentication, and TLS everywhere
- **Tradeoffs:**
  - AWS Lambda + API Gateway adds latency vs. monolith but gains scalability and security
  - Vercel accelerates frontend dev but adds a separate deployment target; mitigated by Terraform multi-provider setup
  - Secrets Manager costs scale with usage; acceptable for POC but monitor for production
- **Actionables:**
  1. Define Terraform modules for Lambda, API Gateway, Secrets Manager, DynamoDB
  2. Setup Vercel project linked to GitHub for frontend CLI/dashboard
  3. Implement Lambda proxy for Stripe API key abstraction first
  4. Enable logging and audit trail in DynamoDB
  5. Secure API Gateway with API keys or JWT authorizer
  6. Automate deployment pipeline via GitHub Actions integrating Terraform and Vercel CLI

This shape balances rapid POC delivery, security, and scalability, enabling quick iteration and early user feedback.
- DevOps Engineer: GitHub Automation & Checks for Unified API Key Gateway POC:

1. **CI Workflow** (`.github/workflows/ci.yml`):
   - Trigger: `push` & `pull_request` on `main` and feature branches.
   - Steps:
     - Checkout code
     - Run lint (e.g., ESLint or Go vet)
     - Run unit tests with coverage
     - Build CLI binary (local-first, file-backed)
     - Run integration tests against mocked Stripe API proxy
   - Fail fast on errors to ensure code quality and proxy correctness.

2. **Security Checks**:
   - Use `secret-scanning` GitHub Action to prevent accidental API key commits.
   - Enforce branch protection rules requiring passing CI before merge.

3. **Deployment Notes**:
   - POC is CLI-first, local-only, file-backed; no external deployment needed.
   - Deployment is manual: users clone repo, build CLI, and run locally.
   - Document setup steps clearly in README for quick onboarding.
   - Proxy logs stored locally for auditability; no cloud infra yet.

**Tradeoffs**:
- No automated deployment reduces complexity and risk but limits demo scalability.
- Mocked API proxy simplifies early validation but defers real API integration challenges.
- Local-first approach accelerates POC delivery but postpones multi-user and cloud security concerns.

This setup enables a fast, secure, and focused POC validating core hypothesis within one week.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that manages a project’s unified API key.
2. File-backed storage of key mappings and proxy config, readable by other teams.
3. Proxy support for 2–3 high-value APIs (e.g., Stripe, Twilio, Google Analytics) with request forwarding and response passthrough.
4. Centralized logging of all proxied API calls for audit and compliance.
5. Secure storage/encryption of third-party API keys locally; no external paid services or cloud dependencies.
6. One unified API key per project that authenticates all proxied calls.
7. Minimal UI: CLI commands for onboarding new APIs, rotating keys, and viewing logs.
8. Demo scope limited to a single project context, no multi-tenant or user management initially.
9. Automated tests for proxy correctness, key rotation, and logging.

Acceptance Checks:
- CLI can onboard Stripe API key, generate unified project key, and proxy calls successfully.
- Logs show all proxied requests with timestamps and API target.
- Rotation of underlying API keys updates proxy without downtime.
- No external service dependencies; runs fully locally.
- Documentation enables another crew to read config files and extend proxy support.

Tradeoffs:
- Local-first limits immediate SaaS scalability but accelerates POC speed and security.
- Proxying only 2–3 APIs narrows scope but proves core value quickly.
- CLI over UI reduces polish but prioritizes developer adoption and iteration speed.
