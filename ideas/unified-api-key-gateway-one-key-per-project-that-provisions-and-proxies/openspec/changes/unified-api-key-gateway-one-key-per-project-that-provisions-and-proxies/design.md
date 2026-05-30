# Design: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Architecture
The first draft should be a complete local POC with a static frontend, a small backend API when useful, SQLite persistence, install/run docs, and deployment guidance.

## Data
Use SQLite locally. Document Neon and Supabase as production database options. Avoid paid APIs until explicitly approved.

## Auth
Use no auth for local POC unless required. Document Clerk and Firebase Auth integration points for production.

## Infra And DevOps
Prefer Vercel for frontend previews and AWS services for backend/infra when needed. Include Terraform placeholders and GitHub Actions checks.

## Risks
- The POC may prove interface feasibility without proving market demand.
- External integrations may need a second design pass.
- Deployment docs are scaffolding until real cloud accounts and project IDs are selected.


## Implementation Plan
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

1. **Scope & Target APIs**  
   - Focus on top 3-5 third-party APIs with well-documented, programmatic key management (e.g., Stripe, Twilio, SendGrid).  
   - Exclude OAuth-only or manual key APIs initially to reduce complexity.

2. **User Onboarding**  
   - GitHub Marketplace app triggered on new repo creation for seed-stage SaaS projects.  
   - CLI tool for local-first usage with file-backed config for offline access and auditability.

3. **Provisioning Flow**  
   - User authenticates GitHub repo → selects desired third-party APIs → app auto-provisions API keys via vendor APIs or prompts for manual input if automation unavailable.  
   - Store encrypted keys locally and optionally in a minimal backend (e.g., encrypted DB or file storage) for proxying.

4. **Proxying Requests**  
   - Implement a lightweight local proxy or serverless function that intercepts API calls from the app using the unified key and forwards them with the correct third-party key.  
   - Log usage for audit and rotation triggers.

5. **Rotation & Revocation**  
   - Support manual rotation via CLI commands initially; automate rotation only for APIs with supported endpoints.

6. **Security & Trust**  
   - Encrypt all stored keys with user-controlled keys.  
   - Provide clear docs on data ownership and no backend key exposure.  
   - No paid services or complex infra dependencies to speed MVP.

**Tradeoffs:**  
- Limited API coverage initially to ensure fast delivery and reliability.  
- Local-first approach limits multi-user collaboration but reduces trust barriers.  
- Proxy adds minimal latency but centralizes key usage for easier rotation and audit.

Deliverables: CLI tool, GitHub Marketplace app, proxy component, docs. MVP ready in 1-2 weeks.
- POC Coder: POC Plan: Unified API Key Gateway (Local CLI-first)

Scope:  
- CLI tool managing one unified project key locally (file-backed JSON).  
- Proxy requests to 2–3 popular third-party APIs with static API keys (e.g., Stripe, SendGrid).  
- Manual key entry for third-party keys (no automated provisioning yet).  
- Proxy forwards requests adding correct third-party key from local store.  
- Basic encryption of stored keys (e.g., AES with user password).  
- Simple HTTP proxy server runs locally, authenticates requests with unified key, injects third-party keys.

Tradeoffs:  
- No automation of key provisioning (due to API limitations and complexity).  
- Local only, no cloud or multi-user sync (avoids trust/security risks, accelerates build).  
- Minimal UI (CLI + config files) to prove concept quickly.  
- No OAuth/token refresh support yet; static keys only.

Implementation Steps:  
1. CLI scaffold: init project, add third-party keys, generate unified key.  
2. Local encrypted JSON store for keys.  
3. Local HTTP proxy server authenticates unified key, proxies requests with injected keys.  
4. Demo: curl or Postman calls to proxy with unified key, hitting Stripe/SendGrid APIs.

Outcome:  
Proves unified key concept, centralizes key usage, minimal viable demo in <1 week without external dependencies or paid services.
- Frontend Engineer: POC Interface Plan: CLI-First with Minimal Web Dashboard

1. CLI Tool (Primary Interface)
- Commands:
  • `init` — create new project with unified key
  • `add-tool <tool-name>` — provision & link 3rd-party API keys (Stripe, Twilio, SendGrid)
  • `list` — show linked tools and status
  • `rotate <tool-name>` — rotate underlying keys
  • `proxy-request <tool-name> <endpoint> [--data]` — proxy API calls via unified key
- File-backed config: JSON/YAML storing project key and tool mappings locally
- Benefits: fast iteration, local-first, no external dependencies, easy artifact sharing
- Tradeoff: CLI-only limits discoverability and onboarding UX; no GUI for non-CLI users

2. Minimal Web Dashboard (Secondary, Optional)
- Show project status, linked tools, usage logs
- Onboard via GitHub Marketplace OAuth flow
- Tradeoff: adds complexity but aids trust & visibility; defer to post-POC

3. Security & Trust
- Local encryption of stored keys, no cloud storage in POC
- Proxy requests signed with unified key, logged locally

4. MVP Scope
- Support 3 top APIs with known key management APIs
- No paid services or external deployment required

Next Steps: Implement CLI skeleton + local config + proxy stub; demo key provisioning + proxy call for Stripe.
- Backend Engineer: **API Design for POC**

1. **Project API Key Management**
- `POST /projects`  
  Request: `{ "name": "My SaaS Project" }`  
  Response: `{ "project_id": "uuid", "unified_key": "proj-unified-key" }`  
- `GET /projects/{project_id}`  
  Response: `{ "project_id": "uuid", "unified_key": "proj-unified-key", "linked_services": [...] }`

2. **Third-Party API Key Provisioning (Manual for POC)**
- `POST /projects/{project_id}/keys`  
  Request: `{ "service": "stripe", "api_key": "sk_test_..." }`  
  Response: `{ "status": "linked" }`

3. **Proxy Endpoint**
- `POST /proxy/{project_id}/{service}/...`  
  Forwards requests to third-party API using stored key, adding authentication headers.

---

**Local Persistence**

- Use a local file (YAML/JSON) storing:  
  ```yaml
  projects:
    - id: uuid
      unified_key: string
      services:
        stripe: sk_test_...
        sendgrid: SG.xxxx
  ```
- CLI-first, file-backed for easy inspection and handoff.
- Encryption at rest optional for POC; document as tradeoff.

---

**Tradeoffs**

- **Manual key input** vs full automated provisioning: POC uses manual input due to API heterogeneity and rate limits.
- **Local file storage** vs cloud DB: local enables fast iteration, no infra cost, but no multi-user sync.
- **Proxying requests** adds latency and complexity but centralizes credential use and hides keys from clients.
- **Security**: POC minimal; production requires encryption, audit logs, and compliance.

---

**Actionables**

- Define CLI commands to create projects, add keys, and proxy requests.
- Implement local JSON/YAML persistence with schema validation.
- Build proxy middleware to inject keys per service.
- Mock 3 services (Stripe, SendGrid, Twilio) with manual key input.
- Document security gaps and next steps for automation and trust.
- Auth Engineer: For local POC:  
- Use a CLI-first, local-first approach with file-backed storage (e.g., encrypted JSON/YAML) for unified API keys per project.  
- Proxy requests locally or via a lightweight local server that injects third-party keys.  
- No external paid services or deployments to keep iteration fast and low-risk.  
- Implement minimal encryption (e.g., libsodium) for stored keys and basic access control (local user only).  
- Support a small fixed set of APIs with documented manual provisioning steps to sidestep automation gaps.  

Tradeoffs:  
+ Fast to build, easy to demo, no cloud dependency, low trust barrier for early adopters.  
- Limited automation, no multi-user sync, no centralized auditing or rotation.  

For production handoff:  
- Move to a cloud-hosted gateway with hardened security (encryption at rest/in transit, zero-trust auth).  
- Integrate with established identity providers (OAuth/OIDC) for team access control.  
- Automate provisioning/rotation where APIs allow; fallback to manual workflows with audit logs.  
- Provide a web dashboard and API for key management and usage monitoring.  
- Pursue SOC 2 or ISO 27001 compliance to build trust.  

Tradeoffs:  
+ Scalable, secure, multi-tenant, audit-ready, easier onboarding.  
- Higher complexity, cost, longer dev cycle, requires trust-building and compliance effort.  

Action: Start POC locally with CLI + encrypted file store; plan cloud gateway MVP with automated key lifecycle and compliance roadmap for production.
- Database Engineer: For a local, deployable database to support the Unified API Key Gateway POC, choose SQLite as the default:

- **Why SQLite?**  
  • Zero-config, file-based, no server needed → perfect for CLI-first, local-first approach  
  • Lightweight and fast for small-to-medium datasets (API keys, project metadata)  
  • ACID compliant, supports encryption extensions (e.g., SQLCipher) for credential security  
  • Easy to snapshot, backup, and share artifacts with other teams or agents  

- **Tradeoffs:**  
  • Not suited for high concurrency or multi-user production environments → fine for MVP and demos  
  • Limited built-in user access control → rely on OS-level file permissions and encryption  
  • No built-in replication or clustering → future upgrades can migrate to PostgreSQL or Vault-backed stores  

- **Implementation:**  
  • Store API keys encrypted at rest using SQLCipher or application-layer encryption  
  • Use a simple schema: Projects table, API Keys table with metadata and encrypted secrets  
  • Bundle DB file in project repo or local config directory for portability  
  • Provide CLI commands to read/write keys, rotate, and export artifacts  

This approach enables rapid POC delivery without external dependencies, aligns with the builder’s CLI-first, local-first mandate, and keeps security manageable for seed-stage SaaS teams.
- Infra Engineer: Deploy a minimal viable unified API key gateway as a serverless app on AWS + Vercel, managed via Terraform:

1. **AWS Infra:**
   - Use AWS Lambda (Node.js) for API key proxy and provisioning logic.
   - Store encrypted keys in AWS Secrets Manager with fine-grained IAM roles.
   - Use API Gateway to expose Lambda endpoints securely.
   - Enable CloudWatch logging and alarms for anomaly detection.
   - Use AWS KMS for encryption keys, ensuring zero-trust architecture.

2. **Vercel Frontend:**
   - Host a React dashboard for onboarding and key management.
   - Integrate with GitHub OAuth for repo-based project onboarding.
   - Use Vercel Serverless Functions for lightweight API calls (e.g., GitHub webhook handling).

3. **Terraform:**
   - Define AWS resources (Lambda, API Gateway, Secrets Manager, KMS).
   - Manage Vercel project and environment variables via Terraform provider.
   - Automate deployment pipelines with Terraform Cloud or GitHub Actions.

**Tradeoffs:**
- Serverless reduces ops burden but may hit cold start latency.
- AWS Secrets Manager adds cost but ensures secure key storage.
- Partial automation due to third-party API limitations; start with top 5 APIs with best automation support.
- Vercel frontend accelerates developer onboarding but adds cross-cloud complexity.
- Terraform ensures reproducibility but requires initial learning curve.

**Action:**
- Build POC Lambda functions for Stripe and Twilio key proxy.
- Deploy minimal Vercel dashboard with GitHub onboarding.
- Write Terraform scripts for AWS infra and Vercel config.
- Validate security posture and latency under load.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions to automate CI/CD pipelines triggered on PRs and merges.
- Implement linting, security scanning (e.g., secret detection, dependency checks), and unit tests as mandatory checks to catch credential leaks early.
- Add a custom workflow step to validate API gateway config files (YAML/JSON) for correct key mappings and scopes.
- Automate semantic version tagging and changelog generation on release branches.

Deployment Notes:
- Deploy CLI-first POC as a GitHub Marketplace app with minimal external dependencies.
- Use GitHub Secrets to store any deployment credentials securely.
- Deploy on GitHub-hosted runners initially to avoid infrastructure overhead.
- Release with a free tier supporting top 5 APIs; monitor usage and errors via GitHub Actions logs.
- Document manual rollback steps and emergency key revocation procedures.

Tradeoffs:
- GitHub Actions limits runtime and concurrency; suitable for POC but may need dedicated CI for scale.
- Marketplace app deployment accelerates adoption but requires compliance with GitHub policies.
- Avoid paid services initially to reduce cost and complexity but may limit automation scope.
- Security scanning in CI adds overhead but is critical given sensitive credential handling.

Action:
- Define GitHub Actions workflows for lint, test, security scan, and deploy.
- Prepare Marketplace app manifest and onboarding docs.
- Implement config validation step in CI.
- Plan manual rollback and incident response playbook.
- OpenSpec Writer: Implementation Requirements for Unified API Key Gateway MVP:

1. Scope: Support top 5 third-party APIs (e.g., Stripe, Twilio, SendGrid, GitHub, Slack) with documented API key provisioning endpoints or OAuth token refresh flows.

2. Architecture: CLI-first, local-first, file-backed prototype that generates config/artifacts readable by downstream agents; no external paid services or deployments initially.

3. Features:
   - Single unified API key per project that proxies requests to underlying third-party APIs.
   - Automated provisioning and rotation where API supports it; manual fallback UI for others.
   - Secure local storage of credentials with encryption at rest.
   - Simple onboarding flow triggered at repo creation (GitHub Marketplace app integration optional for POC).
   - Audit logs of key usage and rotation events.

4. Security:
   - Encrypt stored credentials using strong symmetric encryption.
   - Zero-trust design: no credentials sent outside local environment during POC.
   - Clear documentation of data ownership and breach response.

Acceptance Criteria:

- CLI tool can create a unified key that proxies calls to at least 3 supported APIs.
- Automated provisioning works end-to-end for at least 2 APIs.
- Manual fallback UI allows adding keys for APIs without automation.
- Local encrypted storage persists keys and config files.
- Onboarding flow completes within 5 minutes for a new project.
- No external paid services or fragile integrations used.
- Security review confirms no plaintext credential leaks.

Tradeoffs:

- Limiting to 5 APIs reduces scope but enables focused POC.
- Local-first approach avoids early trust/security barriers but delays cloud multi-user sync.
- Partial automation accepted due to API heterogeneity; manual fallback ensures coverage.

Next step: Build CLI prototype with local encrypted storage and proxy logic for 3 APIs, demo automated provisioning for 2, and validate onboarding flow.