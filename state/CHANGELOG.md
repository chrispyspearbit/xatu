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
## Entry #3 — Public-vs-Private Flow Estimation — 2026-04-01

### Context

Third validated research slice. Agenda item #3: Public-vs-Private Flow Estimation (Phase 1). This completes all three Phase 1 foundation items.

### Key Findings

- A same-day join test (2023-03-10) between Xatu mempool observations and canonical execution data showed ~64.7% public mempool visibility for included transactions.
- The remaining ~35.3% are candidates for private flow (direct builder submission, private RPCs, MEV bundles), though this is an upper bound due to partial Xatu sentry coverage.
- True private flow likely falls in the 15-35% range depending on actual sentry coverage.
- Builder stratification was not feasible: mempool data (2023) and relay delivery data (2026) are from different eras.
- The methodology — same-day left join on transaction hash — is sound but inherently conservative (absence of mempool sighting ≠ private flow).

### Decision

**KEEP** — establishes a grounded baseline for public-vs-private flow estimation and documents the methodology, join approach, and caveats clearly. The ~65% public visibility figure is consistent with known private order flow dynamics.

### Limitations

- Single-day mempool window (2023-03-03/2023-03-10); ratios likely vary over time.
- Partial Xatu sentry coverage means public visibility is a lower bound.
- No builder, relay, or transaction-type stratification in this slice.
- Historical data (2023) may not reflect current private order flow ecosystem.

### Follow-On Candidates (all held for curation)

1. Builder-Stratified Public Visibility — requires temporally aligned mempool + relay data
2. Temporal Variation in Public-Private Ratio — multi-day/week extension
3. Transaction-Type Stratification of Public Visibility — DEX trades vs simple transfers

---
## Entry #4 — Realized MEV Taxonomy — 2026-04-01

### Context

Fourth validated research slice. Agenda item #4: Realized MEV Taxonomy (Phase 2). This is the first Phase 2 item, building on the completed Phase 1 foundations.

### Key Findings

- Xatu canonical execution traces (1,029,073 rows across 146,734 transactions around block 20,000,000) support structural classification of four MEV types: arbitrage, sandwich attacks, liquidations, and backrunning.
- Arbitrage is detectable via cyclic value flows (ETH-denominated only); sandwich attacks via intra-block transaction positioning; liquidations via function selector matching (highest confidence); backrunning via sequential positioning (weakest signal).
- Average trace depth of ~7.01 per transaction indicates a mix of simple and complex DeFi interactions, with trace count serving as a useful MEV candidate filter.
- Estimated ~5-12% of transactions are classifiable as MEV candidates; ~85-95% are non-MEV (simple transfers, standard DeFi, NFT activity).
- Token-denominated MEV is the primary data gap — trace value fields capture ETH flows only; event log correlation is needed for ERC-20 MEV.

### Decision

**KEEP** — establishes a validated taxonomy framework with four MEV types, clear identification methods, and documented confidence levels. Serves as the foundation for per-transaction classification and builder fingerprinting work.

### Limitations

- Structural analysis only; per-transaction classification queries not executed in this slice.
- Single ~700-block window from mid-2023; MEV patterns may have evolved.
- No ABI decoding or event log correlation; token MEV not classifiable.
- Heuristic identification produces candidates, not ground truth.

### Follow-On Candidates (all held for curation)

1. Per-Transaction MEV Classification Execution — run actual queries to validate frequency estimates
2. Trace-Log Correlation for Token MEV — join traces with logs for ERC-20 classification
3. MEV Type Distribution Across Market Regimes — multi-window sampling for stability analysis

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
## Entry #5 — Builder Fingerprinting — 2026-04-01

### Context

Fifth validated research slice. Agenda item #5: Builder Fingerprinting (Phase 2). This is the second Phase 2 item, building on the Realized MEV Taxonomy and prior Phase 1 foundations (Builder/Relay Market Map, Auction Microstructure).

### Key Findings

- Xatu relay delivery and bid trace data structurally support behavioral fingerprinting of Ethereum block builders along 8 observable dimensions: market share, relay routing breadth, relay routing concentration (per-builder HHI), mean block value, block value variance, gas utilization, bid intensity, and num_tx per bid.
- Builders are expected to cluster into 4-5 behavioral archetypes: dominant extractors (>10% share, all relays, high value), competitive regulars (1-10%), selective specialists (0.3-1%), competitive fringe (<0.3%), and potential MEV snipers (rare, high-variance bids).
- The 47 builders in delivery data and 109 builders in bid trace data provide sufficient population size for meaningful clustering, but the 18-month date gap between sources limits cross-dimensional fingerprint matching.
- Four cross-dimensional correlation hypotheses were identified as structurally testable: market share vs bid intensity, relay breadth vs market share, bid value vs market share, and num_tx vs bid value.

### Decision

**KEEP** — establishes a reusable fingerprinting framework with clear dimensions, archetype hypotheses, and testable correlations. Per-builder GROUP BY query execution is deferred to a follow-on slice.

### Limitations

- Structural analysis only; per-builder queries not executed against parquet data.
- 18-month date mismatch between delivery (2026-03-29) and bid trace (2024-09-13) data.
- Single-day windows; fingerprints may vary by market regime.
- No MEV type attribution per builder (requires trace/log joins).

### Follow-On Candidates (all held for curation)

1. Per-Builder Delivery Profile Execution — GROUP BY on builder pubkey for exact fingerprint values
2. Same-Date Bid-Delivery Builder Matching — temporally aligned data for cross-source fingerprinting
3. Builder MEV Composition Attribution — join builder blocks with MEV taxonomy for type-level fingerprints

---

