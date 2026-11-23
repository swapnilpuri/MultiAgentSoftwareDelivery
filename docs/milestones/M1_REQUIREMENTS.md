# MultiAgentSoftwareDelivery — Milestone M1
## Project Workspace, Multi-LLM Gateway & AI Chat Studio

### 1. Role and execution context

You are the implementation engineer responsible for Milestone M1 of MultiAgentSoftwareDelivery.

M0 — Multi-Repository Microservices Foundation — has been reported complete.

**Do not assume the state of M0 without verification.**

Read the actual repository state, M0 handoff, architecture decisions, standards manifests and available test evidence before implementation.

The primary architecture repository is:

https://github.com/swapnilpuri/MultiAgentSoftwareDelivery.git

The platform uses independently owned and deployable Git repositories.

The existing AIEngineeringStandards operating model remains mandatory.

**Responsibility boundaries:**

- ChatGPT UI: Product architecture, roadmap, milestone definition, architectural review and independent acceptance assessment.
- Codex: Code implementation, testing, debugging, documentation, Git operations and pull request preparation.
- Human: Approval of material scope, security, architecture and production changes.
- Git: Authoritative source for implementation, specifications, decisions and evidence.

This prompt authorizes implementation of M1 only.

---

### 2. M1 objective

Implement a functional, integrated **Project Workspace and Multi-LLM Chat Studio**.

A user must be able to:

1. Open the MultiAgentSoftwareDelivery Angular portal.
2. Create a new software project.
3. Enter the project's name, description, goals and high-level requirements.
4. View and edit the project details.
5. Open a project-specific AI conversation.
6. Select an available LLM provider and model.
7. Submit prompts and receive streamed AI responses.
8. Continue the conversation with prior context.
9. View persisted conversation history.
10. Switch between projects without mixing their conversation histories.
11. Configure a default model for each project.
12. View errors clearly when a model provider is unavailable.
13. See basic model execution metadata.
14. Return to a previous conversation after restarting the application.

The experience should resemble a professional project-aware AI chat workspace rather than a generic chatbot demo.

No autonomous coding agents or deployment workflows are required in M1.

---

### 3. Mandatory M0 reconciliation

Before changing code:

1. Inspect the architecture repository.
2. Read its root `AGENTS.md`.
3. Read `AI_DEVELOPMENT_OPERATING_MODEL.md`.
4. Read `docs/ROADMAP.md`.
5. Read all relevant M0 ADRs.
6. Read `M0_HANDOFF.md` and `M0_COMPLETION_REPORT.md`.
7. Discover actual service repositories and their configured Git remotes.
8. Inspect branch, commit SHA and working-tree status in each affected repository.
9. Confirm M0 changes are merged or identify any pending pull requests.
10. Protect existing user work.

Do not create duplicate repositories or replace working M0 implementations.

If material M0 acceptance gates remain incomplete, report them and resolve only the prerequisites necessary for M1 before proceeding.

Use targeted inspections. Avoid repeatedly scanning all repositories.

---

### 4. Repository boundaries

Expected repositories:

- `MultiAgentSoftwareDelivery`
- `masd-web`
- `masd-project-service`
- `masd-contracts`
- `masd-infrastructure`

M1 also introduces the following independently deployable service if it does not already exist:

- `masd-llm-gateway`

Suggested responsibility boundaries:

**masd-web**

Owns Angular routes, pages, forms, reusable components, conversation presentation and frontend API integration.

**masd-project-service**

Owns projects, project settings, conversation metadata, persisted messages and project access checks.

**masd-llm-gateway**

Owns provider integrations, model discovery, model routing, LLM requests, streamed completions and provider-specific error normalization.

**masd-contracts**

Owns versioned REST/OpenAPI contracts and future event-contract conventions.

**masd-infrastructure**

Owns local Docker Compose integration and environment configuration.

**MultiAgentSoftwareDelivery**

Owns architecture, standards, ADRs, milestone specifications and cross-service acceptance evidence.

Maintain independent build and deployment processes.

Do not directly access another service's database tables.

Avoid introducing tightly coupled shared source-code libraries across independent repositories.

If existing M0 architecture defines equivalent responsibilities differently, reconcile that design before implementation and record any consequential change as an ADR requiring review.

---

### 5. AI Engineering Standards

All affected repositories must conform to AIEngineeringStandards.

Mandatory engineering practices:

- Read repository-specific `AGENTS.md`.
- Follow the pinned AI Engineering Operating Model.
- Maintain traceability from M1 acceptance criteria to implementation and tests.
- Work in small verifiable implementation batches.
- Preserve backward compatibility with approved M0 contracts.
- Use strict typing and validated API boundaries.
- Keep configurations externalized.
- Never hardcode secrets.
- Run focused tests after each implementation batch.
- Run required regression tests before completion.
- Record actual execution evidence.
- Do not conceal or bypass failing quality checks.
- Use feature branches.
- Never automatically merge protected branches.
- Maintain a durable milestone handoff.

Run the available standards-compliance checks in each affected repository.

If mandatory standards checks cannot execute, record why.

---

### 6. M1 functional component A — Project Management

Implement the first usable Project Workspace.

#### Project domain

A project should initially support:

- Project ID.
- Project name.
- Description.
- High-level requirements.
- Business goals.
- Technology preferences.
- Project status.
- Default LLM provider/model.
- Creation and update timestamps.
- Owner or scoped user identifier where supported.

Use appropriate database constraints, length limits and input validation.

#### Backend APIs

Implement or extend versioned REST endpoints for:

- Create project.
- Get project by ID.
- List projects.
- Update project.
- Archive project.

Use consistent pagination, error handling and response models.

Archival should not delete the project's conversations or other records.

Project ownership and access checks must be enforced server-side.

If full identity management is not implemented, use an explicitly documented local-development identity strategy.

Do not claim multi-user production security without real authentication and authorization.

#### Project UI

Implement:

- Project listing.
- Create project dialog/page.
- Project detail page.
- Project edit functionality.
- Project status display.
- Project-specific navigation to AI Chat.

Use responsive Angular components and consistent application navigation.

Avoid duplicated layouts and inconsistent navigation groups.

---

### 7. M1 functional component B — Multi-LLM Gateway

Create or extend `masd-llm-gateway`.

Use the approved LiteLLM-based model abstraction.

Support these provider categories:

1. OpenAI.
2. Anthropic Claude.
3. Ollama-hosted local models.

Do not hardcode a fixed list of commercial model names.

Expose supported model discovery/configuration using actual provider capabilities and configured model catalogs.

For Ollama, support discovering locally installed models when the Ollama instance is reachable.

For commercial models, use configured model definitions or provider-supported discovery where available.

#### Model configuration

Each model configuration should support:

- Provider.
- Provider-specific model identifier.
- Display name.
- Enabled/disabled state.
- Availability.
- Supported capabilities where discoverable.
- Context and output limits when known.
- Optional default generation settings.
- Model routing policy.
- Optional token/cost metadata.

Do not assume every model supports tool calling, streaming, structured outputs or the same context window.

Validate requested capabilities before routing when possible.

#### Provider error handling

Normalize:

- Invalid credentials.
- Provider unavailable.
- Model unavailable.
- Rate limiting.
- Timeouts.
- Context-length errors.
- Unsupported features.
- Unexpected provider failures.

Do not expose provider credentials or raw sensitive payloads in frontend errors.

#### Model gateway isolation

The frontend must never call commercial LLM providers directly using secret API keys.

Model credentials belong only in a trusted backend configuration or secret manager.

The LLM gateway must not expose unrestricted provider proxy access. Requests require the appropriate project and authorization context.

---

### 8. M1 functional component C — AI Chat Studio

Implement project-aware conversations.

#### Conversation features

Support:

- Create conversation.
- List project conversations.
- Open an existing conversation.
- Submit user message.
- Stream assistant response.
- Persist user and assistant messages.
- Display previous messages.
- Rename conversation.
- Continue an existing conversation.
- Recover safely after network failures.
- Show model/provider used for an assistant response.

Conversation history must survive backend and browser restarts.

#### Chat UI

Build a professional chat interface with:

- Conversation list/sidebar.
- Main message area.
- Rich-text input area.
- Markdown response rendering.
- Syntax-highlighted code blocks where practical.
- Copy-message functionality.
- Model selection dropdown.
- Send button.
- Stop/cancel generation control.
- Streaming response display.
- Loading indicators.
- Clear error messages.
- Empty-state and first-use guidance.

Render Markdown safely. Do not allow untrusted LLM output to execute arbitrary HTML or scripts.

Maintain consistent navigation with the rest of the Angular application.

#### Streaming

Prefer Server-Sent Events or another appropriate transport consistent with the existing architecture.

Ensure:

- Incremental token/text delivery.
- Cancellation handling.
- Disconnect handling.
- Timeout behavior.
- Structured completion/error events.
- No duplicate saved assistant responses after reconnect or retry.
- Reliable final message persistence.

Do not advertise resume-from-token streaming unless it is actually implemented.

#### Conversation context

Implement bounded conversation history.

Do not transmit unlimited conversation messages to an LLM.

Use a configurable context budget and a deterministic truncation strategy for M1.

Record which history messages were included where practical.

Advanced summarization, long-term memory and RAG are future capabilities.

---

### 9. M1 functional component D — Project-specific LLM configuration

Every project must have a default model configuration.

A conversation may override the project default.

Allow the user to select among configured available models.

Store:

- Project model configuration.
- Conversation model selection.
- Actual model used for each response.
- Provider name.
- Request status.
- Available token usage metadata.
- Estimated cost when pricing data is configured.

Do not invent usage or costs when the provider does not return the required information.

Plan future support for per-agent model configuration, but do not implement the full agent policy engine in M1.

Model changes must not silently expose restricted project information to another provider.

Document the future project data-classification and model-routing governance policy.

---

### 10. Persistence design

Use PostgreSQL for the Project Service.

Introduce database migrations using an established migration tool appropriate to the existing Python stack.

Suggested logical entities:

- Project.
- ProjectSettings.
- Conversation.
- ConversationMessage.
- ModelUsageRecord.

Keep schema ownership within the appropriate service.

The Project Service stores project and conversation state.

The LLM Gateway should not directly read Project Service tables.

Use explicit service contracts to transfer only authorized conversation context.

Include:

- Database constraints.
- Migration tests.
- Consistent timestamps.
- Appropriate indexes.
- Transactional persistence.
- Safe retries and idempotency for message submission.

Do not expose internal database identifiers as a substitute for authorization.

Document retention and future deletion requirements.

---

### 11. API contracts

Update `masd-contracts` before or alongside implementation.

Define OpenAPI contracts for:

Project management:
- Project CRUD and archive.
- Project settings.

Conversation management:
- Conversation CRUD where applicable.
- Message history.
- Message submission.

Model gateway:
- Available models.
- Model configuration metadata.
- Streaming completion.
- Request cancellation where supported.

Ensure the contracts describe:

- Request and response schemas.
- Error responses.
- Pagination.
- Authentication/authorization expectations.
- Streaming event format.
- Idempotency requirements.
- API versioning.

Implement contract validation tests.

Validate frontend and backend compatibility against the published contracts.

Do not break previously approved M0 API contracts without documenting the change.

---

### 12. Security requirements

Implement appropriate security boundaries for M1.

Mandatory controls:

- Server-side input validation.
- Project authorization checks.
- Secret handling through environment/secret configuration.
- No credentials in source control.
- No raw secrets in logs.
- Bounded request sizes.
- Configurable generation limits.
- Provider timeouts.
- Rate limiting or documented local-development limits.
- Safe Markdown rendering.
- Controlled CORS.
- Sanitized error responses.
- Explicit separation of local-development identity from production security.

Treat prompt content and LLM responses as untrusted data.

Do not let chat text trigger arbitrary system commands or unrestricted tool execution.

No coding-agent tool calls are authorized in M1.

---

### 13. Frontend quality standards

Use the existing Angular version and project conventions.

Requirements:

- Strict TypeScript.
- Reusable components.
- Reactive state management appropriate to the existing app.
- Typed API clients.
- Clear loading/error states.
- Accessible forms and controls.
- Keyboard usability.
- Responsive layout.
- No duplicate application shells.
- Consistent route naming.
- Proper cleanup of streaming subscriptions.
- No exposed provider credentials.

Provide accessible labeling and sensible focus management for chat and modal interactions.

Do not add large UI frameworks without architectural justification.

---

### 14. Independent deployment and integration

Update `masd-infrastructure`.

Local environment should support:

- Angular UI.
- Project Service.
- LLM Gateway.
- PostgreSQL.
- Ollama as an optional external or locally hosted dependency.

Commercial provider credentials must be optional.

The entire local environment should remain startable without commercial API credentials.

Provide a documented mock LLM provider or deterministic test adapter for automated integration tests.

Do not silently simulate a successful commercial provider response and label it real.

Each service must retain:

- Independent Dockerfile.
- Independent CI workflow.
- Independent versioning.
- Health and readiness endpoints.
- Externalized configuration.

Prove that changing the UI does not require rebuilding backend service source, and that the LLM Gateway can be built independently.

Do not provision cloud resources in M1.

---

### 15. Testing strategy

Implement meaningful automated tests.

#### Project Service

Test:

- Project creation.
- Validation failures.
- Project listing.
- Project updates.
- Archive behavior.
- Project access isolation.
- Conversation persistence.
- Conversation retrieval.
- Message ordering.
- Idempotent message submission.
- Database migrations.

#### LLM Gateway

Test:

- Provider configuration.
- Model discovery.
- Provider routing.
- Streaming event handling.
- Invalid model selection.
- Provider failures.
- Timeout handling.
- Cancellation.
- Sensitive-data redaction.

Use mocked provider responses for deterministic unit tests.

#### Frontend

Test:

- Project form behavior.
- Project listing.
- Project detail display.
- Chat rendering.
- Model selector.
- Streaming updates.
- Error handling.
- Cancellation.
- Navigation consistency.

#### End-to-end acceptance

Verify the following real workflow where the environment permits:

1. Start all local services.
2. Create a project from Angular.
3. Select that project.
4. Open AI Chat.
5. Select an available model.
6. Send a prompt.
7. Receive a streamed response.
8. Refresh the page.
9. Confirm conversation persistence.
10. Switch projects.
11. Confirm conversations remain isolated.
12. Return to the original project.
13. Continue its prior conversation.

A deterministic test-provider path must pass even without paid provider credentials.

Where credentials are available and authorized, perform real provider smoke tests.

Report mock tests and live provider tests separately.

---

### 16. Observability

Implement structured logs and request correlation IDs.

Capture:

- Project ID.
- Conversation ID.
- Request ID.
- LLM provider.
- Model identifier.
- Request duration.
- Status.
- Token usage when available.
- Failure category.

Do not log API keys or full conversation content by default.

Prepare trace propagation across UI-facing services.

Use existing OpenTelemetry conventions where available.

Full agent-level observability is a future milestone.

---

### 17. Milestone documentation

Update the central architecture repository with:

- `docs/milestones/M1_REQUIREMENTS.md`
- `docs/milestones/M1_DESIGN.md`
- `docs/milestones/M1_IMPLEMENTATION_PLAN.md`
- `docs/milestones/M1_ACCEPTANCE_CRITERIA.md`
- `docs/milestones/M1_HANDOFF.md`
- `docs/milestones/M1_COMPLETION_REPORT.md`

Update existing architecture or ADR documentation only when M1 introduces actual design decisions.

Document:

- Project domain.
- Conversation model.
- LLM gateway interaction.
- API contracts.
- Data ownership.
- Security boundaries.
- Local deployment.
- Testing strategy.
- Open issues.

Maintain requirement-to-implementation and requirement-to-test traceability.

---

### 18. M1 acceptance criteria

M1 cannot be marked complete unless these mandatory capabilities are implemented and appropriately verified.

AC-01: All affected repositories conform to AIEngineeringStandards.

AC-02: Project creation works through the Angular UI and persists in PostgreSQL.

AC-03: Projects can be viewed, edited, listed and archived.

AC-04: Project Service operates independently.

AC-05: LLM Gateway operates independently.

AC-06: OpenAI, Anthropic and Ollama adapters are implemented with documented configuration and appropriate mocked tests.

AC-07: An available configured model can be selected through the UI.

AC-08: Project-specific conversations can be created and retrieved.

AC-09: Streaming assistant responses render correctly.

AC-10: Conversation history persists across page reloads and application restarts.

AC-11: Conversation access is scoped to the appropriate project and user context.

AC-12: Provider failures produce safe, understandable errors.

AC-13: No commercial provider credentials are exposed in the browser, repository or logs.

AC-14: API contracts are published and validated.

AC-15: Frontend and backend unit/integration tests pass.

AC-16: Local multi-service integration works.

AC-17: Services remain independently buildable and deployable.

AC-18: CI validation is configured for each affected repository.

AC-19: The M1 handoff contains exact test results and implementation evidence.

AC-20: The architecture and governance documents are current.

AC-21: No autonomous coding or deployment actions are enabled through the chat interface.

AC-22: Git branches and pull requests follow the approved workflow.

For each criterion, distinguish:

- PASSED
- FAILED
- BLOCKED
- NOT EXECUTED

Do not claim full acceptance if a mandatory criterion remains unresolved.

---

### 19. GitHub workflow

Use feature branches in all affected repositories:

`feature/m1-project-chat-studio`

Before coding, confirm whether M0 has been merged into the appropriate default branches.

Do not overwrite existing user modifications.

Use independent commits and pull requests for each repository.

Suggested delivery order:

1. Contracts.
2. Project Service.
3. LLM Gateway.
4. Angular UI.
5. Infrastructure integration.
6. Central architecture and completion evidence.

This ordering defines compatibility dependencies, not a requirement to serialize all independent implementation work.

If local service integration requires multiple feature branches simultaneously, document the exact compatible commits.

Do not merge pull requests automatically.

Do not push directly to protected branches.

If creating the new LLM Gateway repository requires a permission or visibility decision, report the approval needed and continue safe local work.

---

### 20. Codex efficiency and execution policy

Follow the AIEngineeringStandards efficiency guidelines.

1. Begin with a concise plan of approximately 3–7 steps.
2. Inspect relevant files and M0 evidence first.
3. Reuse working M0 components and conventions.
4. Implement the smallest coherent features.
5. Avoid repeated architecture redesign.
6. Run focused tests after each batch.
7. Parallelize independent inspections and tests when safe.
8. Do not race modifications to shared Git or database state.
9. Run full regression and integration tests at milestone completion.
10. Keep response summaries short; put detailed evidence in repository documents.
11. Never sacrifice correctness for speed.
12. Do not implement unrelated features or future milestones.

Keep progressing through independently verifiable M1 tasks without asking for permission at each routine step.

Escalate only material scope changes, consequential architectural changes, missing privileges and human authorization requirements.

---

### 21. Final completion report

At the end of M1, provide:

1. Repository names and GitHub URLs.
2. Feature branches and commit SHAs.
3. Pull request URLs where available.
4. Implemented project-management capabilities.
5. Implemented AI chat capabilities.
6. Supported provider/model configurations.
7. Published API contracts.
8. Database migrations.
9. Local execution instructions.
10. Exact tests executed and their results.
11. Live provider tests versus mocked tests.
12. Security and standards-validation results.
13. Acceptance checklist.
14. Known risks, blockers and unverified functionality.
15. Recommended M2 scope.

Update the consolidated M1 handoff and completion report in the central architecture repository.

Do not describe unfinished features as working.

---

### 22. Execution directive

**Proceed with M1 implementation now.**

Begin by reconciling the actual M0 repositories and documentation.

Do not introduce a monorepo.

Do not change the established independent deployment architecture.

Do not start autonomous PM, Architect, Developer, QA or DevOps agents in M1.

Implement, validate and document the Project Workspace, Multi-LLM Gateway and AI Chat Studio.

Create the appropriate pull requests and stop before merging.

**Stop at M1 completion and await independent architectural and acceptance review.**
