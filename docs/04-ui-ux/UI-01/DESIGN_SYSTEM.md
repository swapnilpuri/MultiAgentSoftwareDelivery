# MASD application design system — foundation

**DRAFT — v0.1; exact values proposed for F3 review.** UI-01 only. No UI framework, font dependency or application code is introduced.

## Visual direction and tokens

Retain the reference boards' violet identity, clear content cards, persistent header/project selector and collapsible navigation. Concentrate decorative gradients/illustration on sign-in and empty states. Working pages use a neutral canvas and restrained borders; gradients are not text backgrounds or status indicators. Brand/logo selection is still a human decision (R01).

| Semantic token | Light | Dark | Usage |
|---|---|---|---|
| canvas | `#F8FAFC` | `#0F172A` | Page background |
| surface | `#FFFFFF` | `#1E293B` | Cards, menus, drawer |
| text | `#0F172A` | `#F8FAFC` | Primary text |
| text-muted | `#475569` | `#CBD5E1` | Secondary text, never reduced opacity |
| border-subtle | `#CBD5E1` | `#475569` | Decorative divisions only |
| control-border | `#64748B` | `#94A3B8` | Required input/control boundaries |
| primary-fill | `#6D28D9` | `#6D28D9` | Primary button with white text |
| primary-hover | `#5B21B6` | `#5B21B6` | Hover/pressed primary |
| link / focus | `#6D28D9` | `#C4B5FD` | Links and focus rings on neutral surfaces |
| selected-bg | `#EDE9FE` | `#3B2468` | Selected navigation; text uses link token |
| success-text | `#166534` | `#86EFAC` | Verified completed outcome |
| warning-text | `#92400E` | `#FDE68A` | Attention, cancellation requested |
| error-text | `#B91C1C` | `#FCA5A5` | Failure, field error |
| shell-bg / shell-text | `#2E1065` / `#FFFFFF` | `#170D2C` / `#F8FAFC` | Header/brand region |

Use status text/icon with color. “Future,” “not available,” “status unavailable” and “no records” have different copy and must not look like successful zero counts. White primary-button text remains white in both themes. Use a white focus ring on the dark violet shell/primary buttons; use a 2px ring with 2px separation on neutral surfaces. Do not assume a neutral focus token works against every violet control.

Accessibility targets: WCAG 2.2 AA text contrast (4.5:1 normal, 3:1 large), 3:1 meaningful control boundaries/focus against adjacent colors; keyboard operability and visible unobscured focus. These are proposed acceptance targets, not a certification claim. Token-pair arithmetic can be checked now; final composited screenshots, hover/disabled states, forced colors and browser behavior require implementation validation.

## Typography and spacing

Use the installed system UI stack `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`. Reference “Inter or similar” is satisfied by a consistent system face without adding a hosted font. Propose 16px/24px body; 14px/20px secondary labels; 12px/16px metadata only; page heading 32px/40px weight 700, section heading 24px/32px weight 600, card heading 20px/28px weight 600. Mobile page heading 24px/32px. Controls inherit the font; technical IDs use the existing monospace stack and wrap. Use rem units and support 200% text scaling.

Spacing scale: 4, 8, 12, 16, 24, 32, 48px. Control height 44px minimum for touch access; 8px control radius, 12px card/menu radius. Use a 1px border; subtle shadow only for elevated menus/drawers, not every card. Icons 20–24px with one consistent existing icon approach. Icon-only buttons always have accessible names; tooltips supplement rather than replace names.

## Layout and responsive shell

Desktop ≥1280 CSS px: 64px header; expanded sidebar 256px or collapsed rail 72px; content padding 24–32px. Tablet 768–1279: compact header, 72px rail by default with expandable overlay. Mobile <768: menu-trigger drawer, no permanent rail, 16px content padding and stacked cards. These are proposed defaults, with content-driven wrapping allowed. Desktop collapse preference never forces a mobile rail.

At 320 CSS px (also representing 1280px at 400% zoom), shell has no horizontal page scrolling; long project names truncate visually with full accessible name. Keep selector, operations and user/menu access available. Data tables may use a labeled internal horizontal scroll region when meaningful relationships require it. Header should grow/wrap rather than clip at text zoom. At narrow widths operations becomes a full-screen dialog; project selection is a full-width dialog/list. Only the topmost modal is active; avoid stacked dialogs. Content focus is never hidden beneath sticky headers/drawers.

## Shared components and states

| Component | Shared rule |
|---|---|
| Button/link | Button for mutation/overlay; link for destination. One primary CTA per task region; loading prevents duplicate submission without losing label. Destructive cancel operation names the operation |
| Input/select | Persistent label, helper/validation association, required indicator in text; validate against existing API constraints; retain user input on error; do not embed secrets in telemetry |
| Card/project row | Semantic heading and single clear Open destination; do not nest clickable buttons inside a whole clickable card; no unrelated metrics |
| Menu/selector | Trigger expanded state, clear current selection; keyboard open/traverse/activate/Escape; return focus on dismiss; pagination/error/no-match states |
| Drawer/dialog | Accessible title, Close control, focus containment when modal, Escape dismissal, background inert; navigation and request actions have separate semantics |
| Navigation | Landmark label, current-page marker, same destinations expanded/collapsed; Future text visible or included in accessible name; no color-only active state |
| Status/banner | Polite live update for progress/state; alert for actionable error once; avoid announcing every poll; timestamps from API, no invented percent |
| Loading/empty/error | Distinct states; loading does not show zero data; empty only after successful authorized response; retry is explicit; preserve unaffected shell navigation |
| Theme preference | Light / Dark / System; System initial proposal, follow OS until manually selected; persist theme only, tolerate unavailable storage; apply before content paint where feasible |

Motion: 120–180ms for simple transitions; respect reduced-motion settings and disable nonessential animation. No spinner/progress animation should imply measured completion. Components must remain usable in both themes with keyboard, touch and screen readers.

## Foundation visual acceptance

V01: All shell variants share logo, labels, spacing and selected-project name. V02: light and dark carry identical information/actions. V03: no unresolved glyphs, clipping or unreadable crop text at agreed viewports. V04: 320/768/1280/1600px layouts preserve critical controls and focus. V05: measured token contrast meets targets; final state/composite contrast remains a browser acceptance item. V06: future/unavailable/stale/empty are visibly distinct. V07: illustrative screenshots are marked DRAFT and never used as test evidence. Full screenshot tolerances and per-page visual criteria remain in later acceptance design.
