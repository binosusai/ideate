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

1. **CLI-First Local Setup**  
- User runs CLI to create a new project, generating a single unified API key.  
- CLI stores config and encrypted third-party API keys in a local file (YAML/JSON) for easy inspection and version control.  
- Tradeoff: No cloud sync initially reduces complexity and security risk but limits team collaboration.

2. **Proxy Server (Local or Lightweight Cloud)**  
- Proxy accepts unified key, maps requests to respective third-party APIs using stored keys.  
- Logs usage per tool for audit trail.  
- Tradeoff: Start with local proxy to avoid paid infra; cloud proxy can follow for multi-user support.

3. **Key Rotation & Revocation**  
- CLI commands to rotate/revoke third-party keys or unified key, updating local config and proxy behavior.  
- Tradeoff: Manual rotation initially; automation can come later.

4. **Slack Onboarding Bot (Optional MVP Stretch)**  
- Simple bot that creates project and returns unified key, easing initial adoption.  
- Tradeoff: Adds integration complexity; defer if timeline tight.

**Focus:** Deliver a working proof-of-concept within one week that shows single-key usage, proxying, and rotation without paid services or fragile dependencies. Prioritize security by never exposing raw keys outside proxy and local config.
- POC Coder: POC Plan: Local CLI-first unified API key gateway (file-backed, no external deps)

**Goal:** Prove unified key proxies calls to 2+ third-party APIs with minimal setup, showing onboarding & rotation ease.

**Scope:**
- CLI tool to create a local project config file storing encrypted 3rd-party API keys.
- Generate one "unified" API key (e.g., JWT or UUID) per project.
- Local HTTP proxy server that:
  - Authenticates requests via unified key.
  - Routes requests to configured 3rd-party APIs, injecting stored keys.
- Rotation: CLI command to update underlying keys without changing unified key.
- Audit: Log proxied requests locally.

**Tradeoffs:**
- No multi-user/team support (focus on individual dev proof).
- No cloud deployment or UI (reduce complexity).
- File-backed config limits scalability but ensures offline, local-first proof.
- Minimal security: encrypt keys with local passphrase, no hardened secrets vault.

**Next steps:**
1. Define config schema for project keys + unified key.
2. Implement CLI commands: init, add-key, rotate-key, start-proxy.
3. Proxy logic: authenticate unified key, route with injected keys.
4. Demo with 2 real APIs (e.g., GitHub + Slack) showing single-key usage and rotation.

This POC validates core value: one key per project, proxying multiple APIs, enabling seamless onboarding and rotation locally.
- Frontend Engineer: POC Interface Plan for Unified API Key Gateway

1. **Core UI Components:**
- **Project Dashboard:** List projects with unified API key status (active, revoked).
- **API Tool Catalog:** Browse/add third-party tools with minimal config.
- **Unified Key Display:** Show one project-level API key; hide raw third-party keys.
- **Key Rotation Button:** Trigger unified key rotation; auto-propagate changes.
- **Audit Log Viewer:** Read-only timeline of key usage and provisioning events.

2. **Workflow:**
- User creates a project → system generates unified key.
- User adds third-party APIs from catalog → system proxies keys internally.
- User uses unified key in apps; gateway proxies requests.
- User rotates unified key or revokes per tool via UI.

3. **Tradeoffs:**
- **Simplicity vs Security:** Hide raw keys to reduce leaks but must securely store/proxy keys server-side (POC can simulate with local file).
- **Minimal UI:** Focus on essentials; no team management or billing yet.
- **No external deployment:** CLI-first local server with React frontend to demo proxy and UI.

4. **Tech Stack:**
- React + Tailwind for UI.
- Node.js Express local proxy server.
- File-backed JSON store for keys and audit logs.

Action: Build React dashboard with project and API management views; implement local proxy server to simulate unified key usage and rotation.
- Backend Engineer: API Definition for POC:
- POST /projects — create project, returns unified API key (UUID)
- GET /projects/{id}/keys — list proxied third-party API keys metadata (no raw keys)
- POST /projects/{id}/keys — add third-party API key (encrypted at rest)
- DELETE /projects/{id}/keys/{keyId} — revoke third-party API key
- POST /proxy/{unifiedKey}/{toolEndpoint} — proxy request to third-party API, inject real key server-side, log usage

Local Persistence:
- File-backed JSON store per user: projects.json and keys.json encrypted with user passphrase
- Store unified API key, project metadata, encrypted third-party keys, and usage logs locally
- CLI-first: local read/write, sync to remote optional for POC

Tradeoffs:
- Security: local encryption limits exposure but single unified key is a single point of failure
- No external paid services: simplifies POC, but limits scalability and audit log centralization
- File-backed local store enables quick iteration, but not multi-user sync or high availability
- Proxy endpoint implementation is minimal, focusing on key injection and logging, not rate limiting or caching

Actionables:
- Implement CLI commands to create projects, add/remove keys, and proxy requests
- Encrypt third-party keys locally with strong symmetric encryption (e.g., AES-256)
- Log proxy usage locally with timestamps and endpoints accessed
- Design API so that unified key never exposes raw third-party keys to clients
- Prepare README with usage and security caveats for early adopters
- Auth Engineer: For local POC:  
- Use a **CLI-first, local-only, file-backed auth posture**.  
- Generate one unified API key per project stored encrypted in a local config file (e.g., JSON with AES-256).  
- Proxy requests through a local lightweight server that injects third-party keys dynamically from the file.  
- No external dependencies or paid services to maximize speed and simplicity.  
- Implement minimal access control (e.g., local user permissions) and audit logs in local files.  

Tradeoffs:  
+ Fast iteration, no cloud lock-in, easy to demo and hand off.  
- No multi-user/team support, limited security (local machine trust), no centralized revocation.  

For production handoff:  
- Move to a **centralized, multi-tenant API gateway service** with:  
  - Per-project unified API keys issued and managed via a secure backend.  
  - Proxy layer that never exposes raw third-party keys to clients.  
  - Fine-grained RBAC, centralized key rotation, audit logging, and compliance controls.  
  - Integration with existing secrets managers or vaults for backend key storage.  

Tradeoffs:  
+ Strong security posture, compliance-ready, scalable multi-user/team support.  
- Higher complexity, requires secure hosting and operational overhead, potential switching friction.  

Action: Start POC with local CLI + file-backed proxy to prove concept; design production architecture for secure centralized gateway with RBAC and audit trails.
- Database Engineer: For a local-first, deployable unified API key gateway POC, choose SQLite as the default database:

- **Why SQLite?**  
  - Zero-config, file-backed, no server needed → fits CLI-first, local-first approach.  
  - ACID compliant, reliable for credential storage and audit logs.  
  - Easy to bundle and deploy with the CLI tool, no external dependencies.  
  - Supports encryption extensions (e.g., SQLCipher) for securing stored keys locally.

- **Schema essentials:**  
  - Tables for projects, third-party API keys (encrypted), unified keys, audit logs (timestamped).  
  - Index on project ID and key usage for efficient lookup.

- **Tradeoffs:**  
  - Not suitable for multi-user concurrent access or distributed setups—acceptable for MVP local use.  
  - Limited scalability; future cloud or team-shared versions should migrate to PostgreSQL or Vault integrations.  
  - Encryption must be handled carefully at app layer or via SQLCipher to protect keys at rest.

**Action:**  
Start with SQLite + SQLCipher for local encrypted storage. Design schema for easy export/import to enable future cloud sync or team collaboration. This keeps the POC minimal, secure, and deployable without external services.
- Infra Engineer: **Deployment Shape for Unified API Key Gateway**

1. **AWS Infrastructure:**
   - Use **AWS Lambda** (Node.js/Python) for the proxy API layer to minimize server management.
   - Store third-party API keys securely in **AWS Secrets Manager** with fine-grained IAM roles.
   - Use **API Gateway** to expose a single unified API key endpoint per project.
   - Enable **CloudWatch Logs** for audit trails and monitoring.
   - Use **DynamoDB** for metadata (projects, keys, usage logs).

2. **Vercel Frontend:**
   - Host the dashboard/UI on Vercel for fast iteration and developer experience.
   - Integrate with AWS API Gateway via environment variables.
   - Use serverless functions on Vercel for lightweight CLI onboarding bot integration (Slack).

3. **Terraform:**
   - Define all AWS resources (Lambda, API Gateway, Secrets Manager, DynamoDB, IAM) in Terraform for reproducible infrastructure.
   - Use Terraform workspaces or modules per project for isolation.

**Tradeoffs:**
- **Security:** Centralizing keys improves rotation and audit but creates a single point of failure; mitigate with strict IAM and encryption.
- **Cost:** Lambda + API Gateway is cost-effective at low scale but may increase with heavy usage; DynamoDB scales well.
- **Complexity:** Terraform adds initial setup overhead but ensures consistent environments.
- **Speed:** Vercel accelerates frontend deployment; AWS Lambda enables rapid backend iteration without servers.

**Actionables:**
- Prototype Lambda proxy + API Gateway + Secrets Manager with Terraform.
- Deploy minimal Vercel frontend with Slack onboarding bot.
- Implement audit logging and key rotation workflows.
- Validate security posture with IAM least privilege and encryption.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions for CI/CD pipelines.
- On PR: run lint, unit tests, and security scans (e.g., secret scanning, dependency checks).
- On merge to main: trigger integration tests and build artifacts.
- Use branch protection rules requiring passing checks before merge.
- Automate changelog generation from commit messages (Conventional Commits).
- Add a manual approval step before deployment to production.

Deployment Notes:
- Deploy CLI-first, local-first POC as a Docker container or standalone binary.
- Use GitHub Releases for versioned artifacts.
- Deployment to a staging environment for integration testing.
- Document environment variables and secrets management (local file-backed for POC).
- Include rollback instructions and monitoring hooks for proxy uptime and error rates.

Tradeoffs:
- Avoid external paid services to keep POC lightweight and fast.
- Local-first approach limits scalability but accelerates MVP delivery.
- Proxying keys improves security but introduces a single point of failure; mitigate with strict access controls and audit logs.
- Manual approval balances speed and risk for initial deployments.

Actionables:
1. Define GitHub Actions workflows for lint, test, security scan, and deploy.
2. Configure branch protections requiring checks.
3. Prepare deployment scripts for local Docker/CLI usage.
4. Write deployment and rollback docs emphasizing security and auditability.
- OpenSpec Writer: Implementation Requirements:
1. **Unified API Key Proxy Service**: Build a local-first, CLI-driven proxy that accepts one unified API key per project and routes requests to third-party APIs using stored keys. Store keys encrypted in a local file with strict access controls.
2. **Key Provisioning & Rotation**: Enable centralized key provisioning, rotation, and revocation without redeploying client apps. Support fine-grained per-tool permissions.
3. **Audit Logging**: Log all API key usage and provisioning events locally, exportable for compliance.
4. **Security Controls**: Harden proxy against privilege escalation and leaks. Use zero-trust principles: never expose raw third-party keys to clients.
5. **Onboarding UX**: Provide a Slack onboarding bot and CLI commands to add new third-party APIs with one click.
6. **Free Tier Limits**: Limit free tier to 3 APIs/project; paid plans unlock advanced audit and team features.

Acceptance Criteria:
- Proxy correctly routes requests using unified key and third-party keys.
- Rotation/revocation of keys applies immediately without client changes.
- Audit logs capture all key usage events.
- Slack bot successfully provisions new API keys in under 2 minutes.
- Security tests confirm no raw key exposure or privilege escalation.
- CLI-first, local-first workflow runs without external dependencies or paid services.

Tradeoffs:
- Local-first limits multi-user real-time sync; prioritize MVP speed and security.
- Avoid external paid services initially to reduce complexity and risk.
- CLI-first may reduce initial UX polish but accelerates proof-of-concept delivery.
