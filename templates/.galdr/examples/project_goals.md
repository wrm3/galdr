# PROJECT_GOALS.md — Example

> This example shows PROJECT_GOALS for a Norse mythology avatar web app.
> The AI loads this at session start to validate decisions and steer work.

---

## Vision

Build an interactive 3D Norse mythology office scene where users can explore,
customize their cast of characters, and eventually share or publish their
personalized workspace as a product with tiered feature access.

---

## Primary Goals

| ID   | Goal                                    | Target / Metric                              | Status   |
|------|-----------------------------------------|----------------------------------------------|----------|
| G-01 | Ship a working 3D scene with 5+ characters | All Season 1 cast rendered, animated, and interactive in browser | active |
| G-02 | Enable per-user theme customization      | Users can create, edit, save their own theme  | active   |
| G-03 | Establish monetization foundation        | Stripe billing + tiered theme packs designed  | active   |
| G-04 | Performance: load under 5 seconds        | LCP < 5s on average broadband connection      | active   |

---

## Secondary Goals

Goals that support the primaries but aren't critical path:

- **Voice + Lip Sync**: Characters speak with ElevenLabs TTS and accurate lip sync
- **Mobile Responsive**: Core scene viewable on mobile (no interaction required)
- **Accessibility**: Keyboard navigation for key scene controls
- **Analytics**: Track which characters and scenes users engage with most

---

## Non-Goals (Explicitly Out of Scope)

Things we are consciously NOT building right now:

- **Multi-user collaborative scenes** — requires real-time sync infrastructure (post-v1)
- **User-generated characters from scratch** — use predefined cast only (post-v1)
- **Mobile-first interaction** — desktop web is the primary platform for v1
- **Offline/PWA support** — cloud-first; offline is a v2 consideration
- **AI-generated scene backgrounds** — API costs too high for MVP stage

---

## Success Metrics

How we know we've achieved the vision:

- 5+ Norse mythology cast members rendered with toon shading in browser at < 5s load
- User can create a named theme, edit it, save it, and reload it from their account
- Stripe checkout flow works end-to-end for a $35 starter pack purchase
- Zero critical security vulnerabilities in auth/storage layer
- 10+ beta users have created custom themes without bug reports

---

## Goal Log

| Date       | Change                                          | Reason                                      |
|------------|-------------------------------------------------|---------------------------------------------|
| 2026-02-15 | Initial goals defined (G-01, G-02, G-04)        | Project setup                               |
| 2026-02-18 | Added G-03 (monetization foundation)            | User introduced theme pack pricing concept  |
| 2026-02-21 | Added per-user theme isolation to Non-Goals     | Clarified scope: isolation is required, not optional |
| 2026-02-21 | Added Voice + Lip Sync to Secondary Goals       | Animation pipeline completed                |

---

## Goal Status Reference

| Status    | Meaning                                      |
|-----------|----------------------------------------------|
| `active`  | Current active goal being worked toward      |
| `complete`| Goal achieved — log the completion date      |
| `retired` | Goal no longer relevant — log the reason     |
| `paused`  | Temporarily deprioritized                    |
