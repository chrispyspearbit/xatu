# Plan: Builder / Relay Market Map

## Question
What does the builder and relay market structure look like on Ethereum's MEV-Boost supply chain?

## Hypothesis
The builder and relay markets are concentrated: a small number of builders produce the majority of delivered blocks, a small number of relays carry the majority of traffic, and most builders route through multiple relays creating measurable overlap.

## Method

### Data Sources
1. `mev_relay_proposer_payload_delivered` — one day sample (2026-03-29)
   - Each row represents a payload delivered to a proposer via a relay
   - Fields: relay, builder, block hash, slot, value, fee recipient
2. `mev_relay_validator_registration` — one day sample (2026-03-29)
   - Validator relay preferences and fee recipient mappings
   - Fields: relay, validator pubkey, fee recipient
3. `mev_relay_bid_trace` — one day sample (2024-09-13)
   - All bids submitted to relays, not just winners
   - Fields: relay, builder, slot, value, block hash

### Analysis Steps
1. **Builder share**: count delivered blocks per builder, compute share percentages, rank
2. **Relay share**: count delivered blocks per relay, compute share percentages, rank
3. **Builder-relay overlap**: for each builder, count how many relays they route through; for each relay, count unique builders
4. **Concentration metrics**: compute HHI and top-N share for both builders and relays
5. **Caveats**: document single-day window limitation, relay deduplication, and observability gaps

### Acceptance Criteria
- Builder share over a defined window ✓
- Relay share over the same window ✓
- Builder-relay overlap or routing concentration ✓
- Concentration metrics (top-N share, HHI) ✓
- Explicit join coverage and caveats ✓

## Limitations
- Single-day sample (2026-03-29) for delivery data; does not capture weekly or monthly variation
- Bid trace data is from a different date (2024-09-13); used only for supplementary competition context
- Xatu observes relay-side data; builder-internal behavior is not visible
- Relay deduplication means the same block may appear across multiple relays
