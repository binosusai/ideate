# Spec: Micro SaaS landing page roast agent

## ADDED Requirements

### Requirement: Runnable local proof of concept
The system SHALL include a local proof of concept that demonstrates the core idea without requiring paid services by default.

#### Scenario: User runs the POC
- **WHEN** the user follows the instructions in `poc_report.md`
- **THEN** the POC runs locally or clearly explains missing prerequisites

### Requirement: Engineering handoff
The system SHALL provide enough context for a larger agent crew to continue implementation.

#### Scenario: Engineering crew receives the folder
- **WHEN** the crew reads `handoff.md`
- **THEN** it can identify mission, inputs, guardrails, and next tasks
