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

1. **Scope & Core Features (1 week):**  
- CLI tool that creates a single “project key” locally (file-backed JSON config).  
- Support proxying 2-3 popular third-party APIs (e.g., Stripe, Slack, GitHub) via this key.  
- Local proxy server that intercepts calls, injects real API keys securely stored in config, and forwards requests.  
- Basic audit log (local file) tracking API calls per third-party tool.  
- Simple CLI commands: `init`, `add-tool`, `start-proxy`, `rotate-key`, `status`.

2. **Implementation Details:**  
- No external deployment or paid services; run locally or on developer’s machine.  
- Use encrypted local storage (e.g., OS keychain or encrypted file) for real keys.  
- Proxy uses lightweight Node.js/Go server with minimal dependencies.  
- CLI written in Node.js or Python for cross-platform ease.

3. **Tradeoffs:**  
- No multi-user/team sync yet (focus on individual dev onboarding).  
- Limited API coverage to prove concept fast.  
- Local-only limits centralized audit/compliance but reduces trust barriers.

4. **Next Steps Post-MVP:**  
- Add Slack onboarding bot integration.  
- Explore cloud-hosted proxy with team management.  
- Integrate audit logs with compliance dashboards.

This MVP balances speed, security, and demonstrable value to validate demand and unblock further investment.
- POC Coder: POC Plan: CLI-first local unified API key gateway (file-backed)

1. Scope:  
- CLI tool managing a single project config file (YAML/JSON) storing unified API key and mappings to 2–3 third-party API keys (mocked or real sandbox keys).  
- Proxy server locally forwarding requests from unified key to correct third-party API with key injection.  
- Basic commands: `init` (create project config), `add-tool` (register third-party API key), `proxy` (start local proxy).  
- No auth or persistence beyond local files.

2. Implementation:  
- Use Node.js or Python for CLI + proxy server (Express/Flask).  
- Config file stores unified key + tool keys + proxy routes.  
- Proxy inspects incoming requests, replaces unified key with tool-specific key, forwards request, returns response.  
- CLI generates unified key (UUID) and writes config.

3. Tradeoffs:  
- No multi-user or remote storage (simplifies security, no infra).  
- No UI, no audit logs (minimal viable demo).  
- Limited to local dev environment, no scaling or billing.  
- Real third-party API calls optional; can mock responses.

4. Success criteria:  
- Developer runs CLI, sets up unified key + tools in <30 min.  
- Proxy transparently forwards requests using unified key.  
- Demonstrates onboarding friction reduction and centralized key usage.

Deliverables: CLI tool repo + README with usage steps + example config + local proxy server code.  
This POC proves core concept fast, low risk, no paid services.
- Frontend Engineer: POC Interface Plan: CLI-First with Minimal Web Dashboard

1. CLI Tool (Primary Interface)
- Commands:  
  • `init <project>`: create local config file with unified key placeholder  
  • `add-tool <tool-name> --api-key <key>`: register third-party keys locally  
  • `list`: show registered tools and masked keys  
  • `start-proxy`: launch local proxy server exposing unified key endpoint  
  • `rotate <tool-name>`: simulate key rotation  
- Tradeoffs:  
  • Pros: Fast MVP, meets developer preference, local-first avoids early security concerns  
  • Cons: Limited visibility for non-dev roles, onboarding friction if CLI UX unclear

2. Minimal Web Dashboard (Secondary, optional)
- Purpose: Visualize project keys, usage logs, and rotation history  
- Tech: React + simple backend (Node.js or static JSON served)  
- Tradeoffs:  
  • Pros: Improves audit/compliance visibility, aids trust building  
  • Cons: Adds complexity, defers core value to CLI, can be MVP phase 2

Actionable Next Steps:
- Build CLI prototype with config file and proxy server supporting one unified key per project  
- Hardcode 2-3 example third-party tools for demo  
- Prepare README onboarding with clear CLI usage  
- Optional: sketch dashboard wireframe for future iteration

This keeps scope minimal, developer-centric, and focused on proving unified key proxy concept rapidly.
- Backend Engineer: **API Design:**

- **POST /projects**  
  Create a new project and generate a unified API key (UUID). Returns project ID and unified key.

- **GET /projects/{projectId}/keys**  
  List all third-party API keys provisioned under the project (masked).

- **POST /projects/{projectId}/keys**  
  Add a third-party API key to the project, storing encrypted locally. Request includes tool name, key, and metadata.

- **DELETE /projects/{projectId}/keys/{keyId}**  
  Remove a third-party API key.

- **POST /proxy/{projectId}/{toolName}/**  
  Proxy API requests to third-party tools using stored keys. Authenticated by unified key.

- **GET /audit/{projectId}/logs**  
  Retrieve usage and rotation logs for compliance.

---

**Local Persistence:**

- Use encrypted JSON file per project (e.g., `.uapigateway/keys.json.enc`) storing:  
  - Project ID, unified key  
  - List of third-party keys (encrypted with a local master key derived from user passphrase)  
  - Metadata and audit logs

- CLI-first, file-backed for offline use and easy artifact sharing.

---

**Tradeoffs:**

- **Security vs Simplicity:** Local encryption avoids cloud risk but requires secure passphrase management.  
- **No external dependencies:** Enables quick POC without paid services but limits real-time multi-user sync.  
- **Proxying:** Adds latency and complexity but essential for unified key abstraction and auditability.

---

**Action:** Implement CLI tool with above API stub and local encrypted JSON storage to validate unified key creation, key addition/removal, and proxying in a single dev sprint.
- Auth Engineer: **Auth posture recommendation for POC and production handoff:**

**POC (Local, CLI-first, file-backed):**  
- Use a local encrypted file store (e.g., AES-256 encrypted JSON/YAML) for API keys per project.  
- Authenticate users via local OS user context or a simple CLI login with a short-lived token.  
- Proxy requests with a minimal local HTTP server that injects third-party API keys from the encrypted store.  
- No external dependencies or paid services.  
- Tradeoffs: Minimal security (local only), no multi-user support, no audit logs, but fastest to build and demo core concept.

**Production (Cloud-hosted, multi-tenant):**  
- Use a managed secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault) for secure, centralized key storage.  
- Authenticate users via OAuth2/OIDC (e.g., GitHub or Google SSO) for team-based access control.  
- Proxy API requests through a hardened gateway with per-project API keys, request logging, and rate limiting.  
- Implement audit trails and key rotation workflows.  
- Tradeoffs: Higher complexity and cost, requires robust security and compliance design, but essential for trust, scalability, and commercial viability.

**Action:** Build POC with local encrypted file + CLI auth to validate workflow. Plan production architecture with cloud secrets + OAuth2 + audit for handoff.
- Database Engineer: For the unified API key gateway POC, choose a local-first, deployable database that is zero-config, embeddable, and file-backed to align with CLI-first and offline-friendly goals:

**Recommended default:** SQLite  
- **Why:**  
  • Serverless, zero setup, stores data in a single file per project  
  • ACID-compliant, reliable for credential storage and audit logs  
  • Widely supported, easy to integrate with CLI tools and agents  
  • Portable and easy to backup/migrate  
- **Tradeoffs:**  
  • Limited concurrent writes (acceptable for single-user CLI use)  
  • No built-in encryption—encrypt sensitive fields at the app layer or use OS-level encryption  
  • Not ideal for multi-user concurrent access or heavy scaling (out of scope for MVP)  

**Implementation notes:**  
- Store API key metadata, provisioning state, and audit trails in SQLite tables.  
- Encrypt sensitive data fields before insertion (e.g., using libsodium or OS keychain).  
- Bundle SQLite with the CLI tool for zero external dependencies.  
- Use simple migrations for schema evolution.  

This approach enables a minimal, secure, and deployable proof of concept without external services or fragile integrations.
- Infra Engineer: **Deployment Shape for Unified API Key Gateway POC**

1. **Architecture:**
   - **AWS Lambda + API Gateway:** Serverless proxy layer for API key provisioning and proxying; scales on demand, no infra ops.
   - **AWS DynamoDB:** Store encrypted API key metadata and usage logs; serverless, low latency.
   - **Terraform:** Manage AWS infra as code for repeatability and version control.
   - **Vercel:** Host frontend (dashboard/CLI onboarding UI) for low-latency global access, seamless CI/CD.
   
2. **Key Implementation Details:**
   - Lambda functions handle key provisioning, rotation, and proxy requests.
   - API Gateway enforces authentication via the unified project key.
   - DynamoDB encrypted with AWS KMS for compliance.
   - Terraform modules for Lambda, API Gateway, DynamoDB, KMS.
   - Vercel frontend calls API Gateway endpoints securely.
   
3. **Tradeoffs:**
   - **Pros:** Serverless reduces ops burden, scales automatically, fast iteration; Terraform ensures infra consistency; Vercel accelerates frontend delivery.
   - **Cons:** Cold starts on Lambda may add latency; DynamoDB pricing can grow with usage; initial complexity in securing proxy and key encryption.
   - **Mitigation:** Use provisioned concurrency for Lambda; monitor costs; implement strict IAM roles and audit logging.
   
4. **Actionables:**
   - Define Terraform modules for AWS resources.
   - Build minimal Lambda proxy with key validation and rotation.
   - Setup DynamoDB schema for keys and logs.
   - Deploy Vercel frontend with CLI onboarding flow.
   - Integrate AWS KMS for encryption.
   - Implement monitoring and alerting for security events.

This shape enables a secure, scalable POC within one week, focusing on MVP speed and compliance readiness.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions for CI/CD pipelines triggered on PRs and merges to main.
- Checks: Linting (ESLint/Prettier), unit tests, and security scans (e.g., Snyk or GitHub CodeQL) to catch vulnerabilities early.
- Automate API key mock tests to validate proxy logic without real keys.
- Enforce branch protection rules requiring passing checks before merges.

Deployment Notes:
- Start with CLI-first, local-first deployment using file-backed config to minimize external dependencies.
- Deploy a lightweight proxy server (e.g., Node.js or Go) that reads local config and proxies API calls.
- Use GitHub Actions to build and publish CLI binaries and Docker images for proxy server.
- Avoid paid services or fragile integrations in POC to enable rapid iteration.
- Document environment variables and secrets management via GitHub Secrets for CI.

Tradeoffs:
- CLI-first limits initial UX but accelerates MVP delivery and developer adoption.
- File-backed config trades centralized storage for simplicity and offline use.
- Proxying keys centrally raises security concerns; mitigate by strict audit logs and minimal key exposure.
- Avoiding paid services slows scaling but enables quick proof of concept.

Action:
- Define GitHub Actions workflows for lint/test/security.
- Implement CLI tool and proxy server with file-backed config.
- Set branch protection and secrets in GitHub repo.
- Prepare deployment docs emphasizing security and onboarding simplicity.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that manages a single unified API key per project.
2. File-backed storage of API key mappings, readable by other agents.
3. Proxy layer that routes third-party API calls via the unified key, enabling seamless onboarding/offboarding.
4. Support for key provisioning and rotation with audit logging.
5. Free tier support for up to 3 third-party APIs per project.
6. Slack onboarding bot integration for streamlined user onboarding.
7. Security: encrypt stored keys locally; no external paid services or fragile integrations in MVP.
8. Minimal setup friction with clear CLI UX and onboarding docs.

Acceptance Criteria:
- CLI tool can create, list, and rotate unified API keys per project.
- Proxy forwards API calls to third-party tools using provisioned keys.
- Audit logs show key usage and rotation events.
- Slack bot successfully provisions keys and links to CLI tool.
- MVP runs fully locally without external dependencies.
- Demonstrated onboarding of a 5–30 person SaaS startup project with 3 APIs.
- Security review confirms no plaintext key leaks or unauthorized access.

Tradeoffs:
- MVP excludes cloud-hosted key vaults to speed delivery but limits multi-user sync.
- CLI-first approach may deter non-CLI users but targets developer-heavy ICP.
- Proxy adds latency but enables centralized control and audit.

Next step: Build POC CLI tool + proxy + Slack bot with local file storage and demo onboarding flow.
