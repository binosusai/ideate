from __future__ import annotations

from .models import Idea
from .text import bullet_list, md


def research_brief(idea: Idea) -> str:
    track = "commercial opportunity" if idea.category == "money" else "personal leverage"
    return md(
        f"Research Brief: {idea.title}",
        f"""
        ## Raw Intent
        {idea.why or "No extra context captured yet."}

        ## Track
        This idea is on the `{idea.category}` track, so the primary research lens is {track}.

        ## Working Hypothesis
        {idea.title} is worth exploring if it can produce a visible result within one week and a useful proof of concept within one focused session.

        ## Research Questions
        {bullet_list([
            "Who experiences this problem often enough to care?",
            "What painful alternative are they using today?",
            "What is the smallest demo that proves the idea?",
            "What would make this idea obviously not worth pursuing?",
            "What data, API, or permission would block implementation?",
        ])}

        ## Initial Recommendation
        Continue to debate. The idea is strong enough for structured criticism, but not yet ready for full engineering crew handoff.
        """,
    )


def debate_brief(idea: Idea, research: str | None) -> str:
    return md(
        f"Founder Board Debate: {idea.title}",
        f"""
        ## Advocate
        This idea deserves a POC because it addresses a repeated attention and execution problem. If the workflow becomes habitual, it can compound into more shipped projects.

        ## Skeptic
        The risk is overbuilding agent theater before proving that capture, prioritization, and handoff actually change behavior. The system must stay small and runnable.

        ## Builder
        The first useful version should be CLI-first, local-first, and file-backed. It should create artifacts that another agent crew can immediately read.

        ## Strategist
        {"Prioritize revenue path, buyer clarity, and MVP speed." if idea.category == "money" else "Prioritize personal utility, low maintenance, and frequent use."}

        ## Synthesis
        Proceed to planning if the POC can be implemented without paid services, external deployment, or fragile integrations.

        ## Research Context Used
        {"Research brief exists and was considered." if research else "No research brief existed; debate used only captured intent."}
        """,
    )


def implementation_plan(idea: Idea, debate: str | None) -> str:
    return md(
        f"Implementation Plan: {idea.title}",
        f"""
        ## Goal
        Create a working proof of concept that demonstrates the core value of `{idea.title}` with the smallest credible interface.

        ## MVP
        {bullet_list([
            "Represent the idea as a concrete user workflow.",
            "Create one runnable local draft project.",
            "Include acceptance tests or manual verification steps.",
            "Document what the larger engineering crew should improve next.",
        ])}

        ## Approval Gate
        Ask before spending money, publishing, deleting substantial work, or handing this to the 47-agent crew.

        ## POC Feasibility
        Feasible if it can run locally using standard tooling and sample data.

        ## OpenSpec Change ID
        `{idea.slug}`

        ## Debate Context Used
        {"Founder Board debate exists and was considered." if debate else "No debate artifact existed; plan used captured intent."}
        """,
    )


def acceptance_tests(idea: Idea) -> str:
    return md(
        f"Acceptance Tests: {idea.title}",
        """
        ## Required Checks
        - A new user can understand the project from the idea README.
        - The OpenSpec proposal, design, tasks, and capability spec exist.
        - The POC can be run locally or clearly explains why it is infeasible.
        - The handoff file names the next engineering tasks.
        - No paid external service is required by default.
        """,
    )


def poc_report(idea: Idea, feasible: bool) -> str:
    if feasible:
        body = """
        ## Result
        A small local proof of concept was generated in `draft_project/`.

        ## How To Run
        ```bash
        python3 backend/app.py
        ```

        ## Limitations
        - Uses deterministic placeholder logic by default.
        - Does not call external AI services unless the implementation adds exported environment variables.
        - Includes deploy scaffolding, but production deployment still needs project-specific configuration.
        """
    else:
        body = """
        ## Result
        POC generation was skipped because the idea appears to need external services, paid APIs, or missing credentials.

        ## Next Step
        Clarify required integrations and create a mock-only POC.
        """
    return md(f"POC Report: {idea.title}", body)


def handoff_brief(idea: Idea) -> str:
    return md(
        f"Engineering Crew Handoff: {idea.title}",
        f"""
        ## Mission
        Turn the approved POC and OpenSpec files into a production-quality implementation.

        ## Inputs
        {bullet_list([
            "README.md",
            "research.md",
            "debate.md",
            "implementation_plan.md",
            "acceptance_tests.md",
            "poc_report.md",
            "poc_location.md",
            "openspec/changes/" + idea.slug,
            "workspace-level pocs/" + idea.slug + "/",
            "workspace-level pocs/" + idea.slug + "/docs/local_setup.md",
            "workspace-level pocs/" + idea.slug + "/docs/deployment.md",
            "workspace-level pocs/" + idea.slug + "/infra/",
            "workspace-level pocs/" + idea.slug + "/.github/workflows/poc-ci.yml",
        ])}

        ## Guardrails
        Preserve the approved scope unless the user explicitly approves expansion. Escalate spending, external deployment, account setup, or publication.
        """,
    )
