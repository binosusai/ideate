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
- Market Researcher: Findings

- Narrowest ICP: Seed-to-Series B SaaS startups (5–30 devs) building integrations-heavy products (e.g., workflow automation, analytics, SaaS aggregators) that frequently onboard new APIs and already use tools like Zapier, Make, or RapidAPI.
- Willingness-to-pay signals: Teams currently paying for API management (e.g., RapidAPI Teams, AWS Secrets Manager), or using paid CI/CD tools with secret management add-ons; pain is highest during onboarding/offboarding and key rotation.
- Current alternatives: Manual key management in vaults (HashiCorp Vault, AWS Secrets Manager), brittle homegrown scripts, or basic API gateways—none offer unified provisioning/proxying with a single project key.

Risks

- High switching friction: Security/compliance concerns and existing vault integrations may slow adoption, especially for teams with established workflows.
- Tooling inertia: Developers may resist replacing familiar secret management tools unless the new solution is clearly superior and easy to trial.

Recommendation

- Entry wedge: Target VC-backed SaaS startups using Zapier/Make, offering a free tier (up to 3 APIs) and a Slack onboarding bot. Distribute via dev-focused Slack/Discord communities and partner with early-stage accelerators for rapid feedback.
- User Researcher: Findings

- Trigger: Developers face friction when onboarding new integrations or rotating credentials—especially during team growth or security audits—requiring manual distribution and mapping of multiple third-party API keys.
- Workaround: Teams typically store API keys in shared vaults (e.g., AWS Secrets Manager, HashiCorp Vault), use ad hoc scripts for key injection, and rely on tribal knowledge to map which key belongs to which service per project.
- Sharpest pain: Onboarding a new developer or rotating keys is slow and error-prone—manual steps lead to misconfigurations, delays, and increased risk of credential leaks or outages.

Risks

- Security/compliance: Users may hesitate to trust a new proxy with sensitive credentials, especially if it lacks audit trails or enterprise integrations.
- Adoption inertia: Teams already invested in vault tooling may resist switching unless the new workflow is demonstrably faster and safer.

Recommendation

- First-run workflow: CLI tool initializes a project, prompts for 2–3 sandbox API keys, generates a single project key, and starts a local proxy—demoing successful routing to sandbox APIs with visible logs. Success = new dev onboarded and making proxied API calls in under 10 minutes.
- Technical Scout: Findings

- Minimal Architecture: A local CLI tool can generate a unified project API key, store mappings in a file (YAML/JSON), and run a lightweight proxy server that routes requests to 2–3 sandboxed third-party APIs using stored keys. No cloud or user auth needed.
- Mocking Needs: Third-party APIs should be mocked or use public sandbox endpoints to avoid real credential exposure and simplify demo setup. Key rotation can be simulated by updating the config file and reloading the proxy.
- Integration Constraints: The MVP avoids integrating with real secret managers (e.g., AWS Secrets Manager, Vault) and skips multi-user access, focusing solely on local developer experience and CLI-driven workflows.

Risks

- Security Gaps: Local file storage and lack of user authentication are insecure for real use; this is acceptable for a POC but must be flagged to avoid misuse.
- API Compatibility: Some third-party APIs may have non-standard auth flows or rate limits, complicating proxy logic if not carefully selected for the demo.

Recommendation

- Proceed with a CLI-first, local-only MVP using mocked or sandbox APIs, clearly labeling it as a demo to avoid security misunderstandings. Defer secret manager and multi-user integration until core proxying value is proven.
