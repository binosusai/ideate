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
- Product Planner: Develop a CLI-based MVP that generates a single project key, proxies API calls, and stores credentials in local files (e.g., JSON or YAML). Key steps:

1. **Design architecture**: Local CLI app, file-backed storage, simple proxy server.
2. **Implement core features**:
   - Generate a unified project key.
   - Store third-party API keys securely in local files.
   - Proxy API requests, injecting appropriate keys.
3. **Validation**:
   - Test with 2-3 common API integrations (e.g., Stripe, Slack).
   - Measure setup time and error reduction.
4. **Tradeoffs**:
   - *Pros*: Fast to build, no external dependencies, easy to iterate.
   - *Cons*: Limited security (local storage), no multi-user support, not scalable.

This approach ensures rapid proof of concept, aligns with the "local-first" builder directive, and minimizes external dependencies. Future iterations can add cloud sync, multi-user support, and enhanced security.
- POC Coder: Implement a CLI tool in Python with these steps:

1. **Generate a project key**: create a UUID as the project identifier.
2. **Store API keys locally**: save third-party keys in a JSON file, encrypted with a simple symmetric key (e.g., Fernet).
3. **Proxy requests**: use `http.server` with a custom handler to intercept API calls, inject stored keys, and forward requests.
4. **Validation**: test with sample APIs like Slack or Stripe by configuring keys and making sample requests.
5. **Tradeoffs**:
   - *Pros*: Rapid, no external dependencies, easy to demo.
   - *Cons*: Local-only security, no multi-user support, limited scalability.
   
This minimal setup demonstrates core functionality within hours, validating the concept before considering scalable or cloud solutions.
- Frontend Engineer: Implement a CLI-first, local-file-backed MVP with these features:

1. Generate a UUID project key.
2. Store API keys in an encrypted JSON file (Fernet).
3. Proxy server (using Python `http.server`) intercepts requests, injects API keys, and forwards.
4. Command-line commands:
   - `init`: create project and keys.
   - `set`: add/update API keys.
   - `proxy`: run local proxy server.
5. Validation:
   - Test with sample API requests (Slack, Stripe).
   
**Tradeoffs:**
- *Pros*: Fast, no external dependencies, easy to demonstrate core value.
- *Cons*: Local-only security, no multi-user support, limited scalability.

This approach ensures rapid iteration, proof of concept, and validation within hours, aligning with the goal to reduce onboarding friction and demonstrate tangible benefits early.
- Backend Engineer: Implement a CLI tool in Python with these core features:

1. Generate a UUID as the project key (`init` command).
2. Store third-party API keys in an encrypted local JSON file (using Fernet).
3. Proxy API requests via a lightweight HTTP server (`proxy` command), injecting stored keys.
4. Commands for managing keys (`set`, `get`).

**Tradeoffs:**
- *Pros*: Fast, minimal dependencies, easy to iterate, no external services.
- *Cons*: Local-only security (encrypted at rest), no multi-user support, limited scalability.

**Implementation considerations:**
- Use `argparse` for CLI.
- Use `cryptography` for encryption.
- Use `http.server` with custom handler for proxying.
- Validation with sample APIs (Slack, Stripe).

This setup delivers a working proof of concept within hours, validating the core idea before scaling or adding features.
- Auth Engineer: For local POC, implement a CLI-based, file-backed system using Python. Generate a UUID project key, store API keys encrypted with Fernet in a JSON file, and run a lightweight proxy server with `http.server` that injects keys into requests. Keep scope minimal: no multi-user support, local-only security, and no external dependencies beyond `cryptography`. 

**Tradeoffs:**  
- *Pros:* Rapid development, easy to validate core functionality, no external services needed.  
- *Cons:* Limited security (local storage), scalability, and multi-user support.

**Action steps:**  
1. Develop CLI commands: `init`, `set`, `proxy`.  
2. Encrypt/decrypt API keys at rest.  
3. Proxy API requests, injecting keys based on project config.  
4. Validate with sample APIs (Stripe, Slack).  

For production, plan to add multi-user support, cloud storage, and enhanced security, but keep initial scope simple for quick validation.
- Database Engineer: Implement a local, deployable database using SQLite with the following defaults:

1. **Schema**: Tables for `projects` (UUID, name), `api_keys` (project_id, service_name, encrypted_key), and `config` (key-value pairs).
2. **Encryption**: Store API keys encrypted with Fernet symmetric keys, stored securely on disk.
3. **Deployment**: Bundle SQLite with CLI tools for easy setup; no external dependencies beyond `cryptography`.
4. **Tradeoffs**:
   - *Pros*: Lightweight, portable, zero external dependencies, easy to back up.
   - *Cons*: Limited concurrency, not suitable for multi-user environments, potential security risks if disk is compromised.
5. **Action**:
   - Initialize DB with schema.
   - Provide CLI commands: `add-project`, `set-api-key`, `get-api-keys`.
   - Use local file storage for encryption keys.
   
This setup balances simplicity, portability, and security for rapid local deployment and testing.
- Infra Engineer: Implement a Terraform module deploying a Vercel-hosted API Gateway with the following shape:

1. **AWS**:
   - Use API Gateway (REST API) with Lambda proxy integration for key provisioning/proxying.
   - Store API keys securely in AWS Secrets Manager.
   - Lambda functions handle key management, proxy requests, and inject keys.
   - IAM roles restrict access to Secrets Manager.

2. **Vercel**:
   - Deploy serverless functions (Node.js/Next.js API routes) to proxy requests.
   - Use environment variables or Vercel Secrets for initial API key configs.
   - Store per-project keys in Vercel Secrets or a lightweight external store (e.g., Firebase).

3. **Tradeoffs**:
   - *AWS*: More scalable, secure, but higher complexity and cost.
   - *Vercel*: Simpler, lower cost, but limited control over secrets and scaling.
   
**Action**:
- Start with Vercel serverless functions for rapid iteration.
- Use Terraform to provision Secrets Manager and API Gateway if scaling needed.
- Keep the system CLI-configurable for onboarding new projects with minimal friction.
- DevOps Engineer: Implement a CLI tool in Python with the following steps:

1. Generate a UUID project key (`init` command).
2. Store API keys encrypted in a local JSON file using Fernet.
3. Proxy API requests with `http.server`, injecting stored keys.
4. Commands: `set`, `get`, `proxy`.

**Tradeoffs:**
- *Pros*: Rapid, minimal dependencies, easy to validate.
- *Cons*: Local-only security, no multi-user support, limited scalability.

**Implementation:**
- Use `argparse` for CLI.
- Use `cryptography` for encryption.
- Use `http.server` for proxy.
- Validate with sample APIs (Slack, Stripe).

This setup enables a quick proof of concept within hours, demonstrating core benefits before scaling or adding features.
- OpenSpec Writer: Implement a CLI-based MVP in Python with these explicit requirements:

1. **Architecture**:
   - Generate a UUID project key (`init`).
   - Store API keys encrypted in a local JSON file (using Fernet).
   - Proxy API requests via `http.server`, injecting stored keys based on request URL or headers.

2. **Implementation**:
   - Use `argparse` for CLI commands (`init`, `set`, `proxy`).
   - Encrypt/decrypt API keys at rest; store in a version-controlled config directory.
   - Proxy server intercepts requests, identifies target API, injects corresponding key, and forwards.

3. **Tradeoffs & Constraints**:
   - *Pros*: Rapid development, no external dependencies beyond `cryptography`, easy to validate.
   - *Cons*: Local-only security, no multi-user support, limited scalability, minimal error handling.

4. **Acceptance Checks**:
   - Validate setup time (<1 hour).
   - Confirm API key injection for sample APIs (Stripe, Slack).
   - Measure reduction in onboarding steps compared to manual key management.

This ensures a lightweight, actionable proof of concept aligned with rapid iteration and minimal external dependencies.
