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
- Market Researcher: - ICP Segments:  
  - SaaS startups (5–100 devs) integrating multiple third-party APIs (payments, analytics, messaging, etc.)  
  - Agencies building/maintaining client projects with varied API dependencies  
  - DevOps/Platform teams at mid-sized tech companies managing API credentials at scale  

- Willingness-to-Pay Signals:  
  - Teams citing security/audit concerns around API key sprawl  
  - Frequent onboarding/offboarding of devs or tools  
  - Companies subject to compliance (SOC2, HIPAA) needing credential traceability  
  - Current spend on API management, secrets vaults, or internal tooling  

- Competing Tools:  
  - HashiCorp Vault, AWS Secrets Manager, Doppler (for secrets, not unified API proxying)  
  - API gateways (Kong, Tyk) — focus on traffic, not credential abstraction  
  - Homegrown scripts/Spreadsheets for key tracking  

- Entry Pricing Angle:  
  - $49–$99/mo per project for up to X API integrations, targeting cost below combined time/tooling savings  

- Narrow Wedge for Distribution:  
  - Start with dev agencies managing multiple client projects — pain is acute, easy to reach via dev agency networks and communities.
- User Researcher: **Current User Journey**

- **Trigger:** Need to integrate multiple third-party APIs into a project (e.g., payments, analytics, notifications).
- **Friction Points:**
  - Manually generating, storing, and rotating dozens of API keys.
  - Sharing keys securely with teammates.
  - Tracking which key belongs to which service or environment.
  - Revoking access when team members leave.
- **Workarounds:**
  - Ad-hoc key storage (spreadsheets, password managers).
  - Custom scripts for key rotation.
  - Manual onboarding docs for new team members.
- **Desired Outcome:**  
  - One secure, project-scoped API key to access all integrated services.
  - Simplified onboarding/offboarding.
  - Centralized visibility and control over all third-party credentials.

---

**First-Run Workflow Recommendation**

1. **Sign up / Log in.**
2. **Create a new project.**
3. **Select third-party APIs to connect.**
4. **Authorize and provision connections (OAuth, API key input).**
5. **Receive a unified project API key.**
6. **Integrate this single key into project codebase.**
7. **Monitor usage and add/remove APIs as needed.**

**Week-One Success Criteria**

- User provisions at least 2 third-party APIs via the gateway.
- User integrates the unified key into their project.
- User successfully onboards a teammate with minimal friction.
- Technical Scout: - **Local-first MVP Feasibility**
  - Local proxy service can intercept and route API calls using a unified project key.
  - Store third-party API keys locally (e.g., encrypted file, local DB).
  - Map unified key to per-tool credentials in proxy logic.

- **Implementation Risks**
  - Security: Storing and handling multiple sensitive API keys locally increases risk; strong encryption and access controls needed.
  - Key Rotation: Handling third-party key expiry/rotation locally is complex.
  - Rate Limiting: Proxy must handle and surface rate limits/errors from each backend API.
  - API Schema Drift: Third-party API changes may break proxy logic.

- **Integration Constraints**
  - Some APIs require IP allowlisting or OAuth flows—difficult to automate locally.
  - SDKs/libraries may not support proxying out-of-the-box; may require custom adapters.

- **Minimal Architecture**
  - Local proxy (Node.js/Go) with pluggable backend connectors.
  - Config file/UI for managing third-party keys.
  - Mock: Third-party API responses, error handling, and rate limiting.
  - Build: Core proxy logic, local key storage, unified key issuance.

- **Action**
  - Build local proxy with mock connectors for 2-3 popular APIs.
  - Validate unified key routing, local credential management, and error surfacing.
