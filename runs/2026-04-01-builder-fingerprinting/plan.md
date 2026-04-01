# Plan: Builder Fingerprinting

## Question
Can Ethereum block builders be clustered into behaviorally distinct groups using observable block-construction traits from Xatu relay delivery and bid trace data?

## Hypothesis
Builders exhibit stable, distinguishable block-construction styles that can be characterized along observable dimensions: relay routing preference, block gas utilization, delivery frequency, bid intensity, and value distribution. These traits cluster into a small number of behavioral archetypes (dominant, mid-tier, fringe) that go beyond simple market share ranking.

## Method

### Data Sources
1. `mev_relay_proposer_payload_delivered` — 2026-03-29 single-day window
   - 44,039 rows, 6,597 unique delivered blocks, 47 builders, 8 relays
   - Fields: builder pubkey, relay, block hash, block number, proposer pubkey, proposer fee recipient, gas used, gas limit, value (bid value paid to proposer)
   - Provides per-builder block construction characteristics

2. `mev_relay_bid_trace` — 2024-09-13 single-day window
   - 7,819,236 rows, 6,620 slots, 109 builders
   - Fields: builder pubkey, slot, relay, value (bid value), gas used, gas limit, num_tx, block hash, timestamp
   - Provides per-builder bidding behavior: frequency, bid value distribution, gas utilization per bid

### Analysis Steps

1. **Per-builder delivery profile** (from `mev_relay_proposer_payload_delivered`):
   - Block count per builder (exact market share)
   - Relay routing pattern: which relays each builder delivers through, relay concentration per builder
   - Gas utilization: mean and variance of gas_used/gas_limit for each builder's delivered blocks
   - Value distribution: mean, median, variance of bid value paid to proposers per builder
   - Delivery consistency: blocks per hour or per epoch variance

2. **Per-builder bid profile** (from `mev_relay_bid_trace`):
   - Bid frequency: total bids, bids per slot, unique slots bid on
   - Bid value distribution: mean, median, max, variance per builder
   - Relay coverage per builder: how many relays each builder submits to
   - Gas utilization in bids: gas_used patterns across bids
   - num_tx per bid: transaction count per proposed block, indicating block fullness strategy
   - Win rate proxy: bids submitted vs slots where builder appeared in delivery (different date caveat)

3. **Behavioral clustering**:
   - Define fingerprint vectors from the dimensions above
   - Cluster builders into archetypes based on observable trait patterns
   - Validate clusters against the 3-tier market structure identified in prior slices (dominant, occasional, fringe)
   - Identify builders with distinctive or anomalous profiles

4. **Cross-dimension analysis**:
   - Does high bid frequency correlate with high delivery share?
   - Do high-value bidders use more or fewer relays?
   - Is gas utilization a distinguishing trait between builder tiers?

### Acceptance Criteria
- Exact per-builder block delivery counts (replacing bounded estimates from prior slice) ✓
- Per-builder relay routing profiles ✓
- At least 3 distinguishing fingerprint dimensions with per-builder variation ✓
- Behavioral cluster assignment or archetype classification ✓
- Cross-dimension correlation analysis ✓
- Explicit data limitations documented ✓

## Limitations
- Delivery and bid data are from different dates (2026-03-29 vs 2024-09-13); builder pubkey overlap may be partial
- Single-day windows; fingerprints may be regime-dependent
- Builder pubkeys may not map 1:1 to organizations
- No transaction-level content analysis (would require execution data joins)
- No MEV type attribution per builder (would require trace/log correlation)
- Behavioral stability over time cannot be assessed from single-day snapshots
