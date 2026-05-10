# Tasks: AI OSS Good-First-Issue Discovery and Guided Resolution Assistant

## Implementation Tasks
- [ ] 1. Product Workflow
- [ ] 1.1 Implement a backend service to fetch "good first issues" from popular OSS repos via GitHub API.
- [ ] 1.2 Simple user profile form capturing skill level (beginner/intermediate) and preferred languages.
- [ ] 1.3 Use rule-based filters to match issues by language and label difficulty.
- [ ] 1.4 *Tradeoff:* Avoid complex ML ranking initially; use heuristic sorting.
- [ ] 1.5 Allow users to filter by language and difficulty.
- [ ] 2. Backend APIs
- [ ] 2.1 Implement `GET /issues?skills=&languages=&competency=` endpoint in the local proxy API.
- [ ] 2.2 Implement `POST /issue/{id}/todo` endpoint in the local proxy API.
- [ ] 2.3 Implement `POST /email/send` endpoint in the local proxy API.
- [ ] 2.4 Store fetched issues JSON locally (file-based DB like SQLite or JSON files) with indexing on skills, languages, competency for quick filt...
- [ ] 2.5 Cache generated TODOs per issue to avoid repeated AI calls.
- [ ] 2.6 Persist sent email logs with timestamps and user info for metrics.
- [ ] 3. Frontend UI
- [ ] 3.1 # Implementation Plan: AI OSS Good-First-Issue Discovery and Guided Resolution Assistant.
- [ ] 3.2 Create a working proof of concept that demonstrates the core value of `AI OSS Good-First-Issue Discovery and Guided Resolution Assistant`...
- [ ] 3.3 Represent the idea as a concrete user workflow.
- [ ] 3.4 Create one runnable local draft project.
- [ ] 3.5 Include acceptance tests or manual verification steps.
- [ ] 4. Security And Access
- [ ] 4.1 Use OAuth Device Flow or GitHub Personal Access Token (PAT) for GitHub API auth to avoid complex web flows.
- [ ] 4.2 Store tokens encrypted locally (e.g., OS keychain or encrypted file).
- [ ] 4.3 No user accounts or backend session management needed.
- [ ] 4.4 Email sending can use local SMTP config or a simple API key stored locally.
- [ ] 4.5 No centralized user management or token revocation.
- [ ] 5. Data And Storage
- [ ] 5.1 Lightweight but supports complex queries for issue ranking and filtering.
- [ ] 5.2 Easy to backup, share, and inspect artifacts (DB file) by other agents or users.
- [ ] 6. Infrastructure And Delivery
- [ ] 6.1 Deployment Shape Recommendation for AI OSS Good-First-Issue Discovery and Guided Resolution Assistant.
- [ ] 7. Documentation And Handoff
- [ ] 7.1 Allow users to input skill level and preferred languages.
- [ ] 7.2 Map issues to competency tiers (easy, intermediate, hard) based on heuristics (e.g., label presence, issue complexity).
- [ ] 7.3 Allow user selection of an issue.
- [ ] 7.4 On issue selection, call AI agent to generate a step-by-step implementation checklist.

## Tracking
- [ ] 8. Validate all implemented tasks against acceptance tests for `AI OSS Good-First-Issue Discovery and Guided Resolution Assistant`.
- [ ] 9. Mark this OpenSpec change ready for handoff.
