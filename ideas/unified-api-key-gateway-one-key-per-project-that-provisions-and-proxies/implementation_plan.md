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

1. **CLI-first & Local-first Setup**
   - Users install CLI tool.
   - Initialize project with `ukg init` creating a local config file (YAML/JSON) storing unified API key metadata and proxied keys encrypted locally.
   - Tradeoff: Local storage simplifies onboarding and offline use but limits centralized audit/compliance (acceptable for MVP targeting startups).

2. **Provisioning & Proxying**
   - CLI commands to add third-party API keys: `ukg add --tool=slack --key=xxx`.
   - Store encrypted keys locally; generate one unified project key.
   - Proxy requests via CLI or lightweight local proxy server that maps unified key to underlying keys.
   - Tradeoff: Local proxy avoids fragile cloud dependencies but limits multi-user real-time sync.

3. **Single-click Onboarding**
   - Slack onboarding bot (basic webhook) triggers CLI setup instructions and shares unified project key.
   - Tradeoff: Minimal Slack integration accelerates adoption but is limited to Slack users.

4. **Rotation & Audit (Basic)**
   - CLI commands to rotate keys and view usage logs stored locally.
   - Tradeoff: No centralized audit; MVP focuses on proving friction reduction.

5. **Next Steps**
   - Validate with 5–30 person SaaS startups in accelerators.
   - Measure onboarding speed, error reduction, and willingness to pay for advanced features.

This MVP avoids paid services and external deployment, focusing on rapid POC and user feedback.
- POC Coder: POC Plan: CLI-first, local-file-backed unified API key gateway

1. Scope:  
- CLI tool to create/manage one project key that proxies calls to 2-3 hardcoded third-party APIs (e.g., GitHub, Stripe).  
- Store third-party keys encrypted in a local JSON file per project.  
- Proxy requests locally, replacing unified key with actual API keys.

2. Implementation steps:  
- CLI commands: `init-project`, `add-api-key <service>`, `list-keys`, `proxy-request <service> <endpoint>`.  
- Use symmetric encryption (e.g., AES) with a user password to encrypt stored keys.  
- Proxy logic: intercept CLI requests, rewrite with actual keys, forward to third-party API, return response.  
- Minimal error handling and no user management.

3. Tradeoffs:  
- Local file storage simplifies setup, no cloud infra needed, but no centralized audit or team sharing.  
- Hardcoded APIs limit scope but prove core concept quickly.  
- CLI-only excludes UI but accelerates iteration and fits developer workflows.  
- No paid services or external deployment reduces cost and complexity.

4. Success criteria:  
- Developer can onboard a new API key, use the unified project key to call multiple APIs via CLI proxy.  
- Demonstrates friction reduction and centralized key management in a minimal setup.

Deliverables: CLI tool repo + README with usage instructions, example encrypted key file, and proxy demo script.  
Estimated time: 1 focused dev session (4-6 hours).
- Frontend Engineer: POC Interface Plan:

1. CLI-first, local file-backed config (YAML/JSON) per project storing unified API key and proxied keys metadata.
2. Commands:
   - `ukey init` — create project config with single unified key.
   - `ukey add <tool> <api-key>` — add third-party API key to config.
   - `ukey list` — list proxied APIs and status.
   - `ukey proxy <tool> [endpoint]` — proxy API request through unified key.
3. Local HTTP proxy server (localhost:PORT) routes requests using unified key to third-party APIs.
4. Minimal UI: CLI outputs JSON for integration with Slack bot or dashboard later.
5. Security: keys encrypted at rest with user password; no cloud storage to avoid early compliance blockers.
6. Tradeoffs:
   - Pros: Fast, simple, no external dependencies, easy onboarding.
   - Cons: No centralized audit/compliance, limited team collaboration, not enterprise-ready.
7. MVP goal: demonstrate single-key onboarding and proxying within 1 week.

Action: Build CLI tool skeleton + local proxy + config file support. Validate proxying a sample API call with unified key.
- Backend Engineer: POC API & Local Persistence Plan:

1. API Design (CLI-first, minimal):
- POST /projects {name} → create project, returns unified project_key (UUID)
- GET /projects/{id}/keys → list proxied 3rd-party API keys (masked)
- POST /projects/{id}/keys {tool, api_key} → add 3rd-party key
- DELETE /projects/{id}/keys/{key_id} → revoke key
- POST /projects/{id}/proxy/{tool}/request {method, path, body} → proxy API call with stored key

Tradeoff: Simple REST avoids auth complexity in POC; no user mgmt yet.

2. Local Persistence:
- Store projects and encrypted 3rd-party keys in a local JSON file (e.g., ~/.uapkgateway/config.json)
- Encryption: AES-256 with user-provided passphrase at CLI start
- File format example:
  {
    "projects": {
      "proj-uuid": {
        "name": "My Project",
        "keys": {
          "tool1": "encrypted_api_key1",
          "tool2": "encrypted_api_key2"
        }
      }
    }
  }

Tradeoff: Local file simplifies setup and offline use, but no centralized audit or multi-user sync (acceptable for MVP).

3. Proxying:
- CLI acts as a local proxy forwarding requests to 3rd-party APIs with injected keys.
- Logs minimal request metadata locally for audit demo.

Summary: This minimal API + encrypted local JSON persistence enables a working POC demonstrating unified key management and proxying without external dependencies or cloud infra, aligning with MVP speed and compliance tradeoffs.
- Auth Engineer: For local POC, implement a CLI-first, local file-backed auth posture: store the unified API key and proxied third-party keys encrypted in a local config file (e.g., ~/.unified-apikey.json.enc). Use a user passphrase or OS keychain for encryption. This enables quick iteration, offline use, and easy artifact handoff to other crews. Avoid external dependencies or paid services to keep the POC runnable in one session.

Tradeoffs:
- Pros: Fast setup, minimal infra, developer-friendly, no cloud lock-in, easy demo.
- Cons: No centralized audit, no role-based access, limited compliance (SOC2 risk), no team-wide key rotation visibility.

For production handoff, pivot to a cloud-managed secrets vault with:
- Centralized encrypted storage
- Role-based access control (RBAC)
- Audit logs and compliance reporting
- API key proxying service with token exchange
- Integration with identity providers (SSO/OAuth)

Tradeoffs:
- Pros: Enterprise-grade security, compliance-ready, team collaboration, scalable.
- Cons: Higher complexity, infra cost, onboarding friction.

Action: Build local CLI POC first, validate developer UX and proxy logic. Then design cloud vault integration for production, prioritizing compliance and auditability.
- Database Engineer: For the Unified API Key Gateway MVP, choose a local-first, file-backed embedded database to maximize simplicity, speed, and offline capability:

**Recommended DB:** SQLite  
- **Why:** Zero-config, serverless, cross-platform, ACID-compliant, and widely supported by CLI tools and languages.  
- **Storage:** Single encrypted file per project (use SQLCipher or OS-level encryption) to protect keys locally.  
- **Tradeoffs:**  
  - No centralized audit or real-time multi-user sync (acceptable for early-stage startups).  
  - Limited built-in role-based access control; rely on OS permissions and encryption.  
  - Compliance gaps for SOC2-level needs—flag for future cloud vault integration.  

**Implementation notes:**  
- Store API keys and metadata in normalized tables with timestamps for rotation tracking.  
- Provide CLI commands to read/write keys and export artifacts for downstream agents.  
- Encrypt sensitive fields or the entire DB file to mitigate local compromise risk.  
- Plan for future migration to cloud vaults or proxy services as compliance demands grow.

This approach ensures a deployable, low-friction POC aligned with the target ICP’s needs and the project’s rapid iteration goals.
- Infra Engineer: Plan a hybrid AWS + Vercel + Terraform deployment for the Unified API Key Gateway MVP:

1. **AWS Infra (Terraform):**  
- Use AWS Secrets Manager for centralized, encrypted storage of third-party API keys (supports audit/compliance).  
- Deploy a lightweight API Gateway + Lambda proxy layer to handle unified key authentication and proxy requests to third-party APIs.  
- Use DynamoDB for metadata (projects, keys, usage logs).  
- Terraform manages all infra as code for repeatability and versioning.

2. **Vercel Frontend:**  
- Host the developer portal and onboarding UI on Vercel for fast global CDN and easy CI/CD integration.  
- Use serverless functions for CLI token issuance and Slack bot integration.

3. **Tradeoffs:**  
- AWS Secrets Manager adds cost but ensures compliance and centralized control, addressing skeptic concerns.  
- Local file-backed model is simpler but risks auditability and scaling; AWS Secrets Manager mitigates this.  
- Vercel accelerates frontend deployment but adds a second cloud provider; acceptable for MVP speed and developer experience.

4. **Actionables:**  
- Define Terraform modules for AWS Secrets Manager, Lambda, API Gateway, DynamoDB.  
- Build minimal Lambda proxy to authenticate unified key and forward requests.  
- Develop Vercel frontend with CLI token issuance and Slack onboarding bot.  
- Integrate Terraform deployment pipeline with GitHub Actions.

This shape balances MVP speed, compliance readiness, and developer UX for targeted SaaS startups.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions for CI/CD pipelines.
- On PR: run lint, unit tests, and security scans on code and config files (e.g., check for accidental API key commits).
- On merge to main: run integration tests with mocked API key proxying.
- Use branch protection rules requiring passing checks and code review.

Deployment Notes:
- Start with CLI-first, local file-backed MVP to avoid fragile external dependencies.
- Deploy POC as a GitHub Pages or simple static site for docs; CLI tool distributed via GitHub Releases.
- No paid services or external deployments initially to speed iteration.
- Use GitHub Secrets for storing any deployment tokens securely.
- Document manual steps for onboarding and key rotation workflows.

Tradeoffs:
- Local file-backed model limits centralized audit/compliance; acceptable for early-stage startups but not enterprises.
- Avoiding cloud deployment reduces complexity but limits real-time multi-user sync and monitoring.
- GitHub Actions provide free, integrated automation but have runtime limits and less flexibility than dedicated CI.

Action:
- Define GitHub Actions workflows for lint, test, and security scans.
- Create branch protection rules.
- Prepare deployment scripts for CLI tool release.
- Document manual onboarding and rotation steps for MVP users.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first tool that generates a local file-backed project config storing unified API key metadata and encrypted third-party API keys.
2. Proxy server component that reads local config, intercepts unified key requests, and routes them to corresponding third-party APIs with injected keys.
3. Support onboarding new third-party APIs with a single CLI command that updates local config and provisions keys.
4. Basic audit log stored locally, tracking key usage and rotations.
5. Free tier limits: max 3 third-party APIs per project.
6. No external paid services or cloud deployment in MVP; all components run locally or on developer machines.
7. Security: encrypt keys at rest, require local user authentication to unlock keys.
8. Exportable config format for handoff to future agent crews.

Acceptance Checks:
- CLI can create a new project with a unified API key.
- Proxy correctly forwards requests to at least 3 different third-party APIs using stored keys.
- Adding/removing APIs updates local config and proxy behavior immediately.
- Audit logs record key usage events locally.
- Encryption and local authentication prevent unauthorized key access.
- MVP runs fully offline without external dependencies.

Tradeoffs:
- Local file-backed storage limits centralized audit/compliance, acceptable for target startups but not regulated enterprises.
- No cloud deployment reduces complexity and cost but restricts team-wide real-time key sharing.
- CLI-first approach speeds MVP delivery but may limit UX for non-technical users initially.
