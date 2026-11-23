# ADR 0002: Pinned local standards inheritance

Status: implemented under M0 authorization.

C:/Projects/AIEngineeringStandards is absent. Canonical companion files were located in C:/Projects/AiEngineeringStandardProject (no Git metadata); the operating model declares version 1.0. Source SHA-256 identifies the exact input. Preserve generic AGENTS principles; adapt only project-specific settings. Copy the model verbatim to every bootstrapped repository, pin source and imported hashes in JSON-compatible YAML, and run the same offline integrity checks in each CI.

These are local copies, not central enforcement. Future bundle publishing, immutable pins and reviewable synchronization will support generated projects. Updating both a local file and its manifest can defeat local integrity validation; independent review and external signed bundle references are future trust controls.
