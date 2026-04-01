# Plan: Opportunity Archive

## Question
What MEV opportunity classes can be distilled from the validated Phase 1-2 research into a structured historical library, and which classes have sufficient data support, public observability, and recurrence evidence to be meaningful for future work?

## Hypothesis
The six completed research slices (builder/relay market map, auction microstructure, public-vs-private flow, realized MEV taxonomy, builder fingerprinting, validator/proposer dependency) collectively identify a bounded set of MEV opportunity classes that differ meaningfully along dimensions of detectability, public observability, competitive intensity, and data support. A structured archive of these classes — with explicit grounding in prior evidence — provides the input for strategy feasibility assessment.

## Method

### Data Sources
This is a synthesis slice. It does not query new parquet data. Instead it consolidates validated findings from all six prior runs:

1. `runs/2026-04-01-builder-relay-market-map/` — market structure, concentration
2. `runs/2026-04-01-auction-microstructure/` — bid competition, builder tiers
3. `runs/2026-04-01-public-private-flow/` — public/private flow split
4. `runs/2026-04-01-realized-mev-taxonomy/` — 4 MEV types, identification methods
5. `runs/2026-04-01-builder-fingerprinting/` — builder archetypes, behavioral dimensions
6. `runs/2026-04-01-validator-proposer-dependency/` — dependency structure, concentration risk

The underlying Xatu tables referenced across these runs:
- `mev_relay_proposer_payload_delivered` (2026-03-29)
- `mev_relay_validator_registration` (2026-03-29)
- `mev_relay_bid_trace` (2024-09-13)
- `mempool_transaction` (2023-03-03)
- `canonical_execution_traces` (2023-07-01)
- `canonical_execution_transaction` (2023-07-01, 2023-03-10)

### Analysis Steps

1. **Extract opportunity classes**: From the MEV taxonomy (run 4), distill each classified MEV type into a discrete opportunity class entry.

2. **Tag each class with structural attributes**:
   - Detection method and confidence (from taxonomy evidence)
   - Public observability (from public-vs-private flow evidence: ~65% public)
   - Competitive intensity (from auction microstructure: ~1181 bids/slot, builder tiers)
   - Builder competition context (from fingerprinting: archetype distribution)
   - Data support level (which Xatu tables, what join coverage)
   - Frequency estimate (from taxonomy structural estimates)

3. **Identify cross-cutting opportunity dimensions**:
   - Market structure exposure (from market map: top-3 builder dominance)
   - Dependency risk (from validator/proposer dependency: asymmetric relay vs builder risk)
   - Temporal stability (documented as unknown — single-day windows throughout)

4. **Assess archivability**: For each class, determine whether the evidence is sufficient to create a durable library entry or whether it requires further validation.

### Acceptance Criteria
- At least 4 distinct opportunity classes archived with structured metadata ✓
- Each class cites specific evidence from prior runs ✓
- Public observability and competitive intensity tagged per class ✓
- Data support level explicitly documented per class ✓
- Gaps and limitations documented per class ✓

## Limitations
- All underlying data comes from single-day windows at different dates (2023-2026)
- No per-transaction classification was executed in the taxonomy slice; frequency estimates are structural
- Public-private flow ratio is from 2023; current ratio may differ significantly
- Builder fingerprinting used bounded estimates, not exact per-builder GROUP BY results
- No token-denominated MEV observability — only ETH-denominated flows in traces
- This is a consolidation slice; it introduces no new empirical observations
