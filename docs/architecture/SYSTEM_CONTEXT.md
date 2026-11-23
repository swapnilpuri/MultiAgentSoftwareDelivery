# System context

Approved: a multi-repository microservices platform for governed software delivery. The central repository owns architecture, governance and milestone evidence. Four sibling repositories implement only the M0 foundation.

M0 user flow: browser → standalone Angular UI → versioned Project Service API. Health/readiness and the empty project overview are real; future navigation routes explicitly state that integrations are unavailable. No live provider, cloud or database credentials are required.

Future lifecycle: intake → PM/architecture/planning → human approval → dependency-aware development → QA/security → PR/CI → deployment approval → cloud → monitoring/audit. Agent roles are execution definitions, not individual microservices. Human approval and independent review are outside agent self-authorization.

See system-context.puml for a dependency-free C4-style context/container view. It is source documentation; rendered-diagram verification is reported separately.
