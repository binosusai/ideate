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
- Product Planner: Develop a CLI-based MVP that:

1. Reads a project configuration file listing third-party API keys.
2. Generates a single project-specific API key (mocked for MVP).
3. Proxies requests to third-party APIs, attaching the unified key.
4. Stores keys and proxy configs locally in a file-backed database (e.g., SQLite).

**Implementation details:**
- Use Node.js or Python for rapid development.
- Focus on core flow: key provisioning, request proxying, local storage.
- Keep the CLI simple: commands for setup, add keys, proxy requests.

**Tradeoffs:**
- No real API key provisioning with external services—mocked for MVP.
- Limited security features; focus on proof of concept.
- Local-only; no cloud deployment or external integrations initially.

This approach ensures rapid validation, minimal dependencies, and clear demonstration of workflow benefits.
- POC Coder: Develop a CLI tool in Python that:

1. Reads a YAML/JSON config with third-party API keys.
2. Generates a mock unified project key.
3. Proxies HTTP requests, attaching the unified key.
4. Stores keys and configs in a local SQLite database.

**Implementation steps:**
- Use `click` for CLI commands.
- Use `sqlite3` for local storage.
- Use `requests` to proxy API calls.
- Mock key generation (e.g., UUID).

**Tradeoffs:**
- No real API key provisioning; just simulation.
- Local-only, no external auth/security.
- Focused on core flow, not production security or scalability.

This minimal setup validates the concept within hours, demonstrating key management and proxying benefits.
- Frontend Engineer: Implement a CLI in Python with three commands: `init` (creates config and local DB), `add` (stores third-party API keys), and `proxy` (forwards requests with unified key). Use `click` for CLI, `sqlite3` for local storage, and `requests` for proxying. Generate mock project keys with UUIDs. Store API keys and configs in SQLite, ensuring easy future expansion. Keep security minimal—focus on proof of concept. Tradeoffs include local-only operation, no real key provisioning, and limited security. This approach ensures rapid, actionable validation within hours, emphasizing core workflow benefits and setting the foundation for future enhancements.
- Backend Engineer: Implement a CLI in Python using `click` with three commands: `init` (create local SQLite DB and config), `add` (store third-party API keys), and `proxy` (forward requests attaching a mock unified key). Use `uuid` for generating project keys and `requests` for proxying API calls. Store all credentials and configs locally for quick iteration. Focus on core functionality—mock key provisioning, local storage, and request proxying—without external dependencies or security features. Tradeoffs: local-only operation, no real API key provisioning, limited security, and no cloud deployment. This setup enables rapid validation of workflow benefits and can be extended later with real key management and security enhancements.
- Auth Engineer: For local POC, implement a CLI in Python using `click`, `sqlite3`, and `requests`. Commands: `init` (setup local DB/config), `add` (store third-party keys), `proxy` (forward requests with a mock unified key). Generate project keys with `uuid`. Store credentials locally, focusing on core provisioning and proxying. Keep security minimal—no external services or real key provisioning—to ensure rapid validation. 

Tradeoffs:
- Local-only, no external key management or security.
- Mocked API keys, limited scalability.
- No cloud deployment initially.

For production, transition to a secure, cloud-based solution:
- Use Vault or AWS Secrets Manager for real key provisioning.
- Implement OAuth/OIDC for user authentication.
- Enforce RBAC and audit logging.
- Use API gateways with rate limiting and security policies.

This staged approach balances rapid proof of concept with scalable, secure future deployment.
- Database Engineer: Deploy a local SQLite database to store API keys and configs, ensuring portability and ease of setup. Use a simple schema: `projects(id, name, unified_key)` and `api_keys(id, project_id, service_name, key)`. Defaults: initialize with `init` command, creating schema and empty tables. Tradeoffs include limited security—local storage without encryption—and no external key management. For production, replace with managed secrets (e.g., Vault) and secure access controls. This setup balances rapid deployment and future scalability, enabling quick validation while maintaining explicit, actionable steps.
- Infra Engineer: Stage: Planning

Deploy a serverless architecture using AWS API Gateway + Lambda for proxying, with Terraform managing infrastructure. Use Vercel for frontend (if needed). Store API keys securely in AWS Secrets Manager, with Lambda fetching keys dynamically. Implement a Lambda function that, upon receiving a request, retrieves the project’s unified key from Secrets Manager, proxies the request to third-party APIs, and attaches the key.

**Tradeoffs:**
- Pros: Scalable, secure, minimal management overhead.
- Cons: Slightly higher latency, initial complexity in secret management, and potential cost at scale.

**Action steps:**
1. Define Terraform modules for API Gateway, Lambda, Secrets Manager.
2. Develop Lambda in Python/Node.js to handle key retrieval and request proxying.
3. Use Vercel for a minimal frontend if needed.
4. Integrate CI/CD for deployment.
5. Validate with mock API keys before production rollout.

This setup balances rapid deployment, security, and scalability.
- DevOps Engineer: Implement a GitHub Actions workflow triggered on pull requests and main merges. Incorporate checks:  
- **Linting** (e.g., `flake8` or `eslint`) for code quality.  
- **Unit tests** with coverage reports.  
- **Security scans** (e.g., `bandit`, `snyk`) for dependencies and secrets.  
- **Build validation** for CLI tools and proxy functions.  

Deploy notes:  
- Use Terraform for infrastructure provisioning (API Gateway, Lambda, Secrets Manager).  
- Store API keys securely in Secrets Manager, fetched dynamically at runtime.  
- Use GitHub Secrets for deployment credentials.  

Tradeoffs:  
- CI/CD complexity increases; requires maintenance.  
- External secrets management adds latency but enhances security.  
- Focus on automated validation to prevent insecure or broken code from merging.  

This ensures rapid, reliable validation and secure deployment readiness.
- OpenSpec Writer: Implement a CLI-based MVP in Python using `click`, `sqlite3`, and `requests`. Core steps:  
1. `init` command creates a local SQLite database with tables for projects and API keys.  
2. `add` command stores third-party API keys linked to a project.  
3. `proxy` command forwards requests to third-party APIs, attaching a mock unified key generated via `uuid`.  

**Implementation details:**  
- Use `uuid` for mock key generation.  
- Store configs and keys locally for quick iteration.  
- Proxy requests with `requests`, attaching the unified key in headers or params.  

**Tradeoffs:**  
- No real API key provisioning or external security; purely local and mocked.  
- Limited security features; focus on validating workflow benefits.  
- No cloud deployment initially; easy to extend later.  

This setup ensures rapid, actionable validation within hours, demonstrating key management and proxying benefits.
