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
- Narrowest ICP: Seed-stage SaaS startups (2–10 devs) integrating multiple third-party APIs (e.g., Stripe, SendGrid, Twilio) and lacking dedicated DevOps/security resources.  
- Alternatives: Manual key management (env files, vaults), API gateway plugins (Kong, Tyk), and secret managers (AWS Secrets Manager, HashiCorp Vault) — all require more setup and lack unified provisioning.  
- Willingness-to-pay signals: Startups paying for developer productivity tools (e.g., Sentry, Linear), and those with recent security incidents or compliance needs, show higher urgency and budget ($30–$100/mo/project).

Risks  
- High switching friction: Existing projects may resist migrating key management due to perceived risk or integration effort.  
- Security trust barrier: Early-stage tool must overcome skepticism about centralizing sensitive credentials.

Recommendation  
- Entry wedge: Launch as a GitHub Marketplace app targeting new SaaS projects at repo creation, offering instant API key provisioning for top 5 third-party APIs with a free tier and simple onboarding.
- User Researcher: Findings:
- Trigger: Developers need to integrate multiple third-party APIs for a new or existing project, prompting tedious credential setup and sharing.
- Current workaround: Teams manually create, store, and rotate individual API keys in environment files or secret managers, often duplicating effort and risking exposure.
- Sharpest pain point: High cognitive load and security risk from scattered keys; onboarding new APIs or rotating credentials is slow and error-prone.

Risks:
- Integrations may break if the unified gateway fails or is misconfigured, causing cascading downtime across all connected APIs.
- Third-party APIs with complex auth flows (OAuth, scopes) may not be easily abstracted, limiting immediate compatibility.

Recommendation:
- First-run workflow: On project creation, prompt user to connect required third-party APIs via OAuth or key input, auto-generate a single unified project key, and provide a test endpoint to validate proxying works. Success: User provisions at least 2 APIs and successfully makes a proxied call within the first week.
- Technical Scout: Findings:
- Minimal MVP can proxy requests via a local gateway (e.g., Node.js/Express) that maps a unified project key to stored third-party API keys; local storage (e.g., SQLite or flat file) suffices for initial credential management.
- For a POC, third-party API integrations should be mocked (e.g., stubbed HTTP responses) to avoid handling real credentials and rate limits; real key provisioning and rotation logic can be deferred.
- Core logic (key mapping, proxy routing, basic authentication) can be built now; UI for onboarding and key management can be CLI-based to accelerate delivery.

Risks:
- Secure storage and handling of third-party API keys is non-trivial; local storage may not meet security requirements for real use.
- Some APIs require OAuth or dynamic secrets, complicating unified key abstraction and requiring more complex mocking or integration logic.

Recommendation:
- Build a CLI-based local gateway MVP with mocked third-party APIs and simple key mapping; validate developer workflow before investing in secure storage or real integrations.
