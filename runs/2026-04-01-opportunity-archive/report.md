# Report: Opportunity Archive

## Summary

This study consolidates all validated Phase 1 and Phase 2 research into a structured historical opportunity library. Six MEV-related opportunity classes were distilled from six prior research slices, each tagged with detection method, public observability, competitive intensity, data support level, and key limitations. The archive provides the structured input for strategy feasibility assessment (agenda item #8).

## Key Findings

### 1. Six Opportunity Classes Identified

The completed research program supports archiving six distinct opportunity classes:

| # | Class | Type | Detection Confidence | Archivable |
|---|-------|------|---------------------|------------|
| 1 | ETH-Denominated Arbitrage | Extraction | Medium | Yes |
| 2 | Sandwich Attacks | Extraction | Medium | Yes |
| 3 | Liquidation MEV | Extraction | High | Yes |
| 4 | Backrunning | Extraction | Low | Conditional |
| 5 | Builder Market Position | Structural | Medium | Yes |
| 6 | Validator Dependency Risk | Systemic | Medium | Yes |

Four classes are per-transaction MEV types from the realized taxonomy (Run 4). Two are structural/systemic classes derived from market map, fingerprinting, and dependency analysis (Runs 1, 5, 6).

### 2. Public Observability Creates a Natural Hierarchy

The ~65% public mempool visibility baseline (Run 3) creates an observability gradient across opportunity classes:

- **Most observable**: Liquidation targets (on-chain health factors are public), validator dependency (registration data is public)
- **Partially observable**: Backrun targets (the target tx is often public), builder market position (delivery data is public)
- **Least observable**: Sandwich attack legs (frontrun/backrun submitted via private bundles), sophisticated arbitrage (likely private submission)

This gradient is the most important structural finding for strategy feasibility: opportunity classes that depend on private order flow observation are fundamentally limited by the ~35% private flow ceiling.

### 3. Competition Intensity Is Extreme and Tiered

From auction microstructure (Run 2): ~1,181 bids per slot with a three-tier builder hierarchy. This means:
- ETH arbitrage and sandwich attacks are dominated by Tier 1 builders (3-5 dominant, >10% share each)
- Liquidations during market stress attract intense but bursty competition
- Backrunning is the most accessible MEV type but also the least reliably detectable
- Builder market position analysis is non-competitive (research/analytics, not execution)

### 4. Data Completeness Varies Significantly Across Classes

| Class | Completeness | Primary Gap |
|-------|-------------|-------------|
| ETH Arbitrage | Partial | Token flows require log correlation |
| Sandwich | Partial | Trade direction requires ABI decode |
| Liquidation | High (detection) / Low (sizing) | Economic parameters require ABI decode |
| Backrunning | Low | Intent confirmation ambiguous |
| Builder Market Position | High | Exact GROUP BY values deferred |
| Validator Dependency | High | Per-entity distribution deferred |

The structural classes (5, 6) have the strongest data support. The per-transaction MEV classes (1-4) all share a common gap: token-denominated MEV is invisible without event log correlation.

### 5. Temporal Stability Is Universally Unknown

Every opportunity class estimate derives from single-day windows. Whether the frequency, intensity, or competitive landscape is stable across market regimes is a critical unanswered question that affects all downstream feasibility analysis.

## Methodology

### Synthesis Approach
This slice did not query new parquet data. It systematically extracted findings from all six completed runs, organized them into a structured class library, and cross-referenced attributes that span multiple runs (observability from Run 3, competition from Run 2, detection from Run 4, market structure from Runs 1/5/6).

### Data Sources (Inherited)
- `mev_relay_proposer_payload_delivered` (2026-03-29): 44,039 rows, 6,597 blocks, 47 builders
- `mev_relay_validator_registration` (2026-03-29): 5,829,223 rows, 917,424 validators
- `mev_relay_bid_trace` (2024-09-13): 7,819,236 rows, 6,620 slots, 109 builders
- `mempool_transaction` (2023-03-03): 1,094,776 rows, 747,931 unique transactions
- `canonical_execution_traces` (2023-07-01): 1,029,073 rows, 146,734 transactions
- `canonical_execution_transaction` (2023-07-01, 2023-03-10): cross-referenced for joins

Total inherited row count: ~15.8M rows across 6 tables and 4 distinct date windows.

## Limitations

1. **Synthesis only**: no new empirical observations; all limitations from individual runs carry forward.
2. **Temporal heterogeneity**: data spans 2023-2026 across different tables. The composite archive is not a point-in-time snapshot.
3. **Structural estimates**: frequency figures are bounded, not ground-truth classification counts.
4. **Token MEV gap**: the most economically significant MEV (ERC-20 arb/sandwich) is not observable.
5. **Single-day windows**: no temporal stability assessment possible from current data.
6. **No feasibility evaluation**: this archive catalogs classes but does not assess execution viability.

## Decision

**KEEP** — The archive provides a structured, evidence-grounded library of six opportunity classes with explicit attributes for detection, observability, competition, and data support. It is the necessary input for strategy feasibility assessment (agenda item #8) and cross-chain portability analysis (agenda item #9). The observability gradient and competition hierarchy are the most actionable structural findings.

## Recommendations for Follow-On

1. Strategy Feasibility Layer (agenda item #8): assess which archived classes are recurring, public enough, and not dead on arrival, using the observability and competition attributes as filters.
2. Per-Transaction MEV Classification Execution: produce ground-truth counts to replace the structural frequency estimates in the archive.
3. Token MEV Extension: correlate traces with logs to expand the archive to cover ERC-20 denominated MEV classes.
