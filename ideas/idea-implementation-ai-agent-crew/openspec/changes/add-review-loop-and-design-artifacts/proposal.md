# Proposal: Add Review Loop And Design Artifacts

## Why
The ideation system currently has no durable post-POC review state, so the same idea can be selected again when no newer ideas are available.

The workflow also lacks a clear approval-driven branch for marking a POC as accepted versus rejected with feedback for another iteration.

The crew is missing explicit design and software architecture roles, and generated POCs do not yet include a Mermaid diagram showing how components interact.

There is also no structured plan for optionally verifying a generated POC in a hosted environment.

## What Changes
- Add persisted review state for each idea, including a user-approved `tinkered` outcome and a separate review status for ideas still under revision.
- Add an approval-gated review stage after POC generation in the same pipeline.
- Add a feedback capture path so rejected or revision-requested POCs can feed the next research and debate pass instead of starting from scratch.
- Add `Designer` and `Software Architect` crew roles and require their outputs in planning artifacts.
- Add Mermaid component-diagram generation for generated POC documentation.
- Define a future hosted-verification track for static UI and API deployment on low-cost or free-tier infrastructure.

## Impact
- Prevents already-reviewed ideas from being repeatedly selected by default.
- Creates a repeatable revision loop instead of losing user feedback between runs.
- Improves POC quality with explicit UX and architecture thinking.
- Makes the generated README more useful as an implementation and review artifact.
- Creates a concrete backlog for optional cloud verification without forcing it into the first implementation slice.