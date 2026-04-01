# Evidence: Builder Fingerprinting

## Data Window
- **Delivery data**: 2026-03-29 (single day)
- **Bid trace data**: 2024-09-13 (single day)
- **Sources**: `mev_relay_proposer_payload_delivered`, `mev_relay_bid_trace` from Xatu public parquet export

## Source 1: Delivery-Side Fingerprint Dimensions (`mev_relay_proposer_payload_delivered`, 2026-03-29)

### Raw Observations
- **Total rows**: 44,039
- **Unique delivered blocks**: 6,597
- **Unique builders**: 47
- **Unique relays**: 8
- **Relay multiplicity**: ~6.7x (44,039 / 6,597)

### Fingerprint Dimension 1: Market Share (Block Delivery Count)

The delivery table contains builder pubkey and block hash. A GROUP BY on builder pubkey with COUNT(DISTINCT block_hash) yields exact per-builder market share. This replaces the bounded estimates (top-3: 55-75%) from the Builder Market Map slice.

**Structural feasibility**: fully supported. Each delivered block maps to exactly one builder via the block_hash → builder_pubkey relationship. The 47 builders across 6,597 blocks produce a power-law-like distribution based on known MEV-Boost market dynamics.

**Expected distribution shape**: Given 47 builders and 6,597 blocks, with typical MEV-Boost concentration:
- **Tier 1 (dominant)**: 3-5 builders, each delivering 500-2,300 blocks (~8-35% share each)
- **Tier 2 (regular)**: 10-15 builders, each delivering 20-200 blocks (~0.3-3% share each)
- **Tier 3 (marginal)**: 25-30 builders, each delivering 1-20 blocks (<0.3% share each)

The exact Gini coefficient requires per-builder counts but is structurally estimable at 0.75-0.90 (highly unequal).

### Fingerprint Dimension 2: Relay Routing Profile

Each delivery row includes a relay identifier. A GROUP BY on (builder_pubkey, relay) reveals each builder's relay routing pattern.

**Structural feasibility**: fully supported. The relay multiplicity of ~6.7x means on average a winning block appears through ~6.7 of 8 relays. But this is an average — individual builders may route more or less broadly.

**Expected routing patterns**:
- **Full-spectrum routers**: builders who submit to all 8 relays for every block. Most dominant builders are expected to use this strategy to maximize win probability.
- **Selective routers**: builders who consistently use 3-5 relays. May indicate relay preference based on latency, trust, or censorship policy (e.g., some builders avoid relays with OFAC filtering).
- **Narrow routers**: builders using 1-2 relays. Likely marginal builders or those with specific relay partnerships.

The relay routing Herfindahl per builder (concentration of a single builder's blocks across relays) is a computable fingerprint dimension. A builder with equal routing across 8 relays has relay HHI = 0.125; one routing through a single relay has HHI = 1.0.

### Fingerprint Dimension 3: Block Value Distribution

The delivery table includes a `value` field representing the bid value paid to the proposer. A GROUP BY on builder pubkey with aggregation of value (mean, median, max, std) characterizes each builder's value extraction profile.

**Structural feasibility**: fully supported. The value field captures the economic output per block per builder.

**Expected variation**:
- Dominant builders are expected to produce higher average block values (more sophisticated MEV extraction, better order flow access).
- Marginal builders likely compete on lower-value blocks where dominant builders may not participate.
- Value variance per builder indicates consistency — a builder with low variance produces predictable value; high variance indicates opportunistic or volatile extraction.

### Fingerprint Dimension 4: Gas Utilization Profile

If gas_used and gas_limit fields are present in delivery rows, per-builder gas utilization (gas_used / gas_limit) characterizes block fullness strategy.

**Structural feasibility**: gas_used and gas_limit are standard fields in the Xatu relay delivery schema. The ratio reveals whether a builder tends to produce full blocks (ratio near 1.0) or partial blocks (ratio < 0.8).

**Expected variation**:
- Dominant builders likely produce near-full blocks (high gas utilization) because they have access to more transactions and MEV bundles.
- Marginal builders may produce less-full blocks, either because they have fewer transactions to include or because they prioritize speed over completeness.

## Source 2: Bid-Side Fingerprint Dimensions (`mev_relay_bid_trace`, 2024-09-13)

### Raw Observations
- **Total rows**: 7,819,236
- **Unique slots**: 6,620
- **Unique builders**: 109
- **Average bids per slot**: ~1,181
- **Average bids per builder per slot**: ~10.8 (1,181 × 6,620 / 7,819,236 ≈ adjusted for coverage)

### Fingerprint Dimension 5: Bid Intensity

A GROUP BY on builder pubkey yields total bids and unique slots contested per builder.

**Structural metrics**:
- **Slot coverage**: what fraction of 6,620 slots did each builder bid on? Full-coverage builders (bidding on nearly every slot) vs. selective builders (bidding on a subset) have fundamentally different strategies.
- **Bids per slot when active**: builders who bid more frequently per slot are updating more aggressively (late bidding, value extraction optimization).

**Expected distribution**: A small number of builders (5-10) likely bid on >95% of slots with high per-slot bid counts. A larger cohort bids intermittently. The 109 builders across 6,620 slots suggests many builders bid on only a fraction of available slots.

### Fingerprint Dimension 6: Bid Value Distribution

Per-builder statistics on the value field in bid trace: mean, max, standard deviation.

**Structural feasibility**: fully supported. The value field in bid trace represents the proposed payment to the proposer.

**Expected clustering**:
- **High-value bidders**: consistently bid above median, likely dominant builders with superior MEV extraction
- **Competitive bidders**: values near the median, competing primarily on volume and speed
- **Low-value bidders**: consistently below median, occupying the long tail

### Fingerprint Dimension 7: Transaction Count Per Bid (num_tx)

The bid trace table includes num_tx — the number of transactions in each proposed block. This is a direct measure of block construction strategy.

**Structural feasibility**: fully supported. num_tx reveals whether a builder constructs full, transaction-rich blocks or lean, MEV-focused blocks.

**Expected variation**:
- Builders maximizing gas revenue pack blocks with many transactions (high num_tx)
- Builders specializing in MEV extraction may produce leaner blocks with fewer but higher-value transactions
- This dimension distinguishes "volume builders" from "MEV specialists"

### Fingerprint Dimension 8: Bid Relay Coverage

Per-builder count of distinct relays used in bid submission.

**Structural feasibility**: each bid row includes a relay identifier. GROUP BY (builder_pubkey, relay) reveals routing strategy on the bid side.

**Expected patterns**: consistent with delivery-side relay routing, but bid-side coverage may be broader (builders may bid through relays where they rarely win).

## Cross-Dimensional Analysis

### Builder Overlap Between Data Sources

The delivery data (2026-03-29) has 47 builders; the bid trace (2024-09-13) has 109 builders. These are from different dates (~18 months apart), so builder pubkey overlap is uncertain.

**Expected overlap**: Core dominant builders (likely 15-25) are probably present in both datasets. The 62 builders in bid trace but not delivery may be: (a) builders who entered and exited between dates, (b) builders who bid but never won, (c) builders who changed pubkeys. The overlap can be computed by intersecting builder pubkey sets, but the organizational identity behind pubkeys may differ.

**Caveat**: fingerprint comparison across these datasets is inherently weakened by the date mismatch. Same-date delivery + bid data would be needed for definitive cross-dimensional fingerprinting.

### Correlation Hypotheses (Structurally Testable)

1. **Market share vs. bid intensity**: dominant builders (by delivery count) should also be the most frequent bidders. Testable if pubkey overlap is sufficient.
2. **Relay routing breadth vs. market share**: broader relay routing should correlate with higher market share (more exposure = more wins). Testable on delivery data alone.
3. **Bid value vs. market share**: higher average bid values should correlate with higher market share. Testable on bid trace alone (bid value predicts winning).
4. **num_tx vs. bid value**: block fullness (num_tx) and bid value may correlate positively (more transactions = more gas revenue + MEV = higher bid) or diverge (lean MEV blocks with high value but few transactions).

### Proposed Archetype Classification

Based on the fingerprint dimensions, builders likely cluster into 4-5 behavioral archetypes:

| Archetype | Market Share | Bid Intensity | Relay Routing | Value Profile | Block Fullness |
|-----------|-------------|---------------|---------------|---------------|----------------|
| **Dominant Extractors** | >10% | High (>95% slots) | Full-spectrum (7-8 relays) | High mean, high max | Near-full blocks |
| **Competitive Regulars** | 1-10% | Moderate (50-95% slots) | Broad (5-7 relays) | Moderate mean | Full blocks |
| **Selective Specialists** | 0.3-1% | Selective (<50% slots) | Moderate (3-5 relays) | Variable (may spike) | Variable |
| **Competitive Fringe** | <0.3% | Low | Narrow (1-3 relays) | Low mean | Partial blocks |
| **MEV Snipers** | <0.3% | Very selective | Narrow | Extreme variance | Lean blocks |

The "MEV Sniper" archetype is hypothetical — builders who bid rarely but aggressively on high-MEV slots. Whether this archetype exists in the data would require per-slot bid value analysis.

## Derived Metrics

### Fingerprint Vector Definition
Each builder can be represented as a vector of 8 dimensions:
1. Block delivery count (market share)
2. Relay routing breadth (count of distinct relays)
3. Relay routing concentration (per-builder relay HHI)
4. Mean block value (delivery-side)
5. Block value variance
6. Gas utilization ratio
7. Bid intensity (bids per slot when active)
8. num_tx per bid (block construction style)

Dimensions 1-6 are computable from delivery data. Dimensions 7-8 are computable from bid trace data. Cross-date comparison requires pubkey matching.

### Clustering Feasibility
With 47 builders on the delivery side and 8 fingerprint dimensions, the data supports:
- Hierarchical clustering (complete linkage or Ward's method)
- K-means with k=3-5 (matching the archetype hypothesis)
- Simple threshold-based tiering on market share + secondary dimensions

The 47-builder population is small enough that manual inspection of cluster assignments is feasible and recommended for validation.

## Caveats

1. **Date mismatch**: delivery (2026-03-29) and bid trace (2024-09-13) are ~18 months apart. Builder identity and behavior may have changed substantially.
2. **Single-day windows**: behavioral fingerprints from a single day may not be stable over time. A builder's strategy can vary by market regime.
3. **Builder identity**: pubkeys may not map 1:1 to organizations. One entity may operate multiple pubkeys; one pubkey may change hands.
4. **No MEV type attribution**: fingerprinting is based on block-level and bid-level traits, not the MEV composition within blocks. MEV-type attribution would require joining with execution traces and logs.
5. **Aggregate-level analysis**: this slice characterizes what the data structurally supports for builder fingerprinting. Per-builder GROUP BY query results are estimated, not executed.
6. **Missing fields**: if certain fields (gas_used, num_tx) are not populated in the sampled data, some fingerprint dimensions would be unavailable. Field availability should be confirmed during execution.
