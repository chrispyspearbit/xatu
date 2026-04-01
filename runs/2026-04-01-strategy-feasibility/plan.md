# Plan: Strategy Feasibility Layer

## Question

Which of the six archived MEV opportunity classes are recurring, public enough to observe from Xatu data, and not obviously dead on arrival given the competitive landscape?

## Hypothesis

Of the six archived classes, only a subset will pass a multi-dimensional feasibility screen. Classes requiring private order flow access or dominated by Tier 1 builders will be assessed as infeasible for independent research-grade detection or strategy development. Structural/systemic classes (builder market position, validator dependency) will score highest on feasibility because they rely on fully public relay data.

## Approach

This is a synthesis slice. No new parquet queries are executed. The feasibility assessment applies a structured scoring framework to each archived opportunity class using evidence from all seven prior validated runs.

### Feasibility Dimensions

For each of the 6 opportunity classes from the Opportunity Archive (Run 7):

1. **Recurrence**: Is this class likely to occur repeatedly, or is it regime-dependent and bursty? Score: recurring / bursty / unknown.
2. **Public Observability**: Can the opportunity be detected from Xatu public data alone? Score: full / partial / insufficient.
3. **Competition Barrier**: Given the auction intensity (~1,181 bids/slot) and builder hierarchy, is independent execution realistic? Score: low / high / extreme.
4. **Data Sufficiency**: Does Xatu public data support meaningful analysis of this class? Score: strong / partial / weak.
5. **Feasibility Verdict**: Combining the above: FEASIBLE (for research/analytics), MARGINAL, or DEAD ON ARRIVAL (DOA).

### Data Sources

All inherited from Runs 1-7:
- `mev_relay_proposer_payload_delivered` (2026-03-29)
- `mev_relay_validator_registration` (2026-03-29)
- `mev_relay_bid_trace` (2024-09-13)
- `mempool_transaction` (2023-03-03)
- `canonical_execution_traces` (2023-07-01)
- `canonical_execution_transaction` (2023-03-10, 2023-07-01)

### Validation Checks

1. All 6 opportunity classes assessed
2. Each class has a multi-dimensional score grounded in prior evidence
3. At least one class assessed as FEASIBLE
4. At least one class assessed as DOA or MARGINAL
5. Each verdict cites specific evidence from prior runs

### Expected Artifacts

- `evidence.md`: detailed per-class feasibility scoring with evidence citations
- `metrics.json`: structured metrics
- `report.md`: summary findings and strategy implications
- `follow_on_candidates.json`: up to 3 evidence-backed follow-on items

### Limitations

- No temporal stability data — all recurrence assessments are structural reasoning, not empirical
- No execution cost modeling — feasibility is qualitative, not quantitative
- Single-day data windows underlying all estimates
- Token MEV gap carries forward from the archive
