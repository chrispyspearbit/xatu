# Report: Cross-Chain Portability Framework

## Summary

This study classifies the 8 research methods developed across the Xatu MEV research program into portable, adaptable, and Ethereum-specific components. The result is a structured portability framework that identifies what transfers to other chains and what remains bound to Ethereum's MEV-Boost architecture.

## Key Findings

### 1. Five of Eight Methods Are Fully Portable

The majority of the research program's analytical methods transfer to any chain with analogous market data:
- **Public-vs-Private Flow Estimation** (Run 3): left-join methodology on transaction hash
- **Builder Fingerprinting** (Run 5): multi-dimensional behavioral profiling
- **Dependency/Concentration Risk** (Run 6): multi-layer dependency graph analysis
- **Opportunity Archive** (Run 7): structured opportunity classification schema
- **Strategy Feasibility Layer** (Run 8): four-dimension feasibility scoring

These methods are portable because they encode analytical frameworks, not data format assumptions.

### 2. Three Methods Require Chain-Specific Adaptation

Three methods have portable cores but require adaptation for non-Ethereum chains:
- **Builder/Relay Market Map** (Run 1): concentration metrics transfer; relay-specific dimensions (routing breadth, relay HHI) drop on non-relay chains
- **Auction Microstructure** (Run 2): competition analysis transfers; sealed-bid auction format is MEV-Boost-specific
- **Realized MEV Taxonomy** (Run 4): four-type classification framework transfers; EVM trace-based heuristics require rewrite for non-EVM chains

### 3. The Relay Layer Is Ethereum-Unique but Non-Essential

Four methods use relay-specific data, but in all cases the relay dimensions provide additional analytical depth rather than the sole basis for the method. Removing relay dimensions reduces granularity but does not break the core analysis. The market map becomes a simpler block producer concentration study; dependency analysis loses the intermediary layer but retains the operator-producer dependency path.

### 4. EVM Compatibility Creates a Clean Portability Boundary

MEV taxonomy heuristics (trace format, function selectors, value fields) either transfer completely to EVM-compatible chains (L2 rollups, sidechains) or require complete rewrite for non-EVM chains (Solana, Aptos, Sui). There is no partial transfer for execution-level analysis.

### 5. Data Availability Is the True Portability Bottleneck

The research methodology is more portable than the data it depends on. A chain that publishes block attribution, auction records, and execution traces can immediately benefit from 5-8 of the program's methods. The binding constraint is whether the target chain makes this data publicly available in a queryable format.

## Portability Matrix

| # | Method | Classification | Portable Core | Chain-Specific |
|---|--------|---------------|---------------|----------------|
| 1 | Market Map | ADAPTABLE | Concentration, market share | Relay dimensions |
| 2 | Auction Microstructure | ADAPTABLE | Competition intensity, win rates | Auction format |
| 3 | Public-Private Flow | PORTABLE | Join methodology, visibility ratio | Monitoring source |
| 4 | MEV Taxonomy | ADAPTABLE | Classification framework | Trace format |
| 5 | Fingerprinting | PORTABLE | Behavioral profiling | Dimension selection |
| 6 | Dependency Risk | PORTABLE | Dependency graph analysis | Dependency path |
| 7 | Opportunity Archive | PORTABLE | Classification schema | Class catalog |
| 8 | Feasibility Layer | PORTABLE | Scoring framework | Baseline values |

## Cross-Chain Family Compatibility

| Chain Family | Methods Usable | Key Gap | Portability Effort |
|-------------|---------------|---------|-------------------|
| PBS chains | 8/8 | Parameter recalibration | LOW |
| EVM-compatible L2s | 6-7/8 | No competitive auction | LOW-MEDIUM |
| Integrated builder (Solana) | 5-6/8 | No auction, different traces | MEDIUM |
| Non-EVM L1s | 5/8 | Trace format rewrite | MEDIUM-HIGH |

## Infrastructure Assumption Inventory

| Assumption | Methods Affected | Portability Impact |
|-----------|-----------------|-------------------|
| MEV-Boost / PBS | 4 of 8 | Relay dimensions drop; core analysis survives |
| Relay architecture | 4 of 8 | Relay-specific metrics are non-transferable |
| EVM execution model | 1 of 8 | Binary: transfers to EVM chains, rewrite for others |
| Xatu sentry network | 1 of 8 | Replace with any mempool monitoring source |
| Slot-based timing | 3 of 8 | Recalibrate to chain-specific block time |

## Methodology

### Approach
Synthesis slice reviewing all 8 prior validated runs. Each research method is classified on method portability, data dependency, and infrastructure assumptions. No new parquet queries were executed.

### Data Sources (Inherited)
- `mev_relay_proposer_payload_delivered` (2026-03-29): 44,039 rows
- `mev_relay_validator_registration` (2026-03-29): 5,829,223 rows
- `mev_relay_bid_trace` (2024-09-13): 7,819,236 rows
- `mempool_transaction` (2023-03-03): 1,094,776 rows
- `canonical_execution_traces` (2023-07-01): 1,029,073 rows
- `canonical_execution_transaction` (2023-03-10, 2023-07-01): 46,101 rows

Total inherited row count: ~15.8M rows across 6 tables.

## Limitations

1. **Structural assessment only**: portability is not empirically validated on non-Ethereum chains.
2. **Representative chain families**: three families assessed do not cover all architectures.
3. **No data availability verification**: does not confirm whether target chains publish needed data.
4. **Static snapshot**: chain architectures evolve; portability assessments may change.
5. **Ethereum-centric bias**: the research program was designed for Ethereum, so the assessment inherently starts from Ethereum's perspective.
6. **Synthesis only**: no new data; all limitations from 8 prior runs carry forward.

## Decision

**KEEP** — The portability framework provides a structured, evidence-grounded separation of portable methodology from Ethereum-specific infrastructure dependencies. The key insight — that 5 of 8 methods are fully portable and the bottleneck is data availability, not methodology — directly enables principled scoping of multi-chain research extensions. This completes the Phase 3 agenda: opportunity classification (Run 7), feasibility assessment (Run 8), and cross-chain portability (Run 9).

## Recommendations for Follow-On

1. **L2 MEV Data Availability Survey**: identify which EVM-compatible L2s publish the block attribution, sequencer, and execution trace data needed to apply portable methods.
2. **Solana Block Producer Concentration Study**: apply Methods 1, 5, 6 (market map, fingerprinting, dependency) to Solana validator data as a portability proof-of-concept.
3. **Trace-Log Correlation for Token MEV**: the highest-leverage data gap from the feasibility layer (Run 8) — resolving it would improve portability of MEV taxonomy (Method 4) by making the framework less dependent on ETH-only value flows.
