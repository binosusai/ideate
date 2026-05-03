# Implementation Plan: Medium article writer in my style

## Goal
Create a working proof of concept that demonstrates the core value of `Medium article writer in my style` with the smallest credible interface.

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
`medium-article-writer-in-my-style`

## Debate Context Used
Founder Board debate exists and was considered.

## Crew Implementation Notes
- Product Planner: MVP should focus on one end-to-end path: capture user input, produce structured output, show acceptance criteria, and prepare next engineering tasks.
- POC Coder: Create a complete local POC package under `draft_project/`: static frontend, optional backend API, SQLite persistence, docs, and deploy scaffolding. Keep the default run path dependency-light.
- Frontend Engineer: Create a browser UI with one primary workflow, visible sample data, loading/error states in copy, and no required build step for the first POC.
- Backend Engineer: Create a small HTTP API when the idea needs saved state, generated outputs, or integration boundaries. Use Python stdlib for the draft so it runs locally without dependency installation.
- Auth Engineer: Use no auth for local POC unless the workflow requires identity. Document Clerk and Firebase Auth as production options, with Clerk as the default SaaS recommendation.
- Database Engineer: Use SQLite locally. Document Neon or Supabase Postgres as production upgrade paths, with Supabase preferred when storage/auth integration matters.
- Infra Engineer: Default deploy shape is Vercel for frontend plus AWS Lambda/API Gateway or a small container service for backend. Include Terraform placeholders when cloud resources are needed.
- DevOps Engineer: Add GitHub Actions for basic checks and document environment variables, preview deploys, and rollback notes. Never commit `.env`, database files, or Terraform state.
- OpenSpec Writer: OpenSpec must define a runnable local POC requirement and an engineering handoff requirement. Tasks should stay small enough for the next crew to execute.
