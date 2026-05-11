# Implementation Plan: God Mode AI Proxy CLI - The Universal Context Broker

## Goal
Create a working proof of concept that demonstrates the core value of `God Mode AI Proxy CLI - The Universal Context Broker` with the smallest credible interface.

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
`harmuaq`

## Debate Context Used
Founder Board debate exists and was considered.

## Crew Implementation Notes
- Product Planner: MVP Workflow for God Mode AI Proxy CLI:

1. **Initialize Local Ledger**  
   - CLI command: `godmode init`  
   - Creates a SQLite DB in project root to store handoff entries, file metadata, and guardrail configs.

2. **Configure No-Fly Zones**  
   - CLI command: `godmode config nofly add <pattern>` (e.g., `.env`, `terraform.tfstate`)  
   - Stores blocked file patterns in ledger; these patterns are enforced during export.

3. **Record Handoff Entry**  
   - CLI command: `godmode handoff record --assistant <name> --task <desc> --files <list>`  
   - Captures current task state, constraints, decisions, files touched from local FS and git metadata.  
   - Stores a serialized handoff entry in ledger with timestamp and assistant tag.

4. **Export Portable Handoff Prompt**  
   - CLI command: `godmode handoff export --to <assistant>`  
   - Reads latest handoff entry, prunes files matching no-fly patterns, summarizes included/excluded files in audit.  
   - Produces a deterministic, portable prompt bundle (JSON + markdown summary) for the target assistant.

**Tradeoffs & Notes:**  
- MVP skips live OS-level interception; relies on explicit CLI commands to record/export context.  
- Starts assistant-neutral; no adapter-specific prompt translation yet.  
- Local vector embeddings and semantic pruning postponed to post-MVP.  
- CLI-only avoids IDE/plugin complexity and cloud dependencies.  
- Deterministic export ensures reproducible handoffs for same ledger state.  

This workflow enables immediate cross-assistant handoff with privacy guardrails and minimal setup (<5 min).
- POC Coder: POC Plan: God Mode AI Proxy CLI MVP (Local-first, CLI-only)

**Scope (MVP):**
- CLI commands: `init`, `handoff write`, `handoff read`, `config no-fly`
- Local SQLite ledger storing:
  - Project metadata (name, git info)
  - Handoff entries: task state, constraints, files touched, decisions, next action
  - No-fly file patterns (glob-style)
- Export command generating a portable handoff prompt bundle:
  - Reads ledger state
  - Excludes files matching no-fly patterns
  - Includes audit summary of included/excluded files
  - Deterministic output for same ledger state

**Tech stack:**
- Python + Typer CLI
- SQLite for ledger (local file)
- Use standard `glob` for no-fly pattern matching
- Simple file reads for files touched (no embeddings or vector DB yet)

**Tradeoffs:**
- No embedding/vector indexing yet (optional later)
- No OS-level interception or live shell wrapping (too complex for MVP)
- Assistant-neutral: no adapter, just portable prompt bundle output
- Manual CLI commands for handoff read/write (no automation)
- No semantic pruning yet; rely on user to curate files touched

**Next steps:**
- Implement `init` to create SQLite ledger and config file
- Implement `config no-fly` to add/remove blocked patterns
- Implement `handoff write` to add a handoff entry with metadata + files touched
- Implement `handoff read` to export sanitized prompt bundle with audit
- Validate zero secret file inclusion & deterministic export

This minimal CLI-first POC proves core ledger + no-fly enforcement + portable handoff prompt generation without complex integrations or cloud dependencies.
- Frontend Engineer: Define a minimal CLI interface focused on core MVP flows:

1. `godmode init [--project <path>]`  
   - Initialize local ledger (SQLite) in project dir.  
   - Creates config including no-fly file patterns (default: `.env`, `terraform.tfstate`).  

2. `godmode handoff write --agent <name> --task <desc> --files <file1,file2,...> --decisions <json>`  
   - Record a handoff entry: active task, touched files, decisions, next action.  
   - Validate files against no-fly patterns and exclude blocked files.  
   - Store audit summary with included/excluded files.  

3. `godmode handoff read [--agent <name>]`  
   - Read last or all handoff entries, output portable prompt bundle.  
   - Deterministic output for same ledger state.  

4. `godmode config set no-fly <pattern1,pattern2,...>`  
   - Update no-fly patterns to enforce local security guardrails.  

Tradeoffs:  
- CLI-only ensures minimal dependencies and fast setup (<5min).  
- No live interception or assistant adapters in MVP reduces complexity and maintenance risk.  
- Plain-text ledger and prompt bundles maximize transparency and trust.  
- No mandatory embeddings initially to simplify MVP; add semantic pruning later.  
- Focus on stateless handoff and audit summaries for compliance and clarity.  

This interface covers all must-have MVP criteria, is actionable, and extensible.
- Backend Engineer: Define these core APIs and local persistence schema for MVP:

1. **API Endpoints (CLI commands):**
- `init-ledger --path <project-root>`: create local SQLite ledger file storing all handoff entries and config.
- `record-handoff --assistant <name> --task <json>`: append a handoff entry with task state, touched files, constraints, decisions, next action, timestamp.
- `read-handoff --id <entry-id>`: retrieve a handoff entry for review or export.
- `set-no-fly --patterns <glob-list>`: configure blocked file patterns persisted in ledger.
- `export-handoff --id <entry-id> --output <file>`: generate portable prompt bundle with sanitized context and audit summary.

2. **Local Persistence (SQLite schema):**
- Table `ledger` (id INTEGER PK, created_at TIMESTAMP)
- Table `handoff_entries` (id INTEGER PK, ledger_id FK, assistant TEXT, task_state JSON, files_touched JSON, constraints JSON, decisions JSON, next_action TEXT, created_at TIMESTAMP)
- Table `no_fly_patterns` (id INTEGER PK, pattern TEXT UNIQUE)
- Table `audit_logs` (id INTEGER PK, handoff_id FK, included_files JSON, excluded_files JSON, notes TEXT, created_at TIMESTAMP)

3. **Tradeoffs:**
- SQLite enables local-first, zero-dependency persistence with ACID guarantees.
- JSON fields allow flexible schema evolution for task state and metadata.
- CLI-only MVP avoids complex OS-level interception; later versions may add event hooks.
- Assistant-neutral core avoids brittle adapter maintenance; MVP can start with plain text handoff bundles before embedding indexes.
- No live command wrapping reduces complexity but requires manual handoff invocation.

Actionables:
- Design CLI commands with Typer.
- Define SQLite schema and migration scripts.
- Implement JSON serialization/deserialization for handoff entries.
- Build export logic applying no-fly filters and generating audit summaries.
- Validate deterministic output for repeated exports of same ledger state.
- Auth Engineer: For local POC, adopt a **minimal local-first auth posture**:

- **No user accounts or network auth**: purely local CLI with SQLite ledger and file-based config.
- **File system permissions + OS user isolation** enforce access control.
- **Configurable "no-fly zones"** block sensitive files from export, enforced by CLI logic.
- **Audit logs** stored locally for transparency.
- **No cloud or remote sync** in MVP to avoid trust and complexity issues.

Tradeoffs:
- + Fast setup (<5 min), zero external dependencies, max privacy.
- - No multi-user RBAC or remote state sync (premium SaaS feature later).
- - Relies on OS-level user isolation; no fine-grained user roles initially.

For production handoff:
- Add **optional BYOK SaaS sync with OAuth + token-based auth** for team RBAC.
- Harden audit trails with cryptographic signing.
- Maintain local-first fallback mode for offline and privacy-sensitive users.
- Provide clear privacy/security docs to build trust.

Actionables:
1. Implement CLI auth as local OS user + config file.
2. Enforce no-fly zones in export commands.
3. Log all handoff and export actions locally.
4. Design SaaS auth layer modularly for future integration.
- Database Engineer: For the God Mode AI Proxy CLI MVP, choose **SQLite** as the local ledger DB for its zero-config, file-backed, transactional ACID compliance, and broad Python support (via `sqlite3` stdlib). This ensures easy local-first setup (<5 min) and deterministic exports.

**Schema design:**
- `handoff_entries` table: id, timestamp, assistant_name, task_state (JSON), files_touched (JSON), constraints (JSON), decisions (JSON), next_action (TEXT)
- `no_fly_patterns` table: pattern TEXT, description TEXT
- `audit_logs` table: entry_id, included_files JSON, excluded_files JSON, timestamp

**Tradeoffs:**
- SQLite is lightweight but single-writer; concurrency is limited but acceptable for CLI MVP.
- No built-in vector search; integrate optional LanceDB or local embedding index for semantic pruning later.
- Avoid complex triggers or extensions to keep CLI portable and dependency-light.
- Store JSON blobs for flexible schema evolution and assistant-neutral data.

**Implementation notes:**
- Use Python’s `sqlite3` with `row_factory` for dict-like access.
- Wrap DB access in a repository layer for future adapter/plugin support.
- Enforce no-fly patterns at export by filtering file lists before bundling.
- Ensure export command produces deterministic output by sorting entries and files.

This approach balances simplicity, local privacy, and extensibility for MVP success.
- Infra Engineer: **Deployment Shape for God Mode AI Proxy CLI**

1. **AWS Infrastructure:**
   - Use **EC2 (t3.medium)** for optional remote DB sync SaaS backend (premium BYOK subscription).
   - **RDS (PostgreSQL)** for team RBAC and remote ledger sync.
   - **S3** for optional encrypted backups of ledgers.
   - **API Gateway + Lambda** for lightweight SaaS API endpoints.
   - Use **CloudWatch** for monitoring and alerts.

2. **Vercel:**
   - Deploy optional **FastAPI** frontend/backend for SaaS UI (team RBAC, subscription management).
   - Vercel’s edge functions can serve static docs and CLI help pages.
   - Keep CLI and core logic local-first; Vercel only hosts SaaS UI and API.

3. **Terraform:**
   - Define infrastructure as code for:
     - EC2 instance with security groups (SSH restricted, HTTPS for API).
     - RDS instance with encrypted storage.
     - S3 bucket with lifecycle policies.
     - IAM roles/policies for least privilege.
     - Vercel project and environment variables via Terraform provider.
   - Use Terraform modules for repeatability and environment parity.

**Tradeoffs:**
- Local-first CLI ensures privacy and offline use but complicates OS-level interception; MVP should avoid complex interception, focusing on context bundle generation.
- SaaS backend adds monetization and team features but introduces cloud trust concerns; keep core CLI fully functional offline.
- Vercel simplifies frontend deployment but adds vendor lock-in risk; mitigate by keeping UI optional and decoupled.
- Terraform enables reproducible deployments but adds initial setup complexity; provide simple scripts for MVP users.

**Actionables:**
- Build CLI MVP with Python/Typer + SQLite locally.
- Use Terraform to provision minimal AWS backend (EC2 + RDS) for SaaS features.
- Deploy FastAPI SaaS UI on Vercel.
- Document CLI local usage and optional SaaS integration clearly.
- Prioritize stateless, deterministic ledger exports before adding OS hooks.
- DevOps Engineer: **GitHub Automation & Checks for God Mode AI Proxy CLI**

1. **CI Workflow (GitHub Actions):**
   - Trigger: `push` & `pull_request` on `main` & `develop`.
   - Steps:
     - Setup Python 3.10+ environment.
     - Install dependencies (`pip install -r requirements.txt`).
     - Run linting (e.g., `flake8` or `black --check`).
     - Run unit tests with coverage.
     - Run integration tests simulating ledger init, handoff write/read, and export with no-fly zones.
     - Validate deterministic export output (compare hashes).
   - Artifacts: test coverage report, lint report.

2. **Pre-commit Hooks:**
   - Enforce code style and static analysis.
   - Prevent commits with secrets or blocked file patterns.

3. **Deployment Notes:**
   - CLI distributed via PyPI and GitHub Releases.
   - Versioning follows semantic versioning.
   - Users install locally; no cloud dependency.
   - Document setup under 5 minutes with example commands:
     - `godmode init-ledger`
     - `godmode write-handoff`
     - `godmode export --no-fly .env,terraform.tfstate`
   - Optional: GitHub Actions for auto-building and publishing releases.

**Tradeoffs:**
- Using GitHub Actions keeps CI local and free but may limit complex OS-level interception tests.
- Avoid proprietary IDE extensions to maintain framework-agnostic CLI.
- Focus on assistant-neutral core to reduce maintenance overhead from API changes.
- Semantic pruning and embedding indexing deferred to post-MVP to reduce complexity.

This setup ensures fast feedback, code quality, and reproducible handoff exports aligned with MVP goals.
- OpenSpec Writer: Implementation Requirements:

1. CLI Commands:
   - `init-ledger`: Initialize a local SQLite ledger in the project directory.
   - `write-handoff`: Record a handoff entry with fields: task state, constraints, files touched, decisions, next action.
   - `read-handoff`: Retrieve and display handoff entries.
   - `export-handoff`: Generate a portable prompt bundle excluding blocked files, including an audit summary.

2. Configuration:
   - Support user-defined no-fly file patterns (e.g., `.env`, `terraform.tfstate`) stored in config.
   - Enforce exclusion of blocked files during export with audit logs.

3. Data Storage:
   - Use SQLite for ledger storage.
   - Store file metadata and handoff entries with timestamps and agent identifiers.

4. Context Pruning (nice-to-have):
   - Implement semantic pruning to reduce token count under 4000 tokens.

5. Deterministic Export:
   - Ensure export output is consistent for identical ledger states.

6. Technology Stack:
   - Python 3.9+, Typer CLI framework, SQLite.
   - Optional: LanceDB for local vector embeddings.

Tradeoffs:

- MVP will not intercept live shell commands or network requests to reduce complexity.
- Start with assistant-neutral handoff format; add assistant-specific adapters later.
- Local embeddings optional initially; focus on plain-text ledger export.

Acceptance Checks:

- User can run `init-ledger` in under 5 minutes.
- User can write and read handoff entries successfully.
- Exported handoff excludes blocked files with audit notes.
- Exported prompt includes all required context fields.
- Export output is deterministic for the same ledger state.
- Exported context token count stays below 4000 tokens.
- No secret or blocked files are included in exports.

This scope balances MVP speed, security, and extensibility while avoiding fragile integrations or cloud dependencies.
