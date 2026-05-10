# Proposal: AI OSS Good-First-Issue Discovery and Guided Resolution Assistant

## Why
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

    ## What Changes
    - Create a focused full-stack proof of concept for `AI OSS Good-First-Issue Discovery and Guided Resolution Assistant`.
    - Validate whether the idea should be handed to the larger engineering crew.
    - Keep the first draft local-first, secret-safe, and deploy-aware.

    ## Impact
    - Adds a draft project under the workspace-level `pocs/morhadsxj/` folder.
    - Adds frontend, backend, database, infra, DevOps, and deployment documentation.
    - Defines implementation requirements in `specs/`.


## Research Context
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

## Debate Context
# Founder Board Debate: AI OSS Good-First-Issue Discovery and Guided Resolution Assistant

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
- Advocate: Targeted Research Follow-ups:
Q1. What is the actual willingness to pay among early-career developers and students for AI-guided OSS onboarding, and does a B2B or institutional model (e.g., bootcamps, universities) offer a more viable revenue path?
A1. - Early-career developers and students often have limited disposable income, suggesting low direct willingness to pay for AI-guided OSS onboarding tools unless priced very affordably or freemium-based.  
- Value perception hinges on clear career benefits: faster portfolio building, mentorship-like guidance, and improved job prospects increase willingness to pay.  
- Surveys in developer education show students and juniors prefer free or low-cost tools; paid tiers often succeed when bundled with certification or career services.  
- B2B/institutional models (bootcamps, universities) likely offe

Q2. Does the AI-generated step-by-step resolution plan significantly outperform existing free alternatives (GitHub labels, community forums) in driving first-time OSS contributions and retention?
A2. - AI-generated step-by-step plans provide tailored, actionable guidance beyond generic GitHub labels or forum advice, potentially lowering entry barriers for first-time contributors.  
- Existing free alternatives often lack personalized competency matching and concrete implementation TODOs, which can cause confusion or overwhelm new contributors.  
- Empirical evidence is limited; success depends on plan accuracy, relevance, and user engagement with the email workflow.  
- Metrics like contributor completion rate and time-to-first-meaningful-contribution are key to measuring impact versus fre

Round 1 - Opening Statement:
This idea deserves a proof of concept now because it directly unlocks a proven market pain: new and transitioning developers waste hours scouring GitHub for “good first issues,” often giving up before contributing. Existing alternatives—manual search, generic issue lists, and scattered tutorials—are inefficient, demotivating, and do not scale.

Our proposed assistant uniquely combines personalized discovery (filtered/ranked by skill and language) with actionable, AI-generated step-by-step resolution plans. This means users don’t just find issues; they actually finish contributions, shortening the path from intent to impact. Early-career engineers and students, in particular, are eager for this boost, and OSS maintainers are desperate for higher first-contribution retention.

A minimal POC—GitHub API ingestion, issue ranking by language, and automated TODOs emailed for one issue—can be built in a week and will prove if users convert from browsing to contributing. If even a handful of users complete their first PR using the workflow, we validate both engagement and a monetizable “developer onboarding” wedge.

Let’s build this now and test with targeted users—outcomes will be immediate and actionable for both learning and funding.

Round 2 - Rebuttal:
Building on the strong execution plan from **Builder** and the commercial caution from **Skeptic**, I maintain that a POC is warranted now—but with a strategically focused scope.

**Builder’s** approach proves we can deliver a real, testable workflow (GitHub issue ingestion → AI TODOs → email) in days, not weeks. This satisfies **Strategist’s** timing argument: we can quickly validate core user value—does actionable guidance drive first contributions where generic lists do not? We’re not betting the farm; we’re running a lightweight, low-risk experiment.

**Skeptic** is right to push on willingness to pay, but a POC isn’t about full market validation—it’s about proving delta: can our assistant convert a higher percentage of first-time contributors? The “no-code demo” suggestion is largely met by Builder’s simple backend script: we can begin user testing with minimal investment.

Action: Proceed with Builder’s script-based MVP and, in parallel, launch Strategist’s landing page to gauge interest and collect feedback. This dual-track will answer Skeptic’s concerns and let us iterate fast or shut down if results are weak. Let’s build and test now.
- Skeptic: Targeted Research Follow-ups:
Q1. What is the actual willingness to pay among early-career developers and students for AI-guided OSS onboarding, and does a B2B or institutional model (e.g., bootcamps, universities) offer a more viable revenue path?
A1. - Early-career developers and students often have limited disposable income, suggesting low direct willingness to pay for AI-guided OSS onboarding tools unless priced very affordably or freemium-based.  
- Value perception hinges on clear career benefits: faster portfolio building, mentorship-like guidance, and improved job prospects increase willingness to pay.  
- Surveys in developer education show students and juniors prefer free or low-cost tools; paid tiers often succeed when bundled with certification or career services.  
- B2B/institutional models (bootcamps, universities) likely offe

Q2. Does the AI-generated step-by-step resolution plan significantly outperform existing free alternatives (GitHub labels, community forums) in driving first-time OSS contributions and retention?
A2. - AI-generated step-by-step plans provide tailored, actionable guidance beyond generic GitHub labels or forum advice, potentially lowering entry barriers for first-time contributors.  
- Existing free alternatives often lack personalized competency matching and concrete implementation TODOs, which can cause confusion or overwhelm new contributors.  
- Empirical evidence is limited; success depends on plan accuracy, relevance, and user engagement with the email workflow.  
- Metrics like contributor completion rate and time-to-first-meaningful-contribution are key to measuring impact versus fre

Round 1 - Opening Statement:
Let’s stress-test the commercial assumptions:

1. **Market Pain & Frequency:** Are enough developers *actively* seeking good-first-issue guidance to pay for it? Most OSS contributors are hobbyists or students—groups with limited willingness to pay. Experienced engineers may not need hand-holding. Quantify: How many developers search for “good first issue” monthly? How many would pay $5–$10/mo?

2. **Alternatives:** GitHub already offers “good first issue” labels and search. Discord/Reddit/Stack Overflow provide peer guidance for free. Is your AI-generated TODO list *demonstrably* better and faster? If not, adoption will be low.

3. **Opportunity Cost:** Building ingestion, ranking, and AI guidance is non-trivial. Could this time be better spent on a tool with clearer monetization (e.g., code review automation, hiring platforms)?

4. **API/Permission Risk:** GitHub API rate limits, changes, or ToS restrictions could break your core workflow. What’s your fallback?

**Action:** Survey 30+ target users on their current pain, willingness to pay, and what would make them switch. Build a no-code demo (manual curation + AI TODOs) and test conversion before writing code. Quantify market size and revenue potential before committing.

Round 2 - Rebuttal:
Referencing both Builder and Strategist:

Builder’s MVP plan is admirably lean, but it sidesteps the core risk: **differentiation and monetization**. Strategist is right—B2C willingness to pay is weak; B2B is unproven. Even if you ship a script in a week, you risk building a “nice-to-have” that’s easily copied or ignored if GitHub or Copilot ships a similar feature. The opportunity cost is real: every hour spent here is an hour not spent on a tool with clearer enterprise pain (e.g., code review automation, hiring signal enrichment).

**Quantify before you code:**  
- Can you get 10+ bootcamps or university instructors to say they’d pay or pilot this?  
- Can you show that AI TODOs drive 2x higher first-PR completion than existing “good first issue” lists in a real user test?

**Action:**  
Before any code, run a no-code pilot: manually curate issues, generate AI TODOs, and email 30 users. Measure open, click, and PR completion. If <10% convert, or if B2B buyers balk, pivot fast. Don’t mistake technical feasibility for product-market fit.
- Builder: Targeted Research Follow-ups:
Q1. What is the actual willingness to pay among early-career developers and students for AI-guided OSS onboarding, and does a B2B or institutional model (e.g., bootcamps, universities) offer a more viable revenue path?
A1. - Early-career developers and students often have limited disposable income, suggesting low direct willingness to pay for AI-guided OSS onboarding tools unless priced very affordably or freemium-based.  
- Value perception hinges on clear career benefits: faster portfolio building, mentorship-like guidance, and improved job prospects increase willingness to pay.  
- Surveys in developer education show students and juniors prefer free or low-cost tools; paid tiers often succeed when bundled with certification or career services.  
- B2B/institutional models (bootcamps, universities) likely offe

Q2. Does the AI-generated step-by-step resolution plan significantly outperform existing free alternatives (GitHub labels, community forums) in driving first-time OSS contributions and retention?
A2. - AI-generated step-by-step plans provide tailored, actionable guidance beyond generic GitHub labels or forum advice, potentially lowering entry barriers for first-time contributors.  
- Existing free alternatives often lack personalized competency matching and concrete implementation TODOs, which can cause confusion or overwhelm new contributors.  
- Empirical evidence is limited; success depends on plan accuracy, relevance, and user engagement with the email workflow.  
- Metrics like contributor completion rate and time-to-first-meaningful-contribution are key to measuring impact versus fre

Round 1 - Opening Statement:
Here’s a practical, low-complexity build path for a credible MVP, focused on speed and minimal dependencies:

**1. Core Workflow (no user auth, no fancy UI):**

- **Backend Script:**  
  - Use Python (requests + smtplib) or Node.js to:
    - Call GitHub Search API for issues labeled "good first issue" + language filter.
    - Sort by recency or “comments:0” for easiest.
    - Extract title, repo, issue link, description.
    - (Optional) Use a simple ruleset (e.g., regex for keywords like “typo”, “docs”, “test”) to estimate difficulty.

- **Engineer Agent (TODOs):**  
  - Use OpenAI API (or local LLM) to generate a step-by-step TODO from the issue body.
  - Prompt: “Given this GitHub issue, what are the concrete steps to resolve it?”

- **Email Delivery:**  
  - Compose and send an email with the issue details and TODOs to a hardcoded address.

- **Trigger:**  
  - Manual script run, or simple web form with email + language.

**Result:**  
You’ll have a working pipeline that finds a good first issue, generates a resolution plan, and emails it—no UI or user accounts needed. Expand from here based on feedback.

Round 2 - Rebuttal:
Referencing both Skeptic and Builder:

I support Builder’s minimal, script-based build path—it’s the fastest way to validate core utility with real users. Skeptic rightly highlights commercial risk: willingness to pay is unproven, and alternatives exist. However, as Strategist notes, timing is favorable and the MVP can be built in days, not weeks.

**Rebuttal & Synthesis:**  
Skeptic’s call for pre-build validation is prudent, but a no-code demo (manual curation + AI TODOs) is nearly as much effort as Builder’s proposed script. Automating the flow (even for a single user) yields more credible feedback and lets us measure actual contributor completion rates, not just intent.

**Actionable Path:**  
- **Adopt Builder’s script MVP:** Fetch one “good first issue” (filtered by language), generate TODOs with OpenAI, and email to a test user.
- **Parallel Validation:** While running the MVP, launch a simple landing page to collect interest and survey users on pain points and willingness to pay.
- **Next Step:** If even a handful of users complete PRs via this flow, proceed to UI and B2B outreach as Strategist suggests.

This path balances Skeptic’s caution with Builder’s bias for action.
- Strategist: Targeted Research Follow-ups:
Q1. What is the actual willingness to pay among early-career developers and students for AI-guided OSS onboarding, and does a B2B or institutional model (e.g., bootcamps, universities) offer a more viable revenue path?
A1. - Early-career developers and students often have limited disposable income, suggesting low direct willingness to pay for AI-guided OSS onboarding tools unless priced very affordably or freemium-based.  
- Value perception hinges on clear career benefits: faster portfolio building, mentorship-like guidance, and improved job prospects increase willingness to pay.  
- Surveys in developer education show students and juniors prefer free or low-cost tools; paid tiers often succeed when bundled with certification or career services.  
- B2B/institutional models (bootcamps, universities) likely offe

Q2. Does the AI-generated step-by-step resolution plan significantly outperform existing free alternatives (GitHub labels, community forums) in driving first-time OSS contributions and retention?
A2. - AI-generated step-by-step plans provide tailored, actionable guidance beyond generic GitHub labels or forum advice, potentially lowering entry barriers for first-time contributors.  
- Existing free alternatives often lack personalized competency matching and concrete implementation TODOs, which can cause confusion or overwhelm new contributors.  
- Empirical evidence is limited; success depends on plan accuracy, relevance, and user engagement with the email workflow.  
- Metrics like contributor completion rate and time-to-first-meaningful-contribution are key to measuring impact versus fre

Round 1 - Opening Statement:
**Ranking the AI OSS Good-First-Issue Discovery and Guided Resolution Assistant:**

**1. Focus:**  
Strong. The idea targets a clear, underserved pain point for early-career developers and students. The workflow is well-scoped for an MVP, with a tight focus on actionable outcomes (issue discovery + guided resolution).

**2. Money Potential:**  
Moderate. While the user pain is real, willingness to pay is uncertain. Early-career devs and students are cost-sensitive; monetization likely requires a B2B angle (bootcamps, universities, or hiring platforms) or a freemium model. Market validation is needed.

**3. Timing:**  
Good. AI copilots are hot, and OSS contribution is increasingly valued. GitHub APIs are mature; AI-generated TODOs are feasible with current LLMs. The window to differentiate before GitHub or Copilot expands into this space is now.

**Prioritization:**  
- **Speed:** MVP is achievable in 1-2 weeks with existing APIs and LLMs.
- **Impact:** High for user activation and retention if guidance is actionable.

**Actionable Next Steps:**  
- Validate demand with a landing page and waitlist.
- Build a demo: GitHub issue fetch + AI TODO generation + email workflow.
- Interview potential B2B partners for monetization signals.

Round 2 - Rebuttal:
**Rebuttal and Prioritization:**

Referencing both Skeptic and Builder:

- I agree with **Skeptic** that direct monetization from individual early-career developers is weak; willingness to pay is low, and GitHub’s built-in features are “good enough” for many. However, as **Builder** demonstrates, the MVP can be built rapidly and cheaply—meaning opportunity cost is low and we can validate assumptions quickly.

- Skeptic’s call for a no-code demo and user survey is spot-on. Before investing further, we must prove that AI-generated TODOs drive higher conversion than existing free alternatives. Builder’s minimal script approach is the fastest way to get real user feedback and measure completion rates.

**Revised Stance:**  
Prioritize a rapid, no-frills MVP (Builder’s plan) to test user activation and retention. Simultaneously, run a landing page and survey (Skeptic’s suggestion) to gauge demand and B2B interest. If user conversion and B2B signals are weak, pivot or kill quickly.

**Action:**  
- Build and ship Builder’s MVP in one week.
- Launch a waitlist and survey.
- Interview 3+ bootcamps/universities for B2B validation.

This approach balances speed, risk, and learning—maximizing actionable insight with minimal investment.