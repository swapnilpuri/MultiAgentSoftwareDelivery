# M3.1 requirements — UX modernization, rich AI responses, unified authentication, multi-provider models and workflow reliability

Source: the owner's milestone prompt, recorded verbatim below on 2026-11-24 so that contributors can audit R1–R10 and the acceptance scenario from the repository. The output-quality reference `HRMSSystem.pdf` is owner-supplied and is not stored in Git.

---

### Context

Project repository:
https://github.com/swapnilpuri/MultiAgentSoftwareDelivery

M3 has been implemented and merged into `main`.

This is a stabilization and usability milestone. Do not proceed with M4 until M3.1 acceptance criteria are satisfied.

Use the actual repository structure and existing AIEngineeringStandards documents as the source of truth. Do not recreate existing capabilities or redesign the architecture unnecessarily.

### Execution Guidelines

1. Begin with a bounded read-only inspection of the current M3 implementation.
2. Identify existing frontend, backend, authentication, model integration, operation execution, and artifact management mechanisms.
3. Create a concise gap analysis mapping each requirement below to the current implementation.
4. Reuse established shared libraries, services, conventions, and contracts.
5. Preserve independent service deployment, microservice boundaries, security controls, and existing tests.
6. Work in small implementation batches with focused validation. Avoid excessive sequential reasoning, repeated repository scans, and redundant test runs.
7. Where choices are already established in AIEngineeringStandards, follow those standards.
8. Implement all requirements, create or update tests, update documentation, and deliver through GitHub PRs.
9. Resolve all actionable PR review comments. Do not merely reply to or dismiss findings without addressing them.
10. Merge only when required CI, security, tests, reviews, and acceptance gates pass. Do not bypass branch protection.

## Requirement 1 — Intuitive, Unified UI

The current M3 application is not intuitive.

Redesign the navigation and workflow using a consistent application shell:

- AI Workspace
- Requirements Studio
- Architecture Studio
- Delivery / Milestones
- Operations / Activity
- Administration / Settings

Users should immediately understand where to start and what the next action is.

Provide consistent navigation, breadcrumbs, project context, page titles, help text, loading indicators, error states, and empty states.

Preserve user context across navigation.

Support responsive layouts and accessible interactions.

Do not introduce a second unrelated UI design system.

## Requirement 2 — Rich Conversational AI Workspace

Build or enhance an AI Workspace that produces comprehensive, well-structured responses comparable in presentation and depth to a modern ChatGPT or Claude response.

The attached HRMSSystem.pdf is the output-quality reference.

The reference includes:

- Detailed product vision
- Functional capability matrices
- Prioritization tables
- AI-agent recommendations
- Business workflows and diagrams
- Technology recommendations
- Microservices architecture
- Repository structures
- Security considerations
- Development roadmap
- MVP recommendations

Implement support for:

- Headings, paragraphs, lists, and tables
- Syntax-highlighted code blocks
- Mermaid or supported architecture diagrams
- Expandable sections
- Source references where available
- Incremental/streamed response rendering
- Copy, regenerate, and save actions
- Conversation and response version history
- Long-response rendering without UI freezing

Do not impose artificial short-answer limits.

However, output depth should remain responsive to the user's request and selected generation profile.

Provide response profiles such as Concise, Standard, and Comprehensive.

These are user-facing generation preferences, not different product architectures.

The system must distinguish a helpful AI response from an approved engineering artifact.

## Requirement 3 — Response-to-Artifact Workflow

Allow users to promote complete responses or selected sections into:

- Product vision
- Requirements / PRD
- Architecture specifications
- Architecture Decision Records
- Implementation plans
- Milestone definitions

Preserve traceability:

Source Input → Conversation → Generated Response → Approved Artifact → Downstream Artifact.

Keep source references, versions, generation metadata, and approval records.

Users must be able to revise or approve generated content before it becomes authoritative.

Do not silently overwrite an approved artifact when the source response changes.

## Requirement 4 — Upload and Import

Support:

1. PDF upload.
2. Text and supported document uploads.
3. Pasted URLs.
4. Supported public ChatGPT shared conversation URLs.
5. Supported public Claude conversation URLs.
6. Supported public Gemini conversation URLs.
7. Manual transcript paste or export upload when URL retrieval is unsupported.

Implement provider-specific URL handling where necessary.

Do not assume every shared conversation URL exposes machine-readable content.

Never bypass provider authentication, scrape private sessions, or store browser credentials.

Provide explicit import failure reasons and fallback paths.

Security requirements:

- File type and signature validation
- Configurable upload size limits
- Safe document parsing
- Untrusted-content handling and prompt-injection boundaries
- SSRF protection for imported URLs
- Malware scanning integration where available
- Tenant/project isolation
- Audit logging and retention policies

Uploaded and imported sources must remain traceable.

## Requirement 5 — Character and Upload Limits

Display:

- Maximum prompt character count
- Current character count
- Remaining characters
- Maximum allowed file size
- Supported file formats
- File upload progress
- Clear validation feedback

Limits must come from backend configuration or capability endpoints.

Validate limits on both frontend and backend.

Prevent submissions that exceed configured limits.

For long documents exceeding direct model context constraints, provide an explicit processing strategy rather than silently truncating content.

Document any chunking, extraction, summarization, or retrieval behavior.

## Requirement 6 — Fix Generate PRD Reliability

Current defect:

In Requirement Studio, after clicking Generate PRD, the user receives:

"Operation is running or interrupted; reload before explicit retry"

The entire application then becomes unresponsive, requiring a browser refresh.

Investigate and correct the underlying cause.

Required behavior:

- The application remains responsive while a PRD job runs.
- A running operation has a visible status and identifier.
- Refreshing the browser reconnects to the existing operation.
- Duplicate clicks do not create uncontrolled duplicate jobs.
- Interrupted requests do not leave the UI permanently disabled.
- Errors show recovery actions without requiring page reload.
- Retry operations are explicit and idempotent.
- If a worker or backend restarts, the job is recovered, completed, or marked failed with a clear reason.
- Users can navigate to other supported sections while generation continues.

Do not hide the problem by merely removing the error message.

Implement durable operation management using the existing architecture wherever possible.

## Requirement 7 — Operation Visibility

Provide a reusable operation tracking experience.

Show:

- Operation name and type
- Current lifecycle state
- Started time
- Actual stage or progress where available
- Last activity
- Failure reason where relevant
- Completed result or linked artifact
- Allowed cancel, retry, or resume actions

Suggested states:

QUEUED → RUNNING → COMPLETED / FAILED / CANCELLED.

Include INTERRUPTED or RECOVERING when the execution model genuinely supports those states.

Use SSE, WebSockets, or an established polling mechanism where appropriate.

Never invent percentage completion if actual progress cannot be measured.

Persist state in the backend. Browser memory must not be the authoritative record.

## Requirement 8 — Unified Authentication

Users must log in once to access the authorized parts of the application.

Remove separate login experiences for Requirement Studio, Architecture Studio, and other modules.

Implement or reuse central OIDC authentication and shared authorization.

Requirements:

- Single login entry point
- Consistent application session
- Authenticated routing
- Project and tenant-aware access
- Central logout
- Secure session expiration and renewal
- No credentials in browser local storage or application logs
- No embedded provider API keys in frontend code

Preserve authorization boundaries between services.

Single sign-on must not mean unrestricted access to all services.

## Requirement 9 — Commercial and Open Model Providers

Provide a model gateway/provider abstraction supporting:

- OpenAI models
- Anthropic Claude models
- Google Gemini models
- Existing local or open-source models
- Compatible custom endpoints where supported

The implementation should use official SDKs or supported APIs where practical.

Provider capabilities must be discovered or configured accurately.

Support model selection in the AI Workspace and relevant generation workflows.

Include:

- Provider status
- Available configured models
- Model capability metadata
- Secure credential configuration
- Provider-specific context and output constraints
- Token usage and cost reporting when available
- Timeouts, rate limits, retries, and error classification
- Request tracing without leaking sensitive prompt content

Do not assume subscriptions to ChatGPT, Claude, or Gemini web applications automatically provide API access.

Do not invent provider credentials or hardcode model names as permanently available.

Existing functionality should continue working when a configured provider becomes unavailable.

## Requirement 10 — Engineering Quality and Documentation

Add automated coverage for:

- Navigation and unified login
- Role and tenant authorization
- Character counter and upload limits
- PDF/document ingestion
- Supported and unsupported conversation URLs
- Multi-provider configuration and selection
- Rich response rendering
- Response-to-artifact promotion
- PRD generation success and failure
- Duplicate submissions
- Interrupted operation recovery
- Browser refresh during active generation
- Cancel/retry behavior
- Long-response and large-document performance
- Security controls for uploads, URLs, and credentials

Use contract tests for independently deployed services.

Add end-to-end tests for the principal user journeys.

Perform targeted regression testing throughout implementation and one final comprehensive validation pass.

Document:

- Updated architecture and contracts
- Provider configuration
- Upload limits and supported sources
- Operation lifecycle and recovery
- Authentication and authorization
- User workflows and navigation
- Known limitations and future enhancements

## Required Acceptance Scenario

Demonstrate the following end-to-end workflow:

1. User signs in once.
2. User creates or opens an HRMS project.
3. User uploads HRMSSystem.pdf or enters a comparable detailed product-design prompt.
4. User selects a configured AI model.
5. Application displays the allowed input limits and remaining characters.
6. User generates a comprehensive structured response.
7. Rich content, tables, diagrams, and sections render correctly.
8. The user saves the response.
9. The user promotes the selected content into a draft PRD.
10. Generation progress is visible while the user navigates within the application.
11. The user refreshes the page and can still inspect the operation.
12. The PRD generation completes, or shows a recoverable error without freezing the interface.
13. The user opens the PRD, reviews it, and approves it.
14. The approved PRD is traceably available as input to Architecture Studio.
15. The entire sequence uses one application login.

Use mock providers for deterministic tests and conduct a live-provider smoke test only when credentials are available.

## Delivery

Create an M3.1 implementation plan based on the actual repository.

Implement the requirements in coherent, independently testable batches.

Where a shared contract is required, land compatible contract changes before dependent service changes.

Ensure all relevant PR reviews and CI checks are satisfied.

Do not leave unresolved high-severity review findings.

The final delivery report must contain:

1. Root cause of the Generate PRD freeze
2. Changes made by repository/service
3. Updated UI workflows
4. Provider integrations and configuration
5. Supported import methods and limitations
6. Operation persistence/recovery design
7. Authentication changes
8. Automated test results
9. Security and review results
10. PR and merge links
11. Acceptance scenario results
12. Any remaining limitations or blockers

Do not claim completion based solely on passing unit tests.

M3.1 is accepted only when the principal end-to-end workflow is demonstrated and all mandatory quality gates pass.
