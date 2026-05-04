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
  - SaaS startups (5–100 devs) integrating multiple third-party APIs (payments, comms, analytics)  
  - Agencies building/maintaining client apps with varied API dependencies  
  - DevOps/Platform teams at mid-size tech firms managing API credentials at scale  

- Willingness-to-Pay Signals:  
  - High: Teams citing security/audit pain, onboarding friction, or frequent API churn  
  - Medium: Agencies billing for managed services, seeking operational efficiency  
  - Low: Solo devs, hobby projects, or orgs with strict in-house credential policies  

- Competing Tools:  
  - Vaults (HashiCorp Vault, AWS Secrets Manager) — focus on storage, not proxying or unified key  
  - API gateways (Kong, Tyk) — traffic management, not credential abstraction  
  - Env management (Doppler, 1Password) — storage/sharing, not dynamic provisioning  

- Entry Pricing Angle:  
  - Freemium: Free for 1 project, $29–$99/mo for teams (usage/seat-based)  

- Narrow Wedge for Distribution:  
  - Target agencies managing multiple client projects—offer plug-and-play onboarding and white-labeling to reduce their credential chaos.
- User Researcher: **Daily Pain & Current Workflow:**
- Trigger: Developer starts a new project or integrates a new third-party tool.
- Friction Points:
  - Must sign up and generate separate API keys for each tool.
  - Manually store, rotate, and secure keys (often in multiple places).
  - Onboarding new team members requires sharing and tracking multiple credentials.
  - Revoking or rotating keys across tools is tedious and error-prone.
- Workarounds:
  - Use shared documents or password managers to distribute keys (security risk).
  - Write custom scripts to manage environment variables.
  - Rely on manual tracking (spreadsheets, notes).
- Desired Outcome:
  - Single API key per project.
  - Centralized, secure credential management.
  - Fast onboarding for new tools and team members.

**First-Run Workflow Recommendation:**
1. Sign up and create a new project.
2. Generate a unified project API key.
3. Connect third-party tools via a simple UI (select tools, enter credentials once).
4. Use the unified key in code/configuration.
5. Monitor usage and manage access centrally.

**Week-One Success Criteria:**
- User connects at least 2 third-party tools.
- Unified key is used in a live dev/test environment.
- User successfully onboards a teammate with no extra key sharing.
- Technical Scout: **Local-First MVP Feasibility & Blockers**

- **Minimal Architecture:**
  - Local proxy server (runs on developer machine) intercepts API calls, injects correct third-party keys.
  - Local encrypted store for mapping unified project key → individual service keys.
  - Simple CLI/GUI for key management and onboarding new tools.
  - Config file per project for mapping endpoints/services.

- **POC: What to Mock vs. Build**
  - **Mock:** 
    - Third-party API endpoints (simulate a few popular APIs, e.g., Stripe, SendGrid).
    - Key provisioning backend (hardcode key mapping logic).
    - User authentication (assume trusted local user).
  - **Build:** 
    - Local proxy logic (request interception, key injection, routing).
    - Encrypted local key store.
    - Basic CLI for adding/removing service keys.

- **Likely Blockers:**
  - Handling diverse auth schemes (Bearer, OAuth, API key in headers/query).
  - Secure local storage (cross-platform encryption, key rotation).
  - Proxying non-HTTP APIs or websocket traffic.
  - Scaling to cloud or multi-user scenarios (out of local-first scope).
  - User trust: running a local proxy may raise security/UX concerns.

- **Actionable Next Steps:**
  - Prototype local proxy for 2-3 HTTP APIs with simple key injection.
  - Validate encrypted local key store on target OSes.
  - Gather developer feedback on CLI UX and integration friction.
