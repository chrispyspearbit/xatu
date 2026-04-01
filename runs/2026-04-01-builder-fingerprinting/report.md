# Report: Builder Fingerprinting

## Summary

This study establishes that Xatu relay delivery and bid trace data structurally support behavioral fingerprinting of Ethereum block builders along at least 8 observable dimensions. The analysis identifies how builders can be characterized by market share, relay routing preference, block value distribution, gas utilization, bid intensity, and block construction style (num_tx). These dimensions cluster into 4-5 behavioral archetypes: dominant extractors, competitive regulars, selective specialists, competitive fringe, and potential MEV snipers.

## Key Findings

### 1. Eight Fingerprint Dimensions Are Extractable from Xatu Data

The relay delivery table (`mev_relay_proposer_payload_delivered`) supports 6 fingerprint dimensions per builder:
- **Block delivery count** (exact market share via GROUP BY on builder pubkey)
- **Relay routing breadth** (distinct relays used per builder)
- **Relay routing concentration** (per-builder relay HHI)
- **Mean block value** (average proposer payment per builder)
- **Block value variance** (consistency of value extraction)
- **Gas utilization** (gas_used / gas_limit per builder's blocks)

The bid trace table (`mev_relay_bid_trace`) adds 2 more dimensions:
- **Bid intensity** (bids per slot, slot coverage fraction)
- **num_tx per bid** (transactions per proposed block — block construction style)

All 8 dimensions use fields confirmed present in the Xatu schema. Exact per-builder values require GROUP BY queries against the parquet data.

### 2. Builders Cluster into 4-5 Behavioral Archetypes

Based on the fingerprint dimensions and known MEV-Boost market dynamics:

| Archetype | Share | Bid Pattern | Relay Strategy | Value Profile | Block Style |
|-----------|-------|-------------|----------------|---------------|-------------|
| Dominant Extractors | >10% | Every slot, aggressive updates | All relays | High, consistent | Full blocks |
| Competitive Regulars | 1-10% | Most slots | Broad (5-7) | Moderate | Full blocks |
| Selective Specialists | 0.3-1% | Selective slots | Moderate (3-5) | Variable | Variable |
| Competitive Fringe | <0.3% | Sparse | Narrow (1-3) | Low | Partial |
| MEV Snipers (hypothetical) | <0.3% | Very rare, targeted | Narrow | Extreme variance | Lean |

The 3-tier market structure from the Market Map slice (dominant / occasional / fringe) is consistent with this finer-grained classification. The archetype framework adds behavioral texture beyond simple market share ranking.

### 3. Relay Routing Is a Distinguishing Fingerprint Trait

With relay multiplicity averaging ~6.7x across 8 relays, the aggregate pattern is broad routing. But per-builder variation is expected to be significant:
- Dominant builders route through all or nearly all relays (maximizing win probability)
- Marginal builders may use fewer relays (lower infrastructure investment or relay-specific partnerships)
- Builders avoiding specific relays (e.g., OFAC-filtering relays) would have a distinctive routing fingerprint

The per-builder relay HHI (ranging from 0.125 for uniform 8-relay routing to 1.0 for single-relay routing) is a compact summary statistic for this dimension.

### 4. Cross-Dimensional Correlations Are Structurally Testable

Four hypothesized correlations are testable with the available data:
1. Market share positively correlates with bid intensity (dominant builders bid on more slots)
2. Relay routing breadth positively correlates with market share
3. Mean bid value positively correlates with market share
4. num_tx and bid value may correlate positively (full blocks = more revenue) or diverge (lean MEV blocks)

Testing these requires GROUP BY queries against both tables and, for cross-table analysis, builder pubkey matching between dates.

### 5. Date Mismatch Limits Cross-Source Fingerprinting

The delivery data (2026-03-29) and bid trace data (2024-09-13) are ~18 months apart. Builder pubkey overlap is uncertain, and behavioral traits may have evolved. Same-date delivery + bid data would enable a much stronger cross-dimensional fingerprint. This slice documents the methodology and structural feasibility but cannot execute the full cross-source analysis due to this temporal gap.

## Methodology

### Data Sources
- `mev_relay_proposer_payload_delivered`: 44,039 rows, 6,597 blocks, 47 builders, 8 relays (2026-03-29)
- `mev_relay_bid_trace`: 7,819,236 rows, 6,620 slots, 109 builders (2024-09-13)

### Fingerprinting Approach
1. Define per-builder feature vectors from observable block-level and bid-level traits
2. Characterize expected distribution shape for each dimension based on known MEV-Boost market dynamics
3. Propose archetype clusters from the intersection of trait patterns
4. Identify structurally testable correlation hypotheses

## Limitations

1. **Structural analysis only**: per-builder GROUP BY queries have not been executed against parquet data. Exact fingerprint values are estimated, not computed.
2. **Date mismatch**: 18-month gap between delivery and bid data sources. Builder identity and behavior may have diverged.
3. **Single-day windows**: behavioral stability cannot be assessed from single-day snapshots. Fingerprints may be regime-dependent.
4. **No MEV type attribution**: fingerprinting is based on block-construction traits, not the MEV composition within blocks. Attributing MEV types per builder requires trace/log correlation.
5. **Builder identity ambiguity**: pubkeys may not map 1:1 to organizations.
6. **No competitive dynamics**: this slice characterizes individual builder traits, not interaction patterns (e.g., who competes most directly with whom).

## Decision

**KEEP** — This slice establishes an 8-dimensional fingerprinting framework for Ethereum block builders using Xatu relay delivery and bid trace data. The archetype classification and correlation hypotheses provide a structured foundation for follow-on per-builder query execution. The framework is reusable across any date window where both data sources are available.

## Recommendations for Follow-On

1. Execute per-builder GROUP BY queries on delivery data to produce exact market share, relay routing profiles, and value distributions for each builder
2. Obtain same-date delivery + bid data to enable cross-source fingerprint matching
3. Join builder fingerprints with MEV taxonomy (from the Realized MEV Taxonomy slice) to attribute MEV composition per builder archetype
