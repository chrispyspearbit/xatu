# Evidence: Cross-Chain Portability Framework

## Data Window
- **Synthesis of**: 8 completed research slices from Phase 1-3
- **Underlying data dates**: 2023-03-03 (mempool), 2023-03-10 (join test), 2023-07-01 (traces), 2024-09-13 (bid trace), 2026-03-29 (delivery, registration)
- **No new parquet queries**: this slice classifies prior methods and data dependencies for cross-chain portability

## Portability Framework

Each research method from Runs 1-8 is assessed on three dimensions: method portability, data dependency, and infrastructure assumptions. The classification determines what transfers to other chains and what is Ethereum-specific.

### Portability Tiers

- **PORTABLE**: methodology applies with minimal modification to any chain with analogous market structure data
- **ADAPTABLE**: core analytical approach transfers but requires chain-specific data schema mappings and parameter calibration
- **ETHEREUM-SPECIFIC**: depends on Ethereum-unique infrastructure (MEV-Boost, relay protocol, EVM trace format)

## Per-Method Portability Assessment

### Method 1: Builder / Relay Market Map (Run 1)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **ADAPTABLE** | The core methodology — measure market share, concentration (HHI, top-N), overlap, and churn among block producers — is universal market structure analysis. Run 1 used GROUP BY on builder pubkey and relay name, which is a generic aggregation pattern. However, the specific entity taxonomy (builder vs relay vs proposer) is MEV-Boost-specific |
| Data Dependency | Requires: block producer identity, block assignment records, intermediary routing data | Run 1 used `mev_relay_proposer_payload_delivered` (44,039 rows, 47 builders, 8 relays) and `mev_relay_validator_registration` (917K validators). Functional equivalents needed: block attribution table + intermediary routing table |
| Infrastructure Assumptions | MEV-Boost relay architecture, proposer-builder separation, relay multiplicity (~6.7x per block) | The relay-multiplicity concept (builders routing through multiple relays) is specific to MEV-Boost. Chains without relay intermediaries would skip this dimension entirely |

**Portable Components**: concentration metrics (HHI, top-N share), market share GROUP BY, multi-entity overlap analysis
**Chain-Specific Components**: relay routing breadth, relay multiplicity, proposer-builder separation taxonomy

### Method 2: Auction Microstructure (Run 2)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **ADAPTABLE** | The core methodology — measure competition intensity, bid distribution, and win rates — applies to any system with observable competitive block production. Run 2 analyzed ~1,181 bids per slot across 109 builders. The concept of bids-per-slot, builder-per-slot win rates, and progressive bid updating are generic auction analysis |
| Data Dependency | Requires: per-bid records with builder identity, slot/block assignment, timestamps | Run 2 used `mev_relay_bid_trace` (7.8M rows, 6,620 slots). Functional equivalent needed: block auction bid log |
| Infrastructure Assumptions | Sealed-bid auction via relays, slot-based timing, progressive bid revision across relays | The auction mechanism (MEV-Boost sealed bid with relay-mediated delivery) is Ethereum-specific. Other chains may have different auction formats: Solana's continuous leader schedule, L2 sequencer priority ordering, or first-come-first-serve models |

**Portable Components**: competition intensity metrics, win rate analysis, bid count distributions, tiered market segmentation (dominant/competitive/fringe)
**Chain-Specific Components**: slot-based timing, relay-mediated sealed bid format, progressive bid revision model

### Method 3: Public-vs-Private Flow Estimation (Run 3)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **PORTABLE** | The core methodology — join pre-inclusion observations with post-inclusion canonical records on transaction hash to estimate public visibility — is universally applicable. Run 3 executed a same-day left join yielding ~64.7% public visibility. Any chain with a public transaction propagation layer and inclusion records supports this method |
| Data Dependency | Requires: pre-inclusion transaction observations, post-inclusion canonical records, joinable on transaction identifier | Run 3 used `mempool_transaction` (1.09M rows) and `canonical_execution_transaction` (46K rows). Functional equivalents: any mempool monitoring source + any canonical inclusion table |
| Infrastructure Assumptions | Xatu sentry network provides partial mempool coverage; public P2P gossip exists for transaction propagation | The assumption that some transactions propagate publicly before inclusion is valid for any chain with a public P2P layer. Chains with fully private transaction submission (some L2s with centralized sequencers) would yield 0% public visibility by design |

**Portable Components**: left-join methodology on tx hash, visibility ratio calculation, coverage caveats framework
**Chain-Specific Components**: sentry network coverage characteristics, P2P gossip protocol specifics

### Method 4: Realized MEV Taxonomy (Run 4)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **ADAPTABLE** | The four-type taxonomy (arbitrage, sandwich, liquidation, backrunning) captures generic MEV classes present on any chain with DEX activity. Run 4 used structural detection heuristics: cyclic value flows for arb, intra-block positioning for sandwich, function selectors for liquidation, sequential positioning for backruns. The heuristic approach transfers but parameters are chain-specific |
| Data Dependency | Requires: execution traces with internal calls, transaction ordering within blocks, function selectors or equivalent | Run 4 used `canonical_execution_traces` (1.03M rows across 146K transactions). EVM traces are specific to EVM-compatible chains. Non-EVM chains need equivalent execution introspection |
| Infrastructure Assumptions | EVM execution model with CALL/DELEGATECALL/STATICCALL trace hierarchy, 4-byte function selectors, ETH-denominated value fields in traces | The trace format is EVM-specific. Move-based chains (Aptos, Sui) have different execution models. Solana's instruction-based execution produces different trace structures |

**Portable Components**: four-type MEV taxonomy as a classification framework, the concept of structural detection heuristics, confidence-level classification methodology
**Chain-Specific Components**: EVM trace format, function selector matching, ETH value field semantics, CALL-type hierarchy

### Method 5: Builder Fingerprinting (Run 5)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **PORTABLE** | The core methodology — characterize block producers along multiple behavioral dimensions and cluster into archetypes — is universal behavioral analysis. Run 5 defined 8 dimensions (market share, relay routing breadth, relay HHI, mean block value, block value variance, gas utilization, bid intensity, num_tx per bid) and hypothesized 4-5 archetypes. Behavioral clustering on observable dimensions applies to any system with identifiable block producers |
| Data Dependency | Requires: per-block-producer delivery records, auction/bid records, block content metadata | Run 5 used `mev_relay_proposer_payload_delivered` and `mev_relay_bid_trace`. Functional equivalents: block attribution + auction participation records |
| Infrastructure Assumptions | Identifiable builders via pubkey, relay-mediated routing, gas as the block capacity unit | Builder identity is clear in MEV-Boost but may be ambiguous in other systems (e.g., L2 sequencers are typically single entities, making fingerprinting trivial or meaningless) |

**Portable Components**: multi-dimensional behavioral profiling framework, archetype hypothesis methodology, cross-dimensional correlation analysis
**Chain-Specific Components**: relay routing dimensions (2 of 8 dimensions), gas utilization metric, specific dimension set selection

### Method 6: Validator / Proposer Dependency and Concentration Risk (Run 6)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **PORTABLE** | The core methodology — map dependency chains across layers (operator → validator → builder via intermediary) and quantify concentration at each layer — is generic supply chain risk analysis. Run 6 identified the 37.4:1 aggregation ratio and asymmetric relay vs builder risk. The three-layer dependency model applies to any system with delegation and intermediation |
| Data Dependency | Requires: validator/staker registration records, block producer delivery records, operator aggregation identifiers | Run 6 used `mev_relay_validator_registration` (5.8M rows, 917K validators, 24.5K fee recipients) and `mev_relay_proposer_payload_delivered`. Functional equivalents: staker/delegator registration + block production attribution |
| Infrastructure Assumptions | MEV-Boost relay registration, proposer-builder separation, fee_recipient as operator proxy | The specific dependency path (validator registers with relay, relay routes to builder) is MEV-Boost-specific. But the pattern — delegators depend on operators who depend on block producers — exists on any PoS chain |

**Portable Components**: multi-layer dependency graph methodology, concentration compounding analysis, asymmetric risk assessment framework, operator aggregation ratio analysis
**Chain-Specific Components**: relay registration as intermediary layer, fee_recipient as operator proxy, MEV-Boost-specific dependency path

### Method 7: Opportunity Archive (Run 7)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **PORTABLE** | The archive methodology — catalog opportunity classes with structured attributes (detection method, observability, competition, data support, temporal stability) — is universal research documentation. Run 7 synthesized 6 classes from 6 prior runs into a standardized library. This approach applies to any chain's MEV landscape |
| Data Dependency | Requires: completed prior research runs with classified findings | This is a synthesis method that operates on prior research outputs, not raw data |
| Infrastructure Assumptions | None beyond the assumption that MEV opportunity classes exist on the target chain | The specific classes cataloged (ETH arb, sandwich, liquidation, backrunning, builder position, validator dependency) are Ethereum-flavored but the classification structure is universal |

**Portable Components**: structured opportunity classification schema, multi-attribute characterization methodology, evidence-grounding requirement
**Chain-Specific Components**: specific opportunity class names and descriptions

### Method 8: Strategy Feasibility Layer (Run 8)

| Dimension | Classification | Evidence |
|-----------|---------------|----------|
| Method Portability | **PORTABLE** | The feasibility framework — score each opportunity class on recurrence, observability, competition barrier, and data sufficiency to produce a verdict (FEASIBLE / MARGINAL / DOA) — is universal decision-making methodology. Run 8 produced a clear three-tier ranking. This approach applies to any chain's opportunity set |
| Data Dependency | Requires: completed opportunity archive with evidence-backed attributes | Synthesis method operating on prior outputs |
| Infrastructure Assumptions | None beyond the existence of competitive block production and observable market data | The specific verdicts are Ethereum-specific (e.g., "sandwich is DOA because it requires builder integration") but the scoring framework transfers |

**Portable Components**: four-dimension feasibility scoring framework, three-tier verdict system, observability-competition divide concept
**Chain-Specific Components**: specific verdict rationales, competition barrier calibration, observability baseline values

## Portability Summary Matrix

| # | Method | Portability | Portable Core | Adaptation Required |
|---|--------|------------|---------------|---------------------|
| 1 | Builder/Relay Market Map | ADAPTABLE | Concentration metrics, market share analysis | Entity taxonomy (builder/relay/proposer), relay-specific dimensions |
| 2 | Auction Microstructure | ADAPTABLE | Competition intensity, win rates, bid distributions | Auction format (sealed-bid vs continuous), timing model |
| 3 | Public-vs-Private Flow | PORTABLE | Left-join methodology, visibility ratio | Sentry/monitoring source, P2P protocol |
| 4 | Realized MEV Taxonomy | ADAPTABLE | Four-type taxonomy framework, heuristic methodology | Trace format (EVM vs Move vs instruction), selector matching |
| 5 | Builder Fingerprinting | PORTABLE | Multi-dimensional profiling, archetype clustering | Dimension set selection, identity model |
| 6 | Dependency/Concentration Risk | PORTABLE | Multi-layer dependency graph, asymmetric risk analysis | Dependency path topology, operator proxy |
| 7 | Opportunity Archive | PORTABLE | Structured classification schema | Specific class catalog |
| 8 | Strategy Feasibility Layer | PORTABLE | Four-dimension scoring framework | Verdict calibration, baseline values |

## Infrastructure Assumption Inventory

The following Ethereum-specific assumptions are embedded across the research program:

### 1. MEV-Boost and Proposer-Builder Separation (PBS)
- **Used in**: Runs 1, 2, 5, 6 (4 of 8 methods)
- **Assumption**: block building is separated from block proposing via a relay-mediated auction
- **Impact on portability**: chains without PBS have simpler block production (no relay layer, no sealed-bid auction) — Methods 1, 2 lose relay-specific dimensions but retain core market analysis
- **Chains with PBS-like mechanisms**: potential future L1s adopting enshrined PBS, any chain with external block building services

### 2. Relay Architecture
- **Used in**: Runs 1, 2, 5, 6 (4 of 8 methods)
- **Assumption**: relays serve as trusted intermediaries that aggregate bids and verify block validity
- **Impact on portability**: the relay layer is a unique Ethereum feature. Relay-specific metrics (routing breadth, relay HHI, registration patterns) do not transfer. However, the concept of intermediary routing analysis transfers to any system with analogous intermediaries
- **Chains without relays**: most chains. The relay layer drops entirely from the analysis

### 3. EVM Execution Model
- **Used in**: Run 4 (1 of 8 methods)
- **Assumption**: transactions produce traces with CALL/DELEGATECALL/STATICCALL hierarchy, 4-byte function selectors, and ETH-denominated value fields
- **Impact on portability**: MEV taxonomy heuristics must be rewritten for non-EVM chains. Move-based chains have different execution models (modules, resources, entry functions). Solana has instruction-level execution traces
- **EVM-compatible chains**: L2 rollups, sidechains — these can reuse Run 4's heuristics directly

### 4. Xatu Sentry Network
- **Used in**: Run 3 (1 of 8 methods)
- **Assumption**: Xatu operates sentry nodes that observe P2P gossip and record pre-inclusion transaction observations
- **Impact on portability**: the sentry network is Ethereum-specific infrastructure. However, the methodology (join pre-inclusion observations with post-inclusion records) works with any mempool monitoring source
- **Functional equivalents**: any chain-specific mempool monitoring service, transaction gossip recording

### 5. Slot-Based Consensus Timing
- **Used in**: Runs 1, 2, 6 (3 of 8 methods)
- **Assumption**: Ethereum produces blocks on 12-second slot boundaries
- **Impact on portability**: timing analysis must recalibrate for different block times (Solana: 400ms, L2s: variable, other L1s: various)
- **Adaptation**: replace slot-based timing with chain-specific block production timing

## Cross-Chain Architecture Family Assessment

### Family A: PBS Chains (full relay-mediated block building)
- **Methods transferable**: all 8 (5 directly, 3 with dimension adaptation)
- **Data schema mapping**: relay delivery → block delivery, bid trace → auction bids, registration → staking/delegation
- **Key difference**: relay implementation details, auction timing, builder set composition
- **Portability effort**: LOW — mostly parameter recalibration
- **Current examples**: Ethereum is currently the only production chain with full relay-mediated PBS. Potential future candidates if other L1s adopt enshrined PBS

### Family B: Integrated Builder Chains (monolithic block production)
- **Methods transferable**: 5 of 8 directly (Methods 3, 5, 6, 7, 8); Methods 1, 4 partially; Method 2 drops
- **Missing data**: no auction bids (no competitive block building auction), no relay layer
- **Adaptations needed**: market map becomes validator/sequencer concentration analysis (Method 1 simplifies). Auction microstructure (Method 2) has no equivalent — block production is not auctioned. MEV taxonomy (Method 4) needs chain-specific trace format
- **Key difference**: MEV extraction is internalized by validators/sequencers rather than externalized to builders
- **Portability effort**: MEDIUM — core analytics transfer, auction-specific methods need rethinking
- **Examples**: Solana (leader schedule), most L2 sequencers (centralized)

### Family C: EVM-Compatible L2s (shared execution, different block production)
- **Methods transferable**: 6 of 8 directly (Methods 3, 4, 5, 6, 7, 8); Methods 1, 2 partially
- **Advantage**: EVM trace format is identical — Run 4's MEV taxonomy heuristics transfer without modification
- **Missing data**: typically no competitive block auction (single sequencer), no relay layer
- **Adaptations needed**: market map (Method 1) becomes sequencer analysis. Auction (Method 2) may not apply
- **Key difference**: centralized sequencer means concentration risk is trivially maximal, and public-vs-private flow estimation is bounded by sequencer's private mempool policy
- **Portability effort**: LOW for execution analysis, LOW-MEDIUM for market structure
- **Examples**: Optimism, Arbitrum, Base, zkSync

## Structural Findings

### Finding 1: Methodology Is More Portable Than Data

5 of 8 methods are classified PORTABLE — their analytical frameworks transfer without modification. The portability bottleneck is not methodology design but data schema availability. A chain that publishes block attribution data, auction records, and execution traces enables immediate application of most methods. A chain that publishes only block headers limits analysis to basic concentration metrics.

### Finding 2: The Relay Layer Is a Uniquely Ethereum Feature

4 of 8 methods use relay-specific data (routing breadth, relay HHI, registration patterns). These relay dimensions are Ethereum-specific and drop entirely from the analysis on other chains. However, the core analysis (concentration, dependency, competition) survives because relay data provides additional dimensions, not the only dimensions.

### Finding 3: EVM Execution Portability Is Binary

MEV taxonomy heuristics (Method 4) either transfer completely (EVM-compatible chains) or require complete rewrite (non-EVM chains). There is no partial transfer — the trace format, function selector matching, and value field semantics are all EVM-specific. This creates a clean decision boundary: EVM or not.

### Finding 4: Centralized Block Production Simplifies Some Questions

Chains with single-entity block production (most L2s, some L1s) make concentration analysis trivial (HHI = 1.0, top-1 share = 100%). However, this doesn't eliminate the value of dependency analysis — understanding who depends on the single producer and what happens if they fail remains important. The fingerprinting and feasibility frameworks still apply, though with different implications.

### Finding 5: The Portability Framework Itself Is the Most Portable Output

The structured classification approach — assessing methods on portability, data dependency, and infrastructure assumptions — is a reusable framework for evaluating any research program's cross-chain transferability. This meta-methodology is fully PORTABLE and could be applied to future research programs on different domains.

## Caveats

1. **No empirical validation**: portability is assessed structurally based on architectural analysis, not tested on actual non-Ethereum data.
2. **Representative chain families**: the three families (PBS, integrated, EVM L2) do not cover all architectures (e.g., DAG-based chains, sharded chains, Cosmos appchains).
3. **No data availability assessment**: we do not verify that candidate chains actually publish the data schemas needed for portable methods.
4. **Static assessment**: chain architectures evolve. L2s may adopt competitive sequencing, new L1s may adopt PBS.
5. **Synthesis only**: no new data; all evidence inherited from prior runs.
6. **Ethereum bias**: the research program was designed for Ethereum, so the portability assessment inherently starts from Ethereum's architecture.
