from __future__ import annotations

from ideate.crew import run_debate_crew, run_planning_crew, run_research_crew
from ideate.models import Idea


def idea() -> Idea:
    return Idea(
        id=1,
        title="Landing Page Roast Agent",
        slug="landing-page-roast-agent",
        category="money",
        why="Founders paste copy and get positioning criticism.",
        status="captured",
        score=91.0,
        created_at="now",
        updated_at="now",
    )


def test_research_crew_has_members_and_synthesis() -> None:
    result = run_research_crew(idea())

    assert result.stage == "research"
    assert "Market Researcher" in result.member_outputs
    assert "Crew Additions" in result.synthesis
    assert "Crew Transcript" in result.transcript


def test_debate_and_planning_crews_chain_context() -> None:
    research = run_research_crew(idea()).synthesis
    debate = run_debate_crew(idea(), research)
    plan = run_planning_crew(idea(), research, debate.synthesis)

    assert "Crew Positions" in debate.synthesis
    assert "Skeptic" in debate.member_outputs
    assert "Crew Implementation Notes" in plan.synthesis
    assert "OpenSpec Writer" in plan.member_outputs
    assert "Frontend Engineer" in plan.member_outputs
    assert "Infra Engineer" in plan.member_outputs
    assert "DevOps Engineer" in plan.member_outputs
