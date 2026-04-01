# Evidence: Auction Microstructure

## Data Window
- **Primary**: 2024-09-13 (bid trace, single day)
- **Cross-reference**: 2026-03-29 (delivered payloads, single day, different date)

## Source 1: `mev_relay_bid_trace` (2024-09-13)

### Raw Observations
- **Total rows**: 7,819,236
- **Unique slots**: 6,620
- **Unique builders**: 109
- **Mean bids per slot**: ~1,181 (7,819,236 / 6,620)

### Bids Per Slot Distribution

The mean of ~1,181 bids per slot is extremely high. This count includes all bids across all relays for each slot. Key structural factors:

1. **Multi-relay duplication**: builders submit the same or similar bids to multiple relays. With 8-9 active relays, a single builder's bid may appear 8-9 times per slot.
2. **Progressive bid updating**: builders revise their bids as they observe new transactions entering the mempool within a slot window (~12 seconds). A single builder may submit 10-50+ bid revisions per relay per slot.
3. **Cross-builder competition**: 109 builders competing means ~109 builder × multiple relays × multiple revisions per slot.

**Decomposition estimate**:
- 109 builders × ~10.8 bids per builder per slot = ~1,181 bids per slot
- This ~10.8 average includes relay duplication; per-relay, each builder submits approximately 1-2 bids per slot on average
- Alternatively: if each builder submits to ~8 relays with ~1.4 revisions per relay: 109 × 8 × 1.4 ≈ 1,221 (close to observed 1,181)

**Distribution shape**: bid-per-slot counts are likely right-skewed, with most slots near the mean but some slots (containing high-value transactions or MEV opportunities) attracting significantly more bid revisions. Without per-slot GROUP BY data, we characterize this as the expected pattern based on MEV auction dynamics.

### Builder Competition Per Slot

- **Total unique builders in sample**: 109
- **Mean builders per slot (upper bound)**: 109 (if all builders bid every slot)
- **Realistic estimate**: not all builders bid every slot. Based on typical MEV-Boost dynamics, 50-80 builders likely bid in any given slot, with the full 109 representing the union across all slots in the day.
- **Competition intensity**: even at 50 active builders per slot, this represents intense competition. Each slot is a separate auction with one winner per relay.

### Bid Timing and Progressive Updating

The ~10.8 bids per builder per slot (including relay duplication) implies builders are actively revising bids. The MEV-Boost auction has a defined timeline:

1. **Slot start (t=0s)**: the slot begins; builders begin constructing candidate blocks
2. **Early bids (t=0-4s)**: initial bids based on pending mempool contents
3. **Mid-slot updates (t=4-8s)**: revised bids incorporating newly seen transactions
4. **Late bids (t=8-12s)**: final bid revisions; the highest-value bid typically arrives late as builders pack maximum extractable value
5. **Slot deadline (~t=12s)**: proposer must select and sign a block

The bid revision pattern is a known feature of MEV-Boost auctions. Builders use a "last-look" strategy: submitting progressively higher bids until the deadline. The winning bid is typically among the last submitted.

**Evidence from aggregate statistics**: the ~10.8 bids/builder/slot across ~8 relays implies ~1.4 submissions per builder per relay per slot. This is consistent with at least one initial bid plus occasional revisions per relay.

### Winning vs Losing Bid Patterns

**Builder attrition**: 109 builders submitted bids (2024-09-13) but only 47 delivered winning blocks (2026-03-29, different date). While these are from different dates, the ~57% attrition rate (62 of 109 bidders never winning) is structurally informative:

- The auction is winner-take-all per slot per relay
- Most builders lose most auctions most of the time
- The builder market has a large competitive fringe that bids but rarely wins

**Bid value distribution**: without per-bid value data from the aggregate observations, we cannot directly compare winning vs losing bid values. However, the structural observation is clear: in a market with ~1,181 bids per slot and one winner, the win rate per bid is ~0.085% (1/1,181). Per builder, assuming ~50-80 active builders per slot, the per-slot win rate is ~1.25-2%.

**Win concentration**: from the builder market map (run #1), we know the top-3 builders produce an estimated 55-75% of delivered blocks. This means the top builders win disproportionately, consistent with them having better block construction (more private order flow, better MEV extraction algorithms, or lower latency).

## Source 2: `mev_relay_proposer_payload_delivered` (2026-03-29)

### Raw Observations (cross-reference only)
- **Total rows**: 44,039
- **Unique blocks**: 6,597
- **Unique builders**: 47
- **Relay multiplicity**: ~6.7x (44,039 / 6,597)

### Cross-Reference Interpretation
The delivery data confirms the auction's output: only 47 builders successfully delivered blocks on 2026-03-29 out of the ~109 that bid (on a different date). The ~6.7x relay multiplicity on the delivery side means each winning block appears across ~6.7 relays, consistent with builders submitting to all available relays.

## Derived Metrics

### Auction Intensity Index
- **Bids per slot**: ~1,181 (high intensity)
- **Builders per slot**: estimated 50-80 (high competition)
- **Bids per builder per slot**: ~10.8 (including relay duplication)
- **Per-bid win rate**: ~0.085%
- **Per-builder per-slot win rate**: ~1.25-2%

### Bid Revision Estimate
- ~1.4 bid submissions per builder per relay per slot
- This is a lower bound on true revision count (some revisions may not be captured if they occur within the same observation window)

### Builder Stratification
- **Tier 1 (consistent winners)**: estimated 3-5 builders winning 55-75% of slots
- **Tier 2 (occasional winners)**: estimated 15-25 builders winning the remaining 25-45%
- **Tier 3 (bidders only)**: estimated 60-80 builders that bid but rarely or never win
- Based on cross-referencing 109 bidders (2024-09-13) with 47 delivered builders (2026-03-29) and prior market map concentration estimates

## Join Coverage
- Bid trace is a standalone table for this analysis (no cross-table join required for primary metrics)
- Bid trace → delivery: not directly joined (different dates); cross-referenced for structural context only
- **Join coverage for primary analysis**: N/A (single-table aggregate analysis)

## Caveats
1. **Single-day bid trace**: 2024-09-13 only; bid patterns may vary significantly by day, time, and market regime
2. **Date mismatch**: bid trace (2024-09-13) and delivery (2026-03-29) are ~18 months apart; builder ecosystem changes are expected
3. **Aggregate-only analysis**: exact per-slot, per-builder, and per-bid distributions require GROUP BY queries not yet executed
4. **No timestamp resolution**: bid timing within slots requires sub-second timestamp analysis; the current evidence is structural inference, not measured timing
5. **Relay deduplication**: bid trace rows include cross-relay duplication; true per-relay bid counts are lower
6. **Bid value data**: we observe bid count but not bid value distributions from the aggregate statistics; value-based analysis requires per-row data access
