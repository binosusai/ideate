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
1. **ICP Segment:** 5–30 person, VC-backed SaaS startups in accelerator programs, building integration-heavy products (e.g., workflow automation, SaaS aggregators) without dedicated DevOps/security staff.
2. **Current Alternatives & Willingness-to-Pay:** Teams rely on RapidAPI Teams, AWS Secrets Manager, or custom scripts. Willingness-to-pay spikes during rapid onboarding/offboarding, frequent API key rotation, and audit/compliance events.
3. **Entry Wedge & Pricing:** Free tier for up to 3 APIs/project, promoted via dev-focused Slack/Discord communities and accelerator partnerships. Slack onboarding bot as a differentiator. Paid plans start at $49/mo/project for advanced audit and team features.

**Risks:**
- **Switching Friction:** Security/compliance concerns and existing vault integrations may slow adoption, especially for teams with ingrained workflows.
- **Perceived Redundancy:** If positioned as “just another secrets manager,” developers may not see enough differentiation to justify switching.

**Recommendation:**  
Target integration-heavy SaaS startups in accelerators with a free tier and Slack onboarding bot. Focus messaging on “single-key onboarding” and rapid key rotation to stand out from generic secrets managers.
- User Researcher: Findings  
- Trigger: Developers are forced to wrangle multiple third-party API keys when onboarding a new teammate, rotating credentials, or integrating a new tool—especially acute during rapid team growth or compliance audits.
- Current Workaround: Most teams use a mix of shared password managers (e.g., 1Password), brittle scripts, and copy-pasting keys into local .env files; some use generic secrets managers but still require manual proxy/config for each service.
- Sharpest Pain Point: The highest friction occurs during onboarding/offboarding and key rotation—manual steps are error-prone, slow, and create security/audit gaps, especially when updating keys across multiple environments.

Risks  
- Security Perception: Developers may distrust a local proxy that handles all credentials, fearing leaks or loss of control, especially without visible audit trails or open-source transparency.
- Adoption Hurdle: If initial setup (e.g., configuring the proxy, importing keys) takes more than 10–15 minutes or feels less secure than current methods, users will abandon before seeing value.

Recommendation  
- First-Run Workflow: CLI tool with `init` (new project), `add-tool` (connect Stripe/GitHub), and `start-proxy` (run local gateway); immediately test a real API call via the proxy and show a clear audit log entry to prove it works—success is “one-key, one-command, working API call” within 10 minutes.
- Technical Scout: **Findings:**
1. A local CLI tool can credibly generate a “project key,” store third-party API keys in an encrypted file (e.g., using Python’s `cryptography` or Node’s `keytar`), and run a lightweight proxy (Flask/FastAPI or Express) to inject credentials and forward requests.
2. For MVP, proxying 2–3 APIs (e.g., Stripe, GitHub, Slack) is feasible using their public REST endpoints; real API calls can be made if user supplies valid keys, but for demo, responses can be mocked with static JSON.
3. Audit logging (per-request, per-tool) can be implemented as local file writes; rotation of the “project key” can simply re-encrypt the stored secrets.

**Risks:**
1. Secure local key storage is nontrivial—OS keychains are safer but add cross-platform complexity; file-based encryption is easier but less secure and may deter security-conscious users.
2. Some APIs (e.g., OAuth-based) require interactive flows or callbacks, which complicates proxying and may need to be mocked or deferred for MVP.

**Recommendation:**  
Build the MVP with file-encrypted local storage and static JSON mocks for at least one API; defer OAuth flows and advanced audit features. This enables a credible demo with minimal dependencies and clear next steps.
