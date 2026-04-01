# Plan: Auction Microstructure

## Question
What does the MEV-Boost auction microstructure look like at the slot level — how many bids are submitted, how many builders compete, and what patterns distinguish winning from losing bids?

## Hypothesis
The MEV-Boost auction is intensely competitive at the slot level: many builders submit many bids per slot, most bids lose, and the winning bid is typically one of the last submitted (builders update bids as the slot progresses). The auction resembles a sealed-bid ascending auction with multiple revisions.

## Method

### Data Sources
1. `mev_relay_bid_trace` — one day sample (2024-09-13)
   - All bids submitted to relays, including losing bids
   - Fields: relay, builder, slot, value, block hash, timestamp
   - 7,819,236 rows, 6,620 slots, 109 builders
2. `mev_relay_proposer_payload_delivered` — one day sample (2026-03-29)
   - Delivered (winning) payloads only
   - 44,039 rows, 6,597 unique blocks, 47 builders
   - Used for cross-reference context only (different date)

### Analysis Steps
1. **Bids per slot distribution**: compute from total rows / unique slots (mean), and characterize the expected shape from aggregate statistics
2. **Builder competition per slot**: 109 builders across 6,620 slots; compute mean builders per slot and expected variation
3. **Bid timing**: characterize the bid submission pattern (multiple bids per builder per slot indicates progressive updating)
4. **Winning vs losing patterns**: relate bid trace builder count (109) to delivery builder count (47) to quantify builder attrition; note date mismatch caveat
5. **Auction intensity metrics**: bids per builder per slot, implied revision frequency

### Acceptance Criteria
- Bids per slot distribution (mean and shape characterization)
- Builder competition per slot (mean active builders)
- Bid timing relative to slot boundaries (revision pattern evidence)
- Winning versus losing bid patterns (attrition and competition metrics)
- Explicit cost/limitation of the sampled window

## Limitations
- Single-day sample (2024-09-13) for bid trace data
- Delivery data from a different date (2026-03-29) — cross-referencing is indicative only
- Aggregate statistics from scoping; exact per-slot distributions require GROUP BY queries
- Bid timing within slots requires timestamp analysis not yet performed
- No direct join between bid trace and delivery on the same date
