# Design — Casa Arcana

Locked design system. Feature pages share these tokens and presentation rules; existing routes, application logic, and interactions remain unchanged. `tokens.css` is the canonical token source, imported by `site.css`.

## System
- Genre · atmospheric observatory
- Macrostructure · Ecosystem Index (home), Narrative Workflow (tools), Long Document (glossary)
- Theme · Midnight-inspired custom system
- Navigation · shared floating navigation, inline and detached on desktop; wraps as a compact row on small screens
- Footer · single-line statement

## Tokens (canonical · `site.css` is the shared source of truth)
- Paper · `oklch(16% 0.016 268)`
- Raised paper · `oklch(21% 0.018 268)`
- Ink · `oklch(94% 0.012 268)`
- Muted ink · `oklch(73% 0.016 268)`
- Rule · `oklch(34% 0.024 268)`
- Accent · `oklch(76% 0.13 285)`
- Display · `Newsreader`, roman
- Body · `Geist`
- Label · `Geist Mono`
- Spacing · named 4-point scale in `site.css`

## Interaction and motion
- Preserve existing interaction behavior and handlers.
- Focus-visible rings, consistent control sizing, and clear disabled/loading/error states.
- No decorative reveal motion; short state transitions only. Reduced motion disables spatial transitions.

## Page rules
- Use shared chrome, colors, typography, and focus styling across home, sound, oracle, natal, glossary, and Tarot.
- Feature-specific layouts and content remain intact; the stylesheet maps existing classes into the shared system.
- Do not alter calculations, endpoints, API payloads, data, or feature JavaScript.
