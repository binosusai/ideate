# Research Brief: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Raw Intent
Developers manage dozens of API keys across tools; one unified key per project reduces setup friction, centralizes credential management, and lets teams onboard new tools with a single click

## Track
This idea is on the `money` track, so the primary research lens is commercial opportunity.

## Working Hypothesis
Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys is worth exploring if it can produce a visible result within one week and a useful proof of concept within one focused session.

## Research Questions
- Who experiences this problem often enough to care?
- What painful alternative are they using today?
- What is the smallest demo that proves the idea?
- What would make this idea obviously not worth pursuing?
- What data, API, or permission would block implementation?

## Initial Recommendation
Continue to debate. The idea is strong enough for structured criticism, but not yet ready for full engineering crew handoff.

## Crew Additions
- Market Researcher: **Findings:**
1. **Narrowest ICP:** 5–30 person, VC-backed SaaS startups in accelerator programs, building integration-heavy products (e.g., workflow automation, SaaS aggregators) without dedicated DevOps/security staff.
2. **Current Alternatives & Willingness-to-Pay:** Teams use RapidAPI Teams, AWS Secrets Manager, or brittle scripts; willingness-to-pay spikes during rapid onboarding/offboarding, frequent API key rotation, and audit/compliance events.
3. **Entry Wedge:** Free tier covering up to 3 APIs/project, promoted via dev-focused Slack/Discord communities and accelerator partnerships, with Slack onboarding bot as a differentiator.

**Risks:**
- **Switching Friction:** Security/compliance concerns and existing vault integrations may slow adoption, especially for teams with ingrained workflows.
- **Perceived Redundancy:** If positioned as “just another secrets manager,” developers may not see enough differentiation to justify switching.

**Recommendation:**  
Target integration-heavy SaaS startups in accelerators with a free tier and Slack onboarding bot. Focus messaging on “single-key onboarding” and rapid key rotation to stand out from generic secrets managers.
- User Researcher: **Findings:**
1. **Trigger:** Developers are prompted to manage multiple third-party API keys when onboarding new teammates or integrating additional SaaS tools, often under time pressure (e.g., sprint deadlines, compliance audits).
2. **Current Workaround:** Teams use spreadsheets, password managers (e.g., 1Password), or brittle scripts to share, rotate, and revoke API keys, leading to delays, errors, and security risks.
3. **Sharpest Pain Point:** The highest friction is onboarding new team members—developers waste time requesting, copying, and validating multiple keys for each tool, often missing updates or exposing keys accidentally.

**Risks:**
1. **Perceived Complexity:** If the first-run workflow requires more steps than existing manual methods, users may abandon before seeing value.
2. **Security Skepticism:** Without clear local encryption and zero cloud sync, users may distrust storing sensitive keys in a new tool.

**Recommendation:**  
Design the first-run workflow to deliver a “single-key onboarding” moment within 10 minutes:  
- `uakg init` → `uakg add --tool` for 2–3 tools → share unified key → simulate proxy request.  
Success = user sees all tool requests routed via one key and can onboard a teammate without manual key handoff.
- Technical Scout: **Findings:**  
1. **Minimal Architecture:** A CLI tool can generate a unified project key, locally store encrypted third-party keys, and map unified keys to real API keys using a YAML/JSON config. No backend or network proxy is required for the MVP.  
2. **Mocking Required:** Actual API requests and key rotation must be mocked—simulate proxying and rotation logic with local file reads/writes and canned responses, as real third-party API integration would require network calls and handling sensitive credentials.  
3. **Security Constraints:** Local encryption (e.g., using OS keyring or simple symmetric encryption) is sufficient for POC, but not production. No multi-user or remote access is supported; all data remains on the developer’s machine.

**Risks:**  
1. **Integration Complexity:** Extending from local simulation to real proxying (network layer, secure storage, multi-user) will introduce significant complexity and security review, slowing future delivery.  
2. **Perceived Value:** Without real API proxying, some design partners may not see enough differentiation from a secrets manager or config file, risking weak validation.

**Recommendation:**  
Proceed with the CLI-first, local-only MVP, but explicitly mock all network and rotation actions. Document these mocks and highlight them in demos to manage expectations and gather targeted feedback on the core workflow.
