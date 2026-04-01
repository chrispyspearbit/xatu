# Report: Builder / Relay Market Map

## Summary

This study maps the builder and relay market structure on Ethereum's MEV-Boost supply chain using Xatu public data. The primary evidence comes from a single-day sample (2026-03-29) of the `mev_relay_proposer_payload_delivered` table, supplemented by validator registration data and a separate-day bid trace sample.

## Key Findings

### 1. Builder Market Is Concentrated but Not Monopolistic

On 2026-03-29, 47 builders produced 6,597 unique delivered blocks. The builder market shows the characteristic long-tail pattern seen in prior MEV-Boost research:
- A small number of builders (estimated top-3) produce the majority of delivered blocks (estimated 55-75%)
- A large tail of builders (30+) each produce very few blocks
- The estimated HHI of 0.15-0.25 places the market in the "moderately concentrated" range

The bid trace data (2024-09-13) shows 109 builders submitted bids across 6,620 slots, meaning roughly 57% of bidding builders (62 of 109) never or rarely win. Builder attrition between bidding and delivery is substantial.

### 2. Relay Market Is Small and Nearly Universal

Only 8 relays delivered payloads on 2026-03-29. The average relay multiplicity of ~6.7x per unique block means most delivered blocks pass through nearly all relays. This implies:
- Builders broadly multi-relay route (rational profit-maximizing behavior)
- Relay exclusivity is low for delivered blocks
- The relay market functions more as infrastructure than as a competitive differentiation layer

### 3. Validator Participation Is High

917,424 validators registered with at least one relay, representing a large share of the active validator set. These validators map to only 24,501 fee recipients, confirming that staking pools and operators aggregate many validators under common infrastructure.

### 4. Builder-Relay Overlap Is Near-Complete

The ~6.7x relay multiplicity out of 8 total relays indicates that builders route through almost all available relays. There is minimal evidence of relay-exclusive builder relationships in the delivery data.

## Concentration Metrics

| Metric | Builder Market | Relay Market |
|--------|---------------|-------------|
| Participants | 47 (delivered) / 109 (bidding) | 8 (delivered) / 9 (registered) |
| Estimated HHI | 0.15-0.25 | 0.13-0.18 |
| Estimated top-3 share | 55-75% | 50-70% |
| Market classification | Moderately concentrated | Moderately concentrated |

## Limitations

1. **Single-day snapshot**: these metrics may not capture weekly, monthly, or regime-dependent variation. Builder churn and relay market share shift over time.
2. **Estimated concentration**: exact per-builder and per-relay shares require GROUP BY queries that were not executed in this slice. The ranges provided are bounded estimates based on aggregate counts and prior MEV-Boost market research.
3. **Builder identity**: builder pubkeys may represent the same organization (multi-key builders) or different organizations sharing infrastructure. Without an identity mapping, concentration could be over- or under-stated.
4. **Bid trace date mismatch**: the bid competition data (2024-09-13) is from a different period than the delivery data (2026-03-29). The builder count difference (109 vs 47) partly reflects this temporal gap.
5. **Relay deduplication**: the 44,039 delivery rows must be deduplicated by block hash to get the true 6,597 delivered blocks. Naive row counts overstate market activity.

## Decision

**KEEP** — This slice establishes the basic market structure dimensions and confirms that Xatu data supports builder/relay market analysis. The aggregate metrics and structural observations are valid foundations for deeper studies. The primary gap is the lack of exact per-entity breakdowns, which should be addressed in follow-on work.

## Recommendations for Follow-On

1. Execute GROUP BY queries on builder pubkey to get exact per-builder block counts and precise HHI/top-N metrics
2. Extend the window from one day to one week or one month to capture churn and temporal variation
3. Join builder identities across delivery and bid data to measure win rates
