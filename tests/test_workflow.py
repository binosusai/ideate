from __future__ import annotations

import sqlite3
from pathlib import Path
import pytest

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
    assert (idea / "poc_quality_rubric.md").exists()
    assert (idea / "poc_quality_score.md").exists()
    assert (idea / "poc_improvement_loop.md").exists()
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

    quality_score = (idea / "poc_quality_score.md").read_text(encoding="utf-8")
    improvement_loop = (idea / "poc_improvement_loop.md").read_text(encoding="utf-8")
    assert "Deterministic Score" in quality_score
    assert "Total:" in quality_score
    assert "## Recommended Actions" in improvement_loop

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


def test_capture_supports_yaml_file(tmp_path: Path) -> None:
        assert run(tmp_path, "init") == 0
        payload = tmp_path / "idea.yaml"
        payload.write_text(
                """title: AI invoice follow-up assistant
category: money
why: I want a weekly pipeline that turns new invoices into polite reminders.
details:
    target_users:
        - independent consultants
        - agencies
    constraints:
        - no CRM required
        - email-first MVP
""",
                encoding="utf-8",
        )

        assert run(tmp_path, "capture", "--from-yaml", str(payload)) == 0

        store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
        idea = store.get_idea(1)
        assert idea.title == "AI invoice follow-up assistant"
        assert idea.category == "money"
        assert "Additional details from YAML" in idea.why
        assert idea.details == {
            "target_users": ["independent consultants", "agencies"],
            "constraints": ["no CRM required", "email-first MVP"],
        }


def test_daily_handles_empty_database(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "daily") == 0


def test_cli_prints_backend_banner(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(tmp_path, "init") == 0
    captured = capsys.readouterr()
    assert "[ideate] backend: sqlite" in captured.err


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


def test_store_rejects_invalid_status_transition(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Invalid transition test", "--category", "money") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    store.set_status(1, "killed")
    with pytest.raises(ValueError, match="invalid status transition"):
        store.set_status(1, "planned")


def test_store_allows_expected_linear_status_transitions(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Valid transition test", "--category", "money") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    for status in ["researched", "debated", "planned", "approved", "poc", "handoff", "completed"]:
        store.set_status(1, status)

    assert store.get_idea(1).status == "completed"


def test_research_fails_in_strict_iteration_context_when_prior_artifacts_missing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Strict context test", "--category", "money") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    store.set_review_state(1, "revise", review_feedback="Need better prior iteration continuity")

    monkeypatch.setenv("IDEATE_STRICT_ITERATION_CONTEXT", "1")
    assert run(tmp_path, "research", "1") == 1


def test_board_setup_fails_fast_when_token_missing(tmp_path: Path, monkeypatch) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Board setup preflight", "--category", "money") == 0

    monkeypatch.setenv("IDEATE_GITHUB_TASK_BOARD", "1")
    monkeypatch.setenv("IDEATE_TASKS_REPO", "owner/repo")
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    assert run(tmp_path, "board-setup", "1") == 1


def test_poc_quality_cycle_artifacts_exist_when_poc_is_skipped(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("IDEATE_SKIP_GITHUB_REPO_CREATE", "1")
    assert run(tmp_path, "init") == 0
    assert run(
        tmp_path,
        "capture",
        "Paid API gateway",
        "--category",
        "money",
        "--why",
        "Needs paid api integration",
    ) == 0
    assert run(tmp_path, "approve", "1") == 0
    assert run(tmp_path, "poc", "1") == 0

    idea = next((tmp_path / "ideas").iterdir())
    assert (idea / "poc_quality_rubric.md").exists()
    assert (idea / "poc_quality_score.md").exists()
    assert (idea / "poc_improvement_loop.md").exists()
