# Design: AI invoice follow-up assistant

## Architecture
The first draft should be a complete local POC with a static frontend, a small backend API when useful, SQLite persistence, install/run docs, and deployment guidance.

## Data
Use SQLite locally. Document Neon and Supabase as production database options. Avoid paid APIs until explicitly approved.

## Auth
Use no auth for local POC unless required. Document Clerk and Firebase Auth integration points for production.

## Infra And DevOps
Prefer Vercel for frontend previews and AWS services for backend/infra when needed. Include Terraform placeholders and GitHub Actions checks.

## Risks
- The POC may prove interface feasibility without proving market demand.
- External integrations may need a second design pass.
- Deployment docs are scaffolding until real cloud accounts and project IDs are selected.


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