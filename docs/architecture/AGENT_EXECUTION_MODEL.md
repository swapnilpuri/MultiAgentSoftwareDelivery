# Agent execution model

Planned execution envelope: schema_version, project_id, requirement_ref, task_id, workflow_id, approved_scope, allowed_tools, model_route, policy_bundle_hash and approval_ref. Proposed actions and approved actions are separate immutable records. Agents cannot authorize their own privileged operations.

PM/architect/planner propose work; scoped development agents implement; QA/security provide independent evidence; DevOps acts after deployment approval. Logical roles share runtime infrastructure until a justified domain split exists. Provider routing must not change permissions.

Temporal will own durable transitions, approval signals and recovery. LangGraph executes stateful tasks within approved scope. Workers isolate repository, filesystem, network and credentials by task/project. Activities use idempotency keys, bounded retries and reconcile external side effects before replay. Recovery rechecks authorization and expired approvals, preserving requirement→task→commit→test→release evidence.

M0 runs no agent, workflow engine, approval service or sandbox. These are interface expectations for later authorization.


M1 update: chat is interactive only. No agent tools or workflow/coding execution is enabled. The isolated gateway accepts scoped, bounded chat requests from Project Service, not agent privilege grants.
