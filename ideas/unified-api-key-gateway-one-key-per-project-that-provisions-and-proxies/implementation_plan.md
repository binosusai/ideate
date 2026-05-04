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

1. CLI-first tool to create/manage a single project API key.
2. File-backed local config storing mappings: project key → third-party API keys (sandbox/test keys only).
3. Proxy server (local or lightweight cloud) intercepts requests using project key, routes to corresponding third-party APIs.
4. Support 2–3 sandbox APIs with simple REST proxying and key rotation.
5. CLI commands: `init-project`, `add-api-key`, `rotate-key`, `start-proxy`.
6. Minimal auth: project key as bearer token; no user accounts yet.
7. Demo onboarding new dev: share project key file, start proxy, test API calls.
8. No paid services or external deployment; run locally or on dev machine.
9. Logs for request routing and key usage to visualize proxying.
10. Deliverables: CLI tool, proxy server, README with quickstart.

Tradeoffs:
- No multi-user or UI initially to speed delivery.
- Sandbox keys only to avoid compliance/legal issues.
- Local-first avoids cloud complexity but limits scalability.
- Focus on developer experience, deferring enterprise-grade security.

This MVP proves core value: one key per project proxies multiple APIs, easing onboarding and rotation with minimal setup.
- POC Coder: POC Plan: CLI-first local proxy with unified key and 2 sandbox APIs

1. Scope:  
- Local CLI tool managing a single project config file (YAML/JSON) storing 2–3 third-party API keys (sandbox/test keys).  
- Generate one unified project API key (UUID) that clients use locally.  
- Proxy requests from client CLI through local HTTP server, routing to correct third-party API based on path/prefix.  
- Support key rotation by updating config file and invalidating old unified key.  

2. Implementation:  
- Use Node.js or Python for quick local HTTP proxy and CLI.  
- Store keys encrypted in local file (e.g., AES with user password).  
- Proxy logic: map unified key + endpoint to stored third-party keys, forward requests with proper auth headers.  
- Demo: show onboarding a new API key by editing config, then making proxied requests via unified key.  

3. Tradeoffs:  
- No cloud or multi-user sync (simplifies security, speeds dev).  
- No full compliance or audit logs yet (out of scope).  
- Sandbox APIs only to avoid billing/complexity.  
- CLI-only, no UI (fastest MVP).  

Outcome: Demonstrate unified-key proxying and rotation locally in <1 day, proving core value and enabling user feedback before scaling.
- Frontend Engineer: POC Interface: CLI + Minimal Web Dashboard

1. CLI-first tool for local devs:
- Commands: `init-project`, `add-api <tool>`, `list-keys`, `rotate-key <tool>`, `proxy-request <tool> <endpoint> [payload]`
- File-backed config (YAML/JSON) stores unified project key and mapped third-party keys securely encrypted locally.
- Tradeoff: CLI speeds iteration and fits builder’s local-first vision but limits non-CLI users initially.

2. Lightweight Web Dashboard (React):
- Auth via unified project key.
- Views: Project overview (unified key status), API list with status, Add API button (select from 2–3 sandboxed APIs).
- Proxy test panel: send test requests via unified key, display proxied response.
- Tradeoff: Minimal UI to visualize "aha moment" without full auth/session complexity.

3. Explicit tradeoffs:
- No multi-user or deep RBAC yet (out of scope for POC).
- No paid services or external deployment; run locally or in simple container.
- Focus on 2–3 sandbox APIs with mocked responses to prove proxying and rotation.

Action:
- Build CLI commands with file-backed config and encrypted keys.
- Develop React dashboard to visualize unified key and proxy test.
- Demo onboarding a new API and rotating keys to show immediate value.
- Backend Engineer: API Definition for POC:

- POST /projects  
  Create a project with a unified API key (UUID). Returns project ID and unified key.

- POST /projects/{projectId}/keys  
  Add third-party API keys to project. Request body: {serviceName, apiKey, metadata}. Returns stored key ID.

- GET /projects/{projectId}/proxy/{serviceName}  
  Proxy endpoint that accepts client requests with unified key, forwards to third-party API using stored key, returns response.

- POST /projects/{projectId}/rotate/{serviceName}  
  Rotate stored third-party API key for serviceName. Accepts new key in body.

Local Persistence:

- File-backed JSON store per project, e.g., ~/.uapigateway/projects/{projectId}.json  
  Stores unified key, third-party keys encrypted with a local symmetric key.

- CLI-first: commands to create project, add keys, rotate keys, and run local proxy server.

Tradeoffs:

- File-backed local store avoids early cloud complexity and paid services, enabling rapid iteration.

- Encryption keys stored locally; security limited to local machine—acceptable for POC but not production.

- Proxy implemented as local HTTP server to demonstrate transparent forwarding; no multi-tenant or scaling concerns yet.

- Supports only 2–3 sandboxed APIs to keep scope minimal and demo-ready within one week.

Actionables:

- Implement CLI commands for project/key management with local encrypted JSON.

- Implement lightweight local proxy server validating unified key and forwarding requests.

- Prepare demo scripts showing onboarding, proxying, and rotation flows.
- Auth Engineer: For the local POC, adopt a **CLI-first, local-only, file-backed auth posture**:

- Generate a single project-level API key locally.
- Store third-party API keys encrypted in local config files (e.g., JSON with AES encryption).
- Proxy requests through a local lightweight server that maps the unified key to underlying keys.
- No external dependencies or paid services.
- Rotate keys by updating local config and restarting proxy.
- CLI commands to add/remove third-party keys and export artifacts for handoff.

**Tradeoffs:**
- + Fast iteration, zero cloud cost, no external risk.
- + Easy to demo and share artifacts with other teams.
- - No multi-user concurrency or centralized audit.
- - Limited security posture; local files vulnerable if host compromised.

For production handoff, evolve to a **centralized API gateway with secure vault integration**:

- Store keys in a hardened secrets manager (e.g., AWS Secrets Manager).
- Authenticate clients via OAuth2 or JWT scoped to projects.
- Proxy requests through a scalable gateway enforcing rate limits and audit logs.
- Support multi-user access, rotation workflows, and compliance.

**Tradeoffs:**
- + Enterprise-grade security and compliance.
- + Scalable multi-tenant support.
- - Higher complexity, cost, and longer build time.
- - Requires cloud infrastructure and operational overhead.

**Action:** Build POC with local CLI + file-backed keys to validate core UX and proxy logic. Plan production auth architecture around vault-backed centralized gateway for secure, scalable handoff.
- Database Engineer: For the unified API key gateway POC, choose a local-first, file-backed embedded database to maximize speed, simplicity, and developer control:

**Recommendation:** Use SQLite (v3.40+) with WAL mode enabled.

**Why SQLite?**  
- Zero configuration, no server needed — ideal for CLI-first, local-first workflows.  
- ACID compliance ensures safe concurrent access during proxying and key rotation.  
- File-backed storage means artifacts are portable and can be checked into project repos or shared easily.  
- Mature ecosystem with bindings in all major languages for rapid prototyping.  
- WAL mode improves concurrency and durability without complex setup.

**Tradeoffs:**  
- Not designed for multi-user remote access; acceptable since POC is local-first.  
- Limited horizontal scaling; can migrate to a server DB later if needed.  
- No built-in encryption; sensitive keys must be encrypted at the application layer or via OS-level encryption.

**Actionables:**  
- Embed SQLite DB file in project directory, version-controlled if needed.  
- Implement key encryption/decryption in app code.  
- Use simple schema: projects, API keys, proxy logs.  
- Enable WAL mode for better write concurrency.  
- Document migration path to server DB (Postgres) for future scaling.

This approach balances rapid POC delivery, developer usability, and security readiness.
- Infra Engineer: Deploy a minimal viable unified API key gateway using Terraform, AWS, and Vercel:

1. **AWS Setup (Terraform):**
   - Provision an API Gateway with Lambda proxy integration.
   - Lambda functions handle key provisioning, rotation, and proxying.
   - Use AWS Secrets Manager for storing third-party API keys securely.
   - IAM roles scoped tightly for Lambda to access Secrets Manager only.
   - Terraform manages all infra as code for repeatability.

2. **Vercel Deployment:**
   - Host a lightweight frontend dashboard (React) for project key management.
   - Use serverless functions (Vercel Edge Functions) to interact with AWS Lambda APIs.
   - Frontend authenticates users via OAuth or API key.

3. **Tradeoffs:**
   - AWS Lambda + Secrets Manager ensures secure, scalable backend but adds cost and complexity.
   - Vercel frontend accelerates developer experience but introduces cross-cloud latency.
   - Terraform codifies infra but requires AWS expertise.
   - Start with 2–3 sandboxed APIs to prove proxying; avoid overbuilding integrations initially.
   - Avoid paid third-party services to reduce friction and speed POC delivery.

Action: Define Terraform modules for API Gateway, Lambda, Secrets Manager; build Vercel frontend with minimal UI; test proxy flow end-to-end within one week.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions for CI/CD pipelines.
- On PR: run lint, unit tests, and security scans on API key handling code (e.g., secret scanning, dependency checks).
- On merge to main: trigger integration tests with 2–3 sandboxed third-party APIs, validating proxy and rotation logic.
- Use branch protection rules requiring passing checks before merge.

Deployment Notes:
- Start with a CLI-first, local-first, file-backed POC to minimize dependencies and speed iteration.
- Deploy a lightweight proxy server (e.g., Node.js or Go) that maps unified keys to sandbox API keys.
- Use ephemeral environment variables or GitHub Secrets for sandbox API keys during CI.
- No paid services or external deployments initially; deploy on GitHub Codespaces or local dev machines.
- Document setup and rotation workflows clearly for early adopters.

Tradeoffs:
- Avoiding paid services and external deployment accelerates POC but limits scalability and real-world load testing.
- CLI-first limits UX polish but enables rapid iteration and easier feedback.
- Proxying only 2–3 APIs reduces scope but proves core value quickly.

Action:
- Define GitHub Actions workflows with lint, test, and integration stages.
- Implement minimal proxy server and CLI tooling.
- Prepare sandbox API keys and secrets for CI.
- Write deployment and onboarding docs for early users.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first prototype that manages a single unified API key per project.
2. File-backed storage of API key mappings and proxy configurations (e.g., JSON/YAML).
3. Proxy server component that intercepts requests authenticated by the unified key and routes them to 2–3 sandboxed third-party APIs.
4. Secure key rotation mechanism that updates underlying third-party keys without changing the unified key.
5. Minimal dependencies; no paid services or external deployments required.
6. Basic logging and error handling to demonstrate audit capability.
7. Demo workflow: onboarding a new developer by sharing one unified key, enabling immediate API access.

Acceptance Criteria:
- Unified key successfully proxies requests to at least 2 sandboxed APIs.
- Rotation of underlying keys occurs without downtime or unified key change.
- New developer can use the unified key to access all provisioned APIs within minutes.
- CLI commands to add/remove APIs and rotate keys function correctly.
- Proxy logs requests with timestamps and API target info.
- Prototype runs locally without external service dependencies.

Tradeoffs:
- Security/compliance features (e.g., encryption at rest, RBAC) deferred to post-POC.
- Limited API coverage (2–3 sandboxed APIs) to reduce scope and speed delivery.
- No UI initially; CLI-only to focus on core functionality and rapid iteration.
- File-backed storage chosen over vault integration to avoid complexity and speed prototyping.

Next step: Build POC within one week, test with target ICP users, and gather feedback on usability and value.
