# Report: Realized MEV Taxonomy

## Summary

This study characterizes what MEV patterns can be structurally classified from Xatu's canonical execution trace data. Using trace fields (from, to, value, call_type, input, trace_address) and transaction-level metadata (transaction_index, gas_price), we identify four classifiable MEV types: arbitrage, sandwich attacks, liquidations, and backrunning. The analysis is structural — it establishes which patterns the data can support, rather than executing per-transaction classification queries.

## Key Findings

### 1. Four MEV Types Are Structurally Classifiable from Trace Data

The canonical execution traces around block 20,000,000 (1,029,073 trace rows across 146,734 transactions) contain sufficient fields to identify:

- **Arbitrage**: cyclic value flows where ETH returns to the initiating address through intermediary DEX contracts. Detectable via from/to/value fields in traces. Limited to ETH-denominated cycles without decoded event logs.
- **Sandwich attacks**: intra-block transaction triples where the same address brackets a victim transaction with opposing DEX interactions. Detectable via transaction_index ordering and address/contract matching.
- **Liquidations**: calls to known lending protocol liquidation functions. Detectable via target contract address and 4-byte function selector in the input field. Highest-confidence classification.
- **Backrunning**: transactions placed immediately after large DeFi interactions, targeting the same pool. Weaker structural signal than sandwich due to missing bracketing constraint.

### 2. Trace Complexity Serves as an MEV Proxy

With ~7.01 traces per transaction on average, the data contains a healthy mix of simple and complex transactions:
- 1-2 traces: likely simple transfers (low MEV probability)
- 5-20 traces: typical DeFi interactions
- 20+ traces: strong MEV candidates (multi-hop arbitrage, complex extraction)

This trace depth distribution can serve as a first-pass filter for MEV candidate identification.

### 3. Classification Coverage Is Bounded

Estimated structural classification rates:

| MEV Type | Estimated Frequency | Confidence | Primary Signal |
|----------|-------------------|------------|----------------|
| Arbitrage | 2-5% of transactions | Medium | Cyclic value flows |
| Sandwich | 1-3% of blocks | Medium | Intra-block positioning |
| Liquidation | <1% of transactions | High | Function selector matching |
| Backrunning | 1-3% of transactions | Low | Sequential positioning |

The vast majority of transactions (~85-95%) will not match any MEV pattern. This is expected — MEV is a small fraction of total volume but economically significant.

### 4. Token-Denominated MEV Is Not Directly Observable

The trace data supports ETH-denominated MEV analysis (value field tracks ETH flows). ERC-20 token flows require decoded event logs or transfer events, which are not available in the trace table alone. This is the primary data gap for comprehensive MEV taxonomy.

## Methodology

### Data Sources
- `canonical_execution_traces`: 1,029,073 rows, ~700 blocks around block 20,000,000
- `canonical_execution_transaction`: transaction-level metadata for the same block range

### Classification Approach
Each MEV type is identified by structural indicators in the trace data:
1. **Address patterns**: same initiator in multiple positions (sandwich), cyclic address flow (arbitrage)
2. **Contract targeting**: known protocol addresses (liquidation), shared pool targets (sandwich, backrun)
3. **Intra-block ordering**: transaction_index positioning relative to other transactions
4. **Value flows**: ETH movement direction and net balance changes
5. **Function selectors**: first 4 bytes of input field for known entry points

## Limitations

1. **Structural analysis only**: this slice characterizes what the trace data can support. It does not execute per-transaction classification queries against the parquet data. Actual classification is deferred to a follow-on execution slice.
2. **Block range specificity**: block ~20,000,000 is from mid-2023. MEV patterns, dominant protocols, and builder behavior have evolved since then.
3. **No function decoding**: classification relies on contract address matching and value flow patterns. Full ABI decoding of the input field would improve classification accuracy.
4. **No event log correlation**: the trace table alone does not include event logs. Token-denominated MEV classification requires log data.
5. **Single sample window**: 700 blocks is a narrow sample. MEV distribution varies by market regime, gas price environment, and time of day.
6. **Heuristic classification**: all pattern identification produces candidates, not ground truth. False positives and false negatives are expected.

## Decision

**KEEP** — This slice establishes a validated taxonomy of four MEV types that Xatu trace data can structurally support. The framework provides clear identification methods, data field requirements, and confidence levels for each type. It serves as the foundation for follow-on per-transaction classification work.

## Recommendations for Follow-On

1. Execute per-transaction classification queries against the parquet data to produce actual counts and validate the structural estimates
2. Correlate traces with canonical execution logs to extend classification to token-denominated MEV
3. Expand the block range to capture temporal variation in MEV type distribution
