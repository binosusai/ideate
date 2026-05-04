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
2. **Current Alternatives & Willingness-to-Pay:** Teams use RapidAPI Teams, AWS Secrets Manager, or custom scripts. Willingness-to-pay is highest during rapid onboarding/offboarding, frequent API key rotation, and audit/compliance events.
3. **Entry Wedge:** Free tier for up to 3 APIs/project, promoted via dev-focused Slack/Discord communities and accelerator partnerships. Slack onboarding bot as a differentiator. Paid plans start at $49/mo/project for advanced audit and team features.

**Risks:**
- **Switching Friction:** Security/compliance concerns and existing vault integrations may slow adoption, especially for teams with ingrained workflows.
- **Perceived Redundancy:** If positioned as “just another secrets manager,” developers may not see enough differentiation to justify switching.

**Recommendation:**  
Target integration-heavy SaaS startups in accelerators with a free tier and Slack onboarding bot. Focus messaging on “single-key onboarding” and rapid key rotation to stand out from generic secrets managers.
- User Researcher: **Findings:**  
1. **Trigger:** Developers are prompted to manage multiple third-party API keys when starting new projects or onboarding teammates, especially during integration sprints or compliance reviews.  
2. **Current Workaround:** Teams juggle plaintext .env files, shared vaults (e.g., AWS Secrets Manager), or ad-hoc scripts. These methods are error-prone, slow, and create onboarding friction—especially when keys change or teammates join/leave.  
3. **Sharpest Pain Point:** The highest friction is during initial project setup and key rotation: copying, securing, and updating multiple keys across environments leads to mistakes, delays, and security lapses.

**Risks:**  
1. **Adoption Barrier:** If the unified gateway requires more initial setup than simply copying keys into .env files, developers may abandon it before seeing value.  
2. **Security Trust:** Users may hesitate to trust a new tool with all their API keys unless its local-only, minimal-permission model is obvious and auditable.

**Recommendation:**  
Ship a CLI-first, file-backed MVP:  
- `init` command creates a project and unified key.  
- `add-api` stores third-party keys locally (encrypted).  
- `proxy` command starts a local server for API calls.  
- Success = running a real integration (e.g., Stripe + SendGrid) through the proxy in <30 minutes.  
- Emphasize local-only, no cloud, no raw key exposure.
- Technical Scout: **Findings:**
1. **Minimal Architecture:** A local CLI tool can generate a unified project key, store third-party API keys encrypted in a local file, and run a lightweight local proxy (e.g., Flask/FastAPI) that maps unified key requests to real third-party APIs.  
2. **Mocking Needs:** For the POC, third-party API endpoints should be mocked (e.g., via httpbin or local stub servers) to avoid handling real credentials and rate limits. Key rotation/revocation logic can be implemented with simple file updates and simulated expiry.  
3. **Security Constraints:** Local encryption (e.g., using Fernet or OS keyring) is sufficient for POC, but real-world use will require hardened storage, audit logging, and secure key handling—these can be stubbed or logged to file for now.

**Risks:**
1. **Single Point of Failure:** The unified key and local proxy represent a critical security risk—if compromised, all downstream API keys are exposed.  
2. **Integration Fragility:** Real third-party API integrations may introduce unexpected auth flows (OAuth, JWT, etc.) that are non-trivial to generalize; POC should mock these flows.

**Recommendation:**  
Build the MVP with a local CLI, encrypted file storage, and a mock proxy server. Mock all third-party APIs and key rotation. Defer real integrations and advanced security until after demo validation.
