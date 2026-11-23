# Governance model

The inherited operating model assigns architecture/requirements/independent acceptance to ChatGPT, implementation/verification/Git to Codex and consequential approvals to humans. Git code, ADRs and actual execution evidence are authoritative.

Each repository declares owner, domain, governing architecture URL, standards version, commands and required documents in repository.json. Its project-specific AGENTS.md references the governing architecture and copied operating model. STANDARDS_MANIFEST.yaml records canonical and imported SHA-256, provenance and verification. CLI checks validate existence, integrity, metadata, documented commands, CI invocation and secret exclusions. They are local static compliance, not runtime policy enforcement.

Future governance will enforce requirement→task→approved action→execution→commit/PR→CI→release traceability, authorization, human approvals, drift prevention, OPA policy decisions and release quality. Models may propose operations but cannot approve their own privileged actions. Temporal recovery must preserve the same authorization and evidence. Per-project data and credentials must remain isolated.

Generated projects will select an approved version/digest of a centrally published standards bundle, apply project-only overlays, pin imports and validate them in CI. Updates arrive as reviewable synchronization PRs; never silently replace generic principles. M0 copies are not centrally synchronized. Same-repository file/hash edits can defeat local tamper checks; independent review and future external pins form the eventual trust boundary.
