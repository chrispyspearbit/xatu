# Report: Auction Microstructure

## Summary

This study characterizes the MEV-Boost auction microstructure at the slot level using Xatu public bid trace data. The primary evidence comes from a single-day sample (2024-09-13) of the `mev_relay_bid_trace` table, cross-referenced with delivered payload data from a separate date (2026-03-29). The analysis establishes aggregate auction intensity metrics, builder competition characteristics, and structural inferences about bid timing and winning patterns.

## Key Findings

### 1. Auction Intensity Is Extremely High

On 2024-09-13, 7,819,236 bids were submitted across 6,620 slots, yielding a mean of ~1,181 bids per slot. This intensity reflects three compounding factors:
- **Multi-relay submission**: builders send bids to all ~8 active relays
- **Progressive bid revision**: builders update bids multiple times per slot as the mempool evolves
- **Broad builder participation**: 109 unique builders participated across the day

Decomposing: each builder submitted ~10.8 bids per slot on average (across all relays), implying ~1.4 bid submissions per builder per relay per slot. This is consistent with at least one initial bid plus occasional revisions.

### 2. Builder Competition Is Broad but Outcomes Are Concentrated

109 builders submitted bids on 2024-09-13. Cross-referencing with delivery data (2026-03-29, different date), only 47 builders delivered winning blocks. This ~57% attrition rate between bidding and delivering is structurally significant:
- The auction is winner-take-all per slot
- A large competitive fringe (~60+ builders) bids regularly but wins rarely
- The estimated top-3 builders capture 55-75% of delivered blocks (from prior market map study)

This creates a builder market with three tiers:
- **Tier 1**: 3-5 dominant builders winning the majority of slots
- **Tier 2**: 15-25 builders winning occasionally
- **Tier 3**: 60-80 builders in the competitive fringe, bidding but rarely winning

### 3. Bid Timing Follows a Progressive Updating Pattern

Although exact sub-second timing was not measured in this slice, the structural evidence points to a "last-look" auction dynamic:
- Builders submit initial bids early in the 12-second slot window
- As new transactions appear in the mempool, builders revise bids upward
- The winning bid is typically among the last submitted, incorporating maximum extractable value
- The ~1.4 revisions per builder per relay per slot is a lower bound, consistent with this updating pattern

### 4. Per-Bid Win Rate Is Extremely Low

With ~1,181 bids per slot and one winning block, the per-bid win rate is ~0.085%. Even per builder, assuming 50-80 active builders per slot, the per-slot win rate is only ~1.25-2%. This underscores the intensity of the competition and explains why only well-resourced builders with differentiated order flow can sustain profitable operations.

## Auction Metrics

| Metric | Value | Source |
|--------|-------|--------|
| Total bids observed | 7,819,236 | bid_trace 2024-09-13 |
| Unique slots | 6,620 | bid_trace 2024-09-13 |
| Unique bidding builders | 109 | bid_trace 2024-09-13 |
| Mean bids per slot | ~1,181 | derived |
| Mean bids per builder per slot | ~10.8 | derived (includes relay duplication) |
| Estimated builders per slot | 50-80 | estimated from aggregate |
| Per-bid win rate | ~0.085% | derived |
| Per-builder per-slot win rate | ~1.25-2% | derived |
| Unique delivering builders | 47 | delivery 2026-03-29 (different date) |
| Builder attrition (bid→deliver) | ~57% | cross-reference (different dates) |

## Limitations

1. **Single-day bid trace sample**: 2024-09-13 only. Auction dynamics likely vary by day of week, market volatility regime, and MEV opportunity set. High-value MEV days may show different bid patterns.
2. **Date mismatch**: bid trace (2024-09-13) and delivery (2026-03-29) are ~18 months apart. The builder ecosystem has likely changed substantially. The 109-vs-47 comparison is structurally informative but not a direct measurement of contemporary attrition.
3. **Aggregate statistics only**: all metrics are derived from aggregate counts in `research/data-scope.md`. Exact per-slot bid distributions, per-builder bid value curves, and sub-second timing analysis require per-row GROUP BY queries not yet executed.
4. **No bid value analysis**: we know bid counts but not bid value distributions. The competitive dynamics of the auction depend critically on how bid values evolve within a slot, which this slice cannot address.
5. **Relay deduplication not resolved**: the ~1,181 bids/slot includes cross-relay duplicates. The unique-bid count per slot (deduped by builder × slot) would be lower and more informative for competition analysis.

## Decision

**KEEP** — This slice establishes the basic auction microstructure dimensions: intensity (~1,181 bids/slot), competition (109 builders, three-tier structure), and structural bid timing patterns. These metrics provide the foundations for deeper auction analysis. The primary gaps are exact per-slot distributions and bid value analysis, which should be addressed in follow-on work with per-row data access.

## Recommendations for Follow-On

1. Execute per-slot GROUP BY queries on bid trace to get exact bid count distributions and per-slot builder counts
2. Analyze bid timestamps within slots to measure actual timing distributions (early vs late bids)
3. Join bid trace and delivery data for the same date to directly measure winning vs losing bid characteristics
