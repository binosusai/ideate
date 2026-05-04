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
1. **Trigger:** Developers are tasked with integrating or rotating multiple third-party APIs (e.g., onboarding a new SaaS integration or responding to a security audit).
2. **Current Workaround:** Teams use spreadsheets, shared vaults (e.g., 1Password, AWS Secrets Manager), or ad hoc scripts to track and distribute API keys—often resulting in manual copy-paste, inconsistent access, and audit gaps.
3. **Sharpest Pain Point:** The most acute friction is during urgent key rotation or onboarding/offboarding, where delays or mistakes expose security risks and slow team velocity.

**Risks:**
1. **Perceived Overlap:** Users may see the MVP as duplicative of secrets managers, missing the unique proxying/unified-key value unless clearly demonstrated.
2. **Local-Only Limitation:** A local, file-backed MVP may fail to show value for multi-user or remote teams, limiting validation to solo or small colocated teams.

**Recommendation:**  
Design the first-run workflow as: `CLI install → project init → add one third-party API key → generate unified project key → test proxy with sample API call`. Success in week one = user replaces at least one manual key handoff with the unified key and confirms working proxy.
- Technical Scout: **Findings:**
1. **Minimal Architecture:** A CLI tool can generate a unified project key, store third-party API keys in an AES-256-encrypted local file, and run a local proxy server that maps unified key requests to real API keys. No cloud or external dependencies are required for the MVP.
2. **Mocking Needs:** For the POC, third-party API endpoints should be mocked (e.g., via local HTTP servers or stubbed responses) to avoid handling real credentials and to simplify demo setup. Audit logging can be implemented as local file writes.
3. **Security Constraints:** Local encryption (e.g., using a passphrase or OS keyring) is feasible, but secure key rotation and multi-user access must be deferred or simulated. RBAC and zero-knowledge features should be documented but not built in the POC.

**Risks:**
1. **Security Gaps:** Local storage is vulnerable if the developer’s machine is compromised; this risk is acceptable for a POC but must be addressed before real usage.
2. **Integration Complexity:** Mapping arbitrary third-party API schemas to a unified proxy may require custom adapters; for MVP, limit to 1–2 well-known APIs (e.g., Stripe, SendGrid).

**Recommendation:**  
Build the CLI and local proxy with mock third-party APIs and encrypted file storage. Defer multi-user, cloud sync, and advanced RBAC to post-POC.
