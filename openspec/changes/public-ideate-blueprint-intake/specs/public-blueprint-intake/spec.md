## ADDED Requirements

### Requirement: User Idea Intake
The system SHALL provide a user-facing intake surface for submitting a rough idea or a structured idea blueprint.

#### Scenario: User submits a one-line idea
- **WHEN** an authenticated user submits a one-line idea
- **THEN** the system accepts the text as blueprint-generation input
- **AND** does not start research, debate, planning, proposal, or POC work until a blueprint is approved

#### Scenario: User submits a structured blueprint
- **WHEN** an authenticated user submits a YAML or JSON blueprint
- **THEN** the system validates and normalizes it against the canonical blueprint schema
- **AND** displays validation errors without creating an idea when the blueprint is invalid

### Requirement: AI Blueprint Generation
The system SHALL convert a rough idea into a structured blueprint using an AI tool.

#### Scenario: Blueprint is generated
- **WHEN** the user requests blueprint generation from a rough idea
- **THEN** the AI tool returns a structured draft with title, category, why, and details
- **AND** the system validates the draft before showing it to the user

#### Scenario: Generated blueprint has uncertainty
- **WHEN** the AI tool is uncertain about target users, implementation, monetization, or risks
- **THEN** the blueprint records uncertainty under `open_questions`
- **AND** avoids presenting uncertain assumptions as verified facts

### Requirement: Blueprint Review Gate
The system SHALL require user approval before a generated or submitted blueprint becomes workflow input.

#### Scenario: User approves blueprint
- **WHEN** the user approves a valid blueprint
- **THEN** the system persists the blueprint to the active database
- **AND** creates or updates the corresponding idea with full `why` and `details_json`

#### Scenario: User edits blueprint
- **WHEN** the user edits a generated blueprint before approval
- **THEN** the system validates the edited blueprint
- **AND** persists the edited version, not the original generated version, after approval

### Requirement: Public Intake Uses Protected Server-Side APIs
The system SHALL keep model credentials, database credentials, and workflow credentials server-side.

#### Scenario: Browser generates blueprint
- **WHEN** the browser calls the blueprint-generation API
- **THEN** the browser sends only user input and receives only the generated draft or validation errors
- **AND** the browser never receives model API keys, database URLs, GitHub tokens, or email credentials
