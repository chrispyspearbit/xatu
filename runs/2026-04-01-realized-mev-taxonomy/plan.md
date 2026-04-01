# Plan: Realized MEV Taxonomy

## Question
What MEV patterns can be classified from Ethereum canonical execution traces, and what is the structural distribution of realized MEV types in a representative block range?

## Hypothesis
Canonical execution traces contain sufficient structural information to classify realized MEV into distinct categories (arbitrage, sandwich, liquidation, backrun) based on call patterns, value flows, and intra-block transaction positioning. The distribution is dominated by a small number of pattern types.

## Method

### Data Sources
1. `canonical_execution_traces` — block range around 20,000,000
   - 1,029,073 trace rows across 146,734 transactions
   - Fields: block number, transaction hash, transaction index, from, to, value, call type, input, output, trace address
   - Provides internal transaction structure for every included transaction
2. `canonical_execution_transaction` — same block range (for transaction-level context)
   - Fields: transaction hash, block number, from, to, value, gas, gas_price, nonce
   - Provides outer transaction metadata

### Analysis Steps

1. **Trace structure profiling**: characterize the basic shape of the trace data — distribution of traces per transaction, call depth distribution, unique address counts, value transfer patterns.

2. **Known-contract identification**: identify calls to known DeFi protocol router contracts (Uniswap, Sushiswap, Aave, Compound) by matching `to` addresses in traces against known contract addresses. This provides a coarse label of DeFi interaction type.

3. **Structural pattern classification**:
   - **Arbitrage candidates**: transactions with cyclic call patterns (A→B→C→A value flow) or multiple swap calls in a single transaction that start and end with the same token
   - **Sandwich candidates**: identify intra-block clusters where the same address has transactions at positions i and j bracketing another address's transaction at position k (i < k < j), with opposing trade directions
   - **Liquidation candidates**: calls to known liquidation entry points (liquidate, liquidatePosition, liquidateBorrow)
   - **Backrun candidates**: transactions from known MEV bot addresses placed immediately after high-value DeFi transactions

4. **Classification coverage assessment**: what fraction of transactions in the block range can be assigned to at least one category? What fraction remains unclassified?

5. **Distribution analysis**: for classified transactions, compute the frequency distribution across MEV types. Estimate value extracted per type where the trace data supports it (ETH value flows).

### Acceptance Criteria
- Structural profile of trace data (depth, breadth, value flow) ✓
- At least 3 distinct MEV pattern types identified from trace structure ✓
- Classification coverage rate (what % of transactions match a pattern) ✓
- Distribution of MEV types by frequency ✓
- Explicit documentation of what the trace data can and cannot support ✓

## Limitations
- Block range around 20,000,000 is from mid-2023; MEV patterns may have evolved
- Classification relies on structural heuristics, not ground-truth labels
- Without decoded function selectors or event logs in traces, some patterns may be ambiguous
- Value extraction estimates based on ETH flows may miss token-denominated MEV
- Single block range sample; distribution may vary significantly across market regimes
- No access to private bundle data; only realized (included) MEV is observable
