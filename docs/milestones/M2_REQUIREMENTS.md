# MultiAgentSoftwareDelivery — M2
## AI Product Manager Agent & Requirements Engineering Studio

### 1. Role and project context

You are the implementation engineer for Milestone M2 of MultiAgentSoftwareDelivery, an enterprise-grade, multi-agent software delivery platform.

**M0:** Multi-repository microservices foundation and AI Engineering Standards.

**M1:** Project Workspace, Multi-LLM Gateway, and AI Chat Studio.

**M2:** AI Product Manager Agent, requirements discovery, PRD generation, user stories, acceptance criteria, and human approval.

The central architecture repository is:

https://github.com/swapnilpuri/MultiAgentSoftwareDelivery.git

The platform follows a multi-repository microservices architecture, with independent team ownership, CI pipelines, versioning, and deployment.

Do not convert it into a monorepo.

Use the existing AIEngineeringStandards artifacts as mandatory engineering guidelines.

**Operating model:**

- ChatGPT UI: Architecture, product planning, milestone definition, independent acceptance review.
- Codex: Implementation, tests, debugging, Git and pull request delivery.
- Human: Approval of requirements, architecture changes, milestone authorization, security-sensitive actions, and releases.
- Git: Source of truth for specifications, implementation, ADRs, and evidence.

The future platform's PM Agent must be accessible through the platform UI. It must not depend on manually copying conversations between ChatGPT and Codex.

---

### 2. Mandatory baseline reconciliation

Before implementation:

1. Read the central repository's `AGENTS.md`.
2. Read the AI Engineering Operating Model and standards manifest.
3. Read `docs/ROADMAP.md`.
4. Read relevant ADRs and microservice architecture documentation.
5. Read the latest M1 handoff and completion report.
6. Inspect all relevant M1 pull requests and outstanding review threads.
7. Discover actual Git repositories and remotes.
8. Confirm default branches and relevant commit SHAs.
9. Inspect local uncommitted modifications.
10. Preserve all existing work.

Do not assume M1 was merged simply because it was reported complete.

If M1 has open PRs or unresolved mandatory review findings, record them as prerequisites. Do not silently build M2 on unapproved, incompatible changes.

Use the smallest set of relevant file inspections necessary.

Do not repeat completed M1 work.

---

### 3. M2 objective

Implement an AI-assisted requirements engineering environment.

The user should be able to:

1. Open a project in the Angular portal.
2. Navigate to Requirements Studio.
3. Start a requirements discovery session.
4. Interact with a specialized PM Agent.
5. Provide a high-level software product description.
6. Receive contextual clarification questions.
7. Answer questions through the UI.
8. Ask the PM Agent to generate a PRD.
9. Review the generated requirements.
10. Edit the PRD manually.
11. Request AI-assisted revisions.
12. Generate epics, user stories, and acceptance criteria.
13. Inspect requirement traceability.
14. Identify missing requirements, ambiguities, and contradictions.
15. Save document versions.
16. Compare revisions.
17. Submit a requirements baseline for human approval.
18. Approve, reject, or request changes using a permitted human identity.
19. View approved requirements and approval history.
20. Continue discussions without modifying an approved baseline automatically.

The user must remain in control of the requirements and their approval.

---

### 4. Repository responsibilities

Existing repositories may include:

- `MultiAgentSoftwareDelivery`
- `masd-web`
- `masd-project-service`
- `masd-llm-gateway`
- `masd-contracts`
- `masd-infrastructure`

Introduce the following repository if it does not already exist:

`masd-agent-service`

Responsibilities:

**masd-web**

Owns the Angular Requirements Studio, discovery chat interface, document review, story management, version comparison, and approval screens.

**masd-project-service**

Owns project requirements, artifacts, versions, stories, acceptance criteria, approval records, and persisted requirement-domain state.

**masd-agent-service**

Owns PM Agent execution, agent instructions, structured-generation workflows, clarification strategy, and agent-specific validation.

**masd-llm-gateway**

Owns provider routing, model invocation, model availability, and LLM request handling.

**masd-contracts**

Owns versioned API schemas and compatibility tests.

**masd-infrastructure**

Owns local integration, service configuration, container orchestration, and integration test setup.

**MultiAgentSoftwareDelivery**

Owns platform architecture, roadmap, milestone specification, ADRs, governance, and consolidated acceptance evidence.

Maintain independent deployment boundaries.

Do not allow direct cross-service database access.

Do not duplicate LLM provider integrations inside the PM Agent.

---

### 5. PM Agent design

Implement a specialized Product Manager Agent using the established agent-framework architecture.

Use LangGraph where appropriate for stateful execution.

The initial PM Agent must support:

- Requirement discovery.
- Business-goal analysis.
- User-persona identification.
- Scope definition.
- Functional requirement extraction.
- Nonfunctional requirement identification.
- Clarification question generation.
- Assumption identification.
- Constraint identification.
- Dependency identification.
- Requirement prioritization.
- PRD generation.
- Epic generation.
- User story generation.
- Acceptance criteria generation.
- Requirement completeness analysis.
- Contradiction and ambiguity detection.
- Controlled document revision.

The agent must maintain a clear distinction between:

- User-confirmed facts.
- Existing approved requirements.
- Agent-suggested requirements.
- Unresolved questions.
- Explicit assumptions.

Do not silently convert suggestions into approved requirements.

The PM Agent must not execute development tools, modify unrelated repositories, provision infrastructure, or authorize its own requirements.

---

### 6. PM Agent conversation workflow

Implement a structured discovery lifecycle:

`DISCOVERY_STARTED`
→ `GATHERING_REQUIREMENTS`
→ `CLARIFICATION_REQUIRED`
→ `READY_FOR_DRAFT`
→ `DRAFT_GENERATED`
→ `UNDER_REVIEW`
→ `CHANGES_REQUESTED` or `APPROVED`

Use explicit, validated state transitions.

The agent should prioritize critical clarification questions rather than overwhelming the user with dozens of low-priority questions.

Questions should focus on information that materially affects requirements quality.

Support clarification topics including:

- Intended users.
- Business goals.
- Primary workflows.
- Security expectations.
- Integration requirements.
- Performance requirements.
- Compliance constraints.
- Operating environment.
- Deployment preferences.
- Data requirements.
- Out-of-scope functionality.

Allow the user to defer a question.

Unresolved material issues must remain visible in the resulting PRD.

Do not fabricate business decisions merely to make the document appear complete.

Persist discovery sessions so they survive page refreshes and service restarts.

Use idempotency and durable checkpoints for mutating operations.

---

### 7. PRD generation

Generate a structured PRD containing:

1. Product overview.
2. Problem statement.
3. Business objectives.
4. Target users and personas.
5. Key user journeys.
6. Functional requirements.
7. Nonfunctional requirements.
8. Security and privacy expectations.
9. Data requirements.
10. External integrations.
11. Business rules.
12. Dependencies.
13. Assumptions.
14. Constraints.
15. Out-of-scope items.
16. Risks.
17. Open questions.
18. Success metrics.
19. Acceptance summary.

Each requirement must have a stable identifier.

Use a structured internal representation validated with Pydantic models or equivalent typed schemas.

Render that representation in the UI and support Markdown export.

Keep rendered Markdown and structured requirements synchronized through a defined conversion and validation process.

Do not use fragile regular expressions to infer complex requirement structures from arbitrary Markdown.

Preserve user-provided information faithfully.

Clearly label assumptions, recommendations, and unresolved decisions.

---

### 8. Epics and user stories

Implement generation of:

- Epics.
- User stories.
- Acceptance criteria.
- Priority suggestions.
- Dependencies.
- Requirement relationships.

Suggested hierarchy:

`Project → PRD → Epic → User Story → Acceptance Criterion`

Each epic should trace to one or more requirements.

Each user story should have:

- Stable identifier.
- Title.
- Description.
- Actor/persona.
- Business value.
- Parent epic.
- Requirement references.
- Acceptance criteria.
- Priority.
- Status.
- Assumptions or blockers.

Prefer testable acceptance criteria, including Given/When/Then where appropriate.

Do not generate meaningless acceptance criteria simply to satisfy a count.

Detect duplicated or substantially overlapping stories where practical.

Preserve stable IDs across revisions when the underlying requirement has not changed.

---

### 9. Requirements Studio — Angular UI

Extend the existing Angular navigation without introducing a second application shell.

Create a Requirements Studio with these areas:

**A. Discovery Chat**

- PM Agent conversation.
- Streaming responses.
- Clarification questions.
- Conversation history.
- Model selection.
- Clear distinction between user messages and agent proposals.

**B. PRD Workspace**

- Structured PRD sections.
- Editable content.
- Save draft.
- Request AI revision.
- Validation feedback.
- Version history.

**C. Epics and Stories**

- Epic listing.
- Expandable story hierarchy.
- Acceptance criteria.
- Priority.
- Requirement references.
- Editing and filtering.

**D. Requirements Quality**

- Missing information.
- Contradictions.
- Ambiguities.
- Orphaned requirements.
- Missing acceptance criteria.
- Open questions.

**E. Review and Approval**

- Submit for review.
- Review current version.
- Approve.
- Reject.
- Request changes.
- View approval history.

**F. Version Comparison**

- Compare two saved PRD revisions.
- Display additions and removals.
- Highlight changed requirements.
- Show affected stories where feasible.

Maintain responsive design, accessibility, consistent typography, keyboard usability, and typed API integration.

Use the established Angular design patterns and component library.

Avoid decorative but nonfunctional controls.

---

### 10. Human-in-the-loop approval

Implement the first requirements-level approval gate.

An approval must contain:

- Project ID.
- Artifact ID.
- Artifact version.
- Artifact content hash.
- Decision.
- Approver identity.
- Timestamp.
- Optional comments.
- Approval scope.

Required decisions:

- Approve.
- Reject.
- Request changes.

An approval must apply to one immutable artifact revision.

After approval, editing must create a new draft revision rather than modifying the approved artifact.

Prevent approval of stale revisions.

Approval must be recorded through a validated server-side operation.

The PM Agent cannot approve its own output.

If production-grade authentication/authorization is not yet available, implement a clearly limited development mode and document that approval enforcement is not production-ready.

Do not use hardcoded shared identity values as evidence of secure human approval.

An approval event should be auditable.

The future Architect and Planning Agents must consume only authorized requirements baselines.

---

### 11. Model configuration

Reuse the M1 LLM Gateway.

The PM Agent should support a configurable model profile.

Configuration should include:

- Provider.
- Model.
- Generation settings.
- Token budget.
- Timeout.
- Maximum clarification rounds where applicable.
- Retry policy.
- Structured-output strategy.

Do not hardcode a single commercial LLM.

Use a compatible configured model for structured generation.

Where a provider does not reliably support structured outputs, use validated parsing with bounded retries and clear failure handling.

The UI must display the selected or actual model used.

Never route restricted project content to an unapproved provider.

Do not store credentials in source control or browser storage.

---

### 12. Requirement quality and drift prevention

Implement a requirement-quality validation pipeline.

Use deterministic validators for:

- Required sections.
- Duplicate IDs.
- Broken references.
- Invalid hierarchy.
- Missing acceptance criteria.
- Invalid states.
- Unsupported artifact versions.
- Dangling dependencies.

Use AI-assisted review for:

- Ambiguous requirements.
- Contradictory requirements.
- Potential missing business rules.
- Unverifiable acceptance criteria.
- Scope inconsistencies.

AI-assisted findings must be treated as suggestions or review findings, not absolute truth.

Each finding should include:

- Finding ID.
- Category.
- Severity.
- Affected requirement.
- Explanation.
- Suggested remediation.
- Review status.

Preserve the ability for a human to accept or reject findings.

Do not automatically add unrelated features based on an AI suggestion.

---

### 13. Persistence and data ownership

Extend the Project Service's PostgreSQL schema through versioned migrations.

Suggested domain entities:

- RequirementsSession.
- RequirementDocument.
- RequirementRevision.
- Requirement.
- Epic.
- UserStory.
- AcceptanceCriterion.
- ClarificationQuestion.
- QualityFinding.
- ApprovalRecord.

Adapt the final schema to existing M1 conventions.

Avoid unnecessary duplication.

Use optimistic concurrency or equivalent protection against conflicting edits.

Approval state transitions and immutable baselines must be transactionally consistent.

The Agent Service must access persisted requirements through authorized Project Service APIs, not direct database connections.

Implement appropriate indexes and uniqueness constraints.

Do not introduce a shared database ownership model across services.

---

### 14. API and contract design

Update `masd-contracts` before or alongside implementation.

Provide versioned contracts for:

- Requirements discovery sessions.
- PM Agent interaction.
- Clarification questions and responses.
- PRD generation.
- PRD revisions.
- Requirement listing and editing.
- Epics and stories.
- Quality findings.
- Review submission.
- Human approval.
- Approval history.
- Version comparison.
- Export.

Define structured error responses.

Document streaming event formats where relevant.

Maintain backward compatibility with M1 APIs.

Generate typed clients or use existing contract-driven integration patterns where practical.

Run contract validation and compatibility tests.

---

### 15. Security and governance

Apply AIEngineeringStandards to all affected repositories.

Mandatory controls:

- Project authorization.
- Server-side artifact access checks.
- Validated structured outputs.
- No secret exposure.
- No arbitrary tool execution from PM Agent messages.
- Explicit approval boundaries.
- Immutable approval evidence.
- Request size limits.
- Rate limiting or bounded execution.
- Sanitized errors.
- Safe Markdown rendering.
- Traceable agent actions.
- Controlled model access.
- No unapproved repository modifications.

Treat user documents and LLM-generated content as untrusted.

Do not follow instructions embedded inside imported requirements as privileged system instructions.

Prevent the PM Agent from changing platform governance policies.

Record any governance gaps that require future dedicated services.

---

### 16. Independent deployment

Maintain independent Docker images and CI pipelines.

Update the local infrastructure configuration to include the Agent Service.

Verify:

- Angular starts independently.
- Project Service starts independently.
- LLM Gateway starts independently.
- Agent Service starts independently.
- PostgreSQL is configured correctly.
- Local integration works.
- No commercial API credentials are required for deterministic testing.
- Each service has a health endpoint and documented configuration.
- Services do not depend on another repository's source files at build time.

Use a deterministic test LLM adapter for automated tests.

Do not represent mock responses as live provider results.

Do not deploy cloud infrastructure during M2.

---

### 17. Testing requirements

Implement the following testing layers.

**PM Agent tests**

- Requirement extraction.
- Clarification handling.
- Structured PRD generation.
- Invalid structured response handling.
- Retry limits.
- Model failure handling.
- Ambiguity detection.
- Unresolved question preservation.
- Prompt-injection resistance within practical deterministic fixtures.

**Project Service tests**

- Requirements persistence.
- Version creation.
- Immutable approved revisions.
- Optimistic concurrency.
- State transitions.
- Epic/story associations.
- Acceptance criteria validation.
- Approval and rejection operations.
- Stale revision rejection.
- Project access isolation.

**Frontend tests**

- Requirements Studio navigation.
- Discovery conversation.
- Clarification presentation.
- PRD editor.
- Save/reload.
- Epic and story views.
- Approval screen.
- Version comparison.
- Error handling.

**Integration tests**

- Angular to Project Service.
- Project Service to Agent Service.
- Agent Service to LLM Gateway.
- Contract validation.
- Persistence across restarts.

**End-to-end acceptance scenario**

A user creates or selects a project, describes a software product, answers PM Agent clarification questions, generates a PRD, reviews it, creates epics and stories, edits a requirement, saves a new version, and approves the final version.

Refresh the UI and verify that the approved version, traceability, and approval record persist.

Verify that an approved revision cannot be silently overwritten.

Verify that unrelated project users or contexts cannot access the artifact without authorization.

If live provider credentials are unavailable, execute the workflow using the deterministic test adapter and report it accurately.

---

### 18. Mandatory PR review and comment-resolution gate

This requirement applies to **every repository and every pull request**.

1. Create a feature branch.
2. Implement the approved milestone scope.
3. Run focused and full applicable tests.
4. Open the pull request.
5. Allow the configured AI reviewer, such as CodeRabbit, to review the PR.
6. Retrieve inline comments, review threads, general PR comments, and CI findings.
7. Address every actionable finding.
8. Add or update relevant tests for fixes.
9. Explain any incorrect or non-applicable findings in the PR discussion.
10. Never dismiss or resolve legitimate findings merely to satisfy a merge gate.
11. Push corrections to the same feature branch.
12. Trigger or await re-review where supported.
13. Repeat until actionable findings have been addressed.
14. Ensure all required review conversations are resolved appropriately.
15. Ensure required CI checks pass.
16. Record the final review status in the completion report.
17. Do not automatically merge.

If the reviewer is unavailable or not installed, explicitly report the review as BLOCKED or NOT EXECUTED.

Do not claim successful AI review without actual evidence.

A PR with unresolved required review findings is not ready to merge.

Human approval remains mandatory for merging.

---

### 19. Git workflow

Use independent feature branches:

`feature/m2-pm-requirements-studio`

in affected repositories.

Expected repositories include:

- `MultiAgentSoftwareDelivery`
- `masd-web`
- `masd-project-service`
- `masd-agent-service`
- `masd-llm-gateway`, only if required
- `masd-contracts`
- `masd-infrastructure`

Do not modify unrelated repositories.

Do not create duplicate repositories.

Check the current default branch and remote for each repository.

Commit cohesive changes.

Push and open separate pull requests where authorized.

Do not push directly to protected branches.

Do not merge automatically.

Maintain a list of compatible commits across repositories for local integration testing.

---

### 20. Documentation deliverables

In the central architecture repository, create:

- `docs/milestones/M2_REQUIREMENTS.md`
- `docs/milestones/M2_DESIGN.md`
- `docs/milestones/M2_IMPLEMENTATION_PLAN.md`
- `docs/milestones/M2_ACCEPTANCE_CRITERIA.md`
- `docs/milestones/M2_HANDOFF.md`
- `docs/milestones/M2_COMPLETION_REPORT.md`

Update relevant ADRs and architecture diagrams.

Include diagrams for:

- PM Agent interaction.
- Requirements discovery.
- PRD generation.
- Requirement versioning.
- Approval lifecycle.
- Service communication.

Update repository-specific READMEs and API documentation where necessary.

Avoid creating excessive documents that duplicate existing authoritative specifications.

---

### 21. M2 acceptance criteria

AC-01: Existing M0/M1 architecture and standards are preserved.

AC-02: PM Agent is implemented in its approved service boundary.

AC-03: PM Agent uses the existing LLM Gateway.

AC-04: Requirements discovery is available through Angular.

AC-05: Users can respond to clarification questions.

AC-06: Discovery state persists across application restarts.

AC-07: Structured PRD generation works.

AC-08: PRD sections are editable.

AC-09: PRD revisions are persisted and distinguishable.

AC-10: Epics and user stories can be generated.

AC-11: Stories trace to requirements.

AC-12: Acceptance criteria are structured and testable.

AC-13: Requirements quality validation executes.

AC-14: Unresolved assumptions and questions remain visible.

AC-15: The approval workflow supports approved/rejected/changes-requested decisions.

AC-16: Approved artifact versions are immutable.

AC-17: Stale approval attempts are rejected.

AC-18: PM Agent cannot approve its own output.

AC-19: Project access boundaries are enforced to the extent supported by the authenticated runtime.

AC-20: Version comparison works.

AC-21: API contracts are published and validated.

AC-22: Unit, integration, and applicable frontend tests pass.

AC-23: The full deterministic end-to-end discovery-to-approval workflow is verified.

AC-24: Services remain independently buildable and deployable.

AC-25: CI and AIEngineeringStandards validation pass.

AC-26: PR review comments and required conversations are appropriately resolved.

AC-27: Required CI checks pass on all affected PRs.

AC-28: M2 handoff and completion evidence are accurate.

AC-29: No autonomous coding or deployment activity is introduced in M2.

For every acceptance criterion, report one of:

- PASSED
- FAILED
- BLOCKED
- NOT EXECUTED

A mandatory criterion that remains BLOCKED or NOT EXECUTED prevents declaring M2 fully accepted.

---

### 22. Codex efficiency policy

Follow the existing AIEngineeringStandards efficiency policy.

- Start with a brief 3–7 step implementation plan.
- Review only relevant source files.
- Reuse M1 components.
- Avoid unnecessary framework changes.
- Implement small coherent slices.
- Run targeted tests after each batch.
- Perform full regression at completion.
- Parallelize independent read-only work and tests where safe.
- Avoid conflicting changes to shared Git state.
- Maintain compact progress reports.
- Store detailed evidence in milestone documents.
- Never skip critical validation to save time.
- Do not implement future milestones.

Continue autonomously through ordinary development tasks.

Escalate only consequential decisions, unavailable permissions, missing external authorization, or material architectural changes.

---

### 23. Final completion report

At completion provide:

1. Repositories modified or created.
2. Feature branches and commit SHAs.
3. Pull request URLs.
4. PM Agent capabilities implemented.
5. Requirements Studio functionality.
6. PRD generation and structured-output behavior.
7. Epic/story generation.
8. Versioning and approval implementation.
9. API contracts.
10. Database migrations.
11. Exact test results.
12. Mock versus live provider testing.
13. Security and compliance validation.
14. PR review comments received and their disposition.
15. Remaining unresolved comments or CI failures.
16. Acceptance criteria status.
17. Known limitations.
18. Recommended M3 scope.

Update the consolidated M2 handoff and completion report in the central architecture repository.

---

### 24. Execution directive

Proceed with M2 implementation.

First reconcile the completed M1 implementation and approved architecture.

Do not recreate existing services.

Do not change the multi-repository approach.

Implement the PM Agent and Requirements Studio.

Maintain explicit human approval controls.

Enforce the AI Engineering Standards.

Resolve all actionable pull request review findings and required review conversations before declaring PRs ready for merge.

Prepare independent pull requests and stop before merging.

**Do not begin M3 automatically.**