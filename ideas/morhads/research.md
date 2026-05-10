# Research Brief: AI OSS Good-First-Issue Discovery and Guided Resolution Assistant

## Raw Intent
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

## Track
This idea is on the `money` track, so the primary research lens is commercial opportunity.

## Working Hypothesis
AI OSS Good-First-Issue Discovery and Guided Resolution Assistant is worth exploring if it can produce a visible result within one week and a useful proof of concept within one focused session.

## Research Questions
- Who experiences this problem often enough to care?
- What painful alternative are they using today?
- What is the smallest demo that proves the idea?
- What would make this idea obviously not worth pursuing?
- What data, API, or permission would block implementation?

## Initial Recommendation
Continue to debate. The idea is strong enough for structured criticism, but not yet ready for full engineering crew handoff.

## Crew Additions
- Market Researcher: Findings:

1. Narrowest Buyer Segment: Computer science students and recent bootcamp graduates actively building OSS portfolios for job applications—especially those participating in hackathons or university OSS clubs.
2. Current Alternatives: Manual GitHub search, Up-for-Grabs, First Timers Only, and curated newsletters (e.g., CodeTriage). None offer personalized, actionable step-by-step guidance or automated matching by skill/language.
3. Willingness-to-Pay Signals: High among students seeking internships or jobs (e.g., those paying for LeetCode Premium or LinkedIn Learning). Signals include willingness to pay $5–$15/month for tools that demonstrably accelerate OSS contribution and portfolio-building.

Risks:

1. Switching Friction: OSS beginners may distrust AI-generated guidance or prefer established, free community resources; email workflow may feel impersonal or get lost in inboxes.
2. Market Size: The segment is narrow and price-sensitive; institutional buyers (bootcamps, universities) may require extensive proof of efficacy before adoption.

Recommendation:

- Entry Wedge: Partner with university OSS clubs and bootcamps to offer a branded, cohort-based onboarding challenge (free for first 30 days), leveraging their distribution and social proof to drive initial adoption and testimonials.
- User Researcher: **Findings:**
1. Trigger: Users (especially early-career engineers and students) seek OSS issues after deciding to build a portfolio or learn new stacks, typically searching GitHub or aggregators.
2. Sharpest pain: Filtering for truly “good first issues” that match both skill and language is time-consuming; most issues are too vague or lack actionable next steps.
3. Workaround: Users rely on manual searching, Discord/Reddit recommendations, or “good first issue” labels, then spend hours deciphering project context and next actions.

**Risks:**
1. Issue Relevance: Automated ranking may surface stale, low-quality, or poorly described issues, leading to user frustration or wasted effort.
2. Guidance Quality: Generated TODOs may be too generic or miss project-specific context, reducing user confidence and completion rates.

**Recommendation:**
- First-run workflow: Let users select language/skill level → display top 3 ranked issues with clear competency tags → on selection, immediately show a generated step-by-step TODO list and “email me this plan” button. Success: User receives a relevant, actionable issue+plan in <10 minutes, and attempts a contribution within the first week.
- Technical Scout: Findings:
1. GitHub API supports issue discovery and filtering by labels (e.g., "good first issue"), enabling real-time ingestion and normalization for MVP. Rate limits (60/hr unauthenticated, 5,000/hr authenticated) are manageable for early users.
2. Ranking by competency/language can be prototyped with simple heuristics (e.g., label parsing, repo language metadata) and does not require ML for MVP. Explainability can be mocked with static text.
3. Engineer AI agent for TODO generation must be mocked in POC (e.g., hardcoded or template-based checklists), as reliable step-by-step code guidance requires nontrivial LLM integration and prompt engineering.

Risks:
1. Email delivery (especially from localhost or dev domains) may be blocked or flagged as spam; production-grade email requires verified sender infrastructure (e.g., SES, SendGrid).
2. GitHub API changes, rate limits, or authentication requirements may disrupt ingestion, especially if scaling beyond MVP or supporting private repos.

Recommendation:
Build the MVP with real GitHub API integration, a basic web UI, and a mocked TODO generator. Use a local SMTP server or test email sandbox for POC; defer production email and LLM integration until core workflow is validated.
