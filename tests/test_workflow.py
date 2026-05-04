from __future__ import annotations

import sqlite3
from pathlib import Path

from ideate.cli import build_iteration_context, is_eligible_for_auto_pick, main
from ideate.db import Store


def run(root: Path, *args: str) -> int:
    return main(["--root", str(root), *args])


def test_full_idea_workflow_creates_openspec_and_poc(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("IDEATE_SKIP_GITHUB_REPO_CREATE", "1")
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Dollar idea agent", "--category", "money", "--why", "sell workflow automation") == 0
    assert run(tmp_path, "research", "1") == 0
    assert run(tmp_path, "debate", "1") == 0
    assert run(tmp_path, "plan", "1") == 0
    assert run(tmp_path, "approve", "1") == 0
    assert run(tmp_path, "poc", "1") == 0
    assert run(tmp_path, "handoff", "1") == 0

    idea_folders = [p for p in (tmp_path / "ideas").iterdir() if p.is_dir()]
    assert len(idea_folders) == 1
    idea = idea_folders[0]
    idea_slug = idea.name
    assert "-" not in idea_slug
    assert len(idea_slug) <= 12
    assert (idea / "README.md").exists()
    assert (idea / "openspec" / "changes" / idea_slug / "proposal.md").exists()
    assert (idea / "openspec" / "changes" / idea_slug / "design.md").exists()
    assert (idea / "openspec" / "changes" / idea_slug / "tasks.md").exists()
    assert (idea / "crew_transcripts.md").exists()
    assert (idea / "poc_location.md").exists()
    assert not (idea / "draft_project").exists()
    assert (idea / "handoff.md").exists()

    pocs_root = tmp_path.parent / "pocs"
    generated = [p for p in pocs_root.iterdir() if p.is_dir() and p.name != "_common"]
    assert len(generated) == 1
    poc = generated[0]
    assert "-" not in poc.name
    assert len(poc.name) <= 12
    assert (poc / "frontend" / "index.html").exists()
    assert (poc / "backend" / "app.py").exists()
    assert (poc / "infra" / "terraform" / "main.tf").exists()
    assert (poc / ".github" / "workflows" / "poc-ci.yml").exists()
    assert (poc / "docs" / "local_setup.md").exists()
    assert (poc / "docs" / "deployment.md").exists()
    assert (poc / "docs" / "architecture.md").exists()
    assert (poc / "docs" / "devops.md").exists()
    assert (poc / "PROJECT_RULES.md").exists()
    assert (tmp_path.parent / "pocs" / "_common" / "README.md").exists()

    poc_readme = (poc / "README.md").read_text(encoding="utf-8")
    architecture = (poc / "docs" / "architecture.md").read_text(encoding="utf-8")
    terraform = (poc / "infra" / "terraform" / "main.tf").read_text(encoding="utf-8")
    workflow = (poc / ".github" / "workflows" / "poc-ci.yml").read_text(encoding="utf-8")
    rules = (poc / "PROJECT_RULES.md").read_text(encoding="utf-8")

    assert "```mermaid" in poc_readme
    assert "flowchart LR" in poc_readme
    assert "## Component Diagram" in poc_readme
    assert architecture.count("```mermaid") >= 2
    assert "## Request Flow" in architecture
    assert "sequenceDiagram" in architecture

    assert "terraform-modules/vercel-static-site" in terraform
    assert "your-org/platform/.github/workflows/python-poc-ci.yml@main" in workflow
    assert "rules/security.md" in rules
    assert "hooks/pre-commit" in rules

    tasks = (idea / "openspec" / "changes" / idea_slug / "tasks.md").read_text(encoding="utf-8")
    assert "## Implementation Tasks" in tasks
    assert "- [ ] 1." in tasks
    assert "- [ ] 1.1" in tasks
    assert "## Tracking" in tasks
    assert "## Implementation Plan" not in tasks


def test_poc_requires_approval_without_force(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Personal dashboard", "--category", "personal") == 0
    assert run(tmp_path, "poc", "1") == 2


def test_daily_handles_empty_database(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "daily") == 0


def test_poc_enters_pending_review_and_blocks_auto_pick(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("IDEATE_SKIP_GITHUB_REPO_CREATE", "1")
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "First idea", "--category", "money") == 0
    assert run(tmp_path, "capture", "Second idea", "--category", "money") == 0
    assert run(tmp_path, "approve", "1") == 0
    assert run(tmp_path, "poc", "1", "--force") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    first = store.get_idea(1)
    second = store.get_idea(2)

    assert first.review_status == "pending_review"
    assert first.tinkered is False
    assert first.iteration_count == 1
    assert is_eligible_for_auto_pick(first) is False
    assert is_eligible_for_auto_pick(second) is True


def test_review_feedback_is_cached_for_next_iteration(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("IDEATE_SKIP_GITHUB_REPO_CREATE", "1")
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Proxy gateway", "--category", "money") == 0
    assert run(tmp_path, "research", "1") == 0
    assert run(tmp_path, "debate", "1") == 0
    assert run(tmp_path, "plan", "1") == 0
    assert run(tmp_path, "approve", "1") == 0
    assert run(tmp_path, "poc", "1", "--force") == 0
    assert run(
        tmp_path,
        "review",
        "1",
        "--decision",
        "revise",
        "--feedback",
        "Make onboarding simpler and tighten the proxy flow.",
    ) == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    idea = store.get_idea(1)
    context = build_iteration_context(store, 1)

    assert idea.review_status == "revise"
    assert idea.tinkered is False
    assert idea.review_feedback == "Make onboarding simpler and tighten the proxy flow."
    assert context["review_feedback"] == "Make onboarding simpler and tighten the proxy flow."
    assert context["previous_research"]
    assert context["previous_debate"]
    assert context["previous_plan"]
    assert context["previous_decision"] == "poc-revise"


def test_stage_commands_reuse_cached_artifacts_and_keep_openspec_context(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Unified API Gateway", "--category", "money") == 0
    assert run(tmp_path, "research", "1") == 0
    assert run(tmp_path, "debate", "1") == 0
    assert run(tmp_path, "plan", "1") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        counts_before = {
            kind: conn.execute(
                "SELECT COUNT(*) FROM artifacts WHERE idea_id = 1 AND kind = ?",
                (kind,),
            ).fetchone()[0]
            for kind in ("research", "debate", "plan")
        }

    # These reruns should reuse cached artifacts, not append duplicate artifacts.
    assert run(tmp_path, "research", "1") == 0
    assert run(tmp_path, "debate", "1") == 0
    assert run(tmp_path, "plan", "1") == 0

    with sqlite3.connect(db_path) as conn:
        counts_after = {
            kind: conn.execute(
                "SELECT COUNT(*) FROM artifacts WHERE idea_id = 1 AND kind = ?",
                (kind,),
            ).fetchone()[0]
            for kind in ("research", "debate", "plan")
        }

    assert counts_after == counts_before

    idea_folder = next((tmp_path / "ideas").iterdir())
    proposal = (
        idea_folder
        / "openspec"
        / "changes"
        / idea_folder.name
        / "proposal.md"
    ).read_text(encoding="utf-8")
    spec = (
        idea_folder
        / "openspec"
        / "changes"
        / idea_folder.name
        / "specs"
        / "unified-api-gateway"
        / "spec.md"
    ).read_text(encoding="utf-8")

    assert "## Research Context" in proposal
    assert "## Debate Context" in proposal
    assert "## Implementation Plan" in spec
