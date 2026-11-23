# ADR 0004: M1 project persistence and gateway isolation

Status: M1 implementation decision for independent architecture review; not production approval.

The authorized M1 specification introduces PostgreSQL persistence and LiteLLM. Use SQLAlchemy 2/Alembic in Project Service, with service-owned projects, conversations, messages and turn/usage metadata. Preserve M0 health contracts while adding project/chat APIs. Gateway is a separate stateless service/repository, accessible only to an authenticated backend client; it receives explicit authorized context, not database credentials. No shared source library or shared table access.

For credential-free local use, select a server-configured development identity and explicitly enabled deterministic test provider. Production mode is refused until real OIDC authorization exists. Project allowlists prevent silent provider fallback; changes require an explicit settings save. A test adapter is distinct from commercial adapters. Generated local service/database secrets remain in ignored environment configuration.

M1 streaming uses bounded SSE with durable idempotent turn outcomes. Single-replica startup recovery marks incomplete turns failed. Multi-replica coordination, durable provider resumption, data classification and central routing policy remain future requirements. No irreversible existing-data migration is introduced; M1 adds its first schema to a dedicated local database.
