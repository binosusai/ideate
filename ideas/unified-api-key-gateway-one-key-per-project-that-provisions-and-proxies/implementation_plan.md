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

1. Scope & Tech Stack:
- CLI-first, local-first tool (Node.js or Python)
- File-backed config (YAML/JSON) storing unified project key and mapping to 2-3 third-party API keys (e.g., Stripe, SendGrid, Twilio)
- Proxy server (local or lightweight container) to forward requests authenticated by unified key to actual APIs

2. Core Features:
- CLI commands: init project, add/remove third-party API keys, generate unified key
- Local proxy intercepts calls with unified key, routes to correct API with stored credentials
- Simple access control: unified key validity & usage logs (file-based)

3. Implementation Steps:
- Build CLI to create project config and store encrypted API keys locally
- Implement proxy server that validates unified key and forwards requests with correct API keys
- Demo with 2-3 popular APIs, showing single key usage and seamless API access

4. Tradeoffs:
- No cloud or multi-user sync initially (reduces complexity, speeds MVP)
- Local file storage limits team collaboration; future versions can add cloud sync & RBAC
- Limited API integrations to prove concept quickly

5. Validation:
- Target developer-heavy SaaS teams for demo and feedback
- Measure onboarding time reduction and ease of key management

This MVP keeps scope minimal, avoids paid services, and delivers a tangible “one key, many APIs” demo within one week.
- POC Coder: Smallest working POC plan for Unified API Key Gateway:

1. Scope: CLI tool, local-only, file-backed (YAML/JSON config), no external services.
2. Features:
   - Create a “project” with one unified API key (random UUID).
   - Store 2–3 third-party API keys (e.g., GitHub, OpenWeatherMap) mapped internally.
   - Proxy requests: user calls CLI with unified key + target API name + endpoint.
   - CLI injects corresponding third-party API key and forwards request, returning response.
3. Implementation:
   - Use Node.js or Python for quick CLI and HTTP proxy.
   - Store keys in local encrypted file (simple symmetric encryption).
   - Minimal error handling and logging.
4. Tradeoffs:
   - No multi-user/team support (local single user only).
   - No UI, no real-time rotation or audit logs.
   - Limited to a few APIs hardcoded for demo.
   - No external deployment or paid services.
5. Outcome:
   - Demonstrate one key per project accessing multiple APIs.
   - Show friction reduction and centralized key usage.
   - Ready for user feedback and iterative expansion.

This POC fits one focused session, proves core value, and avoids overbuilding or fragile dependencies.
- Frontend Engineer: POC Interface: CLI-first with minimal local UI

1. CLI commands:
- `apikey init [project-name]` — creates project config & local key store (file-backed JSON)
- `apikey add-tool [tool-name] --api-key [key]` — adds a 3rd-party API key to project
- `apikey list-tools` — lists integrated tools with masked keys
- `apikey get-proxy-key` — returns the unified API key for project use (proxy token)
- `apikey proxy [tool-name] [endpoint]` — sends proxied request to 3rd-party API via unified key

2. Local config file stores:
- Project metadata (name, tools)
- Encrypted API keys (e.g., AES with local passphrase)
- Proxy key (random token mapped internally to underlying keys)

3. Tradeoffs:
- CLI-first: fastest MVP, low UI overhead, familiar to devs
- File-backed: no external dependencies, easy offline use, but limited multi-user sync (future cloud sync possible)
- Proxy key: simple token model, but requires local proxy or lightweight server for request forwarding (POC can mock proxy)
- Security: local encryption only, no centralized vault yet (acceptable for POC)

Action: Implement CLI commands with file-backed encrypted config and a minimal local proxy to demonstrate unified key usage for 2–3 popular APIs. Validate onboarding flow and proxying in under one week.
- Backend Engineer: POC API Design:
- POST /projects/{projectId}/unified-key
  * Creates/returns a single unified API key for the project.
  * Idempotent: returns existing key if present.
- GET /projects/{projectId}/services
  * Lists third-party services integrated under the project.
- POST /projects/{projectId}/services/{serviceId}/keys
  * Stores encrypted third-party API key for the service.
- GET /projects/{projectId}/proxy/{serviceId}/endpoint
  * Proxies requests to the third-party API using stored keys.

Local Persistence:
- File-backed JSON store per project (e.g., ~/.unified-api-keys/{projectId}.json).
- Stores unified key, service keys encrypted with a local master password.
- CLI-first usage: local file sync enables offline key management and quick lookup.

Tradeoffs:
- Pros: Simple, no external dependencies; fast iteration; secure local encryption; easy demo.
- Cons: No multi-user sync or cloud backup; limited audit logs; proxy limited to POC scale.
- Avoids paid services and fragile integrations, enabling quick POC delivery within 1 week.

Action:
- Implement CLI tool with above API endpoints and local JSON persistence.
- Integrate 2-3 popular APIs (e.g., Stripe, SendGrid) for demo.
- Focus on key provisioning, proxying, and local encrypted storage.
- Prepare demo to validate developer onboarding speed and centralized key management benefits.
- Auth Engineer: For local POC:  
**Auth posture:** CLI-first, local-only, file-backed unified API key gateway with a single project key that proxies 2–3 third-party APIs.  
- Implement a lightweight local proxy server that authenticates requests via the unified key, then injects the correct third-party API keys from a local encrypted file (e.g., AES-encrypted JSON).  
- No external dependencies or paid services; no user accounts or cloud storage.  
- CLI commands to generate, rotate, and revoke the unified key locally.  
- Logs and audit trails stored locally for demo purposes.  

**Tradeoffs:**  
+ Fast iteration, minimal infra, no cloud lock-in.  
- Limited multi-user/team support; no real-time revocation or centralized audit.  
- Security depends on local machine protection and encrypted file secrecy.  

For production handoff:  
**Auth posture:** Cloud-hosted gateway with centralized credential vault, RBAC, and audit logging.  
- Use a hardened secrets manager (e.g., HashiCorp Vault or AWS Secrets Manager) for storing third-party keys.  
- Authenticate clients with OAuth2 or JWT tokens scoped per project/team.  
- Proxy requests with fine-grained access control, key rotation, and real-time revocation.  
- Provide an admin UI and API for onboarding tools and users.  

**Tradeoffs:**  
+ Enterprise-grade security, compliance, multi-user collaboration, and auditability.  
- Higher complexity, cost, and operational overhead.  

**Action:** Build local POC first to validate concept and developer UX; then design production auth around centralized vault and token-based access control for secure, scalable deployment.
- Database Engineer: For the Unified API Key Gateway POC, choose a local, deployable database that is zero-config, lightweight, and file-backed to align with CLI-first, local-first goals:

**Recommendation:** SQLite  
- **Why:**  
  - Serverless, no setup or daemon needed  
  - Single-file DB, easy to version/control with project files  
  - ACID-compliant, reliable for credential metadata and audit logs  
  - Widely supported by most languages and frameworks  
- **Tradeoffs:**  
  - Limited concurrent writes (acceptable for single-user CLI POC)  
  - No built-in encryption (encrypt sensitive fields at app layer)  
  - Not suited for multi-node scaling (out of scope for MVP)  

**Implementation:**  
- Store API key mappings, provisioning status, and audit trails in SQLite tables  
- Encrypt sensitive data fields before insertion (e.g., using libsodium or AES)  
- Bundle DB file with project config artifacts for portability  
- Use simple SQL queries for CRUD operations, enabling easy future migration  

This approach minimizes dependencies, accelerates MVP delivery, and supports local-first workflows while keeping the door open for future cloud or multi-user expansions.
- Infra Engineer: Deploy a minimal viable Unified API Key Gateway POC on AWS using Terraform and Vercel for frontend/API proxy:

1. **AWS Infra (Terraform):**  
- Use AWS Lambda (Node.js) for API proxy and key provisioning logic.  
- Store third-party API keys securely in AWS Secrets Manager, scoped per project.  
- Use API Gateway to expose a unified API endpoint, validating the single project key.  
- IAM roles restrict Lambda access to only needed secrets.  
- CloudWatch for logs and metrics.

2. **Vercel Frontend/API:**  
- Deploy a lightweight React app on Vercel for project key management UI and onboarding flows.  
- Use Vercel Serverless Functions as a thin proxy to AWS API Gateway or directly call AWS endpoints securely.

3. **Terraform Automation:**  
- Define all AWS resources and IAM policies in Terraform for repeatable, auditable infra.  
- Use Terraform Cloud or GitHub Actions for CI/CD.

**Tradeoffs:**  
- AWS Lambda + Secrets Manager adds operational security but increases complexity vs local file-backed POC.  
- Vercel accelerates frontend deployment but adds a second cloud dependency.  
- API Gateway adds latency but provides scalable, secure unified endpoint.  
- Early POC scope limits integrations to 2–3 APIs to prove concept fast.

**Action:**  
Start with Terraform AWS Lambda + Secrets Manager + API Gateway stack; deploy Vercel frontend for key management UI; integrate 2–3 popular APIs; validate unified key flow; iterate based on developer feedback.
- DevOps Engineer: GitHub Automation & Checks for Unified API Key Gateway POC:

1. **CI Workflow:**
- Trigger: PRs and pushes to main/feature branches.
- Steps:
  - Lint and unit test CLI-first codebase (Node.js/Python).
  - Run integration tests with mocked 2-3 third-party APIs.
  - Security scan (e.g., GitHub CodeQL) to catch secrets or vulnerabilities.
  - Build artifact: CLI binary or script + config files.

2. **Checks:**
- Enforce branch protection requiring passing CI.
- Require PR reviews (2+ reviewers) to ensure design scrutiny.
- Use Dependabot for dependency updates.

3. **Deployment Notes:**
- POC is local-first, file-backed, no external deployment needed.
- Release artifacts via GitHub Releases for easy download.
- Document CLI usage and config file format in README.
- Include instructions for manual testing with dummy API keys.

**Tradeoffs:**
- No cloud deployment reduces complexity and cost but limits real-world proxy testing.
- Mocked APIs simplify integration tests but may miss edge cases.
- Manual deployment/testing keeps scope small but delays automation feedback.

This setup enables rapid iteration, early feedback, and risk-controlled POC delivery.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that generates a unified API key per project.
2. File-backed storage of key mappings and credentials (e.g., JSON/YAML).
3. Proxy layer that intercepts requests using the unified key and routes them to corresponding third-party APIs with their real keys.
4. Support for 2–3 popular APIs (e.g., Stripe, Twilio, Google Maps) for POC.
5. Minimal dependencies; no paid services or external deployment required.
6. Basic access control and audit logging of key usage.
7. Easy onboarding: single CLI command to add new third-party API keys and generate unified key.
8. Export artifacts readable by other agent crews (e.g., config files).

Acceptance Checks:
- Unified key can successfully proxy requests to all integrated APIs.
- CLI commands to add/remove APIs and keys work without errors.
- Local file storage correctly persists and loads credentials.
- Audit logs record each proxied request with timestamp and target API.
- Demo runs end-to-end within one focused session (~1 day).
- No reliance on external paid services or fragile integrations.

Tradeoffs:
- Local-first limits scalability but accelerates POC speed and security.
- Proxy approach adds latency but centralizes credential management.
- Supporting only 2–3 APIs initially reduces scope but proves concept quickly.

Action:
Start with CLI tool + local proxy + file storage; integrate Stripe, Twilio, Google Maps APIs; demo unified key usage and audit logs; gather feedback for next iteration.
