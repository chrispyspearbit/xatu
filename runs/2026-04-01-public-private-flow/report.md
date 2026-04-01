# Report: Public-vs-Private Flow Estimation

## Summary

This study estimates what share of included Ethereum transactions appeared in the public mempool before inclusion, using Xatu's public mempool observation data. The primary evidence comes from a same-day join test between `mempool_transaction` and `canonical_execution_transaction` data, which found approximately 64.7% public mempool visibility for included transactions. The remaining ~35.3% are candidates for private flow, though this is an upper bound due to partial sentry coverage.

## Key Findings

### 1. Approximately 65% of Included Transactions Were Publicly Visible

A same-day join on 2023-03-10 between Xatu mempool observations and canonical execution data showed that roughly 64.7% of transactions included in canonical blocks had at least one prior sighting in the public mempool. This establishes a baseline: the majority of included flow is publicly observable, but a substantial minority is not.

### 2. Private Flow Is Meaningful but Bounded

The ~35.3% of included transactions with zero mempool sightings represents an upper bound on truly private flow. This includes:
- Transactions submitted via private channels (Flashbots Protect, direct builder APIs, MEV bundles)
- Public transactions missed due to partial Xatu sentry coverage
- Transactions broadcast very close to block inclusion (timing gap)

The true private flow share is likely between 15-35%, depending on actual sentry coverage. Even at the lower bound, private order flow is a structurally significant component of Ethereum's transaction supply chain.

### 3. Builder Stratification Not Yet Feasible

Relay delivery data (which identifies block builders) is available from 2026-03-29, while the mempool data dates from 2023. This ~3-year gap prevents direct analysis of how public/private visibility varies by builder. Builder stratification is a high-priority follow-on requiring temporally aligned data.

## Methodology

### Join Approach
The core methodology is a same-day left join:
1. Take all transactions included in canonical blocks on a target day
2. Check whether each transaction hash appears in `mempool_transaction` for the same day
3. Transactions with at least one mempool sighting = "public flow"
4. Transactions with zero mempool sightings = "private flow candidates"

### Join Coverage
- **Match rate**: ~64.7% (from 2023-03-10 same-day test in data-scope.md)
- **Join key**: transaction hash (keccak256, collision-negligible)
- **Primary failure mode**: false negatives from sentry coverage gaps

## Limitations

1. **Partial sentry coverage**: Xatu sentries do not observe the full Ethereum public mempool. The 64.7% public visibility figure is a lower bound on true public flow. Without an independent measure of sentry coverage, the exact correction factor is unknown.
2. **Single-day snapshot**: the estimate comes from one day (2023-03-10). Public/private ratios likely vary with gas market conditions, MEV regime, and time of day.
3. **Historical data era**: 2023 mempool conditions may differ materially from the current state. The private order flow ecosystem (Flashbots, MEV-Share, builder APIs) has evolved.
4. **No builder or value stratification**: all transactions are treated uniformly. High-value transactions, DEX trades, and MEV-exposed transactions likely have different public visibility patterns.
5. **Absence-of-evidence methodology**: classifying transactions as "private" because no mempool sighting was found is inherently conservative. Some "private" transactions are simply unobserved public transactions.

## Decision

**KEEP** — This slice establishes the first grounded estimate of public-vs-private flow from Xatu data. The ~65% public visibility baseline, while approximate, is consistent with known private order flow dynamics and provides a foundation for more refined analysis. The key gap is the lack of builder stratification and temporal coverage.

## Recommendations for Follow-On

1. Obtain temporally aligned mempool and relay delivery data to enable builder-level stratification of public/private flow
2. Extend the analysis to multiple days or weeks to capture temporal variation in the public/private ratio
3. Stratify by transaction characteristics (value, gas price, contract interaction type) to identify which transaction classes are most likely to be private
