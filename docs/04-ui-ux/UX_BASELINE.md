# MASD product experience v0.1 — DRAFT

## Goal
One coherent product from initial question to operational feedback. Preserve independently deployable UI and backend services; audit existing M0–M3 code before changing it.

## Application shell
One sign-in, persistent project selector, left navigation, breadcrumbs, global operations indicator, notifications, user/settings menu. Project selection persists across studios. No module-specific credentials. Show only authorized actions. Desktop-first responsive design; collapsible sidebar. Do not introduce a new design framework without approval.

## Navigation
Home / Projects; Discovery; Requirements; Architecture; UX Design; Planning; Development; QA; Release; Operations. Shared: Agents, Artifacts, Approvals, Settings. Future capabilities must be clearly marked unavailable, not simulated.

## First journey
Sign in → select/create project → Discovery. A new idea may start as an unassigned draft conversation and be attached to a project. Prompt accepts files, pasted text and accessible chat URLs; provide manual import fallback for inaccessible links. Show actual configured limits, live character count and file validation. Select configured model/provider (including local or hosted models), detail level and optional sources. Stream a readable long-form response with headings, tables, diagrams and source links where available. Preserve thread history, follow-up prompts, copy/export and selected sections. Default to a thorough answer, not a rigid form. Promote selected content to draft Requirements, Architecture, UX or Planning artifacts with source and revision links. Never approve automatically.

## Workflow
Discovery → approved PRD → approved Architecture and UX → approved delivery plan → scoped coding agents/worktrees → PR and CI → independent QA → human milestone acceptance → approved release → deployment verification → feedback/change request. Iterations are permitted; changes to baselines require impact assessment and approval. QA planning begins before coding. Milestone acceptance and deployment approval are distinct.

## Operational states
Queued, running, waiting for input, completed, failed, cancelled, interrupted. Global operations panel displays real persisted state, current stage, timestamps, logs and permitted cancel/retry/resume actions. Navigating away does not lose a run; reload reconnects without duplicate execution. Never freeze unrelated UI or fabricate progress percentages. Errors preserve inputs and identify recovery options.

## Acceptance
One login and consistent project context; keyboard navigation and accessible controls; long-form Discovery response comparable in structure to the supplied HRMS example (vision, features, technology options, diagrams, architecture, risks, roadmap); no invented citations; artifact provenance and revision history; nonblocking generation and recovery; real provider configuration and safe secret handling; Playwright end-to-end and screenshot evidence at agreed viewport; existing contracts and behavior preserved unless approved changes; required CI and review comments resolved; human visual and functional approval.

## Decisions pending
Final visual theme and page layouts, exact navigation grouping, web/desktop integration strategy, actual provider limits and supported imports, existing repository and route mapping. Images are illustrative and have inconsistencies; do not implement sample metrics or contradictory states.
