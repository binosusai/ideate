# Spec: AI invoice follow-up assistant

## ADDED Requirements

### Requirement: Runnable local proof of concept
The system SHALL include a local proof of concept that demonstrates the core idea with frontend, backend when needed, and local persistence without requiring paid services by default.

#### Scenario: User runs the POC
- **WHEN** the user follows the instructions in `poc_report.md`
- **THEN** the POC runs locally or clearly explains missing prerequisites

### Requirement: External POC workspace
Generated POC source code SHALL live outside the Ideate agent factory folder.

#### Scenario: POC is generated
- **WHEN** the user runs `idea poc`
- **THEN** the POC is written under the workspace-level `pocs/` folder

### Requirement: Deployment-ready documentation
The system SHALL include documentation for local setup and production deployment options.

#### Scenario: User reviews deployment path
- **WHEN** the user reads the generated POC `docs/deployment.md`
- **THEN** they can identify Vercel, AWS, Terraform, auth, database, and GitHub Actions next steps

### Requirement: Engineering handoff
The system SHALL provide enough context for a larger agent crew to continue implementation.

#### Scenario: Engineering crew receives the folder
- **WHEN** the crew reads `handoff.md`
- **THEN** it can identify mission, inputs, guardrails, and next tasks


## Research Context
# Research Brief: AI invoice follow-up assistant

## Raw Intent
Freelancers forget to chase late invoices; agent drafts polite follow-ups, tracks aging, and escalates tone over time.

## Track
This idea is on the `money` track, so the primary research lens is commercial opportunity.

## Working Hypothesis
AI invoice follow-up assistant is worth exploring if it can produce a visible result within one week and a useful proof of concept within one focused session.

## Research Questions
- Who experiences this problem often enough to care?
- What painful alternative are they using today?
- What is the smallest demo that proves the idea?
- What would make this idea obviously not worth pursuing?
- What data, API, or permission would block implementation?

## Initial Recommendation
Continue to debate. The idea is strong enough for structured criticism, but not yet ready for full engineering crew handoff.

## Crew Additions
- Market Researcher: Likely buyers are founders, consultants, operators, or creators already spending time on the problem. The strongest signal is whether they already pay with time, tools, or contractors.
- User Researcher: The first workflow should start with one messy input, produce one clear recommendation, and ask for approval only when the next step changes external state.
- Technical Scout: POC is feasible as a local script or small app using sample data and deterministic logic.

## Implementation Plan
# Implementation Plan: AI invoice follow-up assistant

## Goal
Create a working proof of concept that demonstrates the core value of `AI invoice follow-up assistant` with the smallest credible interface.

## MVP
- Represent the idea as a concrete user workflow.
- Create one runnable local draft project.
- Include acceptance tests or manual verification steps.
- Document what the larger engineering crew should improve next.

## Approval Gate
Ask before spending money, publishing, deleting substantial work, or handing this to the 47-agent crew.

## POC Feasibility
Feasible if it can run locally using standard tooling and sample data.

## OpenSpec Change ID
`ai-invoice-follow-up-assistant`

## Debate Context Used
Founder Board debate exists and was considered.

## Crew Implementation Notes
- Product Planner: MVP should focus on one end-to-end path: capture user input, produce structured output, show acceptance criteria, and prepare next engineering tasks.
- POC Coder: Create `draft_project/app.py` first. Keep it dependency-free unless the idea cannot be demonstrated without a small framework.
- OpenSpec Writer: OpenSpec must define a runnable local POC requirement and an engineering handoff requirement. Tasks should stay small enough for the next crew to execute.