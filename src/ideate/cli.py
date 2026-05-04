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
from .projects import refresh_readme, write_handoff, write_planning_files, write_poc


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
}


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
    if database_url:
        return PgStore(database_url)
    return Store(root / ".ideate" / "ideate.sqlite3")


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

        idea = store.get_idea(args.idea_id)

        if args.command == "research":
            sync_agent_tasks(
                idea,
                "research",
                [AgentTaskUpdate(name, "in_progress") for name in STAGE_MEMBERS["research"]],
            )
            result = run_research_crew(idea)
            sync_agent_tasks(
                idea,
                "research",
                [
                    AgentTaskUpdate(name, "done", output)
                    for name, output in result.member_outputs.items()
                ],
            )
            content = result.synthesis
            store.add_artifact(idea.id, "research", content)
            store.add_artifact(idea.id, "crew-research", result.transcript)
            store.set_status(idea.id, "researched")
            print(content)
            return 0

        if args.command == "debate":
            sync_agent_tasks(
                idea,
                "debate",
                [AgentTaskUpdate(name, "in_progress") for name in STAGE_MEMBERS["debate"]],
            )
            research = store.latest_artifact(idea.id, "research")
            result = run_debate_crew(idea, research)
            sync_agent_tasks(
                idea,
                "debate",
                [
                    AgentTaskUpdate(name, "done", output)
                    for name, output in result.member_outputs.items()
                ],
            )
            content = result.synthesis
            store.add_artifact(idea.id, "debate", content)
            store.add_artifact(idea.id, "crew-debate", result.transcript)
            store.set_status(idea.id, "debated")
            print(content)
            return 0

        if args.command == "plan":
            sync_agent_tasks(
                idea,
                "planning",
                [AgentTaskUpdate(name, "in_progress") for name in STAGE_MEMBERS["planning"]],
            )
            research = store.latest_artifact(idea.id, "research") or research_brief(idea)
            debate = store.latest_artifact(idea.id, "debate") or debate_brief(idea, research)
            result = run_planning_crew(idea, research, debate)
            sync_agent_tasks(
                idea,
                "planning",
                [
                    AgentTaskUpdate(name, "done", output)
                    for name, output in result.member_outputs.items()
                ],
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

        if args.command == "poc":
            if idea.status not in {"approved", "poc", "handoff"} and not args.force:
                print("POC requires approved status. Use --force to override.", file=sys.stderr)
                return 2
            feasible = write_poc(root, idea, force_build=args.force)
            store.set_status(idea.id, "poc")
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
    except (KeyError, ValueError) as exc:
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

    approve = sub.add_parser("approve", help="Approve an idea")
    approve.add_argument("idea_id", type=int)
    approve.add_argument("--rationale", default="")

    poc = sub.add_parser("poc", help="Create a draft POC")
    poc.add_argument("idea_id", type=int)
    poc.add_argument("--force", action="store_true")

    handoff = sub.add_parser("handoff", help="Package for engineering crew")
    handoff.add_argument("idea_id", type=int)
    handoff.add_argument("--force", action="store_true")

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

    money = [idea for idea in ideas if idea.category == "money"]
    personal = [idea for idea in ideas if idea.category == "personal"]
    focus = ideas[0]
    print(f"Primary focus: {format_idea(focus)}")
    if money:
        print(f"Money lane leader: {format_idea(money[0])}")
    if personal:
        print(f"Personal lane reminder: {format_idea(personal[0])}")
    print("\nNext action:")
    if focus.status == "captured":
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
