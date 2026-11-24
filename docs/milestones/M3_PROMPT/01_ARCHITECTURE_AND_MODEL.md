# M3 implementation prompt — Sections 1–8

## 1. Role and operating model

You are the implementation engineer for **Milestone M3 — Architect Agent & Solution Architecture Studio** of MultiAgentSoftwareDelivery.

The platform is an enterprise-grade, multi-agent software delivery system supporting AI-assisted requirements engineering, solution architecture, engineering planning, implementation, testing, and delivery under human governance.

**Central architecture repository:**

https://github.com/swapnilpuri/MultiAgentSoftwareDelivery.git

Completed or reported milestones:

- M0 — Multi-Repository Microservices Foundation and AIEngineeringStandards
- M1 — Project Workspace, Multi-LLM Gateway and AI Chat Studio
- M2 — Product Manager Agent and Requirements Engineering Studio (reported complete; independently verify)
- M3 — Architect Agent and Solution Architecture Studio (this milestone)

### Mandatory division of responsibilities

**ChatGPT UI**
- Platform architecture and architectural decisions.
- Milestone planning and scope definition.
- Independent architecture and acceptance review.
- Guidance for subsequent milestones.

**Codex**
- Repository discovery and baseline verification.
- Detailed implementation planning within the approved M3 scope.
- Implementation and refactoring.
- Automated testing and debugging.
- Contract updates and integration.
- Documentation and evidence maintenance.
- Feature branches and pull requests.
- PR-review remediation and CI verification.

**Human**
- Approval of material architecture changes.
- Requirements and solution architecture approval.
- Authorization of sensitive operations.
- Pull-request merge approval.
- Final milestone acceptance.

**Git and repository documentation**
- Authoritative record of designs, contracts, decisions, implementation, acceptance results, and handoffs.

Do not treat ChatGPT or Codex conversations as authoritative project state.

### Mandatory AIEngineeringStandards compliance

Read and follow the existing AIEngineeringStandards operating model and the standards actually incorporated into the repositories.

Inspect:

- AGENTS.md
- docs/AI_DEVELOPMENT_OPERATING_MODEL.md
- docs/ROADMAP.md
- Relevant architecture documents.
- Relevant ADRs.
- Repository manifests.
- Service-specific AGENTS.md files.
- M2 requirements, design, acceptance, completion and handoff documents.

Do not invent standards or silently replace the existing operating model.

If the authoritative AIEngineeringStandards repository or particular standards documents cannot be accessed, record the missing reference and use the verified standards already present. Escalate only material governance ambiguities.

---

## 2. Mandatory M2 baseline verification

**This phase must execute before any M3 application implementation.**

The M2 milestone was reported complete, but the previously inspected GitHub evidence showed that central architecture PR #4 was documentation-only and merged into `feature/m1-main-integration`, rather than directly into `main`.

The PR explicitly did not claim implementation of the M2 runtime.

The previously inspected M2 acceptance document listed 29 acceptance criteria without runtime acceptance evidence.

The earlier review inspection also returned no submitted review for central PR #4.

These observations are historical findings, not proof that M2 remains incomplete now. Recheck current state.

### Step 2.1 — Discover all repositories

Identify the actual repositories, local worktrees, default branches, remote URLs, current commits, and PRs.

Expected repositories include:

- MultiAgentSoftwareDelivery
- masd-web
- masd-project-service
- masd-llm-gateway
- masd-contracts
- masd-infrastructure
- masd-agent-service

Discover additional repositories if they exist.

Do not assume that a repository is missing merely because the current GitHub integration cannot access it. Distinguish between nonexistent, inaccessible, and unavailable.

Do not create duplicate repositories.

### Step 2.2 — Verify M2 implementation

Verify that M2 actually delivers:

1. Product Manager Agent execution.
2. Requirements discovery through Angular.
3. Persistent discovery conversations.
4. Clarification workflows.
5. Structured PRD generation.
6. Editable and versioned PRDs.
7. Epics, stories and acceptance criteria.
8. Requirement quality validation.
9. Requirements traceability.
10. Human approval, rejection and change-request workflows.
11. Immutable approved revisions.
12. Stale approval rejection.
13. Approved baseline retrieval APIs.
14. Versioned API contracts.
15. Applicable frontend, backend and integration tests.
16. Independent builds and deployment boundaries.
17. Required CI and PR review gates.

Read the existing 29 M2 acceptance criteria and reconcile them individually against source code, executed tests and acceptance evidence.

Do not infer implementation from design documents.

### Step 2.3 — Verify PR and merge evidence

For every relevant M2 repository:

- Identify implementation PRs.
- Verify their target branches.
- Verify whether they were actually merged.
- Confirm the resulting implementation exists in the accepted default branch.
- Check submitted reviews and configured AI-review results.
- Inspect inline review threads and top-level feedback.
- Check that actionable comments were addressed.
- Check required thread resolution.
- Verify applicable CI checks.
- Verify documented human merge approval.
- Verify completion and handoff reports.

An AI-generated PR summary or walkthrough is not equivalent to a completed required review unless the configured governance policy explicitly accepts it.

### Step 2.4 — Baseline decision

Produce:

`docs/milestones/M3_BASELINE_VERIFICATION.md`

Classify M2 as:

- VERIFIED_ACCEPTED
- PARTIAL
- BLOCKED
- UNVERIFIED

Include an evidence matrix with repository, revision, PR, review status, CI status, acceptance evidence and outstanding issues.

**Only VERIFIED_ACCEPTED is an eligible M3 implementation baseline.**

If M2 is PARTIAL, BLOCKED or UNVERIFIED:

- Preserve existing work.
- Do not implement M3 runtime or UI functionality.
- Document the exact gaps and corrective recommendations.
- Identify a safe continuation plan.
- Do not falsely report that M3 implementation has begun.
- Do not automatically merge, amend or bypass M2 governance.
- Stop at the M3 baseline gate.

Do not repeat this baseline investigation after it has been verified unless repository changes invalidate the evidence.

---

## 3. M3 mission

Implement an AI-powered **Solution Architecture Studio**, integrated with the approved M2 requirements baseline.

The Architect Agent shall transform approved product requirements into structured, reviewable, version-controlled software architecture proposals.

The user must be able to:

1. Select a project.
2. Open the Architecture Studio.
3. Select an approved M2 PRD revision.
4. Inspect source requirements and approval evidence.
5. Start an architecture design session.
6. Select a permitted model profile.
7. Generate an initial solution architecture proposal.
8. Explore architectural alternatives.
9. Review C4 diagrams.
10. Review technology recommendations.
11. Inspect microservice boundaries.
12. Review API and event contracts.
13. Review conceptual and logical data models.
14. Inspect deployment and security architecture.
15. Review architecture decision records.
16. Ask the Architect Agent questions.
17. Request revisions.
18. Edit drafts manually.
19. Inspect requirement coverage and design tradeoffs.
20. Compare architecture revisions.
21. Submit an architecture revision for human review.
22. Approve, reject or request changes.
23. View immutable approved architecture baselines.
24. Export architecture artifacts.
25. Provide the approved architecture as a controlled input to future engineering agents.

M3 must not generate production application code or deploy the user's target application.

The Architect Agent designs systems; future agents implement them.

---

## 4. Architecture principles

Apply these principles throughout M3:

### 4.1 Independently deployable microservices

Maintain independent repositories, build processes, CI pipelines, runtime configurations and deployment artifacts.

Do not convert the platform into a monorepo.

Do not introduce one shared database accessed directly by multiple services.

Avoid distributed monolith coupling.

### 4.2 Domain-driven service boundaries

Each service owns its domain and data.

Reuse existing platform services wherever responsibility is already established.

### 4.3 Contract-first integration

Use versioned OpenAPI contracts and validated schemas for interservice communication.

Do not introduce undocumented request or response formats.

### 4.4 Human-controlled architecture

AI-generated architecture is a proposal until explicitly approved by an authorized human.

No agent may approve its own output.

### 4.5 Durable state

Architecture sessions, generation attempts, revisions, decisions and approval records must survive application restarts.

### 4.6 Traceability

Every generated architectural component must have appropriate relationships to requirements, constraints, assumptions or documented architectural rationale.

### 4.7 Provider independence

All model invocation must use the established LLM Gateway.

Do not embed commercial-provider SDK integrations directly into the Architect Agent.

### 4.8 Security by design

Enforce project-level authorization, input validation, bounded execution and auditability.

### 4.9 Future extensibility

Design the M3 output as a stable architecture package that future Planning, Development, QA and DevOps Agents can consume without scraping generated Markdown.

---

## 5. Repository ownership

Use verified repository names and structures. The following are the expected ownership boundaries.

### MultiAgentSoftwareDelivery

Owns:

- M3 milestone requirements and design.
- Platform-level architecture.
- C4 architecture documentation.
- ADRs and governance rules.
- Repository/service responsibility definitions.
- M3 implementation plan.
- M3 acceptance criteria.
- Consolidated testing and delivery evidence.
- M3 handoff and completion reports.

### masd-web

Owns:

- Angular Solution Architecture Studio.
- Architecture session UI.
- Architecture proposal workspace.
- Diagrams and visualization.
- Technology stack comparisons.
- Microservice boundary explorer.
- API and data-model views.
- ADR review UI.
- Architecture comparison and traceability.
- Human approval UI.

No backend business rules should be implemented exclusively in Angular.

### masd-agent-service

Owns:

- Architect Agent definition.
- LangGraph workflow.
- Architecture generation and revision.
- Generation-state coordination.
- Prompt/policy versioning.
- Structured response validation.
- Architecture-quality analysis.
- Model invocation through the LLM Gateway.
- Agent execution metadata.

The Agent Service must not become the canonical owner of approved project architecture documents.

### masd-project-service

Owns:

- Architecture workspace records.
- Architecture proposals and revisions.
- Structured architecture artifacts.
- Source requirement references.
- Artifact content hashes.
- Requirement-to-architecture traceability.
- Approval records.
- Approved architecture baseline retrieval.
- Project-domain access control.
- Artifact lifecycle and immutable revision records.

### masd-llm-gateway

Owns:

- Provider routing.
- LiteLLM/Ollama integration where configured.
- Model profiles.
- Retry and timeout handling.
- Provider selection policy.
- Usage reporting.
- Model capability information.
- Streaming transport where already supported.

### masd-contracts

Owns:

- OpenAPI contracts.
- Versioned DTO schemas.
- Typed client generation or validation.
- Contract compatibility tests.
- Architecture package schemas.
- Event schemas where applicable.

### masd-infrastructure

Owns:

- Independent container builds.
- Local multi-service orchestration.
- Database provisioning.
- Migration/test infrastructure.
- Environment configuration examples.
- Health/readiness integration.
- Service discovery and routing.
- Integration testing support.

Do not create another microservice unless a clear domain boundary justifies it and the governing architecture allows it.

---

## 6. Architecture generation capabilities

Implement generation of a structured solution architecture package.

The package must contain the following sections.

### A. Architecture overview

- Solution description.
- Architecture objectives.
- Business context.
- Requirements baseline reference.
- Assumptions and constraints.
- Architecture principles.
- Key quality attributes.
- Major design decisions.
- Explicitly unresolved decisions.

### B. Architectural alternatives

Generate reasonable alternatives when meaningful.

Examples:

- Modular monolith versus microservices.
- Synchronous versus event-driven integration.
- Relational versus document storage.
- Managed versus self-hosted infrastructure.
- Containerized versus serverless deployment.

Every alternative must include:

- Benefits.
- Drawbacks.
- Complexity.
- Operational implications.
- Security implications.
- Estimated cost factors.
- Relevant constraints.
- Decision rationale.

Do not force a microservices recommendation for every project merely because the MultiAgentSoftwareDelivery platform itself uses microservices.

The architecture of the user's target project is determined by its requirements.

### C. Technology stack

Recommend suitable:

- Frontend technologies.
- Backend frameworks.
- Persistence technologies.
- Messaging systems.
- Cache technologies.
- Authentication and authorization.
- Observability.
- Infrastructure.
- Testing tools.
- AI/ML technologies where appropriate.

Include recommendation rationale, alternatives, maturity, major risks, operational tradeoffs and any assumptions about licensing or support.

Do not invent benchmark results, cloud prices or verified compatibility information.

### D. Service boundaries

Generate:

- Bounded contexts.
- Candidate services or modules.
- Service responsibilities.
- Data ownership.
- Internal relationships.
- External integrations.
- Communication patterns.
- Service dependencies.

Validate clear domain ownership and identify overly coupled designs.

### E. API and event architecture

Generate:

- Candidate API inventory.
- Endpoint responsibilities.
- OpenAPI-compatible draft schemas.
- Versioning guidance.
- Authentication expectations.
- Consistent error handling.
- Pagination and idempotency where relevant.
- Event definitions.
- Event producers and consumers.
- Data consistency assumptions.
- Retry and failure semantics.

Clearly distinguish proposed application contracts from the actual platform's implemented contracts.

### F. Data architecture

Generate:

- Domain entities.
- Relationships.
- Aggregate boundaries.
- Conceptual data model.
- Logical data model.
- Ownership of persisted data.
- Data flow.
- Retention considerations.
- Transaction boundaries.
- Consistency requirements.

Do not perform target-application database migrations.

### G. Deployment architecture

Generate:

- Runtime components.
- Environments.
- Network boundaries.
- Deployment topology.
- Scaling assumptions.
- Availability strategy.
- Resilience and disaster-recovery considerations.
- Monitoring and logging.
- Secrets and configuration strategy.
- CI/CD conceptual architecture.

Target-cloud details must reflect actual requirements or be labeled as proposals.

### H. Security architecture

Generate:

- Trust boundaries.
- Identity and access controls.
- Data classification considerations.
- Encryption recommendations.
- Network isolation.
- Secrets management.
- Audit requirements.
- Threats and mitigations.
- Security assumptions.

### I. Architecture Decision Records

Generate structured proposed ADRs with:

- ADR ID.
- Title.
- Status.
- Context.
- Decision.
- Alternatives.
- Consequences.
- Requirement references.
- Version.
- Author/source.
- Review metadata.

Agent-generated ADRs must remain proposed until approved.

### J. Risk and quality assessment

Generate:

- Technical risks.
- Security risks.
- Operational risks.
- Delivery risks.
- Architecture anti-pattern warnings.
- Missing nonfunctional requirements.
- Unresolved tradeoffs.
- Suggested mitigations.

---

## 7. Canonical architecture data model

Use typed, structured artifacts as the canonical representation.

Suggested domain concepts:

- ArchitectureWorkspace
- ArchitectureSession
- ArchitectureProposal
- ArchitectureRevision
- ArchitectureBaseline
- ArchitectureComponent
- ArchitectureRelationship
- TechnologyDecision
- ServiceBoundary
- ApiContractProposal
- EventContractProposal
- DataModel
- DeploymentModel
- SecurityModel
- DiagramArtifact
- ArchitectureDecisionRecord
- ArchitectureRisk
- ArchitectureQualityFinding
- RequirementArchitectureLink
- ArchitectureApproval
- AgentExecution

Adapt these to the existing M2 persistence model instead of duplicating shared project or artifact abstractions.

Every persisted revision must include:

- Project ID.
- Architecture ID.
- Revision ID.
- Source PRD ID.
- Source PRD revision.
- Source PRD content hash.
- Source approval reference.
- Architecture schema version.
- Architecture content hash.
- Creation timestamp.
- Creation source.
- Status.
- Generation metadata, if AI-generated.

Use stable identifiers for architecture components and relationships.

Preserve identifiers across revisions when identity is unchanged.

Use explicit schema validation and documented schema migrations.

Rendered Markdown, JSON, diagrams and exports must be generated from or validated against the canonical representation.

Do not use Markdown as the only database representation.

Approved revisions must be immutable.

---

## 8. C4 diagrams and visualization

M3 must support generation and review of C4 diagrams.

Required diagram types:

**Level 1 — System Context**

Show users, the proposed system and external dependencies.

**Level 2 — Container**

Show applications, services, databases, messaging systems and major communication paths.

**Level 3 — Component**

Show meaningful internal components within selected containers.

Level 4 source-code diagrams are outside the mandatory M3 scope.

### Diagram implementation

Use a structured graph representation.

Generate PlantUML/C4-PlantUML source from the graph.

Implement controlled rendering and preview of diagrams through an approved rendering approach.

Prefer existing diagram libraries and conventions.

For browser-native visualization, Mermaid or another established renderer may be used as a supported presentation format when appropriate.

The structured architecture model must remain authoritative.

### UI requirements

Users must be able to:

- View C4 levels.
- Zoom and pan.
- Inspect components.
- Inspect relationships.
- Select components to view details.
- View requirement references.
- Download diagram source.
- Export diagram images where supported.
- Inspect rendering errors.

Do not silently accept invalid diagram syntax.

Do not execute arbitrary user-authored PlantUML directives without appropriate restrictions.

Validate rendering errors, resource limits and access permissions.

If a rendering dependency is unavailable, provide an understandable error rather than displaying a false success state.

---

