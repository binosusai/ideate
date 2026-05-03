from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

from .agents import debate_brief, implementation_plan, research_brief
from .models import Idea
from .text import bullet_list, md


def _record_crew_event(stage: str, idea_title: str, member_names: list[str], synthesis: str) -> None:
    """Record a crew run as an AgentOps ActionEvent. No-op if agentops is not available or not initialised."""
    try:
        import agentops  # type: ignore[import]

        agentops.record(
            agentops.ActionEvent(
                action_type=f"crew_{stage}",
                params={"stage": stage, "idea": idea_title, "agents": member_names},
                returns=synthesis[:1000],
            )
        )
    except Exception:
        pass


@dataclass(frozen=True)
class CrewMember:
    name: str
    role: str
    mission: str
    run: Callable[[Idea, dict[str, str]], str]


@dataclass(frozen=True)
class CrewResult:
    stage: str
    synthesis: str
    transcript: str
    member_outputs: dict[str, str]


def run_research_crew(idea: Idea) -> CrewResult:
    members = [
        CrewMember(
            "Market Researcher",
            "research",
            "Find who might pay, what they use today, and why now.",
            market_researcher,
        ),
        CrewMember(
            "User Researcher",
            "research",
            "Describe the daily pain and the first user workflow.",
            user_researcher,
        ),
        CrewMember(
            "Technical Scout",
            "research",
            "Identify local-first POC feasibility and likely blockers.",
            technical_scout,
        ),
    ]
    return run_crew("research", idea, members, synthesize_research)


def run_debate_crew(idea: Idea, research: str | None) -> CrewResult:
    members = [
        CrewMember(
            "Advocate",
            "debate",
            "Argue why this idea deserves a POC now.",
            advocate,
        ),
        CrewMember(
            "Skeptic",
            "debate",
            "Attack assumptions, risk, and opportunity cost.",
            skeptic,
        ),
        CrewMember(
            "Builder",
            "debate",
            "Find the smallest credible build path.",
            builder,
        ),
        CrewMember(
            "Strategist",
            "debate",
            "Rank the idea against focus, money potential, and timing.",
            strategist,
        ),
    ]
    return run_crew("debate", idea, members, synthesize_debate, {"research": research or ""})


def run_planning_crew(idea: Idea, research: str | None, debate: str | None) -> CrewResult:
    members = [
        CrewMember(
            "Product Planner",
            "planning",
            "Turn the refined idea into an MVP workflow.",
            product_planner,
        ),
        CrewMember(
            "POC Coder",
            "planning",
            "Define the smallest working local proof of concept.",
            poc_coder,
        ),
        CrewMember(
            "Frontend Engineer",
            "planning",
            "Define the first usable interface for the POC.",
            frontend_engineer,
        ),
        CrewMember(
            "Backend Engineer",
            "planning",
            "Define API and local persistence needs for the POC.",
            backend_engineer,
        ),
        CrewMember(
            "Auth Engineer",
            "planning",
            "Choose the auth posture for local POC and production handoff.",
            auth_engineer,
        ),
        CrewMember(
            "Database Engineer",
            "planning",
            "Choose local and deployable database defaults.",
            database_engineer,
        ),
        CrewMember(
            "Infra Engineer",
            "planning",
            "Define AWS/Vercel/Terraform deployment shape.",
            infra_engineer,
        ),
        CrewMember(
            "DevOps Engineer",
            "planning",
            "Define GitHub automation, checks, and deployment notes.",
            devops_engineer,
        ),
        CrewMember(
            "OpenSpec Writer",
            "planning",
            "Define implementation requirements and acceptance checks.",
            openspec_writer,
        ),
    ]
    context = {"research": research or "", "debate": debate or ""}
    return run_crew("planning", idea, members, synthesize_plan, context)


def run_crew(
    stage: str,
    idea: Idea,
    members: list[CrewMember],
    synthesizer: Callable[[Idea, dict[str, str], dict[str, str]], str],
    context: dict[str, str] | None = None,
) -> CrewResult:
    context = context or {}
    outputs: dict[str, str] = {}
    for member in members:
        outputs[member.name] = member.run(idea, context | outputs)
    synthesis = synthesizer(idea, context, outputs)
    _record_crew_event(stage, idea.title, [m.name for m in members], synthesis)
    return CrewResult(
        stage=stage,
        synthesis=synthesis,
        transcript=crew_transcript(stage, idea, members, outputs, synthesis),
        member_outputs=outputs,
    )


def crew_transcript(
    stage: str,
    idea: Idea,
    members: list[CrewMember],
    outputs: dict[str, str],
    synthesis: str,
) -> str:
    sections = [
        f"## Stage\n{stage}",
        f"## Idea\n{idea.title}",
        "## Crew\n"
        + bullet_list([f"{member.name} ({member.role}): {member.mission}" for member in members]),
    ]
    for member in members:
        sections.append(f"## {member.name}\n{outputs[member.name]}")
    sections.append(f"## Coordinator Synthesis\n{synthesis}")
    return md(f"Crew Transcript: {stage.title()} - {idea.title}", "\n\n".join(sections))


def market_researcher(idea: Idea, context: dict[str, str]) -> str:
    if idea.category == "money":
        return (
            "Likely buyers are founders, consultants, operators, or creators already spending time "
            "on the problem. The strongest signal is whether they already pay with time, tools, or contractors."
        )
    return (
        "Primary user is the owner of the recurring personal pain. Value depends on frequent use, "
        "low upkeep, and whether the tool removes a repeated decision."
    )


def user_researcher(idea: Idea, context: dict[str, str]) -> str:
    return (
        "The first workflow should start with one messy input, produce one clear recommendation, "
        "and ask for approval only when the next step changes external state."
    )


def technical_scout(idea: Idea, context: dict[str, str]) -> str:
    blockers = ("paid api", "credential", "oauth", "production deploy", "hardware")
    text = f"{idea.title} {idea.why}".lower()
    if any(blocker in text for blocker in blockers):
        return "POC should use mocks because the idea mentions external prerequisites or credentials."
    return "POC is feasible as a local script or small app using sample data and deterministic logic."


def advocate(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Build the POC because a fast artifact will reveal whether the idea has real pull. "
        "The cost of one local draft is low, and the learning value is high."
    )


def skeptic(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Do not confuse a polished agent conversation with validation. The POC must prove a painful "
        "workflow improves, and weak ideas should be paused quickly."
    )


def builder(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Build the smallest local draft: accept input, run a simple scoring or transformation step, "
        "then produce a prioritized next action and handoff notes."
    )


def strategist(idea: Idea, context: dict[str, str]) -> str:
    if idea.category == "money":
        return "Favor this idea if it has a clear buyer, fast demo, obvious before/after, and repeat usage."
    return "Favor this idea if it saves attention every week and will not become a maintenance chore."


def product_planner(idea: Idea, context: dict[str, str]) -> str:
    return (
        "MVP should focus on one end-to-end path: capture user input, produce structured output, "
        "show acceptance criteria, and prepare next engineering tasks."
    )


def poc_coder(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Create a complete local POC package under `draft_project/`: static frontend, optional backend API, "
        "SQLite persistence, docs, and deploy scaffolding. Keep the default run path dependency-light."
    )


def frontend_engineer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Create a browser UI with one primary workflow, visible sample data, loading/error states in copy, "
        "and no required build step for the first POC."
    )


def backend_engineer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Create a small HTTP API when the idea needs saved state, generated outputs, or integration boundaries. "
        "Use Python stdlib for the draft so it runs locally without dependency installation."
    )


def auth_engineer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Use no auth for local POC unless the workflow requires identity. Document Clerk and Firebase Auth "
        "as production options, with Clerk as the default SaaS recommendation."
    )


def database_engineer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Use SQLite locally. Document Neon or Supabase Postgres as production upgrade paths, with Supabase "
        "preferred when storage/auth integration matters."
    )


def infra_engineer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Default deploy shape is Vercel for frontend plus AWS Lambda/API Gateway or a small container service "
        "for backend. Include Terraform placeholders when cloud resources are needed."
    )


def devops_engineer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "Add GitHub Actions for basic checks and document environment variables, preview deploys, and rollback notes. "
        "Never commit `.env`, database files, or Terraform state."
    )


def openspec_writer(idea: Idea, context: dict[str, str]) -> str:
    return (
        "OpenSpec must define a runnable local POC requirement and an engineering handoff requirement. "
        "Tasks should stay small enough for the next crew to execute."
    )


def synthesize_research(idea: Idea, context: dict[str, str], outputs: dict[str, str]) -> str:
    base = research_brief(idea)
    return (
        base
        + "\n## Crew Additions\n"
        + bullet_list([f"{name}: {output}" for name, output in outputs.items()])
        + "\n"
    )


def synthesize_debate(idea: Idea, context: dict[str, str], outputs: dict[str, str]) -> str:
    base = debate_brief(idea, context.get("research"))
    return (
        base
        + "\n## Crew Positions\n"
        + bullet_list([f"{name}: {output}" for name, output in outputs.items()])
        + "\n"
    )


def synthesize_plan(idea: Idea, context: dict[str, str], outputs: dict[str, str]) -> str:
    base = implementation_plan(idea, context.get("debate"))
    return (
        base
        + "\n## Crew Implementation Notes\n"
        + bullet_list([f"{name}: {output}" for name, output in outputs.items()])
        + "\n"
    )
