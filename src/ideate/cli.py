from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from .agents import debate_brief, research_brief
from .board_sync import AgentTaskUpdate, sync_agent_tasks
from .crew import run_debate_crew, run_planning_crew, run_research_crew
from .db import PgStore, Store
from .models import CATEGORIES
from .projects import refresh_readme, write_handoff, write_openspec, write_planning_files, write_poc


STAGE_MEMBERS: dict[str, list[str]] = {
    "research": ["Market Researcher", "User Researcher", "Technical Scout"],
    "debate": ["Advocate", "Skeptic", "Builder", "Strategist"],
    "planning": [
        "Product Planner",
        "POC Coder",
        "Frontend Engineer",
        "Backend Engineer",
        "Auth Engineer",
        "Database Engineer",
        "Infra Engineer",
        "DevOps Engineer",
        "OpenSpec Writer",
    ],
    "poc": ["POC Builder"],
}


def _mark_stage_reused(idea, stage: str, summary: str) -> None:
    sync_agent_tasks(
        idea,
        stage,
        [AgentTaskUpdate(name, "done", summary) for name in STAGE_MEMBERS.get(stage, [])],
    )


def _agentops_init() -> bool:
    """Start an AgentOps session if AGENTOPS_API_KEY is set. Returns True if started."""
    api_key = os.environ.get("AGENTOPS_API_KEY")
    if not api_key:
        return False
    try:
        import agentops  # type: ignore[import]

        agentops.init(
            api_key=api_key,
            auto_start_session=True,
            instrument_llm_calls=True,
        )
        return True
    except Exception:
        return False


def _agentops_end(started: bool, success: bool) -> None:
    if not started:
        return
    try:
        import agentops  # type: ignore[import]

        agentops.end_session("Success" if success else "Fail")
    except Exception:
        pass


def project_root() -> Path:
    return Path(os.environ.get("IDEATE_HOME", Path.cwd())).resolve()


def terraform_database_url(root: Path) -> str | None:
    """Read DATABASE_URL from terraform output if infra is configured."""
    if os.environ.get("IDEATE_DISABLE_TERRAFORM_DB") == "1":
        return None
    tf_dir = root / "infra" / "terraform"
    if not tf_dir.exists():
        return None
    try:
        result = subprocess.run(
            ["terraform", "output", "-raw", "database_url"],
            cwd=tf_dir,
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def store_for(root: Path) -> Store | PgStore:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        database_url = terraform_database_url(root)
    if os.environ.get("IDEATE_REQUIRE_DATABASE_URL") == "1" and not database_url:
        raise RuntimeError(
            "DATABASE_URL is required for this run. Configure Neon/Postgres and try again."
        )
    if database_url:
        return PgStore(database_url)
    return Store(root / ".ideate" / "ideate.sqlite3")


def is_eligible_for_auto_pick(idea) -> bool:
    return not idea.tinkered and idea.review_status != "pending_review" and idea.status not in {
        "handoff",
        "completed",
        "killed",
        "paused",
    }


def build_iteration_context(store: Store | PgStore, idea_id: int) -> dict[str, str]:
    decision = store.latest_decision(idea_id)
    return {
        "previous_research": store.latest_artifact(idea_id, "research") or "",
        "previous_debate": store.latest_artifact(idea_id, "debate") or "",
        "previous_plan": store.latest_artifact(idea_id, "plan") or "",
        "previous_decision": decision[0] if decision else "",
        "previous_decision_rationale": decision[1] if decision else "",
        "review_feedback": store.get_idea(idea_id).review_feedback or "",
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if getattr(args, "root", None) else project_root()
    store = store_for(root)
    ao_started = _agentops_init()

    try:
        if args.command == "init":
            store.init()
            (root / "ideas").mkdir(parents=True, exist_ok=True)
            print(f"Initialized Ideate at {root}")
            return 0

        store.init()

        if args.command == "capture":
            idea = store.add_idea(args.title, args.category, args.why or "")
            store.log_run("capture", f"Captured idea {idea.id}: {idea.title}", idea.id)
            print(format_idea(idea))
            return 0

        if args.command == "list":
            ideas = store.list_ideas(args.status)
            print_ideas(ideas)
            return 0

        if args.command == "daily":
            ideas = store.list_ideas()
            print_daily(ideas)
            store.log_run("daily", f"Reviewed {len(ideas)} ideas")
            return 0

        if args.command == "openspec":
            idea = store.get_idea(args.idea_id)
            path = root / "ideas" / idea.slug

            def _read_file_or_db(artifact_kind: str, filename: str) -> str:
                from_db = store.latest_artifact(idea.id, artifact_kind) or ""
                if from_db:
                    return from_db
                disk_path = path / filename
                return disk_path.read_text(encoding="utf-8").strip() if disk_path.exists() else ""

            research = _read_file_or_db("research", "research.md")
            debate = _read_file_or_db("debate", "debate.md")
            plan = _read_file_or_db("plan", "implementation_plan.md")
            write_openspec(path, idea, research=research, debate=debate, plan=plan)
            print(f"Regenerated openspec for idea {idea.id} at {path / 'openspec'}")
            return 0

        if args.command == "board-setup":
            idea = store.get_idea(args.idea_id)
            for stage in [s.strip() for s in args.stages.split(",") if s.strip()]:
                members = STAGE_MEMBERS.get(stage, [])
                if members:
                    try:
                        sync_agent_tasks(
                            idea,
                            stage,
                            [AgentTaskUpdate(name, "todo") for name in members],
                        )
                    except Exception as exc:
                        print(
                            f"[ideate] board-setup warning for stage '{stage}': {exc}",
                            file=sys.stderr,
                        )
            return 0

        idea = store.get_idea(args.idea_id)

        def mark_task_done(stage: str):
            def _mark(agent_name: str, output: str) -> None:
                sync_agent_tasks(
                    idea,
                    stage,
                    [AgentTaskUpdate(agent_name, "done", output)],
                )

            return _mark

        if args.command == "research":
            cached = store.latest_artifact(idea.id, "research")
            if cached and not args.force_refresh:
                _mark_stage_reused(idea, "research", "Reused cached research artifact.")
                store.set_status(idea.id, "researched")
                print(cached)
                return 0

            sync_agent_tasks(
                idea,
                "research",
                [AgentTaskUpdate(name, "in_progress") for name in STAGE_MEMBERS["research"]],
            )
            iteration_context = build_iteration_context(store, idea.id)
            result = run_research_crew(
                idea,
                context=iteration_context,
                on_member_complete=mark_task_done("research"),
            )
            content = result.synthesis
            store.add_artifact(idea.id, "research", content)
            store.add_artifact(idea.id, "crew-research", result.transcript)
            store.set_status(idea.id, "researched")
            print(content)
            return 0

        if args.command == "debate":
            cached = store.latest_artifact(idea.id, "debate")
            if cached and not args.force_refresh:
                _mark_stage_reused(idea, "debate", "Reused cached debate artifact.")
                store.set_status(idea.id, "debated")
                print(cached)
                return 0

            sync_agent_tasks(
                idea,
                "debate",
                [AgentTaskUpdate(name, "in_progress") for name in STAGE_MEMBERS["debate"]],
            )
            research = store.latest_artifact(idea.id, "research")
            iteration_context = build_iteration_context(store, idea.id)
            result = run_debate_crew(
                idea,
                research,
                extra_context=iteration_context,
                on_member_complete=mark_task_done("debate"),
            )
            content = result.synthesis
            store.add_artifact(idea.id, "debate", content)
            store.add_artifact(idea.id, "crew-debate", result.transcript)
            store.set_status(idea.id, "debated")
            print(content)
            return 0

        if args.command == "plan":
            cached_plan = store.latest_artifact(idea.id, "plan")
            if cached_plan and not args.force_refresh:
                research = store.latest_artifact(idea.id, "research") or research_brief(idea)
                debate = store.latest_artifact(idea.id, "debate") or debate_brief(idea, research)
                _mark_stage_reused(idea, "planning", "Reused cached plan artifact.")
                store.set_status(idea.id, "planned")
                planned = store.get_idea(idea.id)
                crew_transcripts = [
                    value
                    for value in (
                        store.latest_artifact(idea.id, "crew-research"),
                        store.latest_artifact(idea.id, "crew-debate"),
                        store.latest_artifact(idea.id, "crew-planning"),
                    )
                    if value
                ]
                path = write_planning_files(root, planned, research, debate, cached_plan, crew_transcripts)
                print(f"Planned idea {idea.id} at {path}")
                return 0

            sync_agent_tasks(
                idea,
                "planning",
                [AgentTaskUpdate(name, "in_progress") for name in STAGE_MEMBERS["planning"]],
            )
            research = store.latest_artifact(idea.id, "research") or research_brief(idea)
            debate = store.latest_artifact(idea.id, "debate") or debate_brief(idea, research)
            result = run_planning_crew(
                idea,
                research,
                debate,
                on_member_complete=mark_task_done("planning"),
            )
            plan = result.synthesis
            store.add_artifact(idea.id, "research", research)
            store.add_artifact(idea.id, "debate", debate)
            store.add_artifact(idea.id, "plan", plan)
            store.add_artifact(idea.id, "crew-planning", result.transcript)
            store.set_status(idea.id, "planned")
            planned = store.get_idea(idea.id)
            crew_transcripts = [
                value
                for value in (
                    store.latest_artifact(idea.id, "crew-research"),
                    store.latest_artifact(idea.id, "crew-debate"),
                    result.transcript,
                )
                if value
            ]
            path = write_planning_files(root, planned, research, debate, plan, crew_transcripts)
            print(f"Planned idea {idea.id} at {path}")
            return 0

        if args.command == "approve":
            store.set_status(idea.id, "approved")
            store.add_decision(idea.id, "approved", args.rationale or "Approved by user.")
            refresh_readme(root, store.get_idea(idea.id))
            print(f"Approved idea {idea.id}: {idea.title}")
            return 0

        if args.command == "review":
            if args.decision == "approve":
                store.set_review_state(idea.id, "approved", tinkered=True)
                store.add_decision(idea.id, "poc-approved", args.feedback or "POC approved by user.")
                print(f"POC approved for idea {idea.id}: {idea.title}")
            else:
                note = args.feedback or "POC needs another iteration."
                store.set_review_state(
                    idea.id,
                    "revise",
                    review_feedback=note,
                    tinkered=False,
                )
                store.add_decision(idea.id, "poc-revise", note)
                print(f"POC marked for revision for idea {idea.id}: {idea.title}")
            refresh_readme(root, store.get_idea(idea.id))
            return 0

        if args.command == "poc":
            if idea.status not in {"approved", "poc", "handoff"} and not args.force:
                print("POC requires approved status. Use --force to override.", file=sys.stderr)
                return 2
            feasible = write_poc(root, idea, force_build=args.force)
            store.set_status(idea.id, "poc")
            store.set_review_state(
                idea.id,
                "pending_review",
                review_feedback="",
                tinkered=False,
                increment_iteration=True,
            )
            refresh_readme(root, store.get_idea(idea.id))
            print(f"POC {'created' if feasible else 'skipped'} for idea {idea.id}")
            return 0

        if args.command == "handoff":
            if idea.status not in {"poc", "handoff"} and not args.force:
                print("Handoff requires POC status. Use --force to override.", file=sys.stderr)
                return 2
            path = write_handoff(root, idea)
            store.set_status(idea.id, "handoff")
            store.add_decision(idea.id, "handoff-ready", "Packaged for engineering crew.")
            refresh_readme(root, store.get_idea(idea.id))
            print(f"Handoff ready at {path}")
            return 0

        parser.error(f"unknown command {args.command}")
    except (KeyError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        _agentops_end(ao_started, success=False)
        return 1

    _agentops_end(ao_started, success=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="idea", description="Idea Implementation AI Agent Crew")
    parser.add_argument("--root", help="Project root. Defaults to current directory or IDEATE_HOME.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize local database and folders")

    capture = sub.add_parser("capture", help="Capture a new idea")
    capture.add_argument("title")
    capture.add_argument("--category", choices=sorted(CATEGORIES), default="money")
    capture.add_argument("--why", default="")

    list_cmd = sub.add_parser("list", help="List ideas")
    list_cmd.add_argument("--status")

    sub.add_parser("daily", help="Show daily review")

    for name in ("research", "debate", "plan"):
        cmd = sub.add_parser(name, help=f"{name.title()} an idea")
        cmd.add_argument("idea_id", type=int)
        cmd.add_argument(
            "--force-refresh",
            action="store_true",
            help="Ignore cached artifact and regenerate this stage.",
        )

    approve = sub.add_parser("approve", help="Approve an idea")
    approve.add_argument("idea_id", type=int)
    approve.add_argument("--rationale", default="")

    review = sub.add_parser("review", help="Record the result of reviewing a generated POC")
    review.add_argument("idea_id", type=int)
    review.add_argument("--decision", choices=["approve", "revise"], required=True)
    review.add_argument("--feedback", default="")

    poc = sub.add_parser("poc", help="Create a draft POC")
    poc.add_argument("idea_id", type=int)
    poc.add_argument("--force", action="store_true")

    handoff = sub.add_parser("handoff", help="Package for engineering crew")
    handoff.add_argument("idea_id", type=int)
    handoff.add_argument("--force", action="store_true")

    openspec_cmd = sub.add_parser("openspec", help="Regenerate openspec files from existing research/debate/plan artifacts")
    openspec_cmd.add_argument("idea_id", type=int)

    board_setup = sub.add_parser("board-setup", help="Pre-create TODO task issues for all agents in given stages")
    board_setup.add_argument("idea_id", type=int)
    board_setup.add_argument("--stages", default="research,debate,planning,poc", help="Comma-separated stages")

    return parser


def format_idea(idea) -> str:
    return f"{idea.id}. [{idea.category}] {idea.title} ({idea.status}, score={idea.score:.1f})"


def print_ideas(ideas) -> None:
    if not ideas:
        print("No ideas yet. Capture one with: idea capture \"...\"")
        return
    for idea in ideas:
        print(format_idea(idea))


def print_daily(ideas) -> None:
    print("Daily Idea Review")
    print("=================")
    if not ideas:
        print("No ideas captured yet.")
        print('Prompt: What exciting idea crossed your mind today? Capture it with `idea capture "..."`.')
        return

    eligible = [idea for idea in ideas if is_eligible_for_auto_pick(idea)]
    ranked = eligible or ideas
    money = [idea for idea in ranked if idea.category == "money"]
    personal = [idea for idea in ranked if idea.category == "personal"]
    focus = ranked[0]
    print(f"Primary focus: {format_idea(focus)}")
    if money:
        print(f"Money lane leader: {format_idea(money[0])}")
    if personal:
        print(f"Personal lane reminder: {format_idea(personal[0])}")
    print("\nNext action:")
    if focus.review_status == "pending_review":
        print(f"Review the current POC for idea {focus.id} before selecting another idea.")
    elif focus.review_status == "revise":
        print(f"Run: idea research {focus.id}")
    elif focus.status == "captured":
        print(f"Run: idea research {focus.id}")
    elif focus.status == "researched":
        print(f"Run: idea debate {focus.id}")
    elif focus.status == "debated":
        print(f"Run: idea plan {focus.id}")
    elif focus.status == "planned":
        print(f"Run: idea approve {focus.id}")
    elif focus.status == "approved":
        print(f"Run: idea poc {focus.id}")
    elif focus.status == "poc":
        print(f"Run: idea handoff {focus.id}")
    else:
        print("Capture another idea or review completed handoffs.")


if __name__ == "__main__":
    raise SystemExit(main())
