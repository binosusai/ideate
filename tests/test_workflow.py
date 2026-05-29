from __future__ import annotations

import sqlite3
import subprocess
import time
from pathlib import Path
import pytest

from ideate.cli import build_iteration_context, is_eligible_for_auto_pick, main
from ideate.db import Store
from ideate.projects import poc_dir


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
    assert (poc / "run-local.sh").exists()
    assert (poc / "scripts" / "smoke_check.py").exists()
    assert (poc / "poc.capsule.json").exists()
    assert (poc / "ecosystem.profile.yaml").exists()
    assert (poc / "deploy.targets.json").exists()
    assert (poc / "infra" / "terraform" / "main.tf").exists()
    assert (poc / ".github" / "workflows" / "poc-ci.yml").exists()
    assert (poc / "docs" / "local_setup.md").exists()
    assert (poc / "docs" / "deployment.md").exists()
    assert (poc / "docs" / "architecture.md").exists()
    assert (poc / "docs" / "poc_capsule.md").exists()
    assert (poc / "docs" / "devops.md").exists()
    assert (poc / "PROJECT_RULES.md").exists()
    assert (tmp_path.parent / "pocs" / "_common" / "README.md").exists()

    poc_readme = (poc / "README.md").read_text(encoding="utf-8")
    architecture = (poc / "docs" / "architecture.md").read_text(encoding="utf-8")
    terraform = (poc / "infra" / "terraform" / "main.tf").read_text(encoding="utf-8")
    workflow = (poc / ".github" / "workflows" / "poc-ci.yml").read_text(encoding="utf-8")
    rules = (poc / "PROJECT_RULES.md").read_text(encoding="utf-8")
    runner = (poc / "run-local.sh").read_text(encoding="utf-8")
    capsule = (poc / "poc.capsule.json").read_text(encoding="utf-8")
    ecosystem = (poc / "ecosystem.profile.yaml").read_text(encoding="utf-8")

    assert "```mermaid" in poc_readme
    assert "flowchart LR" in poc_readme
    assert "## Component Diagram" in poc_readme
    assert "./run-local.sh" in poc_readme
    assert architecture.count("```mermaid") >= 2
    assert "## Request Flow" in architecture
    assert "sequenceDiagram" in architecture

    assert "terraform-modules/vercel-static-site" in terraform
    assert "your-org/platform/.github/workflows/python-poc-ci.yml@main" in workflow
    assert "rules/security.md" in rules
    assert "hooks/pre-commit" in rules
    assert "python3 backend/app.py" in runner
    assert "ideate.poc-capsule.v1" in capsule
    assert "run-local.sh" in capsule
    assert "deploy:" in ecosystem

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


def test_generated_poc_runs_local_smoke_check(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("IDEATE_SKIP_GITHUB_REPO_CREATE", "1")
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Runnable capsule idea", "--category", "money") == 0
    assert run(tmp_path, "approve", "1") == 0
    assert run(tmp_path, "poc", "1", "--force") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    poc = poc_dir(tmp_path, store.get_idea(1))
    assert poc.exists()

    proc = subprocess.Popen(
        ["./run-local.sh"],
        cwd=poc,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.time() + 8
        last_error = ""
        while time.time() < deadline:
            smoke = subprocess.run(
                ["python3", "scripts/smoke_check.py"],
                cwd=poc,
                capture_output=True,
                text=True,
            )
            if smoke.returncode == 0:
                assert "POC smoke check passed" in smoke.stdout
                break
            last_error = smoke.stderr or smoke.stdout
            time.sleep(0.4)
        else:
            if "Operation not permitted" in last_error:
                pytest.skip("localhost socket checks are blocked in this sandbox")
            raise AssertionError(f"POC smoke check did not pass: {last_error}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=4)
        except subprocess.TimeoutExpired:
            proc.kill()


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


def test_capture_preserves_all_non_core_yaml_fields(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    payload = tmp_path / "idea.yaml"
    payload.write_text(
        """title: Structured idea
category: engineering productivity
why: Preserve everything.
version: 0.1.0
status: draft
meta_intent:
  core_purpose: capture richer context
problem_definition:
  statement: top-level fields should not disappear
details:
  domain: developer tools
  target_users:
    - builders
""",
        encoding="utf-8",
    )

    assert run(tmp_path, "capture", "--from-yaml", str(payload)) == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    idea = store.get_idea(1)
    assert idea.category == "money"
    assert idea.details == {
        "domain": "developer tools",
        "target_users": ["builders"],
        "version": "0.1.0",
        "status": "draft",
        "meta_intent": {"core_purpose": "capture richer context"},
        "problem_definition": {"statement": "top-level fields should not disappear"},
        "source_category": "engineering productivity",
        "category_note": "Stored category as 'money' because Ideate currently supports: money, personal.",
    }
    assert "problem_definition" in idea.why


def test_examples_context_is_synced_before_proposals(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Structured proposal idea", "--category", "money") == 0
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "idea.structured-proposal-idea.yaml").write_text(
        """title: Structured proposal idea
category: money
why: Respect the detailed example before proposal generation.
details:
  domain: proposal control plane
  target_users:
    - builders
  mvp:
    must_have:
      - proposal uses example context
""",
        encoding="utf-8",
    )

    assert run(tmp_path, "plan", "1") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    idea = store.get_idea(1)
    assert idea.details == {
        "domain": "proposal control plane",
        "target_users": ["builders"],
        "mvp": {"must_have": ["proposal uses example context"]},
    }

    proposal = (
        tmp_path
        / "ideas"
        / idea.slug
        / "openspec"
        / "changes"
        / idea.slug
        / "proposal.md"
    ).read_text(encoding="utf-8")
    assert "Respect the detailed example before proposal generation." in proposal
    assert "## Idea Details" in proposal
    assert "proposal control plane" in proposal


def test_examples_sync_updates_database_context(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Database-backed idea", "--category", "money") == 0
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "idea.database-backed-idea.yaml").write_text(
        """title: Database-backed idea
category: money
why: Push rich details before agents run.
details:
  domain: neon-backed agent memory
  acceptance_criteria:
    - research uses full context
    - debate uses full context
""",
        encoding="utf-8",
    )

    assert run(tmp_path, "examples-sync") == 0

    store = Store(tmp_path / ".ideate" / "ideate.sqlite3")
    idea = store.get_idea(1)
    assert "Push rich details before agents run." in idea.why
    assert idea.details == {
        "domain": "neon-backed agent memory",
        "acceptance_criteria": [
            "research uses full context",
            "debate uses full context",
        ],
    }


def test_yaml_context_change_bypasses_cached_plan_before_proposal(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Cached context idea", "--category", "money") == 0
    assert run(tmp_path, "plan", "1") == 0

    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "idea.cached-context-idea.yaml").write_text(
        """title: Cached context idea
category: money
why: Fresh YAML context must drive the proposal.
details:
  domain: fresh proposal context
  mvp:
    must_have:
      - regenerate stale planning artifacts
""",
        encoding="utf-8",
    )

    assert run(tmp_path, "plan", "1") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        plan_count = conn.execute(
            "SELECT COUNT(*) FROM artifacts WHERE idea_id = 1 AND kind = 'plan'"
        ).fetchone()[0]
    assert plan_count == 2

    store = Store(db_path)
    idea = store.get_idea(1)
    proposal = (
        tmp_path
        / "ideas"
        / idea.slug
        / "openspec"
        / "changes"
        / idea.slug
        / "proposal.md"
    ).read_text(encoding="utf-8")
    assert "Fresh YAML context must drive the proposal." in proposal
    assert "fresh proposal context" in proposal


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


def test_poc_status_is_not_auto_picked_even_with_legacy_review_state(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Legacy POC", "--category", "money") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE ideas
            SET status = 'poc',
                review_status = 'new',
                tinkered = 0
            WHERE id = 1
            """
        )

    store = Store(db_path)
    legacy = store.get_idea(1)
    assert is_eligible_for_auto_pick(legacy) is False


def test_poc_revision_is_not_auto_picked_without_explicit_rerun(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Needs revision", "--category", "money") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE ideas
            SET status = 'poc',
                review_status = 'revise',
                tinkered = 0
            WHERE id = 1
            """
        )

    store = Store(db_path)
    revision = store.get_idea(1)
    assert is_eligible_for_auto_pick(revision) is False


def test_daily_skips_unapproved_ideas_and_picks_another(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(tmp_path, "init") == 0
    assert run(
        tmp_path,
        "capture",
        "High scoring SaaS customer workflow agent",
        "--category",
        "money",
    ) == 0
    assert run(tmp_path, "capture", "Another respected idea", "--category", "money") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE ideas
            SET status = 'planned',
                review_status = 'new',
                score = 99
            WHERE id = 1
            """
        )
        conn.execute(
            """
            UPDATE ideas
            SET score = 50
            WHERE id = 2
            """
        )

    assert run(tmp_path, "daily") == 0
    captured = capsys.readouterr()
    assert "Primary focus: 2. [money] Another respected idea" in captured.out


def test_daily_does_not_fallback_to_waiting_proposals(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Waiting proposal", "--category", "money") == 0
    assert run(tmp_path, "capture", "Waiting POC review", "--category", "money") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE ideas
            SET status = 'planned',
                score = 99
            WHERE id = 1
            """
        )
        conn.execute(
            """
            UPDATE ideas
            SET status = 'poc',
                review_status = 'pending_review',
                score = 98
            WHERE id = 2
            """
        )

    assert run(tmp_path, "daily") == 0
    captured = capsys.readouterr()
    assert "No auto-pickable ideas right now." in captured.out
    assert "Waiting on human decisions:" in captured.out
    assert "Primary focus:" not in captured.out


def test_init_repairs_legacy_poc_review_state(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Stale review state", "--category", "money") == 0

    db_path = tmp_path / ".ideate" / "ideate.sqlite3"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE ideas
            SET status = 'poc',
                review_status = 'new',
                iteration_count = 0
            WHERE id = 1
            """
        )

    assert run(tmp_path, "init") == 0

    store = Store(db_path)
    repaired = store.get_idea(1)
    assert repaired.review_status == "pending_review"
    assert repaired.iteration_count == 1


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
