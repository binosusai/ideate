from __future__ import annotations

import os
import re
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
    temperature: float = 0.4


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
            temperature=0.25,
        ),
        CrewMember(
            "User Researcher",
            "research",
            "Describe the daily pain and the first user workflow.",
            user_researcher,
            temperature=0.45,
        ),
        CrewMember(
            "Technical Scout",
            "research",
            "Identify local-first POC feasibility and likely blockers.",
            technical_scout,
            temperature=0.2,
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
            temperature=0.85,
        ),
        CrewMember(
            "Skeptic",
            "debate",
            "Attack assumptions, risk, and opportunity cost.",
            skeptic,
            temperature=0.3,
        ),
        CrewMember(
            "Builder",
            "debate",
            "Find the smallest credible build path.",
            builder,
            temperature=0.45,
        ),
        CrewMember(
            "Strategist",
            "debate",
            "Rank the idea against focus, money potential, and timing.",
            strategist,
            temperature=0.25,
        ),
    ]
    if os.environ.get("IDEATE_STRICT_DEBATE") == "1":
        return run_debate_crew_strict(idea, members, {"research": research or ""})
    return run_crew("debate", idea, members, synthesize_debate, {"research": research or ""})


def run_debate_crew_strict(
    idea: Idea,
    members: list[CrewMember],
    context: dict[str, str],
) -> CrewResult:
    opening_outputs: dict[str, str] = {}
    for member in members:
        opening_outputs[member.name] = _run_member("debate", member, idea, context, opening_outputs)

    round_two_context = context | {
        "debate_round_1": "\n".join(f"{k}: {v}" for k, v in opening_outputs.items())
    }
    rebuttal_outputs: dict[str, str] = {}
    for member in members:
        rebuttal_outputs[member.name] = _run_member(
            "debate",
            member,
            idea,
            round_two_context,
            opening_outputs | rebuttal_outputs,
            round_label="rebuttal",
        )

    outputs = {
        member.name: (
            "Round 1 - Opening Statement:\n"
            + opening_outputs[member.name]
            + "\n\nRound 2 - Rebuttal:\n"
            + rebuttal_outputs[member.name]
        )
        for member in members
    }
    synthesis = synthesize_debate(idea, context, outputs)
    _record_crew_event("debate", idea.title, [m.name for m in members], synthesis)
    return CrewResult(
        stage="debate",
        synthesis=synthesis,
        transcript=crew_transcript("debate", idea, members, outputs, synthesis),
        member_outputs=outputs,
    )


def run_planning_crew(idea: Idea, research: str | None, debate: str | None) -> CrewResult:
    members = [
        CrewMember(
            "Product Planner",
            "planning",
            "Turn the refined idea into an MVP workflow.",
            product_planner,
            temperature=0.35,
        ),
        CrewMember(
            "POC Coder",
            "planning",
            "Define the smallest working local proof of concept.",
            poc_coder,
            temperature=0.3,
        ),
        CrewMember(
            "Frontend Engineer",
            "planning",
            "Define the first usable interface for the POC.",
            frontend_engineer,
            temperature=0.5,
        ),
        CrewMember(
            "Backend Engineer",
            "planning",
            "Define API and local persistence needs for the POC.",
            backend_engineer,
            temperature=0.35,
        ),
        CrewMember(
            "Auth Engineer",
            "planning",
            "Choose the auth posture for local POC and production handoff.",
            auth_engineer,
            temperature=0.2,
        ),
        CrewMember(
            "Database Engineer",
            "planning",
            "Choose local and deployable database defaults.",
            database_engineer,
            temperature=0.2,
        ),
        CrewMember(
            "Infra Engineer",
            "planning",
            "Define AWS/Vercel/Terraform deployment shape.",
            infra_engineer,
            temperature=0.25,
        ),
        CrewMember(
            "DevOps Engineer",
            "planning",
            "Define GitHub automation, checks, and deployment notes.",
            devops_engineer,
            temperature=0.2,
        ),
        CrewMember(
            "OpenSpec Writer",
            "planning",
            "Define implementation requirements and acceptance checks.",
            openspec_writer,
            temperature=0.2,
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
        outputs[member.name] = _run_member(stage, member, idea, context, outputs)
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


def _env_token(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")


def _resolve_model(stage: str, member: CrewMember) -> str:
    keys = [
        f"IDEATE_MODEL_{_env_token(stage)}_{_env_token(member.name)}",
        f"IDEATE_MODEL_{_env_token(stage)}_{_env_token(member.role)}",
        f"IDEATE_MODEL_{_env_token(stage)}",
        "IDEATE_MODEL",
    ]
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
    return "gpt-4.1-nano"


def _resolve_temperature(stage: str, member: CrewMember) -> float:
    keys = [
        f"IDEATE_TEMPERATURE_{_env_token(stage)}_{_env_token(member.name)}",
        f"IDEATE_TEMPERATURE_{_env_token(stage)}_{_env_token(member.role)}",
        f"IDEATE_TEMPERATURE_{_env_token(stage)}",
        "IDEATE_TEMPERATURE",
    ]
    for key in keys:
        value = os.environ.get(key)
        if not value:
            continue
        try:
            parsed = float(value)
            return min(max(parsed, 0.0), 2.0)
        except ValueError:
            continue
    return member.temperature


def _style_hint(member: CrewMember) -> str:
    if member.name == "Advocate":
        return "Be persuasive, specific, and outcome-focused."
    if member.name == "Skeptic":
        return "Stress-test assumptions and quantify risks."
    if member.name == "Builder":
        return "Propose practical low-complexity build paths."
    if member.name == "Strategist":
        return "Prioritize options by expected impact and speed."
    if member.role == "planning":
        return "Provide implementation-ready detail and explicit tradeoffs."
    return "Use concise bullet points grounded in the idea context."


def _member_prompt(
    stage: str,
    member: CrewMember,
    idea: Idea,
    context: dict[str, str],
    prior_outputs: dict[str, str],
    round_label: str = "opening",
) -> tuple[str, str]:
    context_lines = [
        f"idea_title: {idea.title}",
        f"idea_category: {idea.category}",
        f"idea_why: {idea.why or 'n/a'}",
    ]
    for key, value in context.items():
        if value:
            context_lines.append(f"{key}: {value[:2500]}")

    teammate_text = ""
    if prior_outputs:
        teammate_lines = [f"{name}: {output}" for name, output in prior_outputs.items()]
        teammate_text = "\n\nTeammate outputs so far:\n" + "\n".join(teammate_lines)

    collaboration_rule = ""
    if stage == "debate" and prior_outputs:
        collaboration_rule = (
            "Reference at least one teammate by name and explicitly support or challenge their argument."
        )

    round_note = ""
    if stage == "debate" and round_label == "rebuttal":
        round_note = "This is rebuttal round. Address at least two teammates and revise your stance if needed."

    system_prompt = (
        f"You are {member.name}. Mission: {member.mission}. "
        f"Stage: {stage}. { _style_hint(member) } "
        "Keep response under 180 words and make it actionable."
    )
    user_prompt = (
        "Context:\n"
        + "\n".join(context_lines)
        + teammate_text
        + (f"\n\nCollaboration requirement: {collaboration_rule}" if collaboration_rule else "")
        + (f"\n\nRound instruction: {round_note}" if round_note else "")
    )
    return system_prompt, user_prompt


def _llm_member_output(
    stage: str,
    member: CrewMember,
    idea: Idea,
    context: dict[str, str],
    prior_outputs: dict[str, str],
    round_label: str = "opening",
) -> str | None:
    if not os.environ.get("OPENAI_API_KEY"):
        return None
    if os.environ.get("IDEATE_FORCE_RULE_BASED") == "1":
        return None
    try:
        from openai import OpenAI  # type: ignore[import]
    except Exception:
        return None

    model = _resolve_model(stage, member)
    temperature = _resolve_temperature(stage, member)
    system_prompt, user_prompt = _member_prompt(
        stage,
        member,
        idea,
        context,
        prior_outputs,
        round_label=round_label,
    )
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        output = ((response.choices[0].message.content or "") if response.choices else "").strip()
        if output:
            return output
    except Exception as exc:
        if os.environ.get("IDEATE_REQUIRE_LLM") == "1":
            raise RuntimeError(f"LLM call failed for {member.name}: {exc}") from exc
        return None
    return None


def _run_member(
    stage: str,
    member: CrewMember,
    idea: Idea,
    context: dict[str, str],
    prior_outputs: dict[str, str],
    round_label: str = "opening",
) -> str:
    llm_output = _llm_member_output(
        stage,
        member,
        idea,
        context,
        prior_outputs,
        round_label=round_label,
    )
    if llm_output:
        return llm_output
    if os.environ.get("IDEATE_REQUIRE_LLM") == "1":
        raise RuntimeError(f"LLM output missing for {member.name} while IDEATE_REQUIRE_LLM=1")
    return member.run(idea, context | prior_outputs)


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
