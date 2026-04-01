# Plan: Public-vs-Private Flow Estimation

## Question
What share of included Ethereum transactions was visible in the public mempool before inclusion, and how does that vary by context?

## Hypothesis
A meaningful fraction of included transactions never appears in the public mempool — they arrive via private channels (direct builder submission, private mempools, MEV bundles). The public visibility share is materially below 100% and varies by builder.

## Method

### Data Sources
1. `mempool_transaction` — one day sample (2023-03-03)
   - Each row represents a sentry observation of a transaction in the public mempool
   - Fields: transaction hash, timestamp, sentry metadata
   - Known: 1,094,776 rows, 747,931 unique transaction hashes
2. `canonical_execution_transaction` — same-day window for inclusion matching
   - Each row represents a transaction included in a canonical block
   - Fields: transaction hash, block number, block hash, from, to, value
3. `mev_relay_proposer_payload_delivered` — for builder stratification context
   - Connects delivered blocks to the builder that produced them
   - Fields: relay, builder, block hash, slot

### Analysis Steps
1. **Public visibility baseline**: join mempool_transaction (unique tx hashes observed on 2023-03-03) against canonical_execution_transaction (same-day inclusions) on transaction hash. Compute the share of included transactions that had at least one public mempool sighting.
2. **Inverse: private flow share**: transactions included on-chain but with zero mempool sightings are candidates for private flow (direct builder submission, private order flow, MEV bundles).
3. **Sentry coverage caveat**: Xatu sentries do not observe the full mempool. Partial coverage means some transactions classified as "private" may simply have been missed. The visibility share is a lower bound on true public flow.
4. **Builder stratification** (if joinable): for blocks where the builder is identifiable via relay delivery data, compare public visibility rates across builders. Builders with more private order flow relationships should show lower public visibility.
5. **Join methodology documentation**: explicitly describe every join, the key used, coverage achieved, and failure modes.

### Acceptance Criteria
- Public visibility share over a defined window ✓
- Stratification by builder or relay when possible ✓
- Join methodology and failure modes ✓
- Explicit warning that public mempool coverage is partial ✓

## Limitations
- Mempool data available from 2023-03-03; this is a different era than the 2026-03-29 delivery data
- Xatu sentry coverage is partial — not all public mempool transactions are captured
- The join between mempool and canonical execution depends on transaction hash matching for the same day
- Builder stratification requires joining across relay delivery and execution data, which may have limited overlap for the 2023 date range
- A single day cannot capture time-varying private flow dynamics
