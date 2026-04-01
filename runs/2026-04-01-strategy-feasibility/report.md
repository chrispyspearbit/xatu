# Report: Strategy Feasibility Layer

## Summary

This study applies a structured feasibility framework to the six MEV opportunity classes cataloged in the Opportunity Archive (Run 7). Each class is scored on recurrence, public observability, competition barrier, and data sufficiency, producing a feasibility verdict. The result is a clear three-tier ranking that constrains the strategy space for the Xatu research program.

## Key Findings

### 1. Two Classes Are Fully Feasible for Research

**Builder Market Position** and **Validator Dependency Risk** are the two strongest research targets. Both rely entirely on public relay data (~99.99% join coverage), face no execution competition (they are analytics/research activities), and produce continuously generated data. These classes should be the primary focus for ongoing Xatu-based research work.

### 2. Two Classes Are Marginal

**ETH-Denominated Arbitrage** and **Liquidation MEV** are detectable post-inclusion from execution traces and support useful analytics (frequency counting, pattern characterization). However, both face extreme or high competition barriers for execution, partial observability (arb transactions skew toward private submission), and partial data sufficiency (token MEV and economic sizing require ABI/log decode not yet available). These are useful research subjects but not viable strategy targets.

### 3. Two Classes Are Dead on Arrival

**Sandwich Attacks** and **Backrunning** are not feasible for the Xatu research program:
- Sandwich requires builder integration for execution and ABI decode for detection — both outside the program's scope.
- Backrunning has the weakest detection signal (sequential positioning alone is ambiguous) and still faces intense competition despite being the "most accessible" MEV type.

### 4. The Observability-Competition Divide Is Structural

The feasibility split is not incidental — it reflects the architecture of MEV-Boost. Classes that depend on public relay data (delivery, registration, bids) are fully observable and non-competitive for research. Classes that depend on transaction-level MEV detection require private order flow access or builder integration that is structurally unavailable in public data.

### 5. Token MEV Is the Single Biggest Bottleneck

Four of six classes are limited by the same gap: token-denominated MEV requires joining execution traces with event logs. Resolving this via `canonical_execution_logs` correlation would upgrade both MARGINAL classes and potentially reveal new classes invisible in ETH-only traces.

## Feasibility Matrix

| # | Class | Recurrence | Observability | Competition | Data | Verdict |
|---|-------|-----------|---------------|-------------|------|---------|
| 1 | ETH Arbitrage | recurring | partial | extreme | partial | **MARGINAL** |
| 2 | Sandwich Attacks | recurring | partial | extreme | partial | **DOA** |
| 3 | Liquidation MEV | bursty | partial | high | partial | **MARGINAL** |
| 4 | Backrunning | recurring | partial | high | weak | **DOA** |
| 5 | Builder Market Position | recurring | full | low | strong | **FEASIBLE** |
| 6 | Validator Dependency Risk | recurring | full | low | strong | **FEASIBLE** |

## Strategy Implications

The feasibility layer constrains the Xatu research program to three tracks:

1. **Primary track** — Builder and validator ecosystem monitoring (Classes 5, 6): fully feasible, high data quality, continuous data generation, no competition. This is where the program can produce its most reliable and differentiated outputs.

2. **Secondary track** — MEV detection analytics (Classes 1, 3): useful for characterization and counting, but limited by the token MEV gap and lack of temporal stability data. These classes provide context and supporting evidence for the primary track.

3. **Out of scope** — MEV execution strategy (Classes 2, 4): require infrastructure beyond public data. The program should not invest research effort in execution-focused work on these classes.

## Methodology

### Approach
Synthesis slice applying a structured four-dimensional feasibility framework to each archived opportunity class. All evidence is inherited from seven prior validated runs. No new parquet queries were executed.

### Data Sources (Inherited)
- `mev_relay_proposer_payload_delivered` (2026-03-29): 44,039 rows
- `mev_relay_validator_registration` (2026-03-29): 5,829,223 rows
- `mev_relay_bid_trace` (2024-09-13): 7,819,236 rows
- `mempool_transaction` (2023-03-03): 1,094,776 rows
- `canonical_execution_traces` (2023-07-01): 1,029,073 rows
- `canonical_execution_transaction` (2023-03-10, 2023-07-01): 46,101 rows

Total inherited row count: ~15.8M rows across 6 tables.

## Limitations

1. **Qualitative framework**: feasibility is scored categorically, not quantitatively. No execution cost or profit modeling.
2. **No temporal validation**: recurrence assessments are structural reasoning, not multi-day empirical evidence.
3. **Xatu-specific**: feasibility is assessed relative to Xatu public data. Different data access would yield different verdicts.
4. **Static snapshot**: the MEV ecosystem evolves; verdicts may change with protocol upgrades or market structure shifts.
5. **Synthesis only**: no new data; all limitations from prior runs carry forward.
6. **Token MEV gap**: the most economically significant MEV remains unobservable, limiting the MARGINAL class assessments.

## Decision

**KEEP** — The feasibility layer provides an evidence-grounded, structured assessment that cleanly separates actionable research targets from dead-end directions. The three-tier ranking (FEASIBLE / MARGINAL / DOA) directly constrains the strategy space for the remainder of the Xatu research program. The identification of the token MEV bottleneck as the single highest-leverage data gap is the most actionable finding for program planning.

## Recommendations for Follow-On

1. **Cross-Chain Portability Framework** (agenda item #9): assess which research methods and feasibility conclusions transfer to non-Ethereum chains.
2. **Trace-Log Correlation for Token MEV**: the single highest-leverage data investment — would upgrade both MARGINAL classes and potentially reveal new classes.
3. **Multi-Day Temporal Stability Analysis**: validate the recurrence assumptions across market regimes for FEASIBLE and MARGINAL classes.
