# AI OSS Good-First-Issue Discovery and Guided Resolution Assistant

## Status
`planned`

## Category
`money`

## Why This Exists
Help developers consistently find suitable open source contribution opportunities and get actionable guidance to complete one selected issue end-to-end.

Additional details from YAML:
    problem:
- Developers struggle to find high-quality good first issues that match their skill
  level and language preferences.
- Even after finding issues, many contributors are unsure how to start and what concrete
  steps to take.
users:
- early-career engineers
- students building OSS portfolios
- experienced engineers exploring new stacks
workflow:
- Parse GitHub OSS repositories and collect candidate good first issues.
- Show discovered issues in a UI with filters.
- Rank issues from easy to intermediate to hard using predefined competency levels
  and language preferences.
- Select the easiest ranked issue and ask the user via email.
- Before sending the email, call an engineer AI agent to generate implementation TODOs.
- Send an email where subject is the issue title and body includes repository metadata,
  OSS project metadata, and the step-by-step resolution plan.
capabilities:
- GitHub ingestion and issue normalization
- competency and language preference model
- ranking engine and explainability
- email composition and delivery
- engineer agent for actionable TODO generation
mvp_scope:
- GitHub API integration for issue discovery
- web UI listing issues with ranking labels
- single email workflow for top easiest issue
- generated TODO checklist for selected issue
success_metrics:
- issue-to-selection conversion rate
- email open and click-through rate
- contributor completion rate on selected issues
- time-to-first-meaningful-OSS-contribution

## Current Score
81.0

## Files
- `research.md`
- `debate.md`
- `implementation_plan.md`
- `crew_transcripts.md`
- `acceptance_tests.md`
- `poc_report.md`
- `poc_location.md`
- `poc_quality_rubric.md`
- `poc_quality_score.md`
- `poc_improvement_loop.md`
- `handoff.md`
- `openspec/`
