# Research Changelog

Permanent log of validated slices, pivots, and blocks. Never delete prior entries.

---
## Entry #0 — PROGRAM SETUP — 2026-03-31

### Context

This repository starts from an explicit feasibility study of the Xatu public dataset.

### Key Findings

- Xatu is strong enough for builder / relay market structure research.
- The join path across relay delivery, beacon linkage, and execution inclusion is good enough for serious work.
- Public mempool observations are partial but useful, which makes public-vs-private flow estimation feasible.
- Canonical traces are rich enough for realized MEV classification.
- Public parquet is delayed, so this program is for research and model-building, not direct live execution.

### Decision

Adopt a one-slice-per-loop autoresearch design with:
- Ralph hats for orchestration
- append-only state in `state/`
- hard validation of every run bundle
- bounded parallelism only for isolated runs

### Initial Phase Order

1. Builder / Relay Market Map
2. Auction Microstructure
3. Public-vs-Private Flow Estimation
4. Realized MEV Taxonomy

---
## Entry #1 — Builder / Relay Market Map — 2026-04-01

### Context

First validated research slice. Agenda item #1: Builder / Relay Market Map (Phase 1).

### Key Findings

- 47 builders delivered 6,597 unique blocks on 2026-03-29 across 8 relays.
- Relay multiplicity is ~6.7x per block, meaning builders route through nearly all available relays.
- The builder market is moderately concentrated (estimated HHI 0.15-0.25, top-3 share 55-75%).
- 109 builders submitted bids (2024-09-13 sample) vs 47 delivering, showing substantial builder attrition.
- 917K validators registered with relays, mapping to only 24.5K fee recipients (staking pool aggregation).
- Delivered payload join coverage to beacon/execution is ~99.99%.

### Decision

**KEEP** — establishes basic market structure dimensions and confirms Xatu data supports this research.

### Limitations

- Single-day window; concentration may vary over time.
- Exact per-builder share not computed (bounded estimates only).
- Bid trace from different date (2024-09-13) than delivery data (2026-03-29).

### Follow-On Candidates (all held for curation)

1. Builder Market Share Exact Breakdown — precise GROUP BY on builder pubkey
2. Builder Churn and Temporal Stability — multi-day/week window extension
3. Builder Win Rate from Bid Traces — join bid and delivery for same window

---
## Entry #2 — Auction Microstructure — 2026-04-01

### Context

Second validated research slice. Agenda item #2: Auction Microstructure (Phase 1).

### Key Findings

- ~1,181 bids per slot on 2024-09-13 across 6,620 slots, indicating extremely intense auction competition.
- 109 unique builders submitted bids; cross-referencing with delivery data (different date) shows ~57% builder attrition from bidding to winning.
- Each builder submitted ~10.8 bids per slot (including relay duplication), consistent with progressive bid updating across ~8 relays with ~1.4 revisions per relay.
- Per-bid win rate is ~0.085%; per-builder per-slot win rate is ~1.25-2%.
- Builder market has three tiers: 3-5 dominant winners, 15-25 occasional winners, 60-80 bidders-only in competitive fringe.

### Decision

**KEEP** — establishes basic auction intensity and competition dimensions. Aggregate metrics provide valid foundations for deeper per-row auction analysis.

### Limitations

- Single-day bid trace window (2024-09-13); dynamics may vary by market regime.
- Bid trace and delivery data from different dates (~18 months apart).
- All metrics derived from aggregate statistics; exact per-slot distributions require GROUP BY queries.
- No bid value analysis or sub-second timing measurement.

### Follow-On Candidates (all held for curation)

1. Per-Slot Bid Distribution Analysis — GROUP BY on slot for exact distribution shape
2. Bid Timing Within Slots — sub-second timestamp analysis relative to slot boundaries
3. Same-Day Bid-to-Delivery Win Rate — join bid and delivery for same date

---

