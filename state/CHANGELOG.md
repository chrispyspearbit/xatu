# Research Changelog

Permanent log of validated slices, pivots, and blocks. Never delete prior entries.

---
## Entry #0 — PROGRAM SETUP — 2026-03-31

### Context

This repository starts from an explicit feasibility study of the Xatu public dataset.

### Key Findings

- Xatu is strong enough for builder / relay market structure research.
- The join path across relay delivery, beacon linkage, and execution inclusion is good enough for serious work.
- Public mempool observations are partial but useful, which makes public-vs-private flow estimation feasible.
- Canonical traces are rich enough for realized MEV classification.
- Public parquet is delayed, so this program is for research and model-building, not direct live execution.

### Decision

Adopt a one-slice-per-loop autoresearch design with:
- Ralph hats for orchestration
- append-only state in `state/`
- hard validation of every run bundle
- bounded parallelism only for isolated runs

### Initial Phase Order

1. Builder / Relay Market Map
2. Auction Microstructure
3. Public-vs-Private Flow Estimation
4. Realized MEV Taxonomy

---

