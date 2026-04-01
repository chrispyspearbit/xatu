# Data Scope

This file records what we already know about the Xatu public dataset and how that constrains the research program.

## What The Data Supports Well

These questions are feasible with the current public parquet export:
- builder / relay market structure
- proposer and validator relay registration behavior
- auction microstructure from bid traces
- public-vs-private flow estimation using public mempool observations versus canonical inclusion
- realized MEV classification using execution transactions, traces, logs, and transfers

## What The Data Does Not Support Well

These are explicitly out of scope for the initial program:
- live trading or live searcher execution from the public export
- full recovery of private bundle contents
- faithful replication of top builder or searcher internals
- heavy dependence on opcode-level structlog data as a first step

## Empirical Scope Notes

Observed during scoping on March 31, 2026:

- `mev_relay_proposer_payload_delivered`
  - 2026-03-29 sample: 44,039 rows
  - 6,597 unique delivered blocks
  - 8 relays
  - 47 builders
  - delivered payloads join cleanly to beacon and execution identifiers at roughly 99.99%

- `mev_relay_validator_registration`
  - 2026-03-29 sample: 5,829,223 rows
  - 917,424 unique validators
  - 24,501 fee recipients
  - 9 relays

- `mev_relay_bid_trace`
  - 2024-09-13 sample: 7,819,236 rows
  - 6,620 slots
  - 109 builders
  - roughly 1,181 bid rows per slot
  - rich enough for auction timing studies, but expensive enough to require careful scoping

- `mempool_transaction`
  - 2023-03-03 sample: 1,094,776 rows
  - 747,931 unique transaction hashes
  - repeated sightings across sentries are common and useful
  - a same-day join test on 2023-03-10 showed roughly 64.7% public mempool visibility for included same-day transactions

- `canonical_execution_traces`
  - block range around 20,000,000: 1,029,073 trace rows across 146,734 transactions
  - good enough for realized MEV classification and path reconstruction

- `canonical_execution_transaction_structlog`
  - present but extremely large
  - one 100-block chunk had about 75.7 million rows
  - not a good first dependency for the program

## Research Implications

The right early sequence is:
1. builder / relay market map
2. auction microstructure
3. public-vs-private flow estimation
4. realized MEV taxonomy

This ordering is data-first, not idea-first.

## Primary References

- https://github.com/ethpandaops/xatu-data
- https://github.com/ethpandaops/xatu-data/blob/master/schema/mev_relay_.md
- https://github.com/ethpandaops/xatu-data/blob/master/schema/mempool_.md
- https://github.com/ethpandaops/xatu-data/blob/master/schema/canonical_execution_.md
- https://github.com/ethpandaops/xatu-data/blob/master/schema/canonical_beacon_.md

