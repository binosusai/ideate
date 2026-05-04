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

1. Scope: CLI-first, local-first, file-backed MVP proxying 2 APIs (Stripe, SendGrid) with one unified project key.
2. Setup:
   - User runs CLI to create a new project key.
   - CLI stores encrypted third-party API keys locally in a project config file (e.g., YAML/JSON).
   - CLI generates a local proxy server config that maps unified key to backend API keys.
3. Proxy:
   - Local proxy intercepts requests authenticated by unified key.
   - Routes requests to appropriate third-party API using stored keys.
   - Logs usage for basic observability.
4. Onboarding:
   - CLI exports a shareable project config file for teammates.
   - Teammates import config, get unified key, and run local proxy.
5. Security:
   - Encrypt keys at rest with user password.
   - No cloud storage or external dependencies in MVP.
6. Demo:
   - Show instant setup of unified key.
   - Proxy calls to Stripe and SendGrid APIs.
   - Demonstrate teammate onboarding via config import.
7. Tradeoffs:
   - No multi-user cloud sync or automated key rotation (future).
   - Local proxy limits scalability but accelerates POC.
   - Manual key provisioning avoids complex integrations.
8. Next:
   - Collect feedback on usability and security concerns.
   - Validate willingness to pay and onboarding speed improvements.

This approach delivers a tangible, secure POC in under one week with minimal dependencies, directly addressing early-stage SaaS pain points.
- POC Coder: Smallest working POC plan:

1. CLI tool + local file storage (YAML/JSON) for project config and encrypted API keys.
2. Proxy server (Node.js/Express) running locally, authenticating requests by a single unified project key.
3. Proxy routes for two example APIs (Stripe, SendGrid):
   - Proxy forwards client requests, injects stored API key, returns response.
4. Admin CLI commands:
   - `init` to create project and unified key
   - `add-api-key` to store third-party keys encrypted locally
   - `start-proxy` to launch local proxy server
5. No external dependencies or paid services.
6. Security tradeoff: local encryption with a passphrase; no multi-user or cloud sync yet.
7. UX tradeoff: CLI-only, no UI; no onboarding automation yet.
8. Success criteria: a developer runs CLI, adds Stripe and SendGrid keys, starts proxy, and makes API calls via unified key that proxy correctly.

This proves core value: one key per project proxies multiple APIs, centralizes keys, and reduces setup friction. Next steps depend on user feedback on security and workflow.
- Frontend Engineer: POC Interface Plan: Minimal Web UI + CLI for Unified API Key Gateway

1. Web UI (React):
- Project dashboard: List projects with unified API key status.
- Project detail: Show linked APIs (start with Stripe, SendGrid), their provisioning status, and usage stats.
- Add API button: Select API (dropdown), enter third-party API key, save securely.
- Unified project API key: Display & regenerate button.
- Team onboarding: Invite teammates by email with role assignment.
Tradeoffs: 
- Web UI enables quick feedback and demo but adds frontend scope.
- Limit API integrations to 2 for MVP to reduce complexity.
- Use local file or in-memory store initially to avoid backend infra.

2. CLI (Node.js):
- Commands: create-project, add-api-key, list-projects, get-unified-key.
- Local config file stores encrypted keys, synced with UI.
Tradeoffs:
- CLI-first supports developer workflow and offline use.
- Syncing CLI and UI state adds complexity but critical for adoption.

Security:
- Encrypt keys at rest with local master password.
- No external backend or paid services to speed POC.

Actionables:
- Build React UI with basic routing and forms.
- Implement CLI commands with encrypted JSON config.
- Proxy requests in POC backend stub (mock Stripe/SendGrid).
- Demo onboarding flow: create project, add keys, show unified key usage.

This scope balances quick delivery, developer usability, and core value proof.
- Backend Engineer: API Design:
- POST /projects: Create a project with unified API key (returns project ID + unified key)
- GET /projects/{id}/keys: List proxied third-party API keys metadata (no secrets)
- POST /projects/{id}/keys: Add third-party API key (store encrypted)
- DELETE /projects/{id}/keys/{keyId}: Remove third-party API key
- POST /projects/{id}/proxy/{tool}/call: Proxy API call to third-party tool using stored key, forwarding request and returning response

Local Persistence:
- File-backed JSON/YAML config per project storing:
  - Project ID and unified key (locally generated UUID + secret)
  - Encrypted third-party API keys (AES-256 symmetric encryption with local master key)
  - Metadata (tool name, key ID, scopes)
- CLI-first tool reads/writes this file, enabling offline key management and local dev usability

Tradeoffs:
- File-backed local persistence simplifies POC, no DB needed, but limits multi-user sync (acceptable for MVP)
- Proxy API calls enable centralized audit and rotation but add latency and single point of failure
- Encryption keys stored locally avoids cloud secrets but requires secure local storage and user trust
- Minimal API surface reduces complexity but limits features like key rotation or granular permissions initially

Action:
- Implement CLI tool managing local encrypted config file per project
- Build minimal HTTP server proxying two APIs (Stripe, SendGrid) using stored keys
- Expose unified project key for client apps to authenticate proxy calls
- Focus on security of local encryption and simple onboarding flow
- Auth Engineer: Local POC Auth Posture:
- Use a CLI-first, file-backed approach storing encrypted API keys locally (e.g., AES-256 encryption with a user password-derived key).
- Implement a single unified project API key that maps internally to third-party keys.
- Proxy requests locally without external deployment or paid services.
- Keep auth simple: local user password unlocks keys; no multi-user or networked auth yet.
- Tradeoffs: minimal security scope, no team sync, but fastest to build and demo core value.

Production Handoff Auth Posture:
- Migrate to a centralized, multi-tenant auth service with OAuth2 client credentials flow per project.
- Store third-party keys in a hardened secrets manager (e.g., AWS Secrets Manager or Vault).
- Use JWTs scoped per project and role for unified API key proxying.
- Implement RBAC and audit logging for team onboarding and credential rotation.
- Tradeoffs: higher complexity and cost, requires secure infrastructure and onboarding, but essential for trust, scalability, and compliance.

Action:
1. Build POC locally with encrypted file storage and CLI unlock.
2. Design production auth spec with OAuth2, JWT, RBAC, and secrets manager integration.
3. Validate POC security assumptions with early users before production rollout.
- Database Engineer: For a local-first, deployable POC of the unified API key gateway, choose SQLite as the default database:

- **Why SQLite?**  
  - Zero-configuration, file-based, no server needed — ideal for CLI-first, local-first workflows.  
  - ACID-compliant, reliable storage for API keys and metadata.  
  - Easy to bundle and deploy with the CLI tool, no external dependencies.  
  - Supports concurrent reads and serialized writes, sufficient for single-user or small-team local use.

- **Schema basics:**  
  - Projects table (id, name, unified_key)  
  - Third-party APIs table (id, project_id, api_name, encrypted_api_key)  
  - Users/teammates table (id, project_id, user_email, permissions)

- **Tradeoffs:**  
  - Not suited for multi-node or high-concurrency production use; plan migration path to a server-based DB (Postgres) if scaling.  
  - Encryption of keys must be handled at the application layer; SQLite offers no built-in encryption by default.  
  - Local file storage raises security concerns; recommend OS-level file encryption or user-managed secrets.

- **Action:**  
  - Implement CLI tool with embedded SQLite DB file per project.  
  - Encrypt API keys before storage using a user-provided master password or OS keychain integration.  
  - Provide export/import commands for onboarding and migration.

This approach enables a fast, secure, and deployable POC aligned with the builder’s local-first mandate and the strategist’s MVP speed priority.
- Infra Engineer: Deployment Shape for Unified API Key Gateway POC:

1. **AWS Infrastructure (Terraform-managed):**  
- Use AWS Lambda (Node.js) for API proxy functions (Stripe, SendGrid).  
- Store third-party API keys securely in AWS Secrets Manager, scoped per project.  
- API Gateway fronting Lambda, exposing unified project key auth.  
- DynamoDB for lightweight project metadata and key mappings.  
- Terraform to provision all resources, enabling repeatable infra and easy iteration.

2. **Vercel Frontend (Next.js):**  
- Admin UI for project key creation, onboarding teammates, and viewing usage.  
- Serverless functions for UI backend calls, proxying via AWS API Gateway.

3. **Local-first CLI (optional MVP):**  
- CLI to bootstrap project keys and config files, syncing with cloud backend.

**Tradeoffs:**  
- AWS Lambda + API Gateway ensures scalable, pay-per-use backend, minimizing upfront cost and complexity.  
- Secrets Manager centralizes credentials securely, but adds cost and AWS lock-in.  
- DynamoDB is low-maintenance but may limit complex queries; sufficient for MVP.  
- Vercel enables rapid frontend iteration with minimal ops overhead.  
- Avoids paid third-party services to keep POC cost low and control high.  
- Security risk: centralized keys require strict IAM and encryption policies; mitigate with least privilege and audit logs.  
- MVP scope limited to 2 APIs to prove concept quickly.

**Action:**  
- Define Terraform modules for Lambda, API Gateway, Secrets Manager, DynamoDB.  
- Build minimal Lambda proxy for Stripe and SendGrid.  
- Develop Vercel admin UI with unified project key management.  
- Implement CLI bootstrap for local dev.  
- Deploy and test end-to-end within 1 week.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions for CI/CD pipelines.
- On PR: run lint, unit tests, and security scans (e.g., secret scanning, dependency checks).
- Enforce branch protection requiring passing checks before merge.
- Automate changelog generation from commit messages.
- Use labels and issue templates to track feature vs. bug vs. research tasks.

Deployment Notes:
- Start with CLI-first, local-first POC to avoid fragile external dependencies.
- Deploy proxy server as a containerized app with environment-based config.
- Use GitHub Actions to build and push Docker images on main branch merges.
- Automate deployment to a staging environment for manual QA.
- For secrets, use GitHub Secrets for CI and local encrypted files for dev.
- Document manual onboarding steps for early users; automate onboarding in later iterations.

Tradeoffs:
- Avoid paid services initially to speed MVP; may sacrifice scalability and advanced security.
- Local-first approach limits multi-user concurrency but accelerates iteration.
- Proxying only two APIs reduces scope but proves core value quickly.
- Manual onboarding increases early friction but reduces complexity and risk.

Action:
1. Define GitHub Actions workflows for lint, test, security scan.
2. Configure branch protection rules.
3. Create Dockerfile and deployment scripts.
4. Document manual onboarding and proxy usage.
5. Schedule demo with early-stage SaaS devs for feedback.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-first tool that generates a unified project API key.
2. Secure, file-backed credential storage with encryption (e.g., AES-256).
3. Proxy server that routes requests from the unified key to at least two third-party APIs (e.g., Stripe, SendGrid).
4. Admin UI for onboarding teammates and managing API keys per project.
5. Minimal external dependencies; no paid services or fragile integrations.
6. Logging and error handling for API calls to aid debugging.
7. Support onboarding flow that imports existing API keys securely.
8. Configurable rate limiting and retry logic for proxied APIs.

Acceptance Criteria:
- Unified key successfully proxies authenticated requests to both Stripe and SendGrid APIs.
- CLI generates and stores encrypted credentials locally.
- Admin UI allows adding/removing teammates with access control.
- Onboarding flow imports existing keys without exposing plaintext.
- Proxy logs requests and errors without leaking sensitive data.
- Demo runs fully locally without external paid services.
- Security review confirms no plaintext key exposure or unauthorized access.

Tradeoffs:
- Prioritize minimal MVP scope over broad API coverage.
- Local-first design limits immediate cloud scalability but accelerates POC.
- Proxy adds latency but centralizes control and auditing.
- Avoid complex agent orchestration to reduce fragility and speed delivery.

Next Steps:
- Build CLI and local proxy with Stripe/SendGrid integration.
- Develop minimal admin UI for teammate management.
- Conduct security and usability testing with target users.
