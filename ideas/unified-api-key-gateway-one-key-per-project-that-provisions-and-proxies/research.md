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
  - SaaS startups (5–50 devs) integrating multiple third-party APIs (payments, analytics, messaging)  
  - Agencies building/maintaining client apps with varied API integrations  
  - DevOps/Platform teams at mid-sized tech firms managing internal/external API access

- Willingness-to-Pay Signals:  
  - Teams citing security/audit concerns around API key sprawl  
  - Frequent onboarding/offboarding of devs or tools  
  - Pain around rotating/revoking keys during incidents  
  - Current spend on API management/security tools

- Competing Tools:  
  - Vaults (HashiCorp Vault, AWS Secrets Manager) — focus on secrets, not unified API key provisioning  
  - API gateways (Kong, Tyk) — proxy APIs, but don’t unify third-party key management  
  - Internal scripts/spreadsheets — manual, error-prone

- Entry Pricing Angle:  
  - $49–$99/mo per project for up to X third-party integrations; free tier for 1–2 integrations

- Narrow Wedge for Easiest Distribution:  
  - Target early-stage SaaS startups using 3+ third-party APIs (Stripe, SendGrid, Segment, etc.) via dev tool marketplaces (e.g., GitHub Marketplace, Product Hunt)
- User Researcher: **Daily Pain & Current Workflow:**
- **Trigger:** Developer starts a new project or integrates a new third-party tool.
- **Friction Points:**
  - Must register for each tool separately.
  - Manually generate, copy, and securely store multiple API keys.
  - Risk of exposing keys in code repos or sharing them insecurely with team members.
  - Revoking or rotating keys is tedious and error-prone.
- **Workarounds:**
  - Use spreadsheets or password managers to track keys.
  - Share keys via insecure channels (chat, email).
  - Write custom scripts for key rotation or environment variable management.
- **Desired Outcome:**  
  - Provision and manage all third-party API keys from a single place.
  - Share access with teammates securely.
  - Quickly onboard new tools with minimal manual steps.

**First-Run Workflow (Week-One Success Path):**
1. Sign up and create a new project.
2. Obtain a single unified API key for the project.
3. Select and connect desired third-party tools via the dashboard.
4. Gateway provisions/links all required keys behind the unified key.
5. Copy and use the unified key in app code/config.
6. Invite team members and set permissions.

**Success Criteria:**
- User integrates at least 2 tools using the unified key.
- All project members access and use the same unified key.
- No manual key copying or sharing outside the platform.
- Technical Scout: **Local-First POC Feasibility & Blockers**

- **Core MVP Architecture**
  - Local proxy server (e.g., Node.js/Go) intercepts API calls, maps unified key to stored third-party keys.
  - Local encrypted storage (e.g., SQLite, filesystem, or lightweight vault) for API keys.
  - Config file/UI for mapping unified key to third-party services.
  - Minimal admin UI for key management (can be CLI for POC).

- **Integration Constraints**
  - Third-party APIs have diverse auth flows (static keys, OAuth, JWT, etc.); POC should focus on static API key services (e.g., SendGrid, Stripe).
  - Rate limiting, error handling, and logging must be handled per service.
  - Some APIs may restrict proxying or require IP allowlisting—mock these for POC.

- **POC: Mock vs. Build**
  - **Build:** Local proxy, key mapping logic, encrypted storage, basic CLI.
  - **Mock:** Third-party API endpoints (simulate responses), advanced auth flows (OAuth), team onboarding flows.

- **Likely Blockers**
  - Handling OAuth/refresh tokens locally is complex—defer for POC.
  - Security: Local key storage must be robust even in MVP.
  - Scaling to multi-user/team scenarios requires careful design—single-user focus for POC.
