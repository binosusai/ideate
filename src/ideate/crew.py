from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
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


THEME_NAMES: dict[str, dict[str, dict[str, str]]] = {
    "bihar_jharkhand": {
        "research": {
            "Market Researcher": "Litti Bazaar Scout",
            "User Researcher": "Patna Pain Finder",
            "Technical Scout": "Ranchi Feasibility Scout",
        },
        "debate": {
            "Advocate": "Dhuska Advocate",
            "Skeptic": "Tilkut Skeptic",
            "Builder": "Jamshedpur Builder",
            "Strategist": "Bodhgaya Strategist",
        },
        "planning": {
            "Product Planner": "Sattu Product Planner",
            "POC Coder": "Bokaro POC Coder",
            "Frontend Engineer": "Madhubani Frontend Engineer",
            "Backend Engineer": "Dhanbad Backend Engineer",
            "Auth Engineer": "Deoghar Auth Engineer",
            "Database Engineer": "Gaya Database Engineer",
            "Infra Engineer": "Hazaribagh Infra Engineer",
            "DevOps Engineer": "Muzaffarpur DevOps Engineer",
            "OpenSpec Writer": "Pitha OpenSpec Writer",
        },
    }
}


def _member_display_name(stage: str, member: CrewMember) -> str:
    theme = os.environ.get("IDEATE_AGENT_THEME", "").strip().lower()
    if not theme:
        return member.name
    return THEME_NAMES.get(theme, {}).get(stage, {}).get(member.name, member.name)


def _parallel_enabled(stage: str) -> bool:
    if os.environ.get("IDEATE_PARALLEL", "1") != "1":
        return False
    # Default: keep standard debate sequential for richer back-and-forth context.
    # Strict debate has explicit two rounds and can parallelize within each round.
    return stage in {"research", "planning"}


def _parallel_workers(member_count: int) -> int:
    raw = os.environ.get("IDEATE_MAX_PARALLEL_AGENTS", "")
    if raw:
        try:
            return max(1, min(member_count, int(raw)))
        except ValueError:
            pass
    return max(1, member_count)


def _run_members_parallel(
    stage: str,
    members: list[CrewMember],
    idea: Idea,
    context: dict[str, str],
    prior_outputs: dict[str, str],
    round_label: str = "opening",
    on_member_complete: Callable[[str, str], None] | None = None,
) -> dict[str, str]:
    worker_count = _parallel_workers(len(members))
    completed_outputs: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {
            executor.submit(
                _run_member,
                stage,
                member,
                idea,
                context,
                prior_outputs,
                round_label,
                "parallel",
            ): _member_display_name(stage, member)
            for member in members
        }
        for future in as_completed(future_map):
            member_name = future_map[future]
            output = future.result()
            completed_outputs[member_name] = output
            if on_member_complete:
                on_member_complete(member_name, output)
    return {
        _member_display_name(stage, member): completed_outputs[_member_display_name(stage, member)]
        for member in members
    }


def run_research_crew(
    idea: Idea,
    on_member_complete: Callable[[str, str], None] | None = None,
) -> CrewResult:
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
    return run_crew("research", idea, members, synthesize_research, on_member_complete=on_member_complete)


def run_debate_crew(
    idea: Idea,
    research: str | None,
    on_member_complete: Callable[[str, str], None] | None = None,
) -> CrewResult:
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
        return run_debate_crew_strict(
            idea,
            members,
            {"research": research or ""},
            on_member_complete=on_member_complete,
        )
    return run_crew(
        "debate",
        idea,
        members,
        synthesize_debate,
        {"research": research or ""},
        on_member_complete=on_member_complete,
    )


def run_debate_crew_strict(
    idea: Idea,
    members: list[CrewMember],
    context: dict[str, str],
    on_member_complete: Callable[[str, str], None] | None = None,
) -> CrewResult:
    opening_outputs: dict[str, str]
    if os.environ.get("IDEATE_PARALLEL", "1") == "1":
        opening_outputs = _run_members_parallel("debate", members, idea, context, {}, "opening")
    else:
        opening_outputs = {}
        for member in members:
            member_name = _member_display_name("debate", member)
            opening_outputs[member_name] = _run_member("debate", member, idea, context, opening_outputs)

    round_two_context = context | {
        "debate_round_1": "\n".join(f"{k}: {v}" for k, v in opening_outputs.items())
    }
    if os.environ.get("IDEATE_PARALLEL", "1") == "1":
        rebuttal_outputs = _run_members_parallel(
            "debate",
            members,
            idea,
            round_two_context,
            opening_outputs,
            "rebuttal",
            on_member_complete=(
                lambda member_name, output: on_member_complete(
                    member_name,
                    "Round 1 - Opening Statement:\n"
                    + opening_outputs[member_name]
                    + "\n\nRound 2 - Rebuttal:\n"
                    + output,
                )
                if on_member_complete
                else None
            ),
        )
    else:
        rebuttal_outputs: dict[str, str] = {}
        for member in members:
            member_name = _member_display_name("debate", member)
            rebuttal_outputs[member_name] = _run_member(
                "debate",
                member,
                idea,
                round_two_context,
                opening_outputs | rebuttal_outputs,
                round_label="rebuttal",
            )
            if on_member_complete:
                on_member_complete(
                    member_name,
                    "Round 1 - Opening Statement:\n"
                    + opening_outputs[member_name]
                    + "\n\nRound 2 - Rebuttal:\n"
                    + rebuttal_outputs[member_name],
                )

    outputs = {
        _member_display_name("debate", member): (
            "Round 1 - Opening Statement:\n"
            + opening_outputs[_member_display_name("debate", member)]
            + "\n\nRound 2 - Rebuttal:\n"
            + rebuttal_outputs[_member_display_name("debate", member)]
        )
        for member in members
    }
    synthesis = synthesize_debate(idea, context, outputs)
    _record_crew_event(
        "debate",
        idea.title,
        [_member_display_name("debate", m) for m in members],
        synthesis,
    )
    return CrewResult(
        stage="debate",
        synthesis=synthesis,
        transcript=crew_transcript("debate", idea, members, outputs, synthesis),
        member_outputs=outputs,
    )
def run_planning_crew(
    idea: Idea,
    research: str | None,
    debate: str | None,
    on_member_complete: Callable[[str, str], None] | None = None,
) -> CrewResult:
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
    return run_crew(
        "planning",
        idea,
        members,
        synthesize_plan,
        context,
        on_member_complete=on_member_complete,
    )


def run_crew(
    stage: str,
    idea: Idea,
    members: list[CrewMember],
    synthesizer: Callable[[Idea, dict[str, str], dict[str, str]], str],
    context: dict[str, str] | None = None,
    on_member_complete: Callable[[str, str], None] | None = None,
) -> CrewResult:
    context = context or {}
    if _parallel_enabled(stage):
        outputs = _run_members_parallel(
            stage,
            members,
            idea,
            context,
            {},
            on_member_complete=on_member_complete,
        )
    else:
        outputs: dict[str, str] = {}
        for member in members:
            member_name = _member_display_name(stage, member)
            outputs[member_name] = _run_member(stage, member, idea, context, outputs)
            if on_member_complete:
                on_member_complete(member_name, outputs[member_name])
    synthesis = synthesizer(idea, context, outputs)
    _record_crew_event(stage, idea.title, [_member_display_name(stage, m) for m in members], synthesis)
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
        + bullet_list(
            [
                f"{_member_display_name(stage, member)} ({member.role}): {member.mission}"
                for member in members
            ]
        ),
    ]
    for member in members:
        member_name = _member_display_name(stage, member)
        sections.append(f"## {member_name}\n{outputs[member_name]}")
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
    stage_defaults = {
        "research": "gpt-4.1",
        "debate": "gpt-4.1",
        "planning": "gpt-4.1-mini",
    }
    return stage_defaults.get(stage, "gpt-4.1-nano")


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

    if stage == "research":
        context_lines.append(f"research_focus: {_research_focus(member, idea)}")

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
    execution_mode: str = "sequential",
) -> str:
    def _execute_member() -> str:
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

    try:
        import agentops  # type: ignore[import]

        traced_call = agentops.agent(
            name=f"{stage}:{member.name}:{round_label}",
            tags={
                "execution_mode": execution_mode,
                "stage": stage,
                "round": round_label,
                "member_role": member.role,
            },
            capture_request=False,
            capture_response=True,
        )(_execute_member)
        return traced_call()
    except Exception:
        return _execute_member()


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


def _research_focus(member: CrewMember, idea: Idea) -> str:
    if member.name == "Market Researcher":
        if idea.category == "money":
            return (
                "Identify ICP segments, willingness-to-pay signals, competing tools, and a realistic entry pricing angle. "
                "Highlight one narrow wedge where distribution is easiest."
            )
        return (
            "Identify target user archetypes, recurring trigger moments, and non-monetary value signals such as time saved."
        )
    if member.name == "User Researcher":
        return (
            "Map current user journey: trigger, friction point, workaround, and desired outcome. "
            "Recommend first-run workflow and success criteria for week-one usage."
        )
    if member.name == "Technical Scout":
        return (
            "Evaluate implementation risks, integration constraints, and minimal architecture for a local-first MVP. "
            "Call out what must be mocked in POC vs what can be built now."
        )
    return "Provide practical research insights grounded in the idea context."


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
