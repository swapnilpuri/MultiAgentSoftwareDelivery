# ADR 0003: Independent contract snapshots and local integration

Status: M0 implementation decision consistent with approved architecture.

Use an OpenAPI 3.1 contract 0.1.0 candidate in masd-contracts; consumers vendor the exact reviewed candidate rather than reading sibling source or moving branches. After review, publish immutable contract versions and update consumers through separate PRs. No release is claimed before publication.

Compose coordinates separately tagged web/API images. Frontend dev proxy and nginx route a configurable API base to Project Service. No gateway implementation is created before its use case. Stateless readiness is legitimate because M0 intentionally has no persistence/downstream initialization. Runtime independence must be tested; unavailable Docker is a blocked acceptance item.

The inherited Angular toolchain needed patched glob 14.0.6 and minimatch 11.0.9 overrides for reported advisories; retain compatibility checks and remove overrides when upstream adopts safe versions. UI library, deployment cloud/region, production policy and sandboxing remain open future decisions.
