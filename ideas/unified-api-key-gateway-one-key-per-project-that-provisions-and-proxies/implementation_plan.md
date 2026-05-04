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
- Product Planner: MVP Workflow for Unified API Key Gateway (CLI-first, file-backed, local-only):

1. **Project Initialization:** User runs `uakg init` CLI command to create a local project folder with a config file (e.g., `uakg.yaml`) storing unified API key metadata.

2. **Unified Key Generation:** CLI generates a single project-level API key (UUID or JWT) stored locally, representing the unified gateway key.

3. **Third-Party API Key Registration:** User runs `uakg add --tool <tool_name> --key <api_key>` to register third-party keys. CLI stores encrypted keys in the config file.

4. **Proxy Simulation:** CLI provides a local proxy command `uakg proxy --tool <tool_name> --request <req_file>` that reads the unified key, maps it to the correct third-party key, and simulates forwarding the request (mock response).

5. **Key Rotation:** `uakg rotate --tool <tool_name>` rotates the stored third-party key (simulated) and updates config.

6. **Export Artifacts:** CLI exports config and key mapping files for downstream automation or integration.

**Tradeoffs:**
- No real network proxy or backend—only local simulation to avoid paid services and complexity.
- No multi-user or cloud sync; MVP targets single dev local usage.
- Security is minimal (local encryption only), acceptable for POC.
- Focus on UX flow proving “one key per project” concept and onboarding speed.

Deliverables: CLI tool repo + README with usage steps + demo scripts for design partners.
- POC Coder: POC Plan: CLI-first, local-only unified API key gateway

**Goal:** Prove “one key per project” can proxy multiple third-party APIs with minimal setup, no external services.

**Scope:**
- CLI tool managing a local YAML/JSON file storing multiple API keys per project.
- Single “unified key” (a generated token) that proxies requests to configured APIs.
- Proxy implemented as a local HTTP server that:
  - Authenticates incoming requests using the unified key.
  - Routes requests to the correct third-party API with stored keys.
- Support 2–3 example APIs (e.g., GitHub, Stripe, Slack) with minimal request forwarding logic.
- No persistence beyond local files; no user accounts or cloud deployment.
- Use test/sandbox API keys to avoid security risks.

**Tradeoffs:**
- No multi-user or team features yet (focus on solo dev proof).
- Local-only means no real networked onboarding, but fast iteration and zero infra cost.
- Limited API coverage but enough to demonstrate concept and developer UX.
- No advanced security (e.g., encryption) initially; store keys in plaintext for speed.

**Deliverables:**
- CLI commands: init project, add API keys, start proxy server.
- Proxy server logs and forwards requests with unified key auth.
- README with usage and demo scripts.

This POC can be built in <1 week, requires no paid services, and directly validates the core hypothesis.
- Frontend Engineer: POC Interface: CLI-first, local-only, file-backed

1. CLI commands:
- `keygate init [project-name]`  
  Creates a local project folder with config file (YAML/JSON) storing unified API key metadata.
- `keygate add-tool [tool-name] --api-key [key]`  
  Adds a third-party API key, encrypted locally, linked to the unified project key.
- `keygate list-tools`  
  Lists integrated tools with masked keys.
- `keygate proxy [tool-name] --endpoint [api-path] --method [GET/POST] --data [payload]`  
  Proxies API requests through the unified key gateway locally.
- `keygate rotate [tool-name]`  
  Simulates key rotation by replacing stored key.

2. File structure:
- `.keygate/` folder per project, containing encrypted keys and config.
- Local JSON/YAML config for metadata and tooling.

Tradeoffs:
- No UI initially reduces dev effort and accelerates feedback cycle.
- Local-only avoids security risks but limits multi-user collaboration.
- File-backed storage is simple but not scalable; future cloud sync needed.
- Proxy runs locally, no external deployment or paid infra required.

Action:
- Implement CLI parser + local file encryption.
- Mock proxy behavior for one or two popular tools (e.g., GitHub, Stripe).
- Prepare demo script showing single-key onboarding and proxy usage in <1 week.
- Backend Engineer: API Definition for POC (CLI-first, local-only, file-backed):

1. **Project API Key Creation**
- POST /projects
- Input: { project_name }
- Output: { unified_api_key }
- Purpose: Generate a single unified API key per project (UUID or JWT).
- Tradeoff: Simple in-memory or file-backed mapping; no external auth.

2. **API Key Provisioning**
- POST /projects/{project_id}/keys
- Input: { tool_name, tool_api_key }
- Output: { success }
- Purpose: Store third-party API keys locally, encrypted in project config file.
- Tradeoff: Local encryption (e.g., AES) with user-provided passphrase; no cloud vault.

3. **Proxy Request**
- POST /proxy
- Headers: { Authorization: unified_api_key }
- Body: { tool_name, endpoint, method, payload }
- Output: Proxy response from third-party API.
- Purpose: Proxy calls to third-party APIs using stored keys.
- Tradeoff: Simple HTTP proxy with minimal transformation; no rate limiting or caching.

Local Persistence:
- Store per-project config as encrypted JSON file (e.g., ~/.unified-api/{project_id}.json).
- Fields: unified_api_key, encrypted tool keys, metadata.
- Tradeoff: File-based persistence ensures zero external dependencies but limits multi-user sync and audit.

Actionables:
- Implement CLI commands for project create, key add, and proxy call.
- Use standard encryption libs for local key storage.
- Keep API minimal; focus on core flow to prove “one key per project” concept.
- Avoid external services to reduce risk and speed delivery.

This approach balances MVP speed, security, and demo value while minimizing complexity and cost.
- Auth Engineer: **Auth Posture Recommendation**

**Local POC:**  
- Use a **CLI-first, file-backed, local-only auth model** with a single unified API key per project stored encrypted in a local config file (e.g., JSON/YAML encrypted with a user passphrase).  
- Proxy all third-party API calls through this local gateway using the unified key.  
- No external dependencies or paid services; no user accounts or network auth.  
- Tradeoffs: Minimal security scope (local only), no multi-user support, no audit logs. Fast iteration, zero infra risk, and easy handoff.

**Production Handoff:**  
- Migrate to a **centralized API key gateway service** with:  
  - Per-project API keys issued and managed via a secure backend (e.g., OAuth2 client credentials or JWTs).  
  - Encrypted secrets vault (e.g., HashiCorp Vault or AWS Secrets Manager) for third-party keys.  
  - Role-based access control (RBAC) and audit logging for compliance.  
  - Proxy requests with strict rate limiting and monitoring.  
- Tradeoffs: Higher complexity, requires infra and security ops, but enables team onboarding, rotation, and compliance.

**Action:**  
Start with local CLI POC to validate UX and core proxy logic. Design config and API key formats for smooth migration to centralized service. Document clear upgrade path from local file to vault-backed multi-tenant service.
- Database Engineer: For the local-first, CLI-driven POC of the unified API key gateway, choose SQLite as the default database:

- **Why SQLite?**  
  - Zero-config, file-backed, no server needed — aligns perfectly with local-first and file-backed goals.  
  - ACID-compliant, reliable storage for API key metadata and proxy configs.  
  - Cross-platform support ensures easy onboarding for devs on any OS.  
  - Lightweight and fast for small-to-medium datasets typical in early-stage projects.

- **Tradeoffs:**  
  - Not suitable for multi-user concurrent access or scaling beyond a single machine (acceptable for MVP).  
  - No built-in encryption; sensitive keys should be encrypted at the application layer or stored encrypted in the DB file.  
  - Limited advanced querying and analytics, but sufficient for proof-of-concept.

- **Implementation details:**  
  - Store API keys and project metadata in a single `.db` file within the project directory.  
  - Use a simple schema: Projects, API Keys, and Proxy Config tables.  
  - Provide CLI commands to add, rotate, and revoke keys, updating SQLite accordingly.  
  - Encrypt sensitive fields before insertion (e.g., AES-GCM with a local passphrase).

This approach enables a fast, secure, and deployable MVP without external dependencies or paid services.
- Infra Engineer: Deploy a minimal viable unified API key gateway as follows:

1. **AWS Infrastructure**  
- Use AWS Lambda (Node.js) behind API Gateway for proxying third-party API calls.  
- Store encrypted API keys in AWS Secrets Manager per project.  
- Use DynamoDB for metadata (project, user, key mappings).  
- Deploy with Terraform for repeatability and version control.

2. **Vercel Frontend**  
- Host a React-based dashboard on Vercel for key management and onboarding.  
- Integrate Slack onboarding bot via serverless functions (Vercel Edge Functions or AWS Lambda).

3. **Terraform Deployment Shape**  
- Modularize: separate modules for Lambda/API Gateway, Secrets Manager, DynamoDB, IAM roles.  
- Use Terraform workspaces for dev/staging/prod environments.  
- Automate CI/CD pipeline with GitHub Actions deploying Terraform and Vercel.

**Tradeoffs:**  
- AWS Secrets Manager adds cost but ensures secure key storage and rotation.  
- Lambda/API Gateway adds latency vs direct calls but centralizes proxy logic and auditing.  
- Vercel frontend separates UI concerns but requires cross-cloud integration.  
- Terraform complexity upfront accelerates iteration and rollback but requires initial investment.

This shape balances security, speed-to-market, and scalability for a POC targeting integration-heavy SaaS startups.
- DevOps Engineer: **GitHub Automation & Checks:**

- **CI Workflow:** On PRs and pushes to main, run:
  - Linting and static analysis on CLI codebase (e.g., ESLint, Go vet).
  - Unit tests for key provisioning and proxy logic.
  - Security scan (e.g., GitHub CodeQL) to catch secrets or vulnerabilities early.
- **Pre-merge Checks:** Require passing CI, no secrets in code, and updated changelog.
- **Branch Protection:** Enforce PR reviews (2+ reviewers) and signed commits.

**Deployment Notes:**

- MVP is CLI-first, local-only, file-backed; no external deployment initially.
- Deployment automation deferred until after POC validation.
- Document manual release steps: tagging, changelog update, GitHub release creation.
- Use semantic versioning for CLI artifacts.
- Store test keys and config in encrypted GitHub secrets for CI tests only.

**Tradeoffs:**

- No automated deployment reduces risk and complexity but delays user feedback on hosted service.
- Local-first approach limits immediate integration testing but accelerates MVP delivery.
- Security scans in CI mitigate risk of leaking keys in codebase early.

**Actionables:**

1. Define GitHub Actions workflow with lint, test, and security scan jobs.
2. Configure branch protection rules.
3. Write deployment README for manual CLI release.
4. Store test credentials securely in GitHub secrets.
5. Schedule demo after 1 week to validate POC.
- OpenSpec Writer: Implementation Requirements:
1. CLI-first, local-only prototype that manages a single unified API key per project.
2. File-backed storage of API key mappings (project key → third-party keys) in a human-readable format (e.g., YAML/JSON).
3. Proxy layer that intercepts API calls authenticated with the unified key and forwards them with the correct third-party key.
4. Support for provisioning and rotating keys locally without external dependencies or paid services.
5. Minimal UI: CLI commands for onboarding new third-party APIs, listing keys, and rotating keys.
6. Logging of proxy requests for audit and debugging.
7. Test mode with dummy API keys to avoid sensitive data exposure.

Acceptance Criteria:
- A developer can create a project key and link at least 3 third-party API keys locally.
- API calls using the unified key are correctly proxied to the third-party APIs with appropriate credentials.
- The system runs fully offline without external services.
- CLI commands complete within seconds and produce readable config files.
- Logs demonstrate correct request routing and key usage.
- Prototype can be delivered within one week.

Tradeoffs:
- Local-only limits immediate multi-user/team collaboration but accelerates MVP delivery and reduces risk.
- File-backed storage sacrifices scalability for simplicity and transparency.
- No paid services or external deployment reduces complexity but defers cloud-based multi-tenant features.

Next Steps:
- Define CLI commands and config schema.
- Build proxy and key mapping logic.
- Prepare test suite with dummy keys.
- Demo to design partners for feedback.
