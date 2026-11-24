# ADR 0007: M3 C4 diagrams — structured graph, generated sources, native SVG preview

Status: accepted for M3 implementation (Slice 0); human approval via the M3 PR.

## Context

M3 requires C4 context, container and component diagrams: generated, rendered, zoomable, inspectable, and exportable. PlantUML/C4-PlantUML source is required. The prompt forbids silently accepting invalid diagram syntax and executing arbitrary PlantUML directives, and requires understandable errors when a renderer is unavailable. The platform has no PlantUML/Java runtime, and adding one would be a new network-reachable rendering service.

## Decision

- The canonical package stores C4 **views** over the structured element/relationship graph. Diagrams are never stored as free text.
- Project Service generates **C4-PlantUML** and **Mermaid** source deterministically from a view. Labels are escaped, line breaks normalized, and length bounded. Only the fixed stdlib include `!include <C4/C4_Container>` (or `C4_Context` / `C4_Component`) is emitted, never user-supplied directives. The generated text is a download artifact; the platform does not execute it.
- The Studio renders an **inline SVG** directly from the validated graph with a deterministic layered layout: level-based rows, labels as text nodes (no HTML injection), zoom and pan via SVG transforms, and selectable, inspectable elements and relationships (each also reachable as a keyboard button). The view's focus is drawn as a labelled scope boundary around its children, matching the C4-PlantUML `System_Boundary`/`Container_Boundary`. SVG download exports the same rendering.
- Graph validation (dangling references, wrong level for the element kind, empty view, cycles in containment) runs server-side. The Studio shows these errors instead of a diagram; it never shows a false success.

## Alternatives considered

- **Server-side PlantUML rendering (Java or PlantUML server).** Rejected: a new runtime and attack surface, with directive and include risks. Users can render the downloaded source with their own trusted tooling.
- **Mermaid in the browser.** Rejected for the preview: a large dependency with its own parsing and HTML-label security history. Mermaid *source* export is still provided.
- **Storing diagram source text as canonical.** Rejected: the structured model must stay authoritative.

## Consequences

The preview layout is simpler than PlantUML's, but it is always consistent with the canonical graph. PNG export is not provided (SVG only). Rendering PlantUML is left to the user's tooling, and this is stated in the Studio.
