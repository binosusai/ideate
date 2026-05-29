## ADDED Requirements

### Requirement: Phase 1 Runs Under Operator Context
The first public-free test SHALL run workflows using the configured operator GitHub and email context.

#### Scenario: Workflow needs GitHub or email
- **WHEN** Phase 1 workflow automation needs GitHub or email access
- **THEN** it uses server-side operator configuration already available to the deployment
- **AND** it does not ask the user for GitHub OAuth scopes or email credentials

### Requirement: User-Owned Integrations Are Deferred
The system SHALL defer per-user GitHub account and email configuration to a later phase.

#### Scenario: User signs in during Phase 1
- **WHEN** a user signs in during Phase 1
- **THEN** the system may identify the user for product access and quotas
- **AND** does not require user-owned GitHub or email authorization for workflow execution

### Requirement: Minions Handoff Is Prepared But Not Executed
The system SHALL define a future handoff point to Minions without requiring Minions execution in Phase 1.

#### Scenario: POC is accepted
- **WHEN** the user accepts the POC
- **THEN** Ideate records that the idea is ready for a future Minions handoff
- **AND** Phase 1 does not create a Minions organization, sprint, or agent roster
