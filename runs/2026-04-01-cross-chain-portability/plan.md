# Plan: Cross-Chain Portability Framework

## Question

Which components of the Xatu MEV research methodology are Ethereum-specific, and which can transfer to other chains with PBS-like or MEV-aware architectures?

## Hypothesis

The research program's methodology splits into three tiers: (1) structural analysis methods (market maps, concentration metrics, dependency graphs) are broadly portable to any chain with analogous data schemas; (2) detection heuristics (MEV taxonomy, fingerprinting dimensions) require chain-specific parameter adaptation but the frameworks transfer; (3) specific data dependencies (MEV-Boost relay protocol, Xatu sentry mempool coverage, Ethereum execution trace format) are Ethereum-specific and would need replacement data sources on other chains.

## Approach

This is a synthesis slice. No new parquet queries are executed. The portability assessment reviews all 8 prior validated runs and classifies each research component along three dimensions.

### Portability Classification

For each research method, data dependency, and finding from Runs 1-8:

1. **Method Portability**: Does the analytical approach (e.g., concentration metrics, behavioral clustering, feasibility scoring) transfer to other chains?
   - `PORTABLE`: methodology applies to any chain with analogous market structure
   - `ADAPTABLE`: core approach transfers but needs chain-specific parameters or data mappings
   - `ETHEREUM-SPECIFIC`: depends on Ethereum-unique infrastructure or protocol

2. **Data Dependency Classification**: What data schemas does each method require?
   - Map each Xatu table to its functional role (relay data → auction data, mempool → pre-inclusion flow, traces → execution internals)
   - Identify which functional roles exist on candidate chains

3. **Infrastructure Assumption Audit**: What implicit Ethereum assumptions are embedded?
   - MEV-Boost and PBS architecture
   - Relay-mediated block building
   - Proposer-builder separation
   - EVM execution model and trace format
   - Xatu sentry network coverage

### Candidate Chain Families

Assess portability against three chain architecture families:
- **PBS chains**: chains with proposer-builder separation (e.g., other chains adopting MEV-Boost-like mechanisms)
- **Integrated builder chains**: chains where block production is monolithic (e.g., most L2s, Solana)
- **EVM-compatible L2s**: chains sharing EVM execution but with different block production (e.g., rollups)

### Data Sources (Inherited)

All from Runs 1-8:
- `mev_relay_proposer_payload_delivered` (2026-03-29)
- `mev_relay_validator_registration` (2026-03-29)
- `mev_relay_bid_trace` (2024-09-13)
- `mempool_transaction` (2023-03-03)
- `canonical_execution_traces` (2023-07-01)
- `canonical_execution_transaction` (2023-03-10, 2023-07-01)

### Validation Checks

1. All 8 prior research methods assessed for portability
2. Each method has a portability classification grounded in specific evidence
3. At least one method classified as PORTABLE
4. At least one method classified as ETHEREUM-SPECIFIC
5. Infrastructure assumptions are explicitly enumerated

### Expected Artifacts

- `evidence.md`: per-method portability assessment with evidence citations
- `metrics.json`: structured metrics
- `report.md`: summary findings and cross-chain implications
- `follow_on_candidates.json`: up to 3 evidence-backed follow-on items

### Limitations

- No empirical validation on non-Ethereum chains — portability is assessed structurally
- Candidate chain families are representative, not exhaustive
- No data availability assessment for specific non-Ethereum chains
- Synthesis only; no new data
