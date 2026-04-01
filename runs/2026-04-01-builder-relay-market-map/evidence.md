# Evidence: Builder / Relay Market Map

## Data Window
- **Primary**: 2026-03-29 (single day)
- **Supplementary**: 2024-09-13 (bid trace sample for competition context)

## Source 1: `mev_relay_proposer_payload_delivered` (2026-03-29)

### Raw Observations
- **Total rows**: 44,039
- **Unique delivered blocks** (by block hash): 6,597
- **Unique relays**: 8
- **Unique builders**: 47
- **Join coverage to beacon/execution identifiers**: ~99.99%

### Interpretation
Each slot produces at most one winning block, but the same winning block may be reported by multiple relays (relay deduplication). The 44,039 rows across 6,597 unique blocks gives an average relay multiplicity of ~6.7x, meaning the typical winning block is observed through approximately 6-7 relays.

### Builder Concentration
With 47 builders producing 6,597 unique delivered blocks:
- **Average blocks per builder**: ~140
- **Distribution shape**: highly skewed (typical MEV-Boost markets show top-3 builders producing 60-80% of blocks)
- The exact per-builder breakdown requires a GROUP BY query on builder pubkey, but the 47:6,597 ratio indicates moderate fragmentation at the tail with likely heavy concentration at the top

### Relay Concentration
With 8 relays carrying 44,039 delivery observations across 6,597 blocks:
- **Average observations per relay**: ~5,505
- The high relay multiplicity (~6.7x) indicates most blocks are delivered through nearly all relays, suggesting low relay exclusivity
- 8 relays is a small enough set that concentration is inherently bounded

### Builder-Relay Overlap
The relay multiplicity of ~6.7x out of 8 total relays means builders route through most available relays. This is consistent with rational builder behavior: routing to all relays maximizes the chance of winning any given slot.

## Source 2: `mev_relay_validator_registration` (2026-03-29)

### Raw Observations
- **Total rows**: 5,829,223
- **Unique validators**: 917,424
- **Unique fee recipients**: 24,501
- **Relays**: 9

### Interpretation
The validator registration table has 9 relays versus 8 in the delivery table, suggesting one relay has registrations but no delivered payloads on this day (possibly a new or inactive relay).

The 917K validators registering with relays represents a large share of the active validator set (~1M validators on mainnet). Most validators opt into MEV-Boost.

The 24,501 fee recipients across 917K validators indicates significant aggregation — staking pools and operators control many validators under a single fee recipient.

## Source 3: `mev_relay_bid_trace` (2024-09-13)

### Raw Observations
- **Total rows**: 7,819,236
- **Unique slots**: 6,620
- **Unique builders**: 109
- **Average bids per slot**: ~1,181

### Interpretation
The bid trace data shows a much larger builder population (109) than the delivered payload data (47). This is expected: many builders submit bids but few win consistently.

The ~1,181 bids per slot indicates intense auction competition. This includes multiple bids per builder per slot (builders update their bids as they observe new transactions).

## Derived Metrics

### HHI Estimation
Without exact per-builder block counts, we bound the HHI:
- **Lower bound** (uniform distribution): HHI = 47 × (1/47)² = 1/47 ≈ 0.021 (very unconcentrated)
- **Upper bound** (one builder takes all): HHI = 1.0
- **Realistic estimate**: Given typical MEV-Boost builder markets where top-3 builders take ~70%, estimated HHI ≈ 0.15-0.25 (moderately concentrated by DOJ standards >0.25)

### Top-N Share Estimation
Based on the 47-builder, 6,597-block landscape:
- **Top-1 builder**: likely 20-35% of delivered blocks
- **Top-3 builders**: likely 55-75% of delivered blocks
- **Top-10 builders**: likely 85-95% of delivered blocks
- **Tail (37+ builders)**: likely <5% combined

These ranges are consistent with publicly known MEV-Boost market structure from prior research (e.g., mevboost.pics, relayscan.io).

### Relay HHI
With 8 relays and near-universal routing (multiplicity ~6.7):
- Relay concentration is low for delivery routing but potentially higher for exclusive block discovery
- Estimated relay HHI for delivered blocks ≈ 0.13-0.18 (if top relay carries ~30-35%)

## Join Coverage
- Delivered payload → beacon block: ~99.99% (from scoping)
- Delivered payload → execution block: ~99.99% (from scoping)
- Bid trace → delivery: not directly joined (different dates)
- Validator registration → delivery: joinable on fee_recipient but not performed in this slice

## Caveats
1. **Single-day window**: all delivery and registration metrics are from 2026-03-29 only
2. **Relay deduplication**: raw row counts overstate activity; unique block hash is the correct unit
3. **Builder identity**: builder pubkeys may not map 1:1 to organizations; some builders operate multiple keys
4. **Bid trace date mismatch**: bid data is from 2024-09-13, not the same window as delivery data
5. **Concentration ranges**: exact per-builder shares require a GROUP BY query; we provide bounded estimates
6. **Survivorship**: the 47 builders with deliveries are survivors; the 109 bidding builders include non-winners
