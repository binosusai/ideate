# Ideate

Ideate is a local-first Idea Implementation AI Agent Crew. It captures ideas, ranks money-making ideas first, runs deterministic research/debate/planning workflows, creates OpenSpec-backed idea folders, drafts a small proof of concept outside the agent factory when feasible, and packages the result for your larger engineering crew.

## Quick Start

```bash
cd /Users/siddharthshankar/workspace/codex/ideate
PYTHONPATH=src python3 -m ideate.cli init
PYTHONPATH=src python3 -m ideate.cli capture "AI agent that turns rough ideas into POCs" --category money --why "I forget good ideas when I am busy"
PYTHONPATH=src python3 -m ideate.cli capture --from-yaml examples/idea.capture.yaml
PYTHONPATH=src python3 -m ideate.cli daily
PYTHONPATH=src python3 -m ideate.cli research 1
PYTHONPATH=src python3 -m ideate.cli debate 1
PYTHONPATH=src python3 -m ideate.cli plan 1
PYTHONPATH=src python3 -m ideate.cli approve 1
PYTHONPATH=src python3 -m ideate.cli poc 1
PYTHONPATH=src python3 -m ideate.cli handoff 1
```

By default, Ideate stores state in `.ideate/ideate.sqlite3`, creates idea memory folders in `ideas/`, and creates runnable POCs as sibling projects in `../pocs/`.

## Capture From YAML

You can capture ideas natively from YAML:

```bash
PYTHONPATH=src python3 -m ideate.cli capture --from-yaml examples/idea.capture.yaml
```

Use this schema:

```yaml
title: AI invoice follow-up assistant
category: money
why: I want a weekly pipeline that turns new invoices into polite reminders.
details:
  target_users:
    - independent consultants
    - agencies
  constraints:
    - no CRM required
    - email-first MVP
  monetization:
    model: monthly subscription
    starting_price_usd: 19
```

Field rules:

1. `title` is required.
2. `category` is optional (`money` or `personal`, defaults to `money`).
3. `why` is optional.
4. `details` is optional and can be a map/list/string. It is appended into the stored `why` so richer context is preserved.

## Workflow

1. Capture ideas daily.
2. Triage into `money` or `personal`.
3. Research the opportunity.
4. Debate strengths, risks, and opportunity cost.
5. Create an implementation plan and OpenSpec change.
6. Approve the idea.
7. Generate a small working POC when feasible.
8. Produce a handoff bundle for the 47-agent engineering crew.

## Hybrid Agent Architecture

Ideate uses a hybrid architecture:

- `src/ideate/agents.py` contains deterministic role outputs such as research briefs, debate summaries, plans, POC reports, and handoff briefs.
- `src/ideate/crew.py` organizes those roles into staged crews with named members, individual outputs, transcripts, and coordinator synthesis.
- `src/ideate/cli.py` remains the deterministic coordinator that controls status transitions, approval gates, SQLite memory, and artifact generation.

This keeps the system testable and cron-safe while leaving a clean place to plug in real LLM agents later.

Planning now includes product, POC coding, frontend, backend, auth, database, infra, DevOps, and OpenSpec roles. Generated POCs include a browser UI, Python backend, SQLite local persistence, GitHub Actions, Terraform placeholders, and local/deployment docs.

POCs are intentionally generated outside `ideate/` so the agent crew factory stays clean:

```text
/Users/siddharthshankar/workspace/codex/
  ideate/
  platform/
  pocs/
    _common/
    <onewordpocname>/
```

Override the POC workspace with `IDEATE_POC_HOME=/path/to/pocs`.
Override the shared DevOps/infra library with `IDEATE_PLATFORM_HOME=/path/to/platform`.

The workspace-level `platform/` folder is the local version of a future GitHub organization repo. Generated POCs call or document reusable GitHub Actions and Terraform modules from that library by default, and should only add local infra/devops when their architecture differs.

Each generated POC also gets `PROJECT_RULES.md`, which points to shared security, git, GitHub, CI/CD, deployment, Terraform, observability, and readiness rules under `platform/rules/`.

## Secret Safety

Do not store secrets in repo-tracked files. This project includes `.gitignore`, `.codexignore`, `.cursorignore`, `AGENTS.md`, and `CLAUDE.md` guardrails that tell coding agents not to read `.env` files.

Install the optional git hook after initializing git inside `ideate`:

```bash
python3 scripts/install_git_hooks.py
```

The app should read secrets only from exported environment variables. It should not parse `.env` directly.

## Cron Example

```cron
0 9 * * * cd /Users/siddharthshankar/workspace/codex/ideate && PYTHONPATH=src python3 -m ideate.cli daily >> .ideate/daily.log 2>&1
```

## Project Kanban Filters

Use a GitHub Project board backed by issue filters.

Base filter (all agent tasks):

```text
is:issue repo:binosusai/ideate label:ideate-task
```

Recommended saved views:

```text
In Progress: is:issue repo:binosusai/ideate label:ideate-task label:task:in-progress
Done: is:issue repo:binosusai/ideate label:ideate-task label:task:done is:closed
Research Stage: is:issue repo:binosusai/ideate label:ideate-task label:stage:research
Debate Stage: is:issue repo:binosusai/ideate label:ideate-task label:stage:debate
Planning Stage: is:issue repo:binosusai/ideate label:ideate-task label:stage:planning
Idea 1 Focus: is:issue repo:binosusai/ideate label:ideate-task label:idea:1
```

When task state is updated by Ideate:

- `task:in-progress` keeps the issue open.
- `task:done` closes the issue automatically.

This helps Project board workflows move cards cleanly across To Do, In Progress, and Done.

## Idea Folder Layout

Each planned idea gets a folder like:

```text
ideas/<idea-slug>/
  README.md
  research.md
  debate.md
  crew_transcripts.md
  implementation_plan.md
  acceptance_tests.md
  poc_report.md
  poc_location.md
  handoff.md
  openspec/
    changes/<idea-slug>/
      proposal.md
      design.md
      tasks.md
      specs/<capability-name>/spec.md

../pocs/<onewordpocname>/
  PROJECT_RULES.md
  frontend/
  backend/
  docs/
  docs/devops.md
  infra/terraform/
  .github/workflows/
```


# Set required env vars
export DATABASE_URL="$PG_CONN_STR"
export AGENTOPS_API_KEY="<your-key-from-agentops.ai>"
export OPENAI_API_KEY="<your-key>"

# Run the pipeline
.venv/bin/idea research 1
.venv/bin/idea debate 1
.venv/bin/idea plan 1
.venv/bin/idea approve 1
.venv/bin/idea poc 1  