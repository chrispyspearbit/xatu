# Phase 1 Foundations

## Summary

Produce the first three validated studies that the rest of the research program depends on:
- builder / relay market map
- auction microstructure
- public-vs-private flow estimation

## Acceptance Criteria

### 1. Builder / Relay Market Map

Given Xatu relay delivery and registration data,
when the study is complete,
then it must report:
- builder share over a defined window
- relay share over the same window
- builder-relay overlap or routing concentration
- concentration metrics such as top-N share or HHI
- explicit join coverage and caveats

### 2. Auction Microstructure

Given Xatu bid trace data and delivered outcomes,
when the study is complete,
then it must report:
- bids per slot distribution
- builder competition per slot
- bid timing relative to slot boundaries
- winning versus losing bid patterns
- the cost or limitation of the sampled window

### 3. Public-vs-Private Flow Estimation

Given Xatu public mempool observations and canonical execution inclusion,
when the study is complete,
then it must report:
- public visibility share over a defined window
- stratification by builder or relay when possible
- join methodology and failure modes
- explicit warning that public mempool coverage is partial

## Cross-Cutting Requirements

Every phase-1 run must:
- use explicit date ranges or partitions
- name every Xatu table used
- record nonzero row counts for the main evidence tables
- record join coverage for major joins, or say why no join was required
- include a limitations section
- end in a terminal decision

## Done

Phase 1 is complete when all three items are terminal in `state/agenda.md` and each has at least one validated run bundle.

