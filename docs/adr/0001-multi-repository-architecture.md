# ADR 0001: Independent repositories and microservices

Status: APPROVED by the user's mandatory architecture correction and revised M0 specification.

Decision: retain MultiAgentSoftwareDelivery for architecture/governance; use separate masd-web, masd-project-service, masd-contracts and masd-infrastructure repositories for M0. Planned services follow documented domain boundaries; agent roles are not separate services. Each service owns build, CI, deployment and future persistence. No cross-service table access or circular source dependencies.

Consequences: independent releases require explicit contract/version coordination and consolidated milestone evidence. Reuse existing API/UI work; preserve original checkpoint d729e8c and superseded files. A shared local Compose environment does not imply shared build/release cadence. Future domain splits remain subject to justified requirements and human approval.
