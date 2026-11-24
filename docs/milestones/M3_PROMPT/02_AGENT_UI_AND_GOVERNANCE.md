# M3 implementation prompt — Sections 9–16

## 9. Architect Agent with LangGraph

Implement the Architect Agent using the existing agent-execution architecture.

Use LangGraph where suitable for explicit stateful execution and checkpointing.

Suggested workflow:

```text
START
  |
  v
Validate Project Authorization
  |
  v
Load Approved PRD Baseline
  |
  v
Validate Source Hash and Approval
  |
  v
Analyze Requirements
  |
  v
Identify Critical Architecture Questions
  |
  +--> Material Questions?
  |       |
  |       +--> Yes: Await Human Clarification
  |       |              |
  |       |              v
  |       |       Resume with Answers
  |       |
  |       +--> No
  |
  v
Generate Architecture Alternatives
  |
  v
Evaluate Quality Attributes
  |
  v
Generate Structured Architecture
  |
  v
Generate C4 Graphs and Diagrams
  |
  v
Generate API/Data/Deployment Proposals
  |
  v
Generate Proposed ADRs
  |
  v
Validate Traceability and Consistency
  |
  v
Persist Draft Revision
  |
  v
Await Human Review
  |
  +--> Changes Requested
  |         |
  |         v
  |     Revise Draft
  |         |
  |         +----> Revalidate
  |
  +--> Rejected
  |         |
  |         v
  |       STOP
  |
  +--> Approved
            |
            v
      Persist Approved Baseline
            |
            v
           END
```

This is a logical workflow. Reuse established graph and approval abstractions when appropriate.

### Required LangGraph state

Include:

- Workflow identifier.
- Project identifier.
- Source requirements revision/hash.
- Agent execution identifier.
- Model profile.
- Workflow status.
- Current node.
- Clarification questions and answers.
- Generated artifact references.
- Validation results.
- Retry metadata.
- Error metadata.
- Persisted checkpoint reference.

### Execution requirements

- Durable checkpointing.
- Restart recovery.
- Bounded retries.
- Idempotent commands.
- Explicit failure states.
- Safe cancellation.
- Duplicate execution prevention.
- Prompt/model version tracking.
- Structured output validation.
- Human interrupts for material decisions.

Do not hold a database transaction open while waiting for an LLM.

Do not let LangGraph checkpoint state replace canonical domain persistence unless the existing architecture explicitly defines it that way.

### Durable approval separation

The human approval decision must be implemented as a server-side domain operation.

Do not treat an LLM-generated "approved" response as an authorization event.

The approval record and final approved architecture revision must be consistent, transactional where possible, and auditable.

---

## 10. Model invocation

Use the M1 LLM Gateway.

Support configurable model profiles rather than a hardcoded provider.

Profiles may include compatible:

- Commercial LLMs.
- Open-source models.
- Local Ollama models.

Provider/model configuration must be consistent with existing Gateway contracts.

The model profile should support:

- Provider identifier.
- Model identifier.
- Structured-output capability.
- Context budget.
- Output budget.
- Temperature and other generation parameters.
- Timeout.
- Retry policy.
- Data-routing policy.
- Maximum estimated cost or token budget where supported.

Record actual model usage metadata where returned.

Do not fabricate token consumption or billing costs.

### Structured generation

Use Pydantic or the established typed-schema mechanism.

Validate generated output before persisting a draft.

On invalid output:

1. Capture validation errors.
2. Perform bounded repair attempts.
3. Preserve execution diagnostics.
4. Return a clear failure if repair is unsuccessful.

Do not store partially invalid content as an approved architecture.

### Security

- Never expose provider credentials to the browser.
- Never commit secrets.
- Respect project data-routing restrictions.
- Do not automatically switch to an unapproved provider.
- Treat PRD content, imported documents and LLM responses as untrusted data.
- Prevent prompt-injection content from changing agent permissions or approval rules.

---

## 11. Requirements traceability and drift prevention

This is a mandatory M3 capability.

Every approved architecture must be tied to an exact approved M2 requirements revision.

### Traceability

Implement mappings such as:

```text
Approved PRD Revision
        |
        v
Requirement
        |
        +--> Architecture Component
        |
        +--> API/Event Contract
        |
        +--> Data Entity
        |
        +--> Security Control
        |
        +--> Quality Attribute
        |
        +--> ADR
```

Support many-to-many relationships.

Not every requirement must map to every artifact type, but all requirements requiring architectural treatment must have appropriate coverage or an explicitly documented disposition.

### Quality validation

Detect:

- Missing architecture coverage.
- Orphaned architecture elements.
- Contradictory design decisions.
- Missing security controls.
- Unsupported technology assumptions.
- Undefined service ownership.
- Undocumented external dependencies.
- Inconsistent communication patterns.
- Invalid API references.
- Broken diagram references.
- Missing material ADRs.
- Unresolved architectural questions.

Clearly distinguish deterministic validation from model-generated quality suggestions.

### Drift prevention

If the source PRD is revised after architecture generation:

- Preserve the original source baseline and hash.
- Identify whether a newer approved PRD exists.
- Display an out-of-date indicator.
- Generate an impact assessment where supported.
- Never silently rewrite an approved architecture.
- Require a new architecture revision for changes.
- Require renewed human approval where the policy demands it.

Prevent approval when the selected source baseline is invalid, withdrawn, unauthorized or inconsistent with recorded hashes.

If newer approved requirements exist, apply the platform's explicit supersession policy rather than silently approving against the wrong version.

---

## 12. Architecture Studio — Angular UI

Extend the existing Angular application.

Do not introduce a second Angular shell.

Reuse existing authentication, project selection, navigation, component libraries and visual conventions.

### Main navigation

Add:

**Architecture Studio**

Place it consistently with the existing Project Workspace, AI Chat Studio and Requirements Studio.

Do not hide Architecture Studio in an inconsistent navigation mechanism.

### A. Architecture dashboard

Show:

- Project name.
- Approved PRD source.
- Current architecture version.
- Architecture status.
- Last modified timestamp.
- Current review status.
- Open architecture questions.
- Available actions.

### B. Architecture discovery and chat

Provide a conversational Architect Agent interface.

Features:

- Conversation history.
- Model selection.
- Streaming or progress updates.
- Architecture clarifications.
- Questions linked to requirements.
- Persisted conversation state.
- Retry failed generation.
- Resume paused workflows.

### C. Architecture document workspace

Provide section-based navigation for:

- Overview.
- Architecture alternatives.
- Technology stack.
- Service boundaries.
- API architecture.
- Data architecture.
- Security.
- Deployment.
- ADRs.
- Risks.

Support:

- Read-only approved versions.
- Editable drafts.
- Save draft.
- Request AI-assisted changes.
- Validation feedback.
- Version history.

### D. Architecture diagram explorer

Provide:

- System Context.
- Container.
- Component diagrams.
- Diagram selection.
- Zoom/pan.
- Component detail inspection.
- Requirement associations.
- Source export.

### E. Microservice boundary explorer

Display:

- Candidate services.
- Responsibilities.
- Owned entities.
- APIs.
- Events.
- Dependencies.
- Bounded contexts.

Allow the user to inspect service coupling and ownership conflicts.

### F. Technology decision explorer

Display:

- Proposed stack.
- Alternatives.
- Decision reasons.
- Advantages and disadvantages.
- Operational implications.
- Risks.

### G. ADR Studio

Support:

- Proposed ADR listing.
- Status filtering.
- ADR details.
- Alternative comparison.
- Decision rationale.
- Comments and revisions.
- Requirement references.

ADR status must remain consistent with the approved architecture revision.

### H. Requirements coverage

Show a requirement-to-architecture traceability matrix.

Users must be able to inspect uncovered requirements and navigate to related architecture artifacts.

### I. Version comparison

Support selecting two revisions and displaying:

- Added components.
- Removed components.
- Changed components.
- Technology changes.
- Contract changes.
- Data-model changes.
- ADR changes.
- Requirement coverage changes.

Use stable identifiers instead of relying exclusively on line-oriented Markdown diffs.

### J. Review and approval

Support:

- Submit for review.
- View frozen submitted revision.
- Review findings.
- Request changes.
- Reject.
- Approve.
- View approval history.
- Read-only approved baseline.

### UI quality

- Responsive layout.
- Accessible keyboard navigation.
- Consistent typography.
- Clear loading and error states.
- No decorative nonfunctional buttons.
- No silent data loss.
- Clear distinction between draft, generated suggestion, submitted and approved content.

All mutating UI operations must use authenticated backend APIs.

---

## 13. Architecture approval workflow

Use the existing M2 approval conventions where possible.

Suggested lifecycle:

```text
NOT_STARTED
    |
    v
GENERATING
    |
    v
DRAFT
    |
    v
UNDER_REVIEW
    |
    +--> CHANGES_REQUESTED --> New Draft Revision
    |
    +--> REJECTED
    |
    +--> APPROVED
```

Implement explicit server-side transition validation.

### Approval record

Record:

- Approval ID.
- Project ID.
- Architecture ID.
- Revision ID.
- Source PRD ID/version/hash.
- Architecture content hash.
- Approver identity.
- Decision.
- Timestamp.
- Comments.
- Approval scope.
- Policy version.

### Mandatory enforcement

- AI agents cannot approve artifacts.
- Only authorized humans can approve.
- The selected revision must be immutable during review.
- Approval must reference the exact submitted content hash.
- Stale approvals must fail.
- Repeated approval requests must be idempotent or explicitly rejected.
- A changed artifact must require a new revision.
- Audit records must be retained.
- Access control must be enforced server-side.

Do not allow browser-provided identity fields to bypass authentication.

If the current platform has development-only identity support, preserve its clearly labeled limitations. Do not claim production-grade authorization.

---

## 14. API and contract design

Extend existing versioned platform contracts.

First inspect the actual M2 OpenAPI paths and DTOs.

Reuse existing project, artifact and approval APIs where appropriate.

Do not create incompatible parallel APIs for concepts already owned by Project Service.

Suggested logical endpoints include:

```text
GET    /projects/{projectId}/architectures
POST   /projects/{projectId}/architectures

GET    /projects/{projectId}/architectures/{architectureId}
GET    /projects/{projectId}/architectures/{architectureId}/revisions
POST   /projects/{projectId}/architectures/{architectureId}/revisions

GET    /projects/{projectId}/architectures/{architectureId}/revisions/{revisionId}
GET    /projects/{projectId}/architectures/{architectureId}/traceability
GET    /projects/{projectId}/architectures/{architectureId}/diagrams
GET    /projects/{projectId}/architectures/{architectureId}/adrs

POST   /projects/{projectId}/architectures/{architectureId}/submit-review
POST   /projects/{projectId}/architectures/{architectureId}/approval-decisions

GET    /projects/{projectId}/architectures/{architectureId}/approved-baseline
```

Architect Agent execution may expose:

```text
POST   /agent-executions/architecture
GET    /agent-executions/{executionId}
POST   /agent-executions/{executionId}/clarifications
POST   /agent-executions/{executionId}/resume
POST   /agent-executions/{executionId}/cancel
```

These are conceptual endpoint proposals, not mandatory incompatible replacements.

Final paths and DTOs must follow established routing conventions.

### API requirements

- OpenAPI validation.
- Documented error responses.
- Project authorization.
- Idempotency support.
- Optimistic concurrency for edits.
- Pagination where needed.
- Input size limits.
- Validated enums.
- Explicit revision identifiers.
- Backward compatibility.
- Contract tests.

Use the existing SSE conventions if streaming is supported.

Ensure Angular typed clients and backend DTOs remain compatible.

---

## 15. Persistence and recovery

Use the established PostgreSQL architecture.

Implement migrations appropriate to existing repository ownership.

Migrations must be additive and safe unless a separate, explicitly authorized migration plan exists.

Required durability:

- Architecture workspace.
- Agent sessions.
- Workflow checkpoints.
- Clarification state.
- Draft revisions.
- Architecture components.
- Requirement links.
- Diagrams and ADRs.
- Approval decisions.
- Audit history.

### Concurrency

Handle:

- Duplicate generation requests.
- Simultaneous editing.
- Stale revision updates.
- Concurrent approvals.
- Retry after timeout.
- Worker restart.
- Browser refresh.

Use version checks, unique constraints and idempotency keys where appropriate.

### Recovery

A workflow must recover from persisted state without regenerating already accepted artifacts unnecessarily.

Use stable execution identifiers.

Do not claim durability solely because state exists in process memory.

---

## 16. Security and governance

Apply all relevant AIEngineeringStandards controls.

### Required safeguards

- Project-level tenant isolation.
- Server-side authorization.
- Secure model routing.
- No secrets in repository artifacts.
- Input validation.
- Output schema validation.
- Prompt-injection resistance.
- Audit logging.
- Safe diagram rendering.
- Resource limits.
- Bounded agent loops.
- Non-destructive migrations.
- Approved revision immutability.

### Prohibited M3 behavior

The Architect Agent must not:

- Merge GitHub PRs.
- Modify production infrastructure.
- Deploy generated applications.
- Execute arbitrary shell commands supplied by an LLM.
- Create production credentials.
- Approve its own work.
- Alter an approved PRD.
- Bypass project authorization.
- Automatically trigger Development Agents.
- Modify unrelated projects.
- Perform irreversible operations without authorization.

Make these boundaries explicit in tests and documentation.

---

