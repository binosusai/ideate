## ADDED Requirements

### Requirement: Ideate Workflow Uses Approved Blueprint Context
The system SHALL use the approved blueprint as the source of truth for Ideate research, debate, planning, proposals, POCs, and review loops.

#### Scenario: Research starts from approved blueprint
- **WHEN** research starts for an idea created from a blueprint
- **THEN** the research stage receives the blueprint `why` and `details_json`
- **AND** the generated research artifact reflects the blueprint context

#### Scenario: Proposal includes blueprint details
- **WHEN** the OpenSpec proposal is generated
- **THEN** the proposal includes the approved blueprint details
- **AND** the proposal does not rely only on the original one-line idea

### Requirement: Workflow Runs Asynchronously
The system SHALL run long-running Ideate work outside dashboard request handlers.

#### Scenario: User starts Ideate workflow
- **WHEN** the user starts the workflow for an approved blueprint
- **THEN** the system queues or dispatches the workflow
- **AND** the HTTP request returns without waiting for all stages to finish

#### Scenario: Workflow fails
- **WHEN** a workflow stage fails
- **THEN** the system records a sanitized error and failed stage
- **AND** the dashboard displays a user-facing failure state

### Requirement: Proposal And POC Review Loop
The system SHALL allow the user to review generated proposals and POCs before advancing the idea.

#### Scenario: User approves proposal
- **WHEN** the user approves a generated proposal
- **THEN** the idea becomes eligible for POC generation
- **AND** a decision row records the approval

#### Scenario: User requests proposal revision
- **WHEN** the user requests revision with feedback
- **THEN** the feedback is stored for the next Ideate iteration
- **AND** the workflow can rerun with prior artifacts and feedback in context

#### Scenario: User accepts POC
- **WHEN** the user accepts a generated POC
- **THEN** the idea is marked accepted for the Ideate phase
- **AND** the idea becomes eligible for future Minions handoff
