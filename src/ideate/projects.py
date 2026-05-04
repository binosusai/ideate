from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

from .agents import acceptance_tests, handoff_brief
from .models import Idea
from .text import md, slugify


def idea_dir(root: Path, idea: Idea) -> Path:
    return root / "ideas" / idea.slug


def ensure_idea_folder(root: Path, idea: Idea) -> Path:
    path = idea_dir(root, idea)
    (path / "openspec" / "changes" / idea.slug / "specs" / slugify(idea.title)).mkdir(
        parents=True, exist_ok=True
    )
    return path


def poc_workspace(root: Path) -> Path:
    return Path(os.environ.get("IDEATE_POC_HOME", root.parent / "pocs")).resolve()


def platform_workspace(root: Path) -> Path:
    return Path(os.environ.get("IDEATE_PLATFORM_HOME", root.parent / "platform")).resolve()


def poc_name(idea: Idea) -> str:
    # Derive a concise readable codename from the idea slug words.
    # e.g., "unified-api-key-gateway-..." -> "unifieda" + 2-char hash suffix.
    _stop = frozenset({
        "a", "an", "the", "and", "or", "of", "to", "for", "in", "on",
        "at", "by", "with", "one", "per", "that", "which", "this", "from",
        "via", "as", "is", "are", "be", "it", "its", "i", "all",
    })
    parts = [p for p in idea.slug.split("-") if p and p not in _stop]
    base = (parts[0] if parts else "idea")[:8]
    seed = int(hashlib.sha1(idea.slug.encode("utf-8")).hexdigest(), 16)
    alpha = "abcdefghijklmnopqrstuvwxyz"
    suffix = alpha[seed % 26] + alpha[(seed // 26) % 26]
    return f"{base}{suffix}"


def poc_dir(root: Path, idea: Idea) -> Path:
    return poc_workspace(root) / poc_name(idea)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_planning_files(
    root: Path,
    idea: Idea,
    research: str,
    debate: str,
    plan: str,
    crew_transcripts: list[str] | None = None,
) -> Path:
    path = ensure_idea_folder(root, idea)
    refresh_readme(root, idea)
    write_text(path / "research.md", research)
    write_text(path / "debate.md", debate)
    write_text(path / "implementation_plan.md", plan)
    write_text(path / "acceptance_tests.md", acceptance_tests(idea))
    if crew_transcripts:
        write_text(path / "crew_transcripts.md", "\n\n---\n\n".join(crew_transcripts))
    write_openspec(path, idea)
    return path


def refresh_readme(root: Path, idea: Idea) -> None:
    path = ensure_idea_folder(root, idea)
    write_text(path / "README.md", idea_readme(idea))


def write_openspec(path: Path, idea: Idea) -> None:
    change = path / "openspec" / "changes" / idea.slug
    capability = change / "specs" / slugify(idea.title)
    write_text(
        change / "proposal.md",
        md(
            f"Proposal: {idea.title}",
            f"""
            ## Why
            {idea.why or "The idea was approved for structured exploration."}

            ## What Changes
            - Create a focused full-stack proof of concept for `{idea.title}`.
            - Validate whether the idea should be handed to the larger engineering crew.
            - Keep the first draft local-first, secret-safe, and deploy-aware.

            ## Impact
            - Adds a draft project under the workspace-level `pocs/{poc_name(idea)}/` folder.
            - Adds frontend, backend, database, infra, DevOps, and deployment documentation.
            - Defines implementation requirements in `specs/`.
            """,
        ),
    )
    write_text(
        change / "design.md",
        md(
            f"Design: {idea.title}",
            """
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
            """,
        ),
    )
    write_text(
        change / "tasks.md",
        md(
            f"Tasks: {idea.title}",
            """
            - [ ] Build a runnable frontend.
            - [ ] Build a backend API if the workflow needs persistence or server-side logic.
            - [ ] Use SQLite locally and document Neon/Supabase upgrade paths.
            - [ ] Document Clerk/Firebase Auth integration points if identity is needed.
            - [ ] Add Vercel/AWS/Terraform deployment scaffolding where useful.
            - [ ] Add GitHub Actions checks.
            - [ ] Document local install, local run, deployment, and limitations.
            - [ ] Prepare handoff notes for the engineering crew.
            """,
        ),
    )
    write_text(
        capability / "spec.md",
        md(
            f"Spec: {idea.title}",
            """
            ## ADDED Requirements

            ### Requirement: Runnable local proof of concept
            The system SHALL include a local proof of concept that demonstrates the core idea with frontend, backend when needed, and local persistence without requiring paid services by default.

            #### Scenario: User runs the POC
            - **WHEN** the user follows the instructions in `poc_report.md`
            - **THEN** the POC runs locally or clearly explains missing prerequisites

            ### Requirement: External POC workspace
            Generated POC source code SHALL live outside the Ideate agent factory folder.

            #### Scenario: POC is generated
            - **WHEN** the user runs `idea poc`
            - **THEN** the POC is written under the workspace-level `pocs/` folder

            ### Requirement: Deployment-ready documentation
            The system SHALL include documentation for local setup and production deployment options.

            #### Scenario: User reviews deployment path
            - **WHEN** the user reads the generated POC `docs/deployment.md`
            - **THEN** they can identify Vercel, AWS, Terraform, auth, database, and GitHub Actions next steps

            ### Requirement: Engineering handoff
            The system SHALL provide enough context for a larger agent crew to continue implementation.

            #### Scenario: Engineering crew receives the folder
            - **WHEN** the crew reads `handoff.md`
            - **THEN** it can identify mission, inputs, guardrails, and next tasks
            """,
        ),
    )


def _init_poc_repo(project: Path, idea: Idea) -> None:
    """Git-init the POC folder and create a GitHub repo when enabled."""
    org = os.environ.get("IDEATE_GITHUB_ORG", "binosusai")
    base_repo_name = poc_name(idea)
    try:
        subprocess.run(["git", "init"], cwd=project, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.name", os.environ.get("IDEATE_GIT_USER_NAME", "ideate-bot")],
            cwd=project,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                os.environ.get("IDEATE_GIT_USER_EMAIL", "ideate-bot@users.noreply.github.com"),
            ],
            cwd=project,
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "add", "."], cwd=project, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial POC scaffold"],
            cwd=project,
            check=True,
            capture_output=True,
        )
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"POC git initialization failed for {project.name}: {exc}") from exc
    if os.environ.get("IDEATE_SKIP_GITHUB_REPO_CREATE") == "1":
        print(f"[ideate] GitHub repo creation skipped for {org}/{base_repo_name}")
        return

    candidates = [base_repo_name]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    seed = int(hashlib.sha1(f"{idea.slug}:{idea.id}".encode("utf-8")).hexdigest(), 16)
    base_trimmed = base_repo_name[:10]
    for offset in range(1, 6):
        candidates.append(
            f"{base_trimmed}{alphabet[(seed + offset) % 26]}{alphabet[(seed // 26 + offset) % 26]}"
        )

    # gh CLI uses GH_TOKEN env var; fall back to current environment (CI sets GH_TOKEN directly)
    for repo_name in candidates:
        result = subprocess.run(
            [
                "gh", "repo", "create",
                f"{org}/{repo_name}",
                "--public",
                "--source", str(project),
                "--push",
                "--description", idea.title,
            ],
            cwd=project,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[ideate] GitHub repo created: https://github.com/{org}/{repo_name}")
            return

        message = result.stderr.strip() or result.stdout.strip() or "unknown error"
        if "Name already exists on this account" in message:
            continue
        raise RuntimeError(f"GitHub repo creation failed for {org}/{repo_name}: {message}")

    raise RuntimeError(
        f"GitHub repo creation failed for {org}: all candidate names are already taken ({', '.join(candidates)})"
    )


def write_poc(root: Path, idea: Idea, force_build: bool = False) -> bool:
    path = ensure_idea_folder(root, idea)
    project = poc_dir(root, idea)
    feasible = is_poc_feasible(idea)
    context = build_project_context(path, idea)
    write_text(path / "poc_report.md", poc_report_for(idea, feasible, project))
    write_text(path / "poc_location.md", poc_location_doc(idea, project))
    if not feasible and not force_build:
        return False

    write_common_poc_infra(poc_workspace(root), platform_workspace(root))
    write_draft_project(project, idea, platform_workspace(root), context)
    copy_openspec_into_poc(path, project)
    _init_poc_repo(project, idea)
    return True


def build_project_context(path: Path, idea: Idea) -> dict[str, str]:
    research = read_optional(path / "research.md")
    debate = read_optional(path / "debate.md")
    plan = read_optional(path / "implementation_plan.md")
    acceptance = read_optional(path / "acceptance_tests.md")
    return {
        "research": research,
        "debate": debate,
        "plan": plan,
        "acceptance": acceptance,
        "research_summary": artifact_summary(
            research,
            "No research artifact found. Run `idea research <id>` before generating POC.",
        ),
        "debate_summary": artifact_summary(
            debate,
            "No debate artifact found. Run `idea debate <id>` before generating POC.",
        ),
        "plan_summary": artifact_summary(
            plan,
            "No implementation plan artifact found. Run `idea plan <id>` before generating POC.",
        ),
        "use_case": infer_use_case(idea, f"{research}\n{debate}\n{plan}"),
    }


def read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def artifact_summary(content: str, fallback: str) -> str:
    if not content:
        return fallback
    lines: list[str] = []
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        lines.append(line)
        if len(lines) == 3:
            break
    if not lines:
        return fallback
    return " ".join(lines)


def infer_use_case(idea: Idea, context: str) -> str:
    text = f"{idea.title}\n{idea.why}\n{context}".lower()
    if "api key" in text or "proxy" in text or "gateway" in text:
        return "api-key-gateway"
    return "workflow-assistant"


def copy_openspec_into_poc(idea_path: Path, project: Path) -> None:
    source = idea_path / "openspec"
    if source.exists():
        shutil.copytree(source, project / "openspec", dirs_exist_ok=True)


def poc_report_for(idea: Idea, feasible: bool, project: Path) -> str:
    if feasible:
        body = f"""
        ## Result
        A complete local proof of concept was generated outside the Ideate folder.

        ## Location
        `{project}`

        ## How To Run
        ```bash
        cd {project}
        python3 backend/app.py
        ```

        Open `http://localhost:8000`.

        ## Limitations
        - Uses deterministic placeholder logic by default.
        - Does not call external AI services unless the implementation adds exported environment variables.
        - Includes deploy scaffolding, but production deployment still needs project-specific configuration.
        """
    else:
        body = f"""
        ## Result
        POC generation was skipped because the idea appears to need external services, paid APIs, or missing credentials.

        ## Intended Location
        `{project}`

        ## Next Step
        Clarify required integrations and create a mock-only POC.
        """
    return md(f"POC Report: {idea.title}", body)


def poc_location_doc(idea: Idea, project: Path) -> str:
    return md(
        f"POC Location: {idea.title}",
        f"""
        ## Generated POC
        `{project}`

        Ideate keeps agent memory, research, debate, OpenSpec, and handoff files in `ideate/ideas/{idea.slug}/`.
        The runnable proof-of-concept source code lives outside the factory under the workspace-level `pocs/` folder.
        """,
    )


def write_common_poc_infra(workspace: Path, platform: Path) -> None:
    write_text(
        workspace / "_common" / "README.md",
        md(
            "Common POC Infrastructure",
            f"""
            Shared conventions for generated POCs.

            ## Shared Platform Library
            `{platform}`

            - Keep real secrets out of generated projects.
            - Prefer Vercel for frontend previews.
            - Prefer AWS for backend/cloud services when needed.
            - Prefer SQLite locally, then Neon or Supabase Postgres for hosted data.
            - Prefer Clerk for SaaS auth, or Firebase Auth for Firebase-centered products.
            - Prefer shared GitHub Actions and Terraform modules from the platform library.
            - Use local project-specific infra only when the architecture materially diverges.
            - Do not commit Terraform state.
            """,
        ),
    )


def write_draft_project(project: Path, idea: Idea, platform: Path, context: dict[str, str]) -> None:
    write_text(project / "backend" / "app.py", backend_app(idea, context))
    write_text(project / "frontend" / "index.html", frontend_index(idea, context))
    write_text(project / "frontend" / "styles.css", frontend_styles(context))
    write_text(project / "frontend" / "app.js", frontend_app_js(context))
    write_text(project / "infra" / "terraform" / "main.tf", terraform_main(idea, platform))
    write_text(project / ".github" / "workflows" / "poc-ci.yml", github_actions(platform))
    write_text(project / ".env.example", env_example())
    write_text(project / "PROJECT_RULES.md", project_rules_doc(platform))
    write_text(project / "README.md", project_readme(idea, context))
    write_text(project / "docs" / "local_setup.md", local_setup_doc())
    write_text(project / "docs" / "deployment.md", deployment_doc(platform))
    write_text(project / "docs" / "architecture.md", architecture_doc(idea, context))
    write_text(project / "docs" / "devops.md", devops_doc(platform))
    write_text(project / "docs" / "engineering_brief.md", engineering_brief_doc(idea, context))


def project_readme(idea: Idea, context: dict[str, str]) -> str:
    research = context.get("research", "")
    debate = context.get("debate", "")
    plan = context.get("plan", "")
    base = md(
        f"Draft POC: {idea.title}",
        f"""
        This repository is generated from approved idea artifacts and should represent a runnable first draft for the approved use case.

        ## Use Case
        `{context.get("use_case", "workflow-assistant")}`

        ## What Is Included
        - Runnable backend API in `backend/`
        - Interactive frontend in `frontend/`
        - Local SQLite persistence
        - OpenSpec copied into `openspec/`
        - Terraform entrypoint in `infra/terraform/`
        - CI checks in `.github/workflows/poc-ci.yml`
        - Project docs in `docs/`

        ## Run Locally

        ```bash
        python3 backend/app.py
        ```

        Then open `http://localhost:8000`.
        """,
    )
    extra: list[str] = []
    if research:
        extra.append(f"## Research\n\n{research}")
    if debate:
        extra.append(f"## Debate\n\n{debate}")
    if plan:
        extra.append(f"## Implementation Plan\n\n{plan}")
    if extra:
        return base + "\n" + "\n\n---\n\n".join(extra) + "\n"
    return base


def backend_app(idea: Idea, context: dict[str, str]) -> str:
    if context.get("use_case") == "api-key-gateway":
        return _gateway_backend_app(idea, context)
    plan_summary = context.get("plan_summary", "")
    research_summary = context.get("research_summary", "")
    use_case = context.get("use_case", "workflow-assistant")
    return f'''from __future__ import annotations

import json
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "poc.sqlite3"
FRONTEND = ROOT / "frontend"
IDEA_TITLE = {idea.title!r}
IDEA_CATEGORY = {idea.category!r}
USE_CASE = {use_case!r}
PLAN_SUMMARY = {plan_summary!r}
RESEARCH_SUMMARY = {research_summary!r}


def init_db() -> None:
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              input TEXT NOT NULL,
              recommendation TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def create_recommendation(raw: str) -> str:
    text = raw.strip() or "No input provided."
    return (
        f"POC recommendation for {{IDEA_TITLE}} ({{USE_CASE}}): "
        f"plan emphasis -> {{PLAN_SUMMARY[:200]}} "
        f"research signal -> {{RESEARCH_SUMMARY[:180]}} "
        f"input reviewed -> {{text[:220]}}"
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def do_GET(self):
        if urlparse(self.path).path == "/api/health":
            self.send_json(
                {{
                    "ok": True,
                    "idea": IDEA_TITLE,
                    "category": IDEA_CATEGORY,
                    "use_case": USE_CASE,
                    "plan_summary": PLAN_SUMMARY[:200],
                }}
            )
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/run":
            self.send_error(404)
            return
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{{}}")
        raw = str(payload.get("input", ""))
        recommendation = create_recommendation(raw)
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO runs(input, recommendation) VALUES (?, ?)",
                (raw, recommendation),
            )
        self.send_json({{"recommendation": recommendation}})

    def send_json(self, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("POC running at http://localhost:8000")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
'''


def _gateway_backend_app(idea: Idea, context: dict[str, str]) -> str:
    plan_summary = context.get("plan_summary", "")
    research_summary = context.get("research_summary", "")
    use_case = context.get("use_case", "api-key-gateway")
    return f'''from __future__ import annotations

import json
import secrets
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "poc.sqlite3"
FRONTEND = ROOT / "frontend"
IDEA_TITLE = {idea.title!r}
IDEA_CATEGORY = {idea.category!r}
USE_CASE = {use_case!r}
PLAN_SUMMARY = {plan_summary!r}
RESEARCH_SUMMARY = {research_summary!r}


def init_db() -> None:
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              api_key TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS proxy_runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              project_id INTEGER REFERENCES projects(id),
              provider TEXT NOT NULL,
              payload TEXT NOT NULL,
              response TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              input TEXT NOT NULL,
              recommendation TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def mock_proxy_response(provider: str, payload: str, project_name: str) -> str:
    return (
        f"[MOCK PROXY] provider={{provider}} project={{project_name}} "
        f"signal={{RESEARCH_SUMMARY[:120]}} payload_echo={{payload[:200]}}"
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json(
                {{
                    "ok": True,
                    "idea": IDEA_TITLE,
                    "category": IDEA_CATEGORY,
                    "use_case": USE_CASE,
                    "plan_summary": PLAN_SUMMARY[:200],
                }}
            )
            return
        if path == "/api/projects":
            with sqlite3.connect(DB) as conn:
                rows = conn.execute(
                    "SELECT id, name, api_key, created_at FROM projects ORDER BY created_at DESC"
                ).fetchall()
            self.send_json(
                [{{"id": r[0], "name": r[1], "api_key": r[2], "created_at": r[3]}} for r in rows]
            )
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length) or b"{{}}")

        if path == "/api/projects":
            name = str(body.get("name", "")).strip()
            if not name:
                self.send_error(400, "name required")
                return
            api_key = f"pk_{{secrets.token_hex(16)}}"
            try:
                with sqlite3.connect(DB) as conn:
                    conn.execute(
                        "INSERT INTO projects(name, api_key) VALUES (?, ?)", (name, api_key)
                    )
            except sqlite3.IntegrityError:
                self.send_error(409, "project name already exists")
                return
            self.send_json({{"name": name, "api_key": api_key}})
            return

        if path == "/api/proxy/mock":
            api_key = str(body.get("api_key", ""))
            provider = str(body.get("provider", "openai"))
            payload = str(body.get("payload", ""))
            with sqlite3.connect(DB) as conn:
                row = conn.execute(
                    "SELECT id, name FROM projects WHERE api_key = ?", (api_key,)
                ).fetchone()
            if not row:
                self.send_error(401, "invalid api_key")
                return
            project_id, project_name = row
            response = mock_proxy_response(provider, payload, project_name)
            with sqlite3.connect(DB) as conn:
                conn.execute(
                    "INSERT INTO proxy_runs(project_id, provider, payload, response) VALUES (?,?,?,?)",
                    (project_id, provider, payload, response),
                )
            self.send_json({{"ok": True, "provider": provider, "response": response}})
            return

        if path == "/api/run":
            raw = str(body.get("input", ""))
            recommendation = (
                f"POC recommendation for {{IDEA_TITLE}} ({{USE_CASE}}): "
                f"plan emphasis -> {{PLAN_SUMMARY[:200]}} "
                f"research signal -> {{RESEARCH_SUMMARY[:180]}} "
                f"input reviewed -> {{raw[:220]}}"
            )
            with sqlite3.connect(DB) as conn:
                conn.execute(
                    "INSERT INTO runs(input, recommendation) VALUES (?, ?)",
                    (raw, recommendation),
                )
            self.send_json({{"recommendation": recommendation}})
            return

        self.send_error(404)

    def send_json(self, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("POC running at http://localhost:8000")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
'''


def frontend_index(idea: Idea, context: dict[str, str] | None = None) -> str:
    gateway_panel = ""
    if context and context.get("use_case") == "api-key-gateway":
        gateway_panel = """
        <section class="gateway-panel">
          <h2>Project Key Management</h2>

          <div class="field-row">
            <input type="text" id="project-name" placeholder="Project name (e.g. team-alpha)" />
            <button id="create-project-btn">Create Key</button>
          </div>
          <div class="key-display" id="key-display" hidden>
            <label for="issued-key">Issued API Key</label>
            <input type="text" id="issued-key" readonly />
          </div>

          <h2>Mock Proxy</h2>
          <div class="field-row">
            <input type="text" id="proxy-key" placeholder="API key (pk_...)" />
            <input type="text" id="provider-name" placeholder="Provider" value="openai" />
          </div>
          <textarea id="proxy-payload" rows="4" placeholder='{"prompt": "hello world"}'></textarea>
          <button id="run-proxy-btn">Run Mock Proxy</button>
          <pre id="proxy-result"></pre>
        </section>
"""
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{idea.title}</title>
    <link rel="stylesheet" href="./styles.css">
  </head>
  <body>
    <main class="shell">
      <section class="workspace">
        <p class="eyebrow">{idea.category} POC</p>
        <h1>{idea.title}</h1>
        <p class="summary">{idea.why or "A local proof of concept generated by Ideate."}</p>

        <form id="idea-form">
          <label for="idea-input">Input</label>
          <textarea id="idea-input" name="input" rows="8" placeholder="Paste a customer note, workflow, landing page copy, or rough project input..."></textarea>
          <button type="submit">Run POC</button>
        </form>

        <section class="output" aria-live="polite">
          <h2>Recommendation</h2>
          <p id="result">Run the POC to generate the first recommendation.</p>
        </section>
{gateway_panel}      </section>
    </main>
    <script src="./app.js"></script>
  </body>
</html>
'''


def frontend_styles(context: dict[str, str] | None = None) -> str:
    gateway_css = ""
    if context and context.get("use_case") == "api-key-gateway":
        gateway_css = """
.gateway-panel {
  margin-top: 32px;
  border-top: 1px solid #ece8dc;
  padding-top: 24px;
}

.gateway-panel h2 {
  font-size: 18px;
  margin: 0 0 12px;
}

.field-row {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.field-row input {
  flex: 1;
  min-width: 160px;
  border: 1px solid #c7c4ba;
  border-radius: 6px;
  padding: 8px 10px;
  font: inherit;
}

.key-display {
  margin-bottom: 16px;
  display: grid;
  gap: 4px;
}

.key-display input {
  font-family: monospace;
  background: #f0ece4;
  border: 1px solid #c7c4ba;
  border-radius: 6px;
  padding: 8px 10px;
  width: 100%;
}

#proxy-payload {
  width: 100%;
  resize: vertical;
  border: 1px solid #c7c4ba;
  border-radius: 6px;
  padding: 10px;
  font: inherit;
  margin-bottom: 10px;
}

#proxy-result {
  background: #f0ece4;
  border: 1px solid #c7c4ba;
  border-radius: 6px;
  padding: 12px;
  font-size: 13px;
  white-space: pre-wrap;
  word-break: break-all;
  min-height: 40px;
  margin-top: 12px;
}
"""
    return """* {
  box-sizing: border-box;
}""" + gateway_css + """

body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
  color: #202124;
  background: #f7f5ef;
}

.shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px;
}

.workspace {
  width: min(920px, 100%);
  background: #ffffff;
  border: 1px solid #dad7cd;
  border-radius: 8px;
  padding: 28px;
  box-shadow: 0 18px 40px rgba(32, 33, 36, 0.08);
}

.eyebrow {
  margin: 0 0 8px;
  color: #3367d6;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: 34px;
  line-height: 1.15;
}

.summary {
  max-width: 760px;
  color: #5f6368;
  line-height: 1.6;
}

form {
  display: grid;
  gap: 10px;
  margin-top: 24px;
}

label {
  font-weight: 700;
}

textarea {
  width: 100%;
  resize: vertical;
  border: 1px solid #c7c4ba;
  border-radius: 6px;
  padding: 12px;
  font: inherit;
}

button {
  justify-self: start;
  border: 0;
  border-radius: 6px;
  background: #1f7a5f;
  color: #fff;
  font-weight: 700;
  padding: 10px 16px;
  cursor: pointer;
}

.output {
  margin-top: 24px;
  border-top: 1px solid #ece8dc;
  padding-top: 18px;
}

.output h2 {
  margin: 0 0 8px;
  font-size: 18px;
}
"""


def frontend_app_js(context: dict[str, str] | None = None) -> str:
    gateway_js = ""
    if context and context.get("use_case") == "api-key-gateway":
        gateway_js = """
const createProjectBtn = document.querySelector("#create-project-btn");
const projectNameInput = document.querySelector("#project-name");
const keyDisplay = document.querySelector("#key-display");
const issuedKey = document.querySelector("#issued-key");
const proxyKeyInput = document.querySelector("#proxy-key");
const providerInput = document.querySelector("#provider-name");
const proxyPayload = document.querySelector("#proxy-payload");
const runProxyBtn = document.querySelector("#run-proxy-btn");
const proxyResult = document.querySelector("#proxy-result");

createProjectBtn.addEventListener("click", async () => {
  const name = projectNameInput.value.trim();
  if (!name) { alert("Enter a project name"); return; }
  try {
    const res = await fetch("/api/projects", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!res.ok) { throw new Error(`${res.status} ${await res.text()}`); }
    const data = await res.json();
    issuedKey.value = data.api_key;
    keyDisplay.removeAttribute("hidden");
  } catch (err) {
    alert(`Failed: ${err}`);
  }
});

runProxyBtn.addEventListener("click", async () => {
  const api_key = proxyKeyInput.value.trim();
  if (!api_key) { alert("Enter an API key"); return; }
  proxyResult.textContent = "Running proxy...";
  try {
    const res = await fetch("/api/proxy/mock", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        api_key,
        provider: providerInput.value.trim() || "openai",
        payload: proxyPayload.value,
      }),
    });
    const data = await res.json();
    proxyResult.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    proxyResult.textContent = `Error: ${err}`;
  }
});
"""
    return f"""const form = document.querySelector("#idea-form");
const input = document.querySelector("#idea-input");
const result = document.querySelector("#result");

form.addEventListener("submit", async (event) => {{
  event.preventDefault();
  result.textContent = "Running...";
  try {{
    const response = await fetch("/api/run", {{
      method: "POST",
      headers: {{ "content-type": "application/json" }},
      body: JSON.stringify({{ input: input.value }}),
    }});
    const data = await response.json();
    result.textContent = data.recommendation;
  }} catch (error) {{
    result.textContent = `POC request failed: ${{error}}`;
  }}
}});
{gateway_js}"""


def terraform_main(idea: Idea, platform: Path) -> str:
    platform_source = str(platform / "terraform-modules")
    return f'''terraform {{
  required_version = ">= 1.6.0"
}}

# Shared-platform infrastructure entrypoint for: {idea.title}
# Keep this file small. Prefer shared modules from:
# {platform_source}

variable "project_name" {{
  type    = string
  default = "{poc_name(idea)}"
}}

variable "use_shared_platform" {{
  type    = bool
  default = true
}}

module "frontend" {{
  source       = "{platform_source}/vercel-static-site"
  project_name = var.project_name
}}

module "api" {{
  source       = "{platform_source}/aws-python-api"
  project_name = var.project_name
}}

# Enable when this POC needs hosted Postgres.
# module "database" {{
#   source       = "{platform_source}/neon-postgres"
#   project_name = var.project_name
# }}
'''


def github_actions(platform: Path) -> str:
    return f"""name: POC checks

on:
  pull_request:
  push:
    branches: [main]

jobs:
  # Future GitHub org form:
  # ci:
  #   uses: your-org/platform/.github/workflows/python-poc-ci.yml@main
  #   with:
  #     backend_path: backend/app.py
  #
  # Local platform source for this workspace:
  # {platform / "github-actions" / "python-poc-ci.yml"}
  backend-smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Compile backend
        run: python -m py_compile backend/app.py
"""


def env_example() -> str:
    return """# Placeholder only. Do not commit real secrets.
# Local POC works without these by default.
CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
FIREBASE_PROJECT_ID=
DATABASE_URL=
OPENAI_API_KEY=
"""


def local_setup_doc() -> str:
    return md(
        "Local Setup",
        """
        ## Requirements
        - Python 3.11+
        - No package install required for the default POC

        ## Run
        ```bash
        python3 backend/app.py
        ```

        Open `http://localhost:8000`.

        ## Secrets
        Do not commit `.env`. Export secrets in your shell or configure them in the deployment provider.
        """,
    )


def deployment_doc(platform: Path) -> str:
    return md(
        "Deployment",
        f"""
        ## Recommended POC Deployment
        - Frontend: Vercel
        - Backend: AWS Lambda + API Gateway, ECS Fargate, or App Runner
        - Database: Neon Postgres or Supabase Postgres
        - Auth: Clerk for SaaS, Firebase Auth when the Firebase ecosystem is preferred
        - Infra: shared Terraform modules from `{platform / "terraform-modules"}`
        - DevOps: shared GitHub Actions from `{platform / "github-actions"}`

        ## Vercel
        Deploy `frontend/` as the static site. Configure API routing once the backend target URL exists.

        ## AWS
        Convert `backend/app.py` to Lambda/API Gateway or containerize it for App Runner/ECS.

        ## Terraform
        Use `infra/terraform/main.tf` as the project entrypoint. It should call shared platform modules by default.

        ## When To Use Local Infra
        Create local project-specific modules only when this POC needs an unusual architecture, special compliance, custom AWS topology, streaming/queues/workers, mobile/desktop distribution, or provider-specific resources not covered by the platform library.

        ## Environment Variables
        Configure secrets in Vercel, AWS, Clerk, Firebase, Neon, or Supabase dashboards. Do not commit `.env`.

        ## Shared Rules
        Follow `PROJECT_RULES.md` and the platform rules in `{platform / "rules"}`.
        """,
    )


def architecture_doc(idea: Idea, context: dict[str, str]) -> str:
    return md(
        "Architecture",
        f"""
        ## POC Goal
        Demonstrate `{idea.title}` with a simple browser workflow and a local backend API.

        ## Use Case Classification
        `{context.get("use_case", "workflow-assistant")}`

        ## Components
        - `frontend/`: static HTML/CSS/JavaScript
        - `backend/`: Python stdlib HTTP API
        - `poc.sqlite3`: local runtime database, ignored by git
        - `infra/`: Terraform placeholders for production resources
        - `.github/workflows/`: CI checks

        ## Production Upgrade Path
        Replace SQLite with Neon or Supabase Postgres, add Clerk or Firebase Auth, deploy frontend to Vercel, and deploy backend to AWS.
        """,
    )


def engineering_brief_doc(idea: Idea, context: dict[str, str]) -> str:
    return md(
        f"Engineering Brief: {idea.title}",
        f"""
        ## Research Summary Used
        {context.get("research_summary", "")}

        ## Debate Summary Used
        {context.get("debate_summary", "")}

        ## Plan Summary Used
        {context.get("plan_summary", "")}

        ## Acceptance Coverage Input
        {context.get("acceptance", "No acceptance tests artifact found.")}

        ## SDLC Next Moves
        - add unit and integration tests for backend endpoints
        - replace mock recommendation logic with real domain logic
        - complete Terraform module wiring and environment-specific configs
        - apply security hardening and observability from platform rules
        """,
    )


def devops_doc(platform: Path) -> str:
    return md(
        "DevOps",
        f"""
        ## Default Strategy
        Use the shared platform library whenever this project fits the standard POC architecture.

        ## Shared Library
        `{platform}`

        ## Shared Rules
        Start with `PROJECT_RULES.md`, then use the detailed rule files in `{platform / "rules"}`.

        ## GitHub Organization Target
        Later, move the platform folder to a repository such as `your-org/platform`.
        Each POC/product repo can then call reusable workflows:

        ```yaml
        jobs:
          ci:
            uses: your-org/platform/.github/workflows/python-poc-ci.yml@main
            with:
              backend_path: backend/app.py
        ```

        ## Terraform Modules
        Keep `infra/terraform/main.tf` small and call shared modules for standard Vercel, AWS, and database resources.

        ## Local Overrides
        Add local workflows or Terraform modules only when this project has a different architecture than the shared templates support.
        """,
    )


def project_rules_doc(platform: Path) -> str:
    rules = platform / "rules"
    hooks = platform / "hooks"
    templates = platform / "templates"
    return md(
        "Project Rules",
        f"""
        This project should follow the shared platform rules unless it has an explicit local exception.

        ## Shared Rulebook
        - Security: `{rules / "security.md"}`
        - Git: `{rules / "git.md"}`
        - GitHub: `{rules / "github.md"}`
        - CI/CD: `{rules / "ci-cd.md"}`
        - Deployment: `{rules / "deployment.md"}`
        - Terraform: `{rules / "terraform.md"}`
        - Observability: `{rules / "observability.md"}`
        - Readiness: `{rules / "project-readiness.md"}`

        ## Shared Hooks
        - Pre-commit: `{hooks / "pre-commit"}`

        ## Shared Templates
        - Pull request template: `{templates / "pull_request_template.md"}`
        - Issue template: `{templates / "issue_template.md"}`
        - CODEOWNERS: `{templates / "CODEOWNERS"}`
        - Dependabot: `{templates / "dependabot.yml"}`

        ## Local Exceptions
        Add project-local infra, workflows, or rules only when this project differs materially from the standard platform architecture.
        Document exceptions in `docs/devops.md`.
        """,
    )


def write_handoff(root: Path, idea: Idea) -> Path:
    path = ensure_idea_folder(root, idea)
    write_text(path / "handoff.md", handoff_brief(idea))
    return path


def idea_readme(idea: Idea) -> str:
    return md(
        idea.title,
        f"""
        ## Status
        `{idea.status}`

        ## Category
        `{idea.category}`

        ## Why This Exists
        {idea.why or "No captured rationale yet."}

        ## Current Score
        {idea.score:.1f}

        ## Files
        - `research.md`
        - `debate.md`
        - `implementation_plan.md`
        - `crew_transcripts.md`
        - `acceptance_tests.md`
        - `poc_report.md`
        - `poc_location.md`
        - `handoff.md`
        - `openspec/`
        """,
    )


def is_poc_feasible(idea: Idea) -> bool:
    text = f"{idea.title} {idea.why}".lower()
    blockers = ("paid api", "stripe live", "production deploy", "hardware", "credential", "oauth")
    return not any(blocker in text for blocker in blockers)
