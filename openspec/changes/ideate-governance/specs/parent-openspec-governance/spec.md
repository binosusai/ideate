## ADDED Requirements

### Requirement: Parent OpenSpec Change Exists
The project SHALL maintain a parent-level OpenSpec change under `ideate/openspec/changes/` to define cross-idea spec governance.

#### Scenario: Parent change is created
- **WHEN** the team initializes a parent OpenSpec change
- **THEN** the change contains proposal, design, tasks, and capability spec artifacts

### Requirement: Parent Requirements Reflect Current Implementation
Parent governance requirements SHALL map to the current ideate workflow and file layout.

#### Scenario: Parent requirements are reviewed
- **WHEN** a maintainer inspects parent spec and tasks
- **THEN** tasks and requirements align with current idea-level OpenSpec generation and workflow behavior

### Requirement: Governance Requirements Stay Implementation-Grounded
Parent governance SHALL remain synchronized with concrete ideate runtime and workflow behavior.

#### Scenario: Governance-linked runtime updates are delivered
- **WHEN** maintainers implement tasks in this parent change
- **THEN** resulting CLI, workflow, and validation updates are reflected in parent proposal, design, and tasks artifacts

### Requirement: Deterministic POC Quality Loop Exists
The project SHALL provide deterministic, file-evidence based quality scoring and iterative improvement reporting for POCs.

#### Scenario: POC quality is generated and re-scored
- **WHEN** a POC is created or scored
- **THEN** the system produces `poc_quality_score.md` and `poc_improvement_loop.md`
- **AND** scoring uses deterministic section checks mapped to required files

### Requirement: Targeted POC Patch Iteration Is Supported
The project SHALL support targeted POC patching that preserves existing POC files and only fills missing required artifacts.

#### Scenario: Improvement loop runs with feedback
- **WHEN** maintainers dispatch manual POC improvement and run patch mode
- **THEN** only missing score-critical files are generated
- **AND** the before/after score delta is available for review and notification

### Requirement: Forward Plan For Additional Governance Features
The parent change SHALL include a task roadmap for future improvements.

#### Scenario: Team plans next improvements
- **WHEN** maintainers review parent tasks
- **THEN** they can identify concrete next steps for validation automation, quality gates, and release-readiness criteria