# Spec: Ideate Review Loop

## ADDED Requirements

### Requirement: Persisted review state for idea iteration
The system SHALL persist review state for each idea so the pipeline can distinguish ideas awaiting review, ideas approved as good enough, and ideas that require another iteration.

#### Scenario: POC awaits human review
- **WHEN** the pipeline completes POC generation
- **THEN** the idea is marked `pending_review`
- **AND** the idea is excluded from automatic reselection until a review outcome is recorded

#### Scenario: User approves a POC
- **WHEN** the user approves the review stage
- **THEN** the idea is marked `approved`
- **AND** `tinkered` is set to true
- **AND** the idea is excluded from future automatic reselection

#### Scenario: User requests another iteration
- **WHEN** the user rejects the current POC or requests changes
- **THEN** the system stores the review outcome as `revise`
- **AND** `tinkered` remains false
- **AND** feedback is persisted for the next run

### Requirement: Revision feedback must inform later research and debate
The system SHALL feed the previous decision and latest review feedback into later research and debate runs for the same idea.

#### Scenario: Revised idea is researched again
- **WHEN** an idea with a previous `revise` outcome enters research
- **THEN** the research agent receives prior artifacts and the latest user feedback as explicit iteration context

#### Scenario: Revised idea is debated again
- **WHEN** an idea with a previous `revise` outcome enters debate
- **THEN** the debate agent receives prior artifacts and the latest user feedback as explicit iteration context

### Requirement: Expanded crew roles for design and architecture
The system SHALL include dedicated design and software architecture roles in the crew.

#### Scenario: Planning artifacts are generated
- **WHEN** the crew produces planning outputs
- **THEN** the outputs include a designer perspective on workflow and UX quality
- **AND** a software architect perspective on component boundaries and system interactions

### Requirement: Generated POCs include a Mermaid architecture diagram
The system SHALL generate a Mermaid diagram showing how the main POC components interact.

#### Scenario: README is generated for a POC
- **WHEN** the POC README is written
- **THEN** it contains a Mermaid component diagram for the generated system

### Requirement: Hosted verification path is documented
The system SHALL document a future hosted verification path for generated POCs.

#### Scenario: User reviews deployment options
- **WHEN** the user reads the generated planning or architecture documentation
- **THEN** they can identify recommended low-cost hosting options for frontend and API verification
- **AND** understand that hosted verification is optional until explicitly implemented