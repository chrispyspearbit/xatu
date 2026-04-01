# Evidence: Public-vs-Private Flow Estimation

## Data Window
- **Primary**: 2023-03-03 (mempool observations, single day)
- **Supplementary join test**: 2023-03-10 (same-day mempool-to-inclusion join)

## Source 1: `mempool_transaction` (2023-03-03)

### Raw Observations
- **Total rows**: 1,094,776
- **Unique transaction hashes**: 747,931
- **Repeated sightings**: common and expected (multiple sentries observe the same transaction)
- **Average sightings per unique transaction**: ~1.46

### Interpretation
Each unique transaction hash was seen an average of ~1.46 times, meaning Xatu's sentry network provides some redundancy in mempool observation. The 747,931 unique hashes represent the observable public mempool footprint on that day.

Repeated sightings across sentries are useful for coverage estimation: more sightings indicate higher confidence that the transaction was genuinely public.

## Source 2: Same-Day Join Test (2023-03-10)

### Raw Observations
From the data-scope feasibility study:
- A same-day join test on 2023-03-10 showed **roughly 64.7% public mempool visibility** for included same-day transactions
- This means approximately 64.7% of transactions included in canonical blocks on that day had at least one prior sighting in `mempool_transaction`

### Interpretation
The 64.7% figure is the core empirical result for this slice. It means:
- **~64.7%** of included transactions were seen in the public mempool before inclusion (public flow)
- **~35.3%** of included transactions had zero mempool sightings before inclusion (candidate private flow)

However, this 35.3% "private" estimate is an **upper bound** on truly private flow because:
1. Xatu sentries have partial mempool coverage — some public transactions are simply not observed
2. Timing: transactions broadcast very close to inclusion may not be captured before the block arrives
3. Geographic coverage: sentries in certain regions may miss transactions propagated elsewhere

The true private flow share is likely lower than 35.3%, but meaningfully above zero.

## Source 3: `mev_relay_proposer_payload_delivered` (context)

### Builder Stratification Feasibility
- Relay delivery data from 2026-03-29 shows 47 builders and 8 relays
- However, the mempool data is from 2023, roughly 3 years before the relay data
- **Direct builder stratification is not feasible for this slice** because the mempool and relay delivery data are from different eras
- Builder stratification would require either:
  - Mempool data from a period where relay delivery data is also available
  - Or execution-level data that maps block builders for the 2023 period

### Structural Observation
Even without direct stratification, the existence of ~35.3% non-public inclusion is consistent with known private order flow channels:
- Flashbots Protect and similar private RPC endpoints
- Direct builder submission APIs
- MEV bundles submitted directly to builders
- Private mempool arrangements between searchers and builders

## Join Methodology

### Primary Join: Mempool → Canonical Inclusion
- **Key**: transaction hash
- **Join type**: left join from canonical_execution_transaction to mempool_transaction
- **Coverage**: ~64.7% of included transactions matched (from 2023-03-10 test)
- **Failure modes**:
  - False negatives: public transactions missed by sentries (sentry coverage gap)
  - Timing edge: transactions arriving in the same block they were first broadcast
  - Hash collisions: negligible (keccak256 hashes)

### Secondary Join: Builder Stratification
- **Status**: Not performed (date mismatch between mempool and relay data)
- **Requirement for future**: Same-window mempool + relay delivery data

## Derived Metrics

### Public Visibility Share
- **Estimate**: ~64.7% (from 2023-03-10 same-day join)
- **Interpretation**: lower bound on true public flow (sentry coverage is partial)
- **Confidence**: medium — single-day observation, partial sentry coverage

### Private Flow Candidate Share
- **Estimate**: ~35.3%
- **Interpretation**: upper bound on truly private flow
- **Includes**: genuinely private transactions + public transactions missed by sentries

### Sentry Coverage Factor
- The gap between observed public flow (64.7%) and true public flow depends on sentry coverage
- If Xatu sentries capture X% of all public mempool transactions, then:
  - True public flow ≈ 64.7% / X
  - True private flow ≈ 1 - (64.7% / X)
- Example: if sentry coverage is 80%, true public flow ≈ 80.9%, true private flow ≈ 19.1%
- Example: if sentry coverage is 90%, true public flow ≈ 71.9%, true private flow ≈ 28.1%
- Sentry coverage is not directly measured in this slice

## Caveats
1. **Single-day window**: the 64.7% figure is from one day (2023-03-10); public/private ratios vary by market regime, gas price, and MEV conditions
2. **Partial sentry coverage**: Xatu sentries do not observe the full public mempool; the public visibility share is a lower bound
3. **Historical data**: 2023-03-03/2023-03-10 mempool data reflects conditions from that era; the MEV supply chain has evolved significantly since then
4. **No builder stratification**: relay delivery data is from 2026, preventing direct builder-level analysis of public/private flow for the same period
5. **No gas price or value stratification**: high-value transactions may have different public visibility patterns than low-value transactions
6. **Methodology relies on absence of evidence**: classifying a transaction as "private" because no mempool sighting was found assumes the sentry network would have seen it if it were public — this assumption is imperfect
