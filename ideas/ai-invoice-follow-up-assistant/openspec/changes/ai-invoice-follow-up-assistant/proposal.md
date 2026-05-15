# Proposal: AI invoice follow-up assistant

## Why
Freelancers forget to chase late invoices; agent drafts polite follow-ups, tracks aging, and escalates tone over time.

## What Changes
- Create a focused full-stack proof of concept for `AI invoice follow-up assistant`.
- Validate whether the idea should be handed to the larger engineering crew.
- Keep the first draft local-first, secret-safe, and deploy-aware.

## Impact
- Adds a draft project under the workspace-level `pocs/aizr/` folder.
- Adds frontend, backend, database, infra, DevOps, and deployment documentation.
- Defines implementation requirements in `specs/`.


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

## Debate Context
# Founder Board Debate: AI invoice follow-up assistant

## Advocate
This idea deserves a POC because it addresses a repeated attention and execution problem. If the workflow becomes habitual, it can compound into more shipped projects.

## Skeptic
The risk is overbuilding agent theater before proving that capture, prioritization, and handoff actually change behavior. The system must stay small and runnable.

## Builder
The first useful version should be CLI-first, local-first, and file-backed. It should create artifacts that another agent crew can immediately read.

## Strategist
Prioritize revenue path, buyer clarity, and MVP speed.

## Synthesis
Proceed to planning if the POC can be implemented without paid services, external deployment, or fragile integrations.

## Research Context Used
Research brief exists and was considered.

## Crew Positions
- Advocate: Build the POC because a fast artifact will reveal whether the idea has real pull. The cost of one local draft is low, and the learning value is high.
- Skeptic: Do not confuse a polished agent conversation with validation. The POC must prove a painful workflow improves, and weak ideas should be paused quickly.
- Builder: Build the smallest local draft: accept input, run a simple scoring or transformation step, then produce a prioritized next action and handoff notes.
- Strategist: Favor this idea if it has a clear buyer, fast demo, obvious before/after, and repeat usage.