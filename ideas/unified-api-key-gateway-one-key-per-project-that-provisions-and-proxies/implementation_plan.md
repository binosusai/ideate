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

1. CLI-first local tool (Node.js or Python) that:
   - Initializes a project config file storing unified API key metadata.
   - Provisions a single unified key per project (UUID-based).
   - Stores 2–3 sandbox third-party API keys (e.g., Stripe, SendGrid) encrypted in a local file.
   - Runs a local proxy server that intercepts calls authenticated by the unified key and forwards them to the correct third-party API with stored credentials.

2. Proxy features:
   - Route requests by path prefix or header to corresponding third-party API.
   - Log all proxied requests and responses for auditing.
   - Support simple token validation for unified key.

3. Demo scope:
   - Support only 2–3 sandbox APIs with stable public test endpoints.
   - No external paid services or cloud deployment.
   - Local file storage only, no DB.

Tradeoffs:
- Local-first limits multi-user/team collaboration but accelerates POC speed.
- Proxying only sandbox APIs avoids legal/production risk but limits real-world complexity.
- CLI + local proxy enables quick iteration but defers UX polish and scalability.

Next steps:
- Build CLI tool + proxy in 3 days.
- Demo to target users for feedback on onboarding time and perceived value.
- Measure willingness-to-pay signals before expanding scope.
- POC Coder: POC Plan: Unified API Key Gateway (Local CLI + Proxy)

**Goal:** Prove unified key concept by proxying 2 sandbox APIs with one project key, local CLI, file-backed config, no paid services.

**Scope:**
- CLI tool to create a project key (UUID) stored in a local JSON file.
- Proxy server (Node.js/Express) that:
  - Accepts requests with the unified key.
  - Maps unified key + target API identifier to stored real API keys.
  - Forwards requests to two sandbox APIs (e.g., Stripe test, SendGrid sandbox).
  - Logs access (timestamp, endpoint).
- Simple config file format:
  ```json
  {
    "projectKey": "uuid",
    "apiKeys": {
      "stripe": "sk_test_...",
      "sendgrid": "SG.test..."
    }
  }
  ```
- CLI commands:
  - `init` to create project key + config file.
  - `add-api` to add third-party keys.
  - `start-proxy` to run local proxy server.

**Tradeoffs:**
- No auth beyond project key (simplifies POC, but limited security).
- Local only, no multi-user or persistence beyond file.
- Proxy limited to two APIs for demo speed.
- No UI, CLI-only for rapid iteration.

**Next Steps:**
- Day 1: Build CLI + config file + proxy skeleton.
- Day 2: Integrate proxy forwarding for Stripe + SendGrid sandbox APIs.
- Day 3: Test end-to-end; demo onboarding with unified key usage.
- Gather feedback from 3 target users on onboarding friction reduction.

This minimal POC proves core value without cloud infra or complex auth, enabling fast commercial validation.
- Frontend Engineer: POC Interface Plan:

1. Project Dashboard (web/CLI):
- List projects with unified API key status
- Create new project: input name, auto-generate unified key
- Show linked third-party tools (start with Stripe, SendGrid)

2. Add Third-Party API Key:
- Form to input API key for a selected tool
- Validate key format client-side (basic)
- Store encrypted locally (file-backed for POC)

3. Proxy Usage Demo:
- Simple UI to send test requests through unified key
- Show request logs with timestamps and proxied API responses

4. Access Logs:
- Display recent proxy calls per project, tool, and key usage
- Highlight errors and latency

Tradeoffs:
- Web UI for demo clarity vs CLI-first simplicity: Start with minimal React frontend to demo value; CLI can follow.
- Local file-backed storage avoids backend complexity but limits multi-user sync.
- Proxy limited to 2 sandbox APIs reduces scope but proves core concept.

Action:
Build minimal React app + Node proxy server with file-based storage. Focus on onboarding flow: create project → add keys → test proxy → view logs. Deliver in 5 days.
- Backend Engineer: POC API Design:
- POST /projects: create project, returns unified API key
- POST /projects/{id}/keys: add third-party API keys (e.g., Stripe, SendGrid)
- GET /projects/{id}/proxy/{service}/{endpoint}: proxy requests using stored keys
- GET /projects/{id}/logs: fetch access logs for auditing

Local Persistence:
- File-backed JSON/YAML storing:
  - Project metadata (ID, unified key)
  - Third-party keys encrypted at rest (use libsodium or OS keyring)
  - Access logs (timestamp, endpoint, response status)

Tradeoffs:
- CLI-first, local file persistence avoids early cloud complexity and paid services, enabling rapid iteration.
- Proxying only 2–3 sandbox APIs limits scope but proves core concept.
- Encryption complexity vs. POC speed: use simple symmetric encryption with a user passphrase.
- No multi-user sync initially; focus on single-user local dev environment.

Actionables:
1. Implement CLI commands for project/key management and proxying.
2. Use local encrypted file store for keys and logs.
3. Proxy requests by injecting stored keys, forwarding client calls.
4. Log each proxied request for audit.
5. Demo with Stripe and SendGrid sandbox APIs within 1 week.
- Auth Engineer: For the local POC, adopt a **CLI-first, file-backed auth posture**:

- Generate a single unified API key per project locally.
- Store third-party API credentials encrypted in a local config file (e.g., JSON/YAML with AES encryption).
- Proxy requests via a lightweight local server that maps the unified key to underlying third-party keys.
- Log all credential usage locally for audit.
- No external dependencies or paid services to keep the POC self-contained and fast to iterate.

**Tradeoffs:**  
+ Fast, low-cost iteration with full control and no cloud lock-in.  
+ Easy to demo and hand off to other teams for integration.  
- No multi-user or team sync; limited scalability.  
- Local storage risks if machine compromised (acceptable for POC).

For production handoff, evolve to a **centralized, cloud-hosted gateway with RBAC and secure vault integration**:

- Store credentials in a hardened secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager).  
- Issue unified API keys via a managed API gateway that proxies and audits all calls.  
- Support team roles, key rotation, and usage quotas.  
- Integrate with SSO for user authentication.

**Tradeoffs:**  
+ Enterprise-grade security, auditability, and multi-user support.  
- Higher complexity, cost, and deployment overhead.  
- Requires cloud infrastructure and operational maturity.

**Action:** Start with CLI-local POC to validate core concept; plan phased migration to cloud gateway for production.
- Database Engineer: For the Unified API Key Gateway POC, choose a local, deployable database that is lightweight, zero-config, and file-backed to align with CLI-first, local-first goals:

**Recommended default: SQLite**  
- **Why:**  
  - Serverless, embedded in the app, no external dependencies  
  - ACID-compliant, reliable for credential storage and access logs  
  - Cross-platform, easy to bundle with CLI tools  
  - Supports simple schema migrations for evolving POC needs  
- **Tradeoffs:**  
  - Not designed for high concurrency or distributed use (acceptable for POC)  
  - Limited built-in encryption; rely on OS-level file encryption or encrypt sensitive fields in app  
- **Implementation notes:**  
  - Store DB file in user’s project directory or config folder  
  - Use parameterized queries to prevent injection  
  - Log all proxy accesses with timestamps for audit trail  
  - Keep schema minimal: projects, unified keys, third-party keys, access logs  

Avoid heavier DBs (Postgres, MySQL) or cloud services to keep POC self-contained, fast to iterate, and deployable without paid dependencies. This choice enables rapid validation of core value with minimal ops overhead.
- Infra Engineer: Deploy a minimal Unified API Key Gateway POC on AWS + Vercel + Terraform:

1. **AWS Infra**  
- Use AWS API Gateway + Lambda proxy to handle unified key validation and route requests to 2–3 sandbox third-party APIs (e.g., Stripe, SendGrid).  
- Store third-party API keys securely in AWS Secrets Manager, referenced by Lambda.  
- Enable CloudWatch logging for audit trails.  

2. **Vercel Frontend**  
- Deploy a lightweight React app on Vercel for project key issuance and dashboard (showing usage, onboarding status).  
- Use serverless API routes on Vercel to call AWS Lambda endpoints securely.  

3. **Terraform**  
- Manage AWS infra (API Gateway, Lambda, Secrets Manager) and Vercel project config with Terraform for repeatable, versioned deployments.  
- Use Terraform Cloud or local runs to keep costs zero and avoid fragile external dependencies.  

**Tradeoffs:**  
- AWS Lambda + API Gateway adds cold start latency but offers low-cost, scalable proxying.  
- Vercel frontend separates UI from backend but requires cross-origin config.  
- Terraform ensures infra reproducibility but adds initial complexity; keep modules minimal.  

**Action:**  
- Define Terraform modules for AWS infra and Vercel.  
- Implement Lambda proxy with unified key auth and secrets fetch.  
- Build minimal React UI for key issuance and usage logs.  
- Demo to target users within 1 week to validate MVP and pricing signals.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions to automate CI/CD.
- Workflow triggers: on PR open/update and main branch push.
- Steps:
  1. Lint and test POC code (Node.js or Python).
  2. Run security scans on credential handling code (e.g., GitHub CodeQL).
  3. Validate API proxy responses against mock third-party APIs.
- Enforce branch protection requiring passing checks before merge.

Deployment Notes:
- Deploy POC as a containerized CLI-first app with local file-backed config.
- Use GitHub Packages or Docker Hub for container registry.
- Deployment target: lightweight VM or developer laptop for demo.
- No paid external services or cloud dependencies to keep POC simple and reproducible.
- Logs must capture API key usage for audit and demo purposes.

Tradeoffs:
- CLI-first and local file-backed limits scalability but accelerates MVP delivery and iteration.
- Proxying only 2–3 sandbox APIs reduces complexity but validates core concept.
- Avoiding paid services reduces cost and risk but may limit real-world integration fidelity.

Action:
- Define GitHub Actions workflow YAML with lint, test, security scan, and deploy steps.
- Prepare mock APIs for Stripe and SendGrid.
- Document deployment and demo instructions for internal crew and early testers.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that generates a single unified API key per project.
2. Proxy layer that routes requests from unified key to 2–3 sandbox third-party APIs (e.g., Stripe, SendGrid).
3. File-backed storage of project config and credentials, readable by other agents.
4. Basic logging of credential access for audit and usage insights.
5. No reliance on paid services or external deployments; all components runnable locally.
6. Minimal UI: CLI commands for key generation, proxy start/stop, and logs retrieval.
7. Security: encrypt stored credentials at rest; validate unified key usage per project.

Acceptance Checks:
- Generate unified key for a sample project via CLI.
- Proxy requests authenticated by unified key correctly to each third-party API sandbox.
- Logs capture each credential access event with timestamp and target API.
- Config and credentials stored in local files, accessible by other tools.
- Run full demo end-to-end within one day without external dependencies.
- Validate proxy rejects unauthorized or malformed requests.

Tradeoffs:
- Limited to sandbox/test APIs initially to avoid costly real API calls.
- Local-first limits immediate multi-user collaboration but accelerates POC speed.
- Minimal UI reduces polish but focuses on core value demonstration.
- Encryption scope limited to local files; no centralized secrets vault yet.

This scope enables a rapid, actionable POC to validate commercial and technical feasibility within one week.
