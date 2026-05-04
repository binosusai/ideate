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

1. Scope & Tech Stack:
- CLI-first, local-only tool (Node.js or Python) with file-backed config (YAML/JSON).
- No external services or paid dependencies.
- Plugin architecture for 2–3 popular APIs (Stripe, SendGrid, Twilio).

2. Core Features:
- Single project key generation (local secret).
- Mapping file: project key → multiple vendor API keys.
- Proxy server that listens locally, intercepts requests with project key, and rewrites them with correct vendor API keys.
- CLI commands: init project, add vendor API keys, start proxy, show status.

3. Security & UX:
- Store vendor keys encrypted on disk with a local master password.
- Minimal onboarding: CLI wizard to add keys and start proxy.
- Transparent logs for requests and key usage.

4. Demo Goals (1 week):
- Show onboarding flow adding 2 vendor keys.
- Proxy a simple API call through unified key.
- Validate no external calls except proxied vendor APIs.
- Open-source repo for community feedback.

Tradeoffs:
- No multi-user/team sync initially (local-only).
- Limited API coverage to reduce scope.
- No UI, CLI-only to speed delivery and reduce complexity.

Next: Define API adapter interfaces and start CLI scaffolding.
- POC Coder: POC Plan: Local CLI + File-Backed Unified API Key Proxy

**Goal:** Prove one project key proxies 2–3 third-party APIs (e.g., Stripe, SendGrid) locally, no external services.

**Components:**
1. CLI tool to:
   - Generate a single project API key (UUID).
   - Store mapping of project key → vendor keys in a local JSON file (encrypted optional).
   - Start a local HTTP proxy server.

2. Proxy server:
   - Accept requests with project key in header.
   - Route requests to correct vendor API using stored keys.
   - Forward response back transparently.

3. Demo:
   - Show onboarding flow: user runs CLI, inputs vendor keys once, gets project key.
   - Use curl/postman with project key to call Stripe/sendgrid endpoints via proxy.

**Tradeoffs:**
- No real provisioning or vendor API key rotation (manual input).
- Local-only, no multi-user or cloud sync (minimizes trust/risk).
- Supports only 2–3 APIs hardcoded (fast dev, proves concept).
- No UI, CLI-only to speed iteration.

**Outcome:**
- Demonstrates unified key usage and proxying.
- Validates developer workflow and integration feasibility.
- Basis for future cloud/managed version.

**Next Steps:**
- Build CLI + proxy in Node.js or Python (fast HTTP libs).
- Hardcode minimal vendor API logic.
- Prepare README with usage and security notes.
- Frontend Engineer: POC Interface: CLI-first + minimal local UI

1. CLI commands:
- `init` — create a local project config (file-backed), generate unified project key
- `add-api <provider>` — add a 3rd-party API key (Stripe, SendGrid, Twilio) to config
- `list-keys` — show mapped APIs and masked keys
- `proxy <api> <endpoint> [--data]` — invoke proxied API via unified key

2. Local config file (JSON/YAML):
```yaml
project_key: <uuid>
apis:
  stripe: <encrypted_key>
  sendgrid: <encrypted_key>
```

3. Minimal web UI (optional):
- Dashboard: shows project key, connected APIs, status
- Add API key form: input provider + secret key
- Proxy test panel: send requests via unified key

Tradeoffs:
- CLI-first & local-only reduces complexity, no backend needed, accelerates iteration
- File-backed config enables easy sharing and audit, but no multi-user sync yet
- Proxy implemented as local CLI agent or lightweight server for POC; no cloud deployment
- Supports only 2–3 top APIs to prove concept, extensible later
- Security via local encryption; no secrets stored remotely in POC

Action:
Start with CLI commands + local config file. Build proxy agent to map unified key to 3rd-party keys. Add minimal UI after CLI demo works. Validate onboarding and request flow within 5 days.
- Backend Engineer: API Design (POC scope):  
- POST /projects — create project, returns unified project_key (UUID)  
- POST /projects/{id}/api-keys — register third-party API key with metadata (vendor, key value)  
- GET /projects/{id}/proxy/{vendor}/{resource} — proxy request to vendor API, authenticating with stored key  
- GET /projects/{id}/api-keys — list registered vendor keys (masked)  
- DELETE /projects/{id}/api-keys/{key_id} — revoke vendor key  

Local Persistence:  
- File-backed JSON/YAML store per project (e.g., ~/.uapigateway/projects/{project_id}.json)  
- Store project metadata, unified key, and encrypted vendor API keys (AES-256 symmetric encryption with local passphrase)  
- CLI-first: local file storage avoids cloud dependency, reduces trust barrier, enables offline dev workflow  

Tradeoffs:  
- No centralized cloud storage means no multi-user sync or audit logs—acceptable for POC to prove core UX  
- Proxying limited to 2–3 popular APIs hardcoded in POC to reduce integration complexity  
- Encryption key management is local only; no KMS integration yet, trading security for simplicity and speed  
- No user auth or RBAC in POC; focus on single-user developer experience  

Actionable next steps:  
1. Define minimal vendor API adapters for Stripe, SendGrid, Twilio proxying  
2. Implement CLI commands for project creation, key registration, and proxy request  
3. Implement local encrypted file persistence with passphrase prompt  
4. Demo unified key usage and proxying in local dev environment within one week
- Auth Engineer: For local POC:  
- **Auth posture:** CLI-first, local-only, file-backed key store with no external dependencies.  
- **Implementation:** Generate one unified project API key locally; proxy requests through a lightweight local server that injects stored third-party keys (e.g., Stripe, SendGrid). Use simple JSON/YAML files for key mapping. No cloud or paid services. Open-source codebase for trust and auditability.  
- **Tradeoffs:** No multi-user sync or high availability; limited to dev/test environments; no hardened security beyond local OS protections. This minimizes risk and speeds iteration.

For production handoff:  
- **Auth posture:** Centralized, multi-tenant API gateway with secure vault-backed key storage (e.g., HashiCorp Vault or AWS KMS), RBAC, audit logging, and TLS-enforced proxying. Issue one project-level API key per team with scoped permissions. Integrate with SSO (OAuth/OIDC) for user auth.  
- **Tradeoffs:** Higher complexity, operational overhead, and initial trust barrier. But necessary for security, compliance, and scalability. Vendor lock-in risk mitigated by modular vault abstraction and open API.

**Action:** Build local POC first to validate UX and proxy logic. Then design production auth with vault-backed secrets, RBAC, and SSO for secure multi-user access and auditability.
- Database Engineer: For the Unified API Key Gateway POC, choose a local-first, file-backed embedded database to maximize simplicity, speed, and developer trust:

**Recommendation:** Use SQLite (v3) with WAL mode enabled.  
- **Why SQLite?**  
  - Zero dependencies, runs locally in-process, no server needed.  
  - ACID-compliant, reliable for credential mapping and proxy metadata.  
  - Easy to inspect and export (plain file), aiding transparency and trust.  
  - Mature ecosystem and tooling for CLI integration.  
- **Schema:**  
  - Projects table (project_id, unified_key, metadata)  
  - API keys table (api_key_id, project_id FK, vendor, encrypted_key, scopes)  
  - Proxy logs table (optional for demo)  
- **Tradeoffs:**  
  - No built-in multi-user concurrency (acceptable for local POC).  
  - Limited horizontal scaling (not needed at this stage).  
  - Encryption must be handled at app layer or via SQLite extensions.  
- **Next steps:**  
  - Implement CLI commands to create projects, add vendor keys, and generate unified keys.  
  - Store encrypted keys in SQLite, decrypt on proxy request.  
  - Keep all data local to avoid trust issues and external dependencies.  

This approach enables a quick, trustworthy POC without paid services or fragile integrations, aligning with crew synthesis and builder advice.
- Infra Engineer: Deploy a local-first, open-source POC on AWS using Terraform and Vercel for frontend/API hosting:

1. **Terraform**:  
- Provision minimal AWS infra: Lambda (Node.js) for proxying API calls, DynamoDB for key mappings, and IAM roles with least privilege.  
- Use Terraform modules for repeatability and easy teardown.  
- Avoid paid AWS services (e.g., Secrets Manager) to keep POC free and simple.

2. **Vercel**:  
- Host a React-based onboarding UI and CLI backend API proxy.  
- Use serverless functions to handle unified key issuance and proxy logic.  
- Integrate with AWS Lambda via API Gateway if needed for secure backend calls.

3. **Implementation tradeoffs**:  
- Local-first open-source POC avoids trust/switching friction but limits scalability and multi-tenant security.  
- AWS Lambda + DynamoDB offer low-cost, scalable backend but add latency vs. pure Vercel serverless.  
- Terraform ensures infra-as-code, enabling quick iteration and rollback.

**Action**:  
- Define Terraform AWS infra with Lambda + DynamoDB.  
- Build Vercel frontend + API routes for key issuance and proxying.  
- Implement proxy logic for 2–3 popular APIs (Stripe, SendGrid).  
- Deliver demo within one week to validate core flows and gather feedback.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions to run on PRs and pushes to main branches.
- Checks: Linting (YAML, JSON), security scans (e.g., secret scanning, dependency vulnerabilities), and unit tests for CLI and proxy components.
- Automate build and container image creation for the gateway plugin.
- Add a workflow to validate API key config files and simulate proxy requests locally.

Deployment Notes:
- Start with a local-first, file-backed CLI POC to minimize trust and external dependencies.
- Package as a plugin for popular API gateways (e.g., Kong) with a simple config mapping one unified key to multiple third-party keys.
- Deployments initially manual or via GitHub Actions to a test environment.
- Use feature flags to enable/disable proxying for specific APIs.

Tradeoffs:
- Local-first POC limits early scalability and multi-user concurrency but reduces risk and complexity.
- Avoid paid services or external secrets managers initially to speed MVP and reduce cost.
- Security tradeoff: proxying keys requires careful encryption and audit logging; start with minimal scope (2-3 APIs) to validate feasibility before expanding.

Action:
1. Define GitHub Actions workflows for lint, test, build, and deploy.
2. Implement CLI tool to generate unified key config and proxy logic.
3. Create example configs for Stripe and SendGrid.
4. Demo onboarding flow and proxy usage within one week.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that generates a single project API key.
2. Proxy server component that maps the unified key to 2–3 popular third-party APIs (e.g., Stripe, SendGrid).
3. File-backed configuration storing encrypted third-party API keys and mapping rules.
4. Minimal dependencies; no paid services or external deployment needed.
5. Open-source codebase to build trust and enable community feedback.
6. Basic onboarding flow: CLI command to initialize project, add third-party keys, and start proxy.
7. Logging for request proxying and error handling.
8. Security: encrypt stored keys locally; no cloud storage in POC.

Acceptance Criteria:
- User can run CLI to create a unified project key.
- Proxy accepts requests with unified key and forwards them correctly to underlying APIs.
- Third-party keys are securely stored and injected per request.
- Demo includes onboarding flow and proxying for at least Stripe and SendGrid APIs.
- No external paid services or cloud dependencies.
- Code is documented and runnable locally within one week.

Tradeoffs:
- Limiting to 2–3 APIs reduces scope but proves core concept.
- Local-only approach avoids trust issues but limits multi-user collaboration.
- File-backed storage simplifies POC but requires future vault integration.
- CLI-first prioritizes developer control over UI polish.

Action: Assign builder to develop CLI + proxy plugin with encrypted local config supporting Stripe and SendGrid keys. Validate proxy correctness and onboarding flow in a 5-day sprint.
