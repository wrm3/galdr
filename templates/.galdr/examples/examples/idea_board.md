# IDEA_BOARD.md — Example

> This example shows a realistic IDEA_BOARD for a Norse mythology avatar web app
> with ideas ranging from raw captures to promoted tasks and shelved concepts.

---

## Active Ideas

### IDEA-003: Starter Theme Pack — Paywall Upsell
**Status**: evaluating
**Category**: monetization
**Captured**: 2026-02-21
**Source**: user

**Description**:
When/if the app ships as a product, offer tiered theme packs as paid upsells.
A $35 starter pack could unlock 1-3 rooms and 2-5 characters. Additional themes,
rooms, or characters are further upsells (~$100/theme + $5/month storage).

**Potential Value**:
Creates a recurring revenue stream beyond initial purchase. Theme packs are
natural expansion content with low marginal cost. The model scales well —
AI assistance uses the user's own API credits, so infrastructure costs stay low.

**When Ready**:
After core product ships and user accounts/cloud storage are implemented.
Needs: user auth, per-user cloud storage, billing/Stripe integration.

**Notes**:
- User-created themes (like "GaldrWorks") are personal and not shared between users
- Default/public theme ("CodeShop") is free and ships as the default
- Token/API costs for AI assistance should be user-funded, not platform-funded
- Related: IDEA-004 (per-user theme isolation in cloud)

---

### IDEA-004: Per-User Theme Isolation in Cloud
**Status**: raw
**Category**: technical
**Captured**: 2026-02-21
**Source**: AI

**Description**:
Each user's custom themes must be stored in their own cloud namespace —
users cannot access each other's themes. Default themes (like CodeShop) are
available to all. This requires a per-user storage partition in the backend.

**Potential Value**:
Privacy and data isolation are table stakes for a multi-user product.
Also enables the monetization model in IDEA-003 (if users pay for extra themes,
those need secure, isolated storage).

**When Ready**:
When user authentication and cloud storage are being designed (Phase 2+).
Should be part of the backend data model, not retrofitted.

---

### IDEA-007: Export Scene as Video / GIF
**Status**: raw
**Category**: feature
**Captured**: 2026-02-19
**Source**: user

**Description**:
Allow users to export a short recording of their 3D Norse mythology scene
as a video or animated GIF for sharing on social media.

**Potential Value**:
Viral marketing — users share their scenes and drive organic discovery.
Could be a premium feature (free users get watermarked GIF, paid users get clean export).

**When Ready**:
After the core scene rendering is stable. Needs: server-side rendering
or client-side canvas capture. Non-trivial but valuable for growth.

---

## Promoted Ideas

### IDEA-001: User-Created Themes → Task #201
**Status**: accepted
**Category**: feature
**Captured**: 2026-02-15
**Source**: user
**Promoted**: 2026-02-18 → Task #201: Implement User Theme System

---

### IDEA-002: Theme Editing UI → Task #202
**Status**: accepted
**Category**: ux
**Captured**: 2026-02-16
**Source**: user
**Promoted**: 2026-02-18 → Task #202: Build Theme Editor Interface

---

## Shelved Ideas

### IDEA-005: Multi-User Collaborative Scenes
**Status**: shelved
**Category**: feature
**Captured**: 2026-02-17
**Source**: AI
**Shelved Reason**: Too complex for MVP. Requires real-time sync infrastructure
(WebSockets, CRDTs). Revisit after v1.0 ships and we have user base to validate demand.

---

### IDEA-006: AI-Generated Scene Backgrounds
**Status**: shelved
**Category**: feature
**Captured**: 2026-02-18
**Source**: user
**Shelved Reason**: API costs too high for current stage. Stable Diffusion
integration is non-trivial. Good idea for v2 with monetization in place.
