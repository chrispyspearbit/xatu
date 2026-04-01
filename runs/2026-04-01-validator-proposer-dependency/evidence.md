# Evidence: Validator / Proposer Dependency and Concentration Risk

## Data Window
- **Primary**: 2026-03-29 (single day)

## Source 1: `mev_relay_validator_registration` (2026-03-29)

### Raw Observations
- **Total rows**: 5,829,223
- **Unique validators**: 917,424
- **Unique fee recipients**: 24,501
- **Unique relays**: 9

### Relay Registration Breadth

With 5,829,223 registration rows across 917,424 unique validators and 9 relays:
- **Average registrations per validator**: 5,829,223 / 917,424 ≈ 6.35
- This means the typical validator registers with ~6-7 of 9 available relays
- **Registration breadth ratio**: 6.35 / 9 ≈ 0.706 (70.6% of available relays)

This indicates broad relay registration — most validators do not depend on a single relay. However, this is registration-level redundancy, not delivery-level redundancy.

### Per-Relay Registration Share

With 917,424 unique validators and 9 relays, if registration were uniform:
- Each relay would have ~647,380 validators (917,424 × 6.35 / 9)
- Per-relay rows ≈ 5,829,223 / 9 ≈ 647,691

The 9:8 relay gap (9 relays in registration vs 8 in delivery) means one relay accepts registrations but delivered no winning blocks on this day. This relay represents a registration sink — validators register but get no MEV-Boost blocks through it.

### Relay Registration HHI Estimation

Given broad registration (average breadth ~6.35/9):
- If all 9 relays had equal registration share: HHI = 9 × (1/9)² = 1/9 ≈ 0.111
- The 9th relay with zero delivery but active registration skews slightly
- **Estimated relay registration HHI**: 0.11-0.14 (low concentration)

## Source 2: Fee Recipient Concentration (from `mev_relay_validator_registration`)

### Raw Observations
- **Unique validators**: 917,424
- **Unique fee recipients**: 24,501
- **Aggregation ratio**: 917,424 / 24,501 ≈ 37.4 validators per fee recipient

### Fee Recipient Distribution Analysis

The 37.4:1 aggregation ratio indicates massive staking pool concentration. This is the critical structural finding:

- **Solo stakers**: likely have 1-10 validators per fee recipient
- **Professional operators**: likely 10-100 validators
- **Large staking pools** (Lido, Coinbase, etc.): likely 1,000-100,000+ validators per fee recipient

The distribution is heavily right-skewed. Based on known Ethereum staking pool structure:
- **Top-1 fee recipient**: likely controls 25-35% of registered validators (Lido operators)
- **Top-5 fee recipients**: likely control 50-65% of registered validators
- **Top-20 fee recipients**: likely control 75-85% of registered validators
- **Long tail** (24,481+ fee recipients): likely control 15-25% combined

### Fee Recipient HHI Estimation

Assuming top-5 control ~60% with the largest at ~30%:
- **Lower bound** (uniform): HHI = 24,501 × (1/24,501)² ≈ 0.00004 (extremely unconcentrated)
- **Realistic estimate at fee recipient level**: HHI ≈ 0.10-0.18 (moderately concentrated)
- **At effective operator level**: higher still, since multiple fee recipients may belong to the same organization

### Concentration Risk from Aggregation

The fee recipient layer is where dependency risk concentrates:
- A single staking pool operator choosing to drop a relay affects thousands of validators simultaneously
- Relay selection by top-5 fee recipients effectively determines relay market viability
- Builder preference by large operators (through MEV-Boost configuration) shapes builder market dynamics

## Source 3: Builder Dependency via `mev_relay_proposer_payload_delivered` (2026-03-29)

### Raw Observations
- **Total rows**: 44,039
- **Unique delivered blocks**: 6,597
- **Unique builders**: 47
- **Unique relays with deliveries**: 8

### Builder Concentration (from Entry #1 — Builder / Relay Market Map)

From the prior validated slice:
- **Estimated top-1 builder**: 20-35% of delivered blocks
- **Estimated top-3 builders**: 55-75% of delivered blocks
- **Estimated top-10 builders**: 85-95% of delivered blocks
- **Estimated builder HHI**: 0.15-0.25 (moderately to highly concentrated)

### Proposer-Builder Dependency

With 6,597 delivered blocks and 47 builders, validators (proposers) are structurally dependent on a small builder set:
- Validators do not choose builders directly — MEV-Boost selects the highest-bidding builder per slot
- However, if top-3 builders control ~65% of blocks, then ~65% of proposer revenue comes from 3 entities
- A single dominant builder going offline could reduce proposer revenue by 20-35% (their block share would be redistributed among remaining builders, but at likely lower values)

### Relay-Builder Delivery Coupling

From the market map evidence:
- Relay multiplicity is ~6.7x (builders route through nearly all relays)
- This means relay failure has limited builder impact — builders would still reach proposers through remaining relays
- But builder failure has no relay compensation — relays cannot manufacture bids

### Asymmetric Dependency Structure

The dependency flows are:
1. **Validators → Relays**: LOW risk. Average registration breadth 6.35/9 relays. Losing 1-2 relays leaves most validators covered.
2. **Validators → Builders** (via MEV-Boost): MODERATE-HIGH risk. Top-3 builders produce ~65% of blocks. Builder concentration is structural.
3. **Relays → Builders**: HIGH risk for individual relays. Relays are substitutable; builders are not (their bids carry unique MEV extraction value).
4. **Fee Recipients → Relay Selection**: HIGH leverage. Top-5 fee recipients control relay viability through registration decisions.

## Derived Metrics

### Scenario: Top-1 Builder Offline
- **Block share lost**: estimated 20-35% of MEV-Boost blocks
- **Revenue impact**: proportional, minus partial redistribution to remaining builders
- **Validator impact**: all validators equally affected (no validator chooses a builder)
- **Recovery**: remaining 46 builders absorb demand, but at likely lower bid values

### Scenario: Top-3 Builders Offline
- **Block share lost**: estimated 55-75% temporarily
- **Revenue impact**: severe — remaining builders may not have capacity or MEV extraction efficiency
- **Market structure**: would effectively restart builder competition among the remaining 44 builders
- **Systemic risk**: proposers might fall back to local block production (vanilla blocks without MEV extraction)

### Scenario: Top-1 Relay Offline
- **Registration impact**: minimal — validators register with 6-7 relays on average
- **Delivery impact**: moderate — blocks delivered through that relay would need re-routing, but relay multiplicity (~6.7x) means most blocks are already available through alternative relays
- **Estimated block delivery disruption**: <5% (most blocks have 6+ relay paths)

### Scenario: Top-2 Relays Offline
- **Registration impact**: still limited — average breadth drops from 6.35 to ~4.35, still covering most validators
- **Delivery impact**: moderate — some blocks may have been exclusive to these relays
- **Estimated block delivery disruption**: 5-15% (depends on relay exclusivity, which is low)

### Concentration Risk Summary

| Dimension | Concentration Level | Key Metric | Risk Level |
|-----------|-------------------|------------|------------|
| Validator → Relay registration | Low | 6.35/9 breadth | LOW |
| Fee recipient aggregation | Moderate-High | 37.4 validators/recipient | HIGH leverage |
| Builder market share | Moderate-High | Top-3 ≈ 55-75% | MODERATE-HIGH |
| Relay delivery | Low-Moderate | 8 relays, 6.7x multiplicity | LOW |
| Builder → Relay routing | Low | Builders use ~all relays | LOW |

## Join Coverage

- Validator registration → delivered payloads: joinable on fee_recipient/proposer_fee_recipient, but not directly executed in this slice (structural analysis from known field availability)
- Delivered payload → beacon block: ~99.99% (from prior scoping)

## Caveats

1. **Single-day window**: all metrics from 2026-03-29 only; concentration may vary over time
2. **No per-entity GROUP BY**: fee recipient distribution and builder share are bounded estimates, not exact computed values
3. **Fee recipient ≠ operator**: multiple fee recipients may belong to the same organization (understates true operator concentration)
4. **Registration ≠ delivery preference**: registering with a relay does not mean receiving blocks from it; delivery is auction-determined
5. **No revenue data**: concentration risk is measured in block share, not value; high-value blocks may be more concentrated
6. **Static snapshot**: dependencies may shift with market conditions, new builder/relay entry, or protocol changes
7. **Builder identity ambiguity**: builder pubkeys may not map 1:1 to organizations
