# Evidence: Strategy Feasibility Layer

## Data Window
- **Synthesis of**: 7 completed research slices from Phase 1-3
- **Underlying data dates**: 2023-03-03 (mempool), 2023-03-10 (join test), 2023-07-01 (traces), 2024-09-13 (bid trace), 2026-03-29 (delivery, registration)
- **No new parquet queries**: this slice applies a feasibility framework to the Opportunity Archive (Run 7)

## Feasibility Framework

Each opportunity class is scored on four dimensions, then assigned a verdict. All scores are grounded in specific prior run evidence.

### Scoring Definitions

**Recurrence**:
- `recurring`: structural feature of every block or slot (always present)
- `bursty`: depends on external market conditions (intermittent)
- `unknown`: insufficient temporal data to assess

**Public Observability** (from Xatu data):
- `full`: all relevant signals are in public relay/beacon/execution data
- `partial`: some signals observable (~65% baseline from Run 3), key elements may be private
- `insufficient`: critical detection signals are not in Xatu public data

**Competition Barrier** (for independent execution):
- `low`: few active competitors or non-competitive research domain
- `high`: significant competition from specialized searchers
- `extreme`: dominated by Tier 1 builders with >10% market share each

**Data Sufficiency** (for meaningful Xatu-based analysis):
- `strong`: primary data tables available with high join coverage
- `partial`: core data available but key dimensions missing (e.g., token flows, ABI decode)
- `weak`: critical data gaps prevent meaningful analysis

## Per-Class Feasibility Assessment

### Class 1: ETH-Denominated Arbitrage

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Recurrence | recurring | Run 4: arbitrage is a structural feature of any block with DeFi activity; 2-5% of transactions estimated as arb candidates |
| Public Observability | partial | Run 3: ~65% of transactions visible in mempool, but arb transactions likely skew toward private submission via builder bundles. Run 4: cyclic value flows detectable in execution traces post-inclusion |
| Competition Barrier | extreme | Run 2: ~1,181 bids/slot. Run 5: Tier 1 builders (3-5 dominant, >10% share each) internalize most high-value arb. Run 1: top-3 builder share 55-75% |
| Data Sufficiency | partial | Run 4: ETH-denominated cycles detectable in `canonical_execution_traces`. Token-denominated arb (the majority of economic value) requires log correlation not yet available |

**Verdict: MARGINAL**

**Rationale**: ETH arb is detectable and recurring, making it feasible for research analytics (e.g., frequency counting, pattern characterization). However, it is dead on arrival for independent execution: Tier 1 builders dominate extraction, private submission means pre-trade detection is limited, and the most economically significant arb (ERC-20) is not observable. Useful as a research subject, not as a strategy target.

**What would change this**: Token MEV data via trace-log correlation (would expand observable arb universe); temporal stability data (would confirm recurrence assumption).

### Class 2: Sandwich Attacks

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Recurrence | recurring | Run 4: 1-3% of blocks contain detectable sandwich triples; sandwich is a structural feature of DEX activity |
| Public Observability | partial | Run 3: victim transactions are ~65% public, but the frontrun/backrun legs are typically private (submitted via builder bundles). The sandwich attacker's transactions are not observable pre-execution |
| Competition Barrier | extreme | Run 2: requires winning builder inclusion for precise intra-block positioning. Run 5: dominant extractor archetype likely internalizes sandwich extraction. Sandwich requires searcher-builder integration |
| Data Sufficiency | partial | Run 4: structural detection via transaction positioning in `canonical_execution_traces`, but confirming trade direction requires ABI decode or event log correlation not yet available |

**Verdict: DEAD ON ARRIVAL**

**Rationale**: Sandwich execution requires builder cooperation or integration, making it inaccessible to independent operators. Detection is possible post-hoc from execution traces but has limited value without ABI decode to confirm directionality. The pre-execution component (identifying victim transactions before inclusion) is fundamentally limited by the ~35% private flow ceiling — the attacker's own transactions are always private. Not feasible for either research detection or independent execution without builder integration.

**What would change this**: Nothing within Xatu's public data scope. Sandwich strategy requires infrastructure (private builder channel) that is outside the research program's bounds.

### Class 3: Liquidation MEV

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Recurrence | bursty | Run 4: <1% of transactions; highly market-condition-dependent. Liquidation volume spikes during drawdowns and is minimal during calm markets |
| Public Observability | partial | Liquidation opportunities are detectable from on-chain health factors (public), but execution transactions are competitive and often private. Run 3: ~65% public baseline. Run 4: function selector matching has highest detection confidence |
| Competition Barrier | high | Run 2: intense during market stress periods. Specialist liquidators use bundles for priority. Run 5: selective specialist archetype competes in this space |
| Data Sufficiency | partial | Run 4: liquidation detection via function selectors in `canonical_execution_traces` is high confidence. But economic sizing (debt amount, collateral) requires ABI decode beyond 4-byte selectors |

**Verdict: MARGINAL**

**Rationale**: Liquidation has the highest detection confidence of any per-transaction MEV type, making it strong for research analytics (counting, characterizing, tracking market-condition dependence). However, execution is competitive with specialist liquidators, recurrence is regime-dependent (bursty), and economic sizing is limited without ABI decode. Feasible for monitoring and analytics; not realistic for independent execution.

**What would change this**: ABI decode for economic parameters (would enable profit estimation); multi-day temporal analysis (would characterize regime dependence); same-date mempool-execution correlation (would assess pre-execution detectability).

### Class 4: Backrunning

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Recurrence | recurring | Run 4: 1-3% of transactions show immediate-successor pattern; backrunning is the default low-complexity MEV strategy |
| Public Observability | partial | Run 3: target transactions are ~65% public. Run 4: backrun identification relies on sequential positioning, which is observable post-inclusion but ambiguous |
| Competition Barrier | high | Run 2: despite being the most accessible MEV type, competition is still intense at ~1,181 bids/slot. Run 5: competitive fringe builders target this class but face extreme latency competition |
| Data Sufficiency | weak | Run 4: weakest structural signal of all four MEV types. Sequential positioning alone cannot distinguish intentional backruns from coincidental interactions. Log correlation needed for validation |

**Verdict: DEAD ON ARRIVAL**

**Rationale**: Backrunning has the weakest detection signal, making even research analytics unreliable. The sequential positioning heuristic produces high false-positive rates without log correlation for intent confirmation. While the competition barrier is lower than for arb or sandwich, it is still intense. The combination of weak signal and high competition makes this class infeasible for both analytics and execution.

**What would change this**: Log correlation for intent confirmation (would dramatically improve detection precision); MEV-specific labeling data (would enable supervised classification).

### Class 5: Builder Market Position Exploitation

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Recurrence | recurring | Run 1: every slot has a builder competition outcome. Builder market structure is continuous and structural |
| Public Observability | full | Run 1: relay delivery data is 100% observable with ~99.99% join coverage to beacon/execution. Run 6: registration data is fully public |
| Competition Barrier | low | This is a research/analytics class, not a direct execution opportunity. No competition barrier for monitoring and modeling |
| Data Sufficiency | strong | Run 1: `mev_relay_proposer_payload_delivered` supports complete market share analysis. Run 2: `mev_relay_bid_trace` supports competitive dynamics. Run 5: 8-dimensional fingerprinting framework defined. Exact per-builder GROUP BY is the main deferred query |

**Verdict: FEASIBLE**

**Rationale**: Builder market structure is the strongest research target in the entire archive. Data is fully public, continuously generated, and high-fidelity. Analysis does not face execution competition because it is a research/analytics activity (monitoring concentration, tracking market share shifts, modeling builder behavior). The only limitation is temporal — single-day windows need extension for regime analysis. This class should be the primary focus for ongoing research.

**What would change this**: Already feasible. Per-builder GROUP BY execution would move from bounded estimates to exact values. Multi-day windows would establish temporal stability.

### Class 6: Validator Dependency Risk

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Recurrence | recurring | Run 6: validator dependency is a continuous structural feature of the MEV-Boost system. Registration patterns change slowly |
| Public Observability | full | Run 6: registration and delivery data are fully public relay data. Fee recipient aggregation is observable |
| Competition Barrier | low | Risk monitoring is non-competitive; this is an analytics/research class |
| Data Sufficiency | strong | Run 6: `mev_relay_validator_registration` (917K validators, 24.5K fee recipients) and `mev_relay_proposer_payload_delivered` both support this analysis. Per-entity GROUP BY is the main deferred query |

**Verdict: FEASIBLE**

**Rationale**: Validator dependency risk analysis shares the same advantages as builder market position: fully public data, continuous generation, no execution competition, and high data fidelity. The 37.4:1 validator-to-fee-recipient aggregation provides a clear entry point for operator-level concentration analysis. This class is immediately actionable for risk monitoring and model-building.

**What would change this**: Already feasible. Per-fee-recipient GROUP BY would produce exact operator concentration metrics. Multi-day analysis would track registration drift.

## Feasibility Summary Matrix

| # | Class | Recurrence | Observability | Competition | Data | Verdict |
|---|-------|-----------|---------------|-------------|------|---------|
| 1 | ETH Arbitrage | recurring | partial | extreme | partial | MARGINAL |
| 2 | Sandwich Attacks | recurring | partial | extreme | partial | DOA |
| 3 | Liquidation MEV | bursty | partial | high | partial | MARGINAL |
| 4 | Backrunning | recurring | partial | high | weak | DOA |
| 5 | Builder Market Position | recurring | full | low | strong | FEASIBLE |
| 6 | Validator Dependency Risk | recurring | full | low | strong | FEASIBLE |

## Structural Findings

### Finding 1: The Observability-Competition Divide

The six opportunity classes split cleanly into two categories based on a single discriminator: whether the class requires private order flow access for detection or execution.

- **Research-feasible classes** (5, 6): rely entirely on public relay data, face no execution competition, and have strong data support. These are the foundation for ongoing Xatu-based research.
- **Execution-dependent classes** (1, 2, 3, 4): require some combination of private mempool access, builder integration, or ABI-decoded event data. Even when detection is possible post-hoc, the combination of partial observability and extreme competition makes independent execution unrealistic.

This divide is structural, not tactical. It arises from the architecture of MEV-Boost and the asymmetric information advantages of integrated builder-searchers.

### Finding 2: The Analytics vs Execution Distinction

All six classes have some value for analytics and research, but only the two FEASIBLE classes support a full research pipeline (detection → measurement → modeling → monitoring). The MARGINAL classes (ETH arb, liquidation) support partial analytics (detection and counting) but not the full pipeline due to data gaps (token MEV, economic sizing).

### Finding 3: Strategy Space Constraint

The feasibility layer constrains the strategy space for the Xatu research program:
- **Primary research track**: builder and validator ecosystem monitoring (Classes 5, 6)
- **Secondary research track**: MEV detection and characterization analytics (Classes 1, 3)
- **Out of scope**: MEV execution strategy (Classes 2, 4) — these require infrastructure beyond public data

### Finding 4: The Token MEV Bottleneck

Four of six classes are limited by the same data gap: token-denominated MEV requires event log correlation with execution traces. Resolving this single bottleneck (via `canonical_execution_logs` join with `canonical_execution_traces`) would upgrade both MARGINAL classes and potentially reveal new opportunity classes not visible in ETH-only traces.

## Caveats

1. **No temporal validation**: all recurrence assessments are structural reasoning from single-day windows, not empirically validated over multiple market regimes.
2. **Qualitative scoring**: feasibility dimensions are scored categorically, not quantitatively. Boundary cases (e.g., liquidation during market stress) may shift between tiers.
3. **No execution cost modeling**: the competition barrier assessment does not include gas cost, latency, or capital requirements for execution.
4. **Xatu-specific constraints**: feasibility assessments are relative to Xatu public data. A program with access to private builder APIs or full mempool coverage would have different feasibility scores.
5. **Static assessment**: the MEV ecosystem evolves. PBS changes, new builder entrants, or Ethereum protocol changes could alter feasibility scores.
6. **Synthesis only**: no new empirical data; all evidence inherited from prior runs.
