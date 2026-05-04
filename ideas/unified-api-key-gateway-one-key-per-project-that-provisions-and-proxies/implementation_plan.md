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
- Product Planner: MVP Workflow for Unified API Key Gateway (CLI-first, local-only, file-backed):

1. **Project Initialization (CLI command)**  
   - `ukg init <project-name>` creates a local project folder with a config file (YAML/JSON) storing unified key metadata and third-party API key placeholders.  
   - Tradeoff: No cloud sync yet; limits collaboration but accelerates dev and trust.

2. **Add Third-Party API Keys**  
   - `ukg add <api-name> --key <test-key>` stores encrypted keys locally in the config file.  
   - Tradeoff: Local encryption only; no multi-user access or vault integration yet.

3. **Generate Unified Project Key**  
   - `ukg generate-key` creates a single unified API key (UUID or JWT) representing the project.  
   - Tradeoff: Simple token, no advanced auth or rotation policies initially.

4. **Proxy Server (local dev mode)**  
   - `ukg proxy start` spins up a local HTTP proxy that accepts unified key requests, routes them to the correct third-party API using stored keys, and returns responses.  
   - Tradeoff: Local-only proxy; no cloud deployment or scaling yet.

5. **Key Rotation & Onboarding**  
   - `ukg rotate <api-name>` updates stored keys and reloads proxy config.  
   - Onboarding new APIs is `ukg add` + config update.  
   - Tradeoff: Manual CLI commands; no UI or automation yet.

**Implementation Notes:**  
- No external dependencies or paid services.  
- Use simple file encryption (e.g., libsodium).  
- Focus on minimal, runnable demo within 1 week.  
- Prioritize clear README and onboarding Slack bot script for early adopters.

This MVP proves core value: one project key manages multiple APIs locally, enabling fast onboarding and rotation without cloud risk or complex infra.
- POC Coder: POC Plan: CLI-first local unified API key gateway (under 1 week)

**Scope:**  
- CLI tool managing a single “project key” (a local token) that maps to multiple third-party API keys stored encrypted in a local file (e.g., JSON + AES).  
- Proxy server (local-only) that accepts requests authenticated by the project key, routes them to configured third-party APIs with their real keys, and returns responses.  
- Basic CLI commands: `init` (create project key + storage), `add-api` (register third-party API key), `proxy` (start local proxy), `rotate` (replace a third-party key).  
- No cloud, no external dependencies, no user accounts.  

**Tradeoffs:**  
- No multi-user/team sync or cloud storage (to avoid complexity and trust issues).  
- Limited to local dev environment; no production deployment yet.  
- Minimal security: local encryption only, no audit logs or RBAC.  
- Supports only a few API types (e.g., REST JSON) to keep proxy simple.  

**Deliverables:**  
- CLI binary (Node.js or Go) + local encrypted JSON file for keys.  
- Local HTTP proxy forwarding requests with injected real API keys.  
- README with usage and demo script.  

This POC proves the core value: one project key to manage and proxy multiple API keys locally, enabling easy onboarding and rotation without external services or security overhead.
- Frontend Engineer: POC Interface Plan for Unified API Key Gateway (CLI-first, Local-only)

1. CLI Commands:
- `init [project-name]`: Create local project folder with config file (YAML/JSON) storing unified API key metadata.
- `add-tool [tool-name] [tool-api-key]`: Register a third-party API key under the project, encrypted locally.
- `list-tools`: Show all registered tools and their masked keys.
- `rotate [tool-name]`: Simulate key rotation by updating the stored key (mocked for POC).
- `proxy [tool-name] [API-endpoint] [--payload]`: Proxy a request through the unified key gateway locally, logging the request/response.

2. File-backed Storage:
- Store all data in a local `.unified-api-gateway/` folder inside the project directory.
- Use encrypted JSON/YAML files to hold keys and config.

3. UX Tradeoffs:
- No UI for now; CLI only to maximize speed and focus on core flows.
- No real external API calls; proxy simulates request/response to avoid dependencies.
- No user auth or multi-user support yet; single-user local dev scenario only.

4. Actionables:
- Build CLI with Node.js + commander.js or Python + Click.
- Implement local encrypted config file read/write.
- Mock proxy requests with logs to stdout.
- Prepare README with usage examples for quick testing.

This minimal interface proves the core value: unified key management + proxying with one project key, locally and safely, enabling rapid iteration and early feedback.
- Backend Engineer: POC API Design & Local Persistence:

1. API Endpoints (local CLI + proxy server):
- POST /project/create  
  Input: { project_name }  
  Output: { unified_project_key }  
  Purpose: create a new project with a single unified key.

- POST /project/{id}/keys/add  
  Input: { tool_name, third_party_api_key }  
  Output: { success }  
  Purpose: add a third-party API key under the project.

- GET /project/{id}/keys  
  Output: { tool_name: masked_key }  
  Purpose: list all keys in the project (mask keys for safety).

- POST /proxy/{unified_project_key}/{tool_name}/request  
  Input: { method, path, headers, body }  
  Output: proxied third-party API response  
  Purpose: proxy requests through unified key, injecting correct third-party key.

2. Local Persistence:
- File-backed JSON store per project, e.g., ~/.uapigateway/projects/{project_id}.json  
- Store unified_project_key, tool keys (encrypted with local symmetric key), metadata.  
- CLI reads/writes this file; proxy server loads keys at startup.

3. Tradeoffs:
- Local file persistence avoids cloud dependencies and security risks but limits multi-user sync and backup.  
- Proxy server is minimal, stateless except for in-memory cache of keys; no external DB.  
- No user auth in POC to reduce complexity; assumes local trust.  
- CLI-first approach enables quick iteration and demo without UI overhead.

Action: Build CLI commands to create projects, add keys, list keys, and start proxy server reading local files. Implement proxy endpoint to rewrite requests with correct keys. Keep code modular for later extension to multi-user and cloud storage.
- Auth Engineer: For the local POC, adopt a **CLI-first, local-only, file-backed auth posture**:

- Generate one unified project API key locally (e.g., a UUID or JWT signed with a local key).
- Store all third-party API keys encrypted in local files (e.g., JSON with AES encryption).
- Proxy requests locally, injecting appropriate third-party keys per API call.
- No external dependencies or cloud services; no user secrets leave the machine.
- Use ephemeral test keys or sandbox credentials only.
- Provide CLI commands for key rotation, onboarding new APIs, and exporting artifacts for handoff.

**Tradeoffs:**
- + Fast to build, minimal security risk, easy to demo onboarding and rotation flows.
- – No multi-user sync or centralized revocation; not production-ready for team scale.
- – Limited audit/logging and no hardened access controls.

For production handoff, plan to evolve into a **centralized, zero-trust API key gateway service**:

- Store keys encrypted at rest in a hardened vault (e.g., HashiCorp Vault or AWS KMS).
- Authenticate clients via OAuth2 or mTLS, issuing scoped tokens per project.
- Proxy API calls with fine-grained access control, audit logging, and rotation APIs.
- Integrate with existing secret managers to reduce switching friction.
- Provide a web dashboard and CLI for team management.

**Tradeoffs:**
- + Enterprise-grade security, compliance, and team collaboration.
- – Higher complexity, longer build time, and requires trust in hosted service.
- – Potential onboarding friction; mitigate with free tier and Slack bot.

**Action:** Build the local CLI POC in <1 week to validate core UX and value. Use it to gather early adopter feedback before investing in production-grade centralized gateway.
- Database Engineer: For the POC of the unified API key gateway, choose a local, file-backed embedded database to maximize simplicity, speed, and developer trust:

**Recommended DB:** SQLite (v3+)
- **Why:** Zero-config, serverless, file-based, ACID-compliant, widely supported, and embeddable in CLI tools.
- **Tradeoffs:** Limited concurrency (fine for single-user CLI POC), no built-in encryption (encrypt files externally if needed).
- **Schema:** Store projects, unified keys, and mappings to third-party API keys in normalized tables.
- **Deployment:** Bundled with CLI; no external dependencies or services.
- **Security:** Keep DB file local and encrypted at rest if possible; no network exposure.
- **Extensibility:** Easy to migrate to client-server DB later (Postgres, MySQL) if scaling needed.

**Alternative:** JSON/YAML file storage for ultra-minimalism, but lacks ACID guarantees and query power.

**Action:** Implement SQLite schema and CLI integration this sprint. Focus on local-first, file-backed persistence to prove core flows without cloud or paid services.
- Infra Engineer: Deploy a minimal, local-first POC on developer machines using Terraform + AWS + Vercel as follows:

1. **Terraform**: Define AWS infrastructure for a lightweight API proxy layer:
   - API Gateway with Lambda proxy integration to route unified keys to third-party APIs.
   - DynamoDB table for key mapping and rotation metadata.
   - IAM roles scoped narrowly to Lambda and DynamoDB.
   - Use Terraform Cloud or local CLI for infra provisioning, enabling repeatable, versioned deployments.

2. **AWS Lambda**: Implement proxy logic in Node.js or Python:
   - Validate unified project key.
   - Lookup and inject third-party API keys from DynamoDB.
   - Forward requests, handle retries, and log usage metrics.

3. **Vercel**: Host a minimal frontend/dashboard and CLI onboarding bot:
   - CLI-first onboarding to generate unified keys and configure local files.
   - Slack bot integration for onboarding and notifications.
   - Frontend for key rotation and usage visualization.

**Tradeoffs**:
- Local-first avoids early trust/security concerns but limits multi-user concurrency.
- AWS Lambda + API Gateway adds cost and complexity but ensures scalability and security isolation.
- Vercel simplifies frontend deployment but adds external dependency; can be replaced with local UI later.
- Terraform ensures infra reproducibility but requires initial learning curve.

**Action**: Build POC infra with Terraform + AWS Lambda; deploy onboarding bot and dashboard on Vercel; test with seed-stage SaaS dev teams.
- DevOps Engineer: GitHub Automation & Checks:
- Use GitHub Actions to run on PRs and main branch pushes.
- Checks:
  - Linting and formatting (e.g., ESLint, Prettier) to ensure code quality.
  - Unit and integration tests for CLI and local file-backed logic.
  - Security scan (e.g., CodeQL) focusing on credential handling code.
  - Build and artifact generation for CLI binaries.
- Automate semantic versioning and changelog generation on merges.

Deployment Notes:
- POC is CLI-first, local-only, file-backed — no cloud deployment needed.
- Release artifacts as GitHub Releases for easy download.
- Document setup: install CLI, generate unified key locally, configure proxy.
- Emphasize sandbox/test keys only to avoid trust/switching friction.
- Plan next steps: add Slack onboarding bot and free tier after POC validation.

Tradeoffs:
- Local-first avoids cloud risk but limits multi-user collaboration and real-time proxying.
- No external services means faster MVP but defers scalability and SaaS integration.
- Security scans focus on code, but real-world trust requires future audits and compliance.

Action:
- Define GitHub Actions workflows with above checks.
- Prepare release pipeline for CLI artifacts.
- Write deployment and onboarding docs targeting seed-stage SaaS devs.
- Schedule feedback sessions post-POC release to validate assumptions.
- OpenSpec Writer: Implementation Requirements for Unified API Key Gateway POC:

1. CLI-first, local-only tool that runs without external dependencies or paid services.
2. File-backed storage of project metadata, unified API key, and proxied third-party API keys.
3. Single unified API key per project that internally maps to multiple third-party API keys.
4. Proxy server that routes requests from unified key to correct third-party APIs, handling authentication.
5. Support key rotation and onboarding of new APIs with one CLI command.
6. Sandbox/test mode only—no production keys or cloud deployment.
7. Generate artifacts (config files, logs) readable by other agent crews.
8. Minimal UI: CLI prompts and Slack onboarding bot for demo.
9. Security: local encryption of stored keys; no network calls except proxying.
10. Demo scenario: onboard 3 APIs, rotate keys, proxy calls with unified key.

Acceptance Checks:

- Can onboard a new API key and proxy requests using the unified key locally.
- Key rotation updates all relevant mappings without downtime.
- CLI commands complete within seconds, with clear user feedback.
- Artifacts generated are valid and consumable by downstream tools.
- Slack bot triggers onboarding flow and confirms success.
- No external network calls except proxied API requests.
- Runs on dev machines without special setup or paid accounts.

Tradeoffs:

- No cloud deployment limits scalability but reduces security/compliance risk.
- Local-only approach may not reflect multi-user team workflows but accelerates POC.
- Sandbox keys avoid trust issues but limit real-world testing.

Next step: build minimal CLI + proxy server + Slack bot within 1 week to validate core hypothesis.
