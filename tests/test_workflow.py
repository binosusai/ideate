from __future__ import annotations

from pathlib import Path

from ideate.cli import main


def run(root: Path, *args: str) -> int:
    return main(["--root", str(root), *args])


def test_full_idea_workflow_creates_openspec_and_poc(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Dollar idea agent", "--category", "money", "--why", "sell workflow automation") == 0
    assert run(tmp_path, "research", "1") == 0
    assert run(tmp_path, "debate", "1") == 0
    assert run(tmp_path, "plan", "1") == 0
    assert run(tmp_path, "approve", "1") == 0
    assert run(tmp_path, "poc", "1") == 0
    assert run(tmp_path, "handoff", "1") == 0

    idea = tmp_path / "ideas" / "dollar-idea-agent"
    assert (idea / "README.md").exists()
    assert (idea / "openspec" / "changes" / "dollar-idea-agent" / "proposal.md").exists()
    assert (idea / "openspec" / "changes" / "dollar-idea-agent" / "design.md").exists()
    assert (idea / "openspec" / "changes" / "dollar-idea-agent" / "tasks.md").exists()
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
    assert (poc / "docs" / "devops.md").exists()
    assert (poc / "PROJECT_RULES.md").exists()
    assert (tmp_path.parent / "pocs" / "_common" / "README.md").exists()

    terraform = (poc / "infra" / "terraform" / "main.tf").read_text(encoding="utf-8")
    workflow = (poc / ".github" / "workflows" / "poc-ci.yml").read_text(encoding="utf-8")
    rules = (poc / "PROJECT_RULES.md").read_text(encoding="utf-8")
    assert "terraform-modules/vercel-static-site" in terraform
    assert "your-org/platform/.github/workflows/python-poc-ci.yml@main" in workflow
    assert "rules/security.md" in rules
    assert "hooks/pre-commit" in rules


def test_poc_requires_approval_without_force(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "capture", "Personal dashboard", "--category", "personal") == 0
    assert run(tmp_path, "poc", "1") == 2


def test_daily_handles_empty_database(tmp_path: Path) -> None:
    assert run(tmp_path, "init") == 0
    assert run(tmp_path, "daily") == 0
