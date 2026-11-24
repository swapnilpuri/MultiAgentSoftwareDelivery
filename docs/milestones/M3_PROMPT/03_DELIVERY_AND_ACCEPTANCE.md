# M3 implementation prompt — Sections 17–25

## 17. Implementation sequencing

Implement in small, independently verifiable vertical slices.

Avoid making large simultaneous changes across all repositories before tests exist.

Recommended order:

### Slice 0 — Baseline and architecture package

- Verify M2.
- Confirm repository boundaries.
- Finalize M3 contracts and architecture.
- Prepare requirements, design and acceptance documentation.
- Document ADRs.

Do not proceed if M2 is not accepted.

### Slice 1 — Canonical architecture persistence

- Architecture domain models.
- Additive persistence migrations.
- Revision APIs.
- Source PRD reference/hash validation.
- Domain tests.

### Slice 2 — Architect Agent execution

- LangGraph execution.
- LLM Gateway integration.
- Requirements analysis.
- Structured architecture generation.
- Durable checkpoints.
- Workflow tests.

### Slice 3 — Architecture artifacts

- Technology decisions.
- Service boundaries.
- API proposals.
- Data models.
- ADR generation.
- C4 graphs.
- Traceability validation.

### Slice 4 — Angular Architecture Studio

- Navigation.
- Dashboard.
- Agent conversation.
- Artifact workspaces.
- Diagram explorer.
- Version and traceability views.

### Slice 5 — Human approval

- Review submission.
- Approval decisions.
- Immutable baselines.
- Audit records.
- Authorization tests.
- UI approval workflow.

### Slice 6 — Integration and hardening

- Contract tests.
- End-to-end workflows.
- Restart recovery.
- Security validation.
- CI pipeline verification.
- Documentation.

### Slice 7 — PR review and milestone handoff

- Complete PRs.
- Process AI-review findings.
- Resolve review threads appropriately.
- Verify CI.
- Prepare completion evidence.
- Await human merge approval.

Where possible, implement service slices independently.

For shared contracts, publish compatible contract changes before relying on them in services.

---

## 18. Mandatory testing

Implement comprehensive tests.

### Unit tests

Cover:

- Architecture schema validation.
- Requirements hash checks.
- Component identity preservation.
- Alternative generation parsing.
- ADR schema validation.
- Diagram graph validation.
- State transitions.
- Approval invariants.
- Traceability calculations.
- Revision diff logic.

### Agent workflow tests

Test:

- Approved source PRD consumption.
- Rejection of unapproved PRDs.
- Model Gateway failure.
- Invalid LLM JSON.
- Structured-output retry.
- Clarification interrupt.
- Resume from checkpoint.
- Duplicate execution.
- Cancellation.
- Restart recovery.
- Bounded retries.
- No unauthorized tool execution.

Use deterministic mock model outputs.

### Integration tests

Validate:

- Project Service persistence.
- Agent Service integration.
- Gateway contract compatibility.
- Database migrations.
- Source PRD retrieval.
- Architecture revision storage.
- Approval record consistency.
- Cross-project isolation.

### Frontend tests

Validate:

- Architecture navigation.
- Project selection.
- Model configuration.
- Draft generation.
- Loading and failure states.
- Diagram viewing.
- Version comparison.
- Traceability.
- Review and approval actions.
- Accessibility-relevant behaviors.

### End-to-end tests

Verify at least one complete:

```text
Approved PRD
    -> Architecture session
    -> Architecture generation
    -> C4 diagrams
    -> ADRs
    -> Traceability review
    -> Architecture revision
    -> Human review
    -> Approval
    -> Immutable baseline retrieval
```

Also test:

- Request changes and resubmit.
- Stale approval rejection.
- Source PRD drift.
- Unauthorized user.
- Application restart.

### Nonfunctional checks

Include:

- Lint.
- Formatting.
- Static typing.
- Dependency and security checks.
- OpenAPI compatibility.
- Migration correctness.
- Independent service builds.
- Independent container builds.
- Health and readiness checks.
- Regression tests for M0–M2.

Use the checks actually configured by AIEngineeringStandards.

Do not invent successful test results.

Distinguish real PostgreSQL tests, mocked provider tests, real browser tests and tests that could not run.

---

## 19. M3 acceptance criteria

Create:

`docs/milestones/M3_ACCEPTANCE_CRITERIA.md`

Track each criterion with its status and executable evidence.

| ID | Acceptance criterion |
|---|---|
| M3-AC-01 | M2 baseline independently verified and accepted |
| M3-AC-02 | Existing microservice boundaries preserved |
| M3-AC-03 | Architecture Studio available in Angular |
| M3-AC-04 | Approved PRD can be selected |
| M3-AC-05 | Unapproved PRD is rejected |
| M3-AC-06 | Architect Agent uses LLM Gateway |
| M3-AC-07 | LangGraph architecture execution works |
| M3-AC-08 | Agent state survives application restart |
| M3-AC-09 | Architecture clarifications can be resumed |
| M3-AC-10 | Structured architecture proposal generated |
| M3-AC-11 | Architecture alternatives and tradeoffs available |
| M3-AC-12 | Technology stack and rationale generated |
| M3-AC-13 | Service boundaries and ownership generated |
| M3-AC-14 | API and event architecture proposals generated |
| M3-AC-15 | Data models generated |
| M3-AC-16 | Deployment architecture generated |
| M3-AC-17 | Security architecture generated |
| M3-AC-18 | C4 System Context diagram generated and rendered |
| M3-AC-19 | C4 Container diagram generated and rendered |
| M3-AC-20 | C4 Component diagram supported |
| M3-AC-21 | ADR proposals generated |
| M3-AC-22 | Architecture revisions persisted |
| M3-AC-23 | Architecture revision comparison works |
| M3-AC-24 | Requirement traceability available |
| M3-AC-25 | Architecture quality validation detects material issues |
| M3-AC-26 | Source PRD drift is detected |
| M3-AC-27 | Architecture review and change requests work |
| M3-AC-28 | Authorized human approval works |
| M3-AC-29 | Stale or unauthorized approval is rejected |
| M3-AC-30 | Approved architecture revision is immutable |
| M3-AC-31 | Architecture exports are consistent with canonical data |
| M3-AC-32 | Versioned platform API contracts validated |
| M3-AC-33 | No direct cross-service database access |
| M3-AC-34 | All applicable unit and integration tests pass |
| M3-AC-35 | Frontend tests and build pass |
| M3-AC-36 | Deterministic end-to-end architecture workflow passes |
| M3-AC-37 | Security, standards and regression checks pass |
| M3-AC-38 | Independent service build/deployment boundaries preserved |
| M3-AC-39 | Configured AI PR reviews completed |
| M3-AC-40 | Actionable PR feedback addressed and required threads resolved |
| M3-AC-41 | Required PR CI checks pass |
| M3-AC-42 | M3 documentation, completion evidence and handoff are accurate |
| M3-AC-43 | Human merge approval remains mandatory |
| M3-AC-44 | M3 does not perform autonomous target-application coding or deployment |

Use the statuses:

- PASS
- FAIL
- BLOCKED
- NOT_EXECUTED
- NOT_APPLICABLE (with justification)

Do not mark a criterion PASS merely because code was written or documentation exists.

A mandatory BLOCKED, FAIL or NOT_EXECUTED criterion prevents full milestone acceptance.

---

## 20. GitHub branches and pull requests

All implementation must occur on feature branches.

Use the repository's actual accepted default branch as the base.

Suggested branch name:

`feature/m3-architect-agent-solution-studio`

Use independent branches in each modified repository.

Do not commit directly to main.

Do not force-push or overwrite user changes.

### PR requirements

Each PR must include:

- Milestone reference.
- Scope summary.
- Changed components.
- Contract changes.
- Architecture decisions.
- Relevant acceptance criteria.
- Tests executed.
- Results and limitations.
- Security implications.
- Dependencies on companion PRs.
- Migration considerations.
- Review status.
- Human approval requirement.

Avoid enormous cross-cutting PRs where smaller independently reviewable changes are practical.

---

## 21. Mandatory AI PR review and comment resolution

**This section is non-negotiable.**

For each affected repository:

1. Push the feature branch.
2. Create or update the pull request.
3. Trigger or request the configured AI PR reviewer, such as CodeRabbit, according to repository configuration.
4. Verify that review execution actually occurred.
5. Inspect submitted reviews, inline threads and top-level comments.
6. Classify findings as actionable, informational, duplicate or disputed.
7. Fix all actionable findings.
8. Add regression tests for functional defects.
9. Reply to review comments with concise evidence of remediation.
10. Resolve review conversations when the required permission and governance policy permit it.
11. Re-run relevant tests.
12. Push corrective commits.
13. Obtain a fresh review where required.
14. Recheck current CI and thread status.
15. Prepare the PR for human approval.

Do not dismiss a valid finding simply to make the PR appear clean.

Do not mark a thread resolved before the issue is actually addressed.

Do not treat a silent reviewer, skipped review, exhausted quota, rate limit, or generated PR summary as a passed required review.

If an AI reviewer cannot run:

- Document the specific blocker.
- Preserve evidence.
- Retry only when justified.
- Use a formally authorized alternative review path if one exists.
- Otherwise mark the review gate BLOCKED.

Do not weaken repository protections to bypass the reviewer.

### Review exit conditions

Before marking a PR ready for human approval:

- All required CI checks pass.
- All actionable review findings are addressed.
- Required review conversations are resolved.
- No unaddressed blocking review remains.
- Required independent reviews are recorded.
- Companion PR dependencies are documented.
- The PR head matches the tested commit.

**Never merge automatically.**

Stop at the human approval boundary.

---

## 22. Codex efficiency requirements

Follow the existing Codex efficiency guidelines in AIEngineeringStandards.

The objective is efficient engineering without losing correctness or governance.

### Required behavior

- Use the current repository state instead of repeatedly rediscovering known facts.
- Inspect relevant files before editing.
- Avoid repeated full-repository scans.
- Prefer targeted searches.
- Reuse existing architecture and service abstractions.
- Implement small testable slices.
- Run targeted tests first.
- Run full regression at integration boundaries.
- Avoid repeatedly invoking expensive LLMs for deterministic validation.
- Use deterministic fixtures for tests.
- Parallelize independent reads/tests where safe.
- Do not parallelize conflicting repository edits.
- Avoid unnecessary framework rewrites.
- Avoid broad speculative redesign.
- Maintain compact progress reports.
- Persist handoff information in repository documentation.
- Resume from previously completed checkpoints.

Use the appropriate reasoning effort for the task.

Routine implementation should not require repeated lengthy architectural deliberation.

For difficult design contradictions or security issues, increase reasoning depth rather than guessing.

Do not optimize speed by skipping required tests, approvals or security checks.

### Execution autonomy

Once the M2 baseline is verified and M3 is authorized, continue through normal implementation slices without asking for routine confirmations.

Do not stop after each ordinary task to request another ChatGPT prompt.

Stop only for genuine approval boundaries, material architecture decisions, inaccessible resources or unsafe operations.

---

## 23. Required documentation deliverables

Create or update the following in the central architecture repository:

```text
docs/milestones/
    M3_REQUIREMENTS.md
    M3_BASELINE_VERIFICATION.md
    M3_DESIGN.md
    M3_IMPLEMENTATION_PLAN.md
    M3_ACCEPTANCE_CRITERIA.md
    M3_HANDOFF.md
    M3_COMPLETION_REPORT.md
```

Provide M3 PlantUML sources in the existing architecture diagram structure.

Include diagrams for:

- Platform-level M3 integration.
- Architect Agent workflow.
- Service interactions.
- Architecture artifact lifecycle.
- Human approval sequence.
- Deployment topology.

Create ADRs when architectural decisions introduce meaningful new tradeoffs.

Update existing documents instead of generating duplicate contradictory versions.

### Completion report

Include:

1. Milestone status.
2. Scope completed.
3. Scope not completed.
4. Architectural decisions.
5. Repository revisions.
6. Changed contracts.
7. Database migrations.
8. Test results.
9. Acceptance matrix.
10. Security validation.
11. PR and CI evidence.
12. AI-review evidence.
13. Unresolved issues.
14. Human approval dependencies.
15. Known limitations.
16. Next milestone recommendations.

---

## 24. Final handoff

At the end of implementation, provide a concise report.

### A. Overall status

Choose:

- IMPLEMENTED_PENDING_REVIEW
- READY_FOR_HUMAN_APPROVAL
- PARTIAL
- BLOCKED

Do not declare full milestone acceptance before all mandatory gates are satisfied.

### B. Repository summary

For each repository, provide:

- Repository name.
- Branch.
- Base commit.
- Current commit.
- PR URL.
- CI status.
- Review status.
- Unresolved findings.
- Merge status.

### C. Acceptance summary

Provide:

- Passed criteria.
- Failed criteria.
- Blocked criteria.
- Not-executed criteria.
- Evidence locations.

### D. Testing

Provide exact commands, counts and results.

Separate:

- Unit tests.
- Integration tests.
- Frontend tests.
- End-to-end tests.
- Security checks.
- Contract checks.
- Build checks.

### E. Outstanding decisions

List only matters requiring a human decision.

Do not disguise ordinary implementation tasks as human decisions.

### F. Next milestone readiness

Explain whether the approved architecture package is ready for future planning and implementation agents.

A possible next milestone is an Engineering Planning Agent that converts approved architecture into an implementation roadmap and dependency-aware task plan.

Do not implement that milestone now.

---

## 25. Final execution instruction

Begin with the **M2 baseline verification**, not M3 coding.

Read the repository instructions and verify current GitHub implementation, PR, review and acceptance evidence.

If M2 is not accepted, produce the complete baseline-gap report and stop at the governance gate.

If M2 is verified and accepted:

1. Establish the M3 design and contracts within the approved architecture.
2. Create feature branches from the accepted baseline.
3. Implement in testable vertical slices.
4. Run all applicable checks.
5. Integrate the independently deployed services.
6. Verify the end-to-end Architecture Studio.
7. Create pull requests.
8. Obtain and process configured AI reviews.
9. Resolve all actionable PR comments and required conversations.
10. Confirm CI success and acceptance evidence.
11. Update milestone completion and handoff documentation.
12. Stop before merging and request human approval.

Do not begin M4.

Do not merge automatically.

Do not claim tests, review completion, production authorization or milestone acceptance without evidence.

**Your objective is a fully implemented, tested, reviewable M3 Architecture Studio, with an immutable approved-architecture workflow and independently deployable service boundaries, ready for human acceptance.**

