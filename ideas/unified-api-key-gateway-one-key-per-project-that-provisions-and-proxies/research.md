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
1. **Narrowest ICP:** 5–30 person, VC-backed SaaS startups building integration-heavy products (e.g., workflow automation, SaaS aggregators) that already use Zapier, Make, or RapidAPI and lack dedicated DevOps/security staff.
2. **Current Alternatives & Willingness-to-Pay:** Teams currently pay for RapidAPI Teams, AWS Secrets Manager, or use brittle homegrown scripts. Willingness-to-pay is highest during rapid onboarding/offboarding, frequent API key rotation, and when audit/compliance pressure grows.
3. **Entry Pricing Angle:** Free tier covering up to 3 APIs per project, with a paid “Pro” plan unlocking unlimited APIs and Slack onboarding support. Distribution is easiest via dev-focused Slack/Discord communities and partnerships with early-stage accelerators.

**Risks:**
- **Switching Friction:** Security/compliance concerns and existing vault integrations may slow adoption, especially for teams with ingrained workflows.
- **Perceived Redundancy:** If positioned as “just another secrets manager,” developers may not see enough differentiation to justify switching.

**Recommendation:**  
Target integration-heavy SaaS startups in accelerator programs with a free tier and Slack onboarding bot. Focus messaging on “single-key onboarding” and rapid key rotation to differentiate from generic secrets managers.
- User Researcher: Findings

1. Trigger: Developers are prompted to manage multiple API keys when onboarding new integrations or rotating credentials—especially during team expansion, offboarding, or compliance reviews.
2. Current workaround: Teams use a mix of manual vault entries (e.g., AWS Secrets Manager, HashiCorp Vault), insecure spreadsheets, or ad-hoc scripts to distribute and rotate keys, leading to lost time and error-prone processes.
3. Sharpest pain point: Onboarding/offboarding and key rotation are slow, require manual coordination, and create security/compliance gaps—especially when multiple APIs/tools must be updated per project.

Risks

1. Security trust barrier: Users may hesitate to trial even a local tool with real secrets, fearing leaks or mishandling, slowing adoption.
2. Local-only limitation: Lack of team collaboration or cloud sync may reduce perceived utility for distributed teams, limiting week-one retention.

Recommendation

- Minimum first-run workflow: CLI tool (`ukg`) initializes a project, adds at least two third-party API keys, generates a unified key, and launches a local proxy. Success is a developer making a real API call via the unified key within 30 minutes of install—proving immediate reduction in manual steps.
- Technical Scout: **Findings:**
1. **Local Proxy Feasibility:** A basic HTTP proxy that maps a unified project key to stored third-party API keys is achievable using standard Python/Node libraries (e.g., http-proxy, Flask, FastAPI) with local file-backed config and encryption (libsodium or cryptography). No external dependencies required.
2. **Mocking Third-Party APIs:** For demo purposes, actual third-party API calls should be mocked (e.g., intercept requests and return canned responses) to avoid handling real credentials and to simplify setup. This enables rapid iteration and safe demoing.
3. **Minimal Security Scope:** Local file encryption for key storage is sufficient for MVP. Advanced features (multi-user, cloud sync, audit logging) can be deferred; CLI-based onboarding and rotation are enough to prove core value.

**Risks:**
1. **Security Perception:** Even with local-only storage, early users may distrust a new tool managing sensitive keys, slowing adoption or feedback.
2. **Proxy Complexity:** Supporting diverse third-party API auth schemes (headers, query params, OAuth) may require early abstraction or hardcoded logic, risking brittle code or demo limitations.

**Recommendation:**  
Build the MVP with a local proxy and file-backed key store, mocking third-party APIs. Explicitly document security limitations and focus on a CLI-driven demo to validate workflow and gather feedback before expanding scope.
