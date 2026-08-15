# ChangeFleet visual system

The accepted primary-screen concept is [`concepts/changefleet-primary.png`](concepts/changefleet-primary.png). It is the visual source of truth for the first desktop implementation.

## Direction

ChangeFleet is an editorial mission-control dossier: true white paper, near-black type, graphite rules, electric chartreuse for verified progress, and vermilion only for blocked mutations. The screen uses open bands, rails, lists, and one diff frame rather than a grid of floating cards.

## Tokens

| Role | Value |
| --- | --- |
| Background / surface | `#ffffff` |
| Ink | `#0a0a0a` |
| Muted ink | `#5b5b55` |
| Rule | `#b9bab4` |
| Strong rule | `#1b1b18` |
| Safe accent | `#bfff00` |
| Safe wash | `#efffd1` |
| Approval | `#ff3d12` |
| Approval wash | `#fff0ec` |
| Removed line | `#ffd8d2` |
| Radius | `0`, `2px`, `4px` only |
| Shadow | none by default |

Headings use `Arial Black`, `Helvetica Neue`, Arial, sans-serif. UI chrome, asset paths, timestamps, and code use `IBM Plex Mono`, `SFMono-Regular`, Consolas, monospace. Controls use deliberate 13–15px typography; body copy uses 15–17px.

## Layout and components

- A quiet 70px header with brand, four navigation items, mode text, and one outlined architecture control.
- A generous introduction band with the exact headline `Protect every downstream contract.` and one change input strip.
- A ruled orchestration rail with five numbered stages and a real four-value summary.
- A two-column main region: open lineage canvas on the left, audit timeline on the right.
- A full-width bottom repair viewer with current/proposed code and a small metadata column.
- Filled geometric status marks: chartreuse circles for verified state, black for observed/in-progress, vermilion for approval-required.
- Interaction motion: a scan dash follows lineage routes while running; timeline rows reveal in order. `prefers-reduced-motion` disables both.

## Above-the-fold copy lock

- `ChangeFleet`
- `Campaigns`, `Agents`, `Policies`, `Evidence`
- `Fixture mode`, `Architecture`
- `Protect every downstream contract.`
- `An agent fleet turns one risky schema change into owner-specific repairs, policy gates, and durable proof.`
- `warehouse.orders`
- `shipping_country → country_code`
- `Run coordinated repair`
- `Scout`, `Architect`, `Repair`, `Govern`, `Proof`
- `6 affected assets · 4 repairs · 3 owners · 1 approval gate`

No eyebrow, badge, decorative statistic, gradient, glow, glass surface, or unrelated product area is permitted above the fold.

## Icon inventory

- Brand: two offset black routing strokes inside a black square, code-native SVG.
- Architecture: three-node hierarchy, 1.5px square-ended stroke.
- Dataset: 3×3 table glyph, 1.25px stroke.
- Stage/status: filled numbered circle; check uses a short two-stroke glyph.
- Timeline: filled circle with check, black dot, or exclamation mark.
- Actions: right arrow and repair navigation chevrons, 1.75px square-ended stroke.

## Responsive continuation

Below 900px, header navigation becomes horizontally scrollable, the change strip stacks, the stage rail scrolls, lineage and evidence become one column, and the diff changes from side-by-side to stacked. The run action and evidence feed remain visible and usable.

