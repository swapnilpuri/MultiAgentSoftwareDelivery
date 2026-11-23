# Security architecture

M0 implements sanitized errors, environment-based configuration, explicit CORS origins, credential-free local execution, source secret scanning, dependency advisory checks, nonroot Dockerfiles and independent CI with read-only GitHub permissions. Compose host exposure is loopback only. CORS is not authentication. Health and readiness are unauthenticated local development endpoints; there are no project-data APIs.

Future required controls: OIDC identity, project-scoped authorization, independent policy decisions, approval records, execution isolation, credential brokerage, provider/data isolation, trace redaction and audit retention. Agents cannot mint their own privileges. Tool proposals must be evaluated against immutable approved scope and allowed tool metadata before execution; drift stops the action for review.

No production deployment, credential setup or repository permission changes occur in M0. Repository visibility must be explicitly authorized. CI checks local copied standards; they do not enforce a central trust root. Branch protection and required review/status rules need human administrator configuration. Secret scans are heuristic and source-tree based; never claim complete credential detection or historical scanning.


M1 security update: Project Service enforces a server-configured local identity and ownership on all nested resources; production mode with that identity is refused. Gateway access uses a backend-only generated bearer credential and explicit project/user/request context. Providers are selected from a canonical provider/model catalog and project allowlist; no silent provider-changing aliases, fallback, tool execution or frontend credentials. Request/context/output sizes, provider timeouts and a local per-user gateway limit bound execution. Markdown raw HTML/remote images are disabled. Prompt content is not logged.

Future production work remains: real OIDC, short-lived project-scoped service capabilities, project data classification/residency policy, distributed rate limits and audit retention. Until classification is enforced, projects must explicitly approve allowed model IDs; catalog/endpoint/credential changes are trusted administrative configuration and require review. No production multi-user security is claimed.
