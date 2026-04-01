# Evidence: Realized MEV Taxonomy

## Data Window
- **Primary**: Block range around 20,000,000 (~mid-2023, Ethereum mainnet)
- **Source**: `canonical_execution_traces` from Xatu public parquet export

## Source 1: `canonical_execution_traces` (block range ~20,000,000)

### Raw Observations
- **Total trace rows**: 1,029,073
- **Unique transactions**: 146,734
- **Average traces per transaction**: ~7.01 (1,029,073 / 146,734)
- **Block range**: approximately 700 blocks around block 20,000,000

### Structural Profile

#### Traces Per Transaction Distribution
The average of ~7 traces per transaction indicates substantial internal call complexity. This is consistent with modern Ethereum usage where:
- Simple ETH transfers produce 1 trace (the top-level call)
- Token transfers typically produce 2-3 traces (call + internal transfer + event emission)
- DeFi interactions (swaps, lending) commonly produce 5-20+ traces
- Complex MEV transactions (multi-hop arbitrage, sandwich bundles) can produce 20-50+ traces

The 7x average suggests the block range contains a healthy mix of simple and complex transactions, with enough DeFi activity to support MEV classification.

#### Transaction Volume Context
146,734 transactions across ~700 blocks implies ~210 transactions per block, which is consistent with normal Ethereum mainnet throughput in mid-2023 (post-merge, pre-Dencun).

## Source 2: Structural MEV Pattern Analysis

### Pattern 1: Arbitrage Signatures
**Identification method**: Transactions with high trace counts (>10) where internal value flows form cycles — value moves from address A through intermediary contracts and returns to address A, typically with a small net gain.

**Structural indicators in trace data**:
- Same `from` address in the outermost call and in a terminal value transfer
- Multiple calls to DEX router contracts (identifiable by known contract addresses)
- Net ETH balance change for the initiating address is positive (profit)
- High gas price relative to block median (priority fee competition)

**What the data supports**: Identifying candidate arbitrage transactions by call pattern structure and value flow direction. The trace data contains `from`, `to`, `value`, and `call_type` fields sufficient for this analysis.

**What the data does not support**: Distinguishing token-denominated arbitrage without decoded event logs. ETH-denominated cycles are identifiable; ERC-20 only cycles require additional data (logs or token transfer events).

### Pattern 2: Sandwich Attack Signatures
**Identification method**: Intra-block transaction triples where:
1. Transaction at position i: address M calls a DEX (frontrun)
2. Transaction at position k (i < k): address V calls the same DEX pool (victim)
3. Transaction at position j (k < j): address M calls the same DEX again (backrun)

**Structural indicators in trace data**:
- Same address M appears as `from` in two transactions within the same block
- Both M-transactions interact with the same contract (DEX pool)
- A third-party transaction V is positioned between M's two transactions (by transaction_index)
- M's net position after both transactions shows profit

**What the data supports**: Identifying candidate sandwich patterns by examining transaction ordering within blocks (transaction_index), address reuse, and contract interaction targets. The trace-level `from`, `to`, and `value` fields plus the transaction-level `transaction_index` field enable this analysis.

**What the data does not support**: Confirming trade direction without decoded function selectors. A definitive sandwich identification requires knowing that the frontrun bought and the backrun sold (or vice versa). Structural heuristics (same address, same pool, bracketing position) provide strong candidates but not certainty.

### Pattern 3: Liquidation Signatures
**Identification method**: Transactions containing calls to known lending protocol liquidation functions.

**Structural indicators in trace data**:
- Calls to Aave's `liquidationCall()`, Compound's `liquidateBorrow()`, or Maker's `bite()`/`bark()`
- These are identifiable by the `to` address (known protocol contracts) combined with the function selector in the `input` field (first 4 bytes)
- Liquidation transactions typically show:
  - A call to the lending protocol
  - Internal transfers of collateral tokens
  - Profit extraction via subsequent swap

**What the data supports**: Identifying liquidation calls by target contract address and function selector prefix. The `input` field in traces contains calldata including the 4-byte function selector.

**What the data does not support**: Full decoded parameters (borrower, debt amount, collateral received) without ABI decoding. The structural presence of a liquidation call is identifiable; the economic details require additional decoding.

### Pattern 4: Backrunning Signatures
**Identification method**: Transactions placed immediately after (transaction_index = target + 1) a large DeFi transaction, from a different address, interacting with the same pool.

**Structural indicators in trace data**:
- Transaction at position k: large value DeFi interaction (target)
- Transaction at position k+1: different address, same DEX pool interaction (backrunner)
- Backrunner typically extracts profit from the price impact created by the target

**What the data supports**: Identifying consecutive transaction pairs that share contract interaction targets. This is a weaker signal than sandwich (which has the bracketing structure) but still detectable from trace-level contract interaction data.

**What the data does not support**: Distinguishing intentional backruns from coincidental sequential interactions without additional context (e.g., gas price analysis showing priority fee competition).

## Classification Coverage Assessment

### Estimable Coverage
Based on the structural analysis above and known MEV research literature:
- **Arbitrage**: estimated 2-5% of transactions in MEV-active blocks contain arbitrage patterns (high trace count + cyclic value flow)
- **Sandwich**: estimated 1-3% of blocks contain detectable sandwich triples
- **Liquidation**: estimated <1% of transactions are liquidation calls (dependent on market conditions)
- **Backrunning**: estimated 1-3% of transactions show immediate-successor pattern to large DeFi transactions

These estimates are structural — they represent what the trace data can plausibly identify. Actual MEV prevalence depends on the specific blocks sampled.

### Unclassifiable Fraction
A significant fraction of transactions (~85-95%) will not match any MEV pattern. This includes:
- Simple ETH transfers
- Standard token transfers
- Non-MEV DeFi interactions (user-initiated swaps, deposits, withdrawals)
- Contract deployments
- NFT mints and transfers

This is expected: MEV is a small fraction of total transaction volume but economically significant.

## Derived Metrics

### Trace Complexity as MEV Proxy
- Average traces per transaction: ~7.01
- Transactions with >10 traces: likely DeFi-heavy, higher MEV candidate probability
- Transactions with 1-2 traces: likely simple transfers, low MEV probability

### MEV Type Distribution (Structural Estimate)
Based on known MEV research and the structural indicators available in Xatu trace data:

| MEV Type | Estimated Frequency (of total txs) | Confidence | Data Support |
|----------|-------------------------------------|------------|-------------|
| Arbitrage | 2-5% | Medium | Cyclic value flows detectable in traces |
| Sandwich | 1-3% of blocks | Medium | Intra-block positioning detectable |
| Liquidation | <1% | High | Function selector identification reliable |
| Backrunning | 1-3% | Low | Weaker structural signal, more false positives |

### Value Extraction Observability
- **ETH-denominated MEV**: directly observable from trace value fields (profit = net ETH gain for MEV actor)
- **Token-denominated MEV**: not directly observable from traces alone; requires decoded transfer events or logs
- **Gas costs**: observable from transaction-level gas_price × gas_used, enabling net profit calculation for ETH-denominated MEV

## Caveats

1. **Heuristic classification**: all pattern identification is structural, not ground-truth. False positives and false negatives are expected.
2. **Block range specificity**: block ~20,000,000 represents mid-2023 conditions. MEV patterns, dominant protocols, and builder behavior have evolved since then.
3. **No function decoding**: without full ABI decoding of the `input` field, classification relies on contract address matching and value flow patterns. Function selectors (first 4 bytes) provide partial disambiguation.
4. **No event log correlation**: the trace data alone does not include event logs. Full MEV classification (especially for token-denominated arbitrage) benefits from correlating traces with logs.
5. **Single sample window**: the 1,029,073 traces span ~700 blocks. MEV distribution varies significantly by market regime, gas price environment, and time of day.
6. **Aggregate analysis**: this slice characterizes what the trace data can structurally support for MEV taxonomy. It does not execute per-transaction classification (that requires running actual queries against the parquet data, which is deferred to a follow-on execution slice).
