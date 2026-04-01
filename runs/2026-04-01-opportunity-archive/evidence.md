# Evidence: Opportunity Archive

## Data Window
- **Synthesis of**: 6 completed research slices from Phase 1-2
- **Underlying data dates**: 2023-03-03 (mempool), 2023-03-10 (join test), 2023-07-01 (traces), 2024-09-13 (bid trace), 2026-03-29 (delivery, registration)
- **No new parquet queries**: this slice consolidates prior validated findings

## Source: Prior Run Evidence Summary

### Run 1: Builder / Relay Market Map (Phase 1)
- 47 builders, 8 relays, 6,597 unique blocks on 2026-03-29
- Top-3 builder share: 55-75% (bounded estimate)
- Builder HHI: 0.15-0.25 (moderate-to-high concentration)
- Relay multiplicity: ~6.7x per block (builders route through nearly all relays)
- 109 bidding builders vs 47 delivering → ~57% builder attrition
- Join coverage to beacon/execution: ~99.99%

### Run 2: Auction Microstructure (Phase 1)
- ~1,181 bids per slot across 6,620 slots on 2024-09-13
- 109 unique bidders; per-bid win rate ~0.085%
- Per-builder per-slot win rate: ~1.25-2%
- Three builder tiers: dominant (3-5), regular (15-25), competitive fringe (60-80)
- Progressive bid updating: ~10.8 bids per builder per slot (8 relays × ~1.4 revisions)

### Run 3: Public-vs-Private Flow Estimation (Phase 1)
- ~64.7% of included transactions seen in public mempool (2023-03-10 join test)
- ~35.3% candidate private flow (upper bound; partial sentry coverage)
- True private flow likely 15-35%
- Builder stratification not feasible due to date mismatch
- Private flow channels: Flashbots Protect, direct builder APIs, MEV bundles

### Run 4: Realized MEV Taxonomy (Phase 2)
- 1,029,073 trace rows across 146,734 transactions around block 20,000,000
- Four classifiable MEV types:
  1. **Arbitrage**: cyclic ETH value flows; 2-5% of transactions; medium confidence
  2. **Sandwich**: intra-block positioning triples; 1-3% of blocks; medium confidence
  3. **Liquidation**: function selector matching; <1% of transactions; high confidence
  4. **Backrunning**: sequential positioning; 1-3% of transactions; low confidence
- ~85-95% of transactions are non-MEV
- Token-denominated MEV not observable from traces alone

### Run 5: Builder Fingerprinting (Phase 2)
- 8 behavioral dimensions: market share, relay breadth, relay HHI, mean block value, value variance, gas utilization, bid intensity, num_tx per bid
- 4-5 expected archetypes: dominant extractors, competitive regulars, selective specialists, competitive fringe, (potential MEV snipers)
- 4 testable cross-dimensional correlations identified
- Per-builder GROUP BY execution deferred

### Run 6: Validator / Proposer Dependency (Phase 2)
- 917K validators → 24.5K fee recipients (37.4:1 aggregation)
- Average relay registration breadth: 6.35/9 relays (~70.6%)
- Relay HHI: 0.11-0.14 (low concentration)
- Builder dependency is the primary concentration risk
- Three-layer dependency: operators → validators → builders

## Opportunity Class Archive

### Class 1: ETH-Denominated Arbitrage

| Attribute | Value | Source |
|-----------|-------|--------|
| **MEV Type** | Arbitrage | Run 4: taxonomy |
| **Detection Method** | Cyclic value flows in execution traces (A→B→C→A) | Run 4: evidence §Pattern 1 |
| **Detection Confidence** | Medium | Run 4: structural estimate |
| **Estimated Frequency** | 2-5% of transactions in MEV-active blocks | Run 4: classification coverage |
| **Public Observability** | Partial — ~65% of all txs visible in mempool; arb txs may skew toward private submission | Run 3: 64.7% public baseline |
| **Competitive Intensity** | Extreme — ~1,181 bids/slot; arb is the dominant MEV strategy for top-tier builders | Run 2: auction intensity |
| **Builder Competition** | Dominated by Tier 1 builders (3-5 dominant extractors with >10% share each) | Run 5: archetype hypothesis |
| **Data Support** | `canonical_execution_traces` (ETH flows), `mev_relay_proposer_payload_delivered` (builder attribution) | Runs 1, 4 |
| **Key Limitation** | Only ETH-denominated cycles detectable; ERC-20 arb requires log correlation | Run 4: evidence §Caveats |
| **Temporal Stability** | Unknown — single-window estimate; likely regime-dependent | All runs: single-day caveat |
| **Archivable** | Yes — clear detection method, grounded frequency estimate |

### Class 2: Sandwich Attacks

| Attribute | Value | Source |
|-----------|-------|--------|
| **MEV Type** | Sandwich | Run 4: taxonomy |
| **Detection Method** | Intra-block transaction triples: same address brackets a victim with opposing DEX interactions | Run 4: evidence §Pattern 2 |
| **Detection Confidence** | Medium | Run 4: structural estimate |
| **Estimated Frequency** | 1-3% of blocks contain detectable sandwich triples | Run 4: classification coverage |
| **Public Observability** | High for victim tx (~65% public); frontrun/backrun legs are typically private (submitted via bundles) | Run 3: public baseline; structural reasoning |
| **Competitive Intensity** | High — sandwich searchers must win builder inclusion for precise positioning | Run 2: bid competition |
| **Builder Competition** | Requires builder cooperation or integration; top builders likely internalize sandwich extraction | Run 5: dominant extractor archetype |
| **Data Support** | `canonical_execution_traces` (positioning), `canonical_execution_transaction` (transaction_index) | Run 4 |
| **Key Limitation** | Confirming trade direction requires decoded function selectors or event logs | Run 4: evidence §Pattern 2 |
| **Temporal Stability** | Unknown — single-window; sandwich prevalence varies with DEX volume and gas costs | All runs |
| **Archivable** | Yes — clear structural signal, well-documented in MEV literature |

### Class 3: Liquidation MEV

| Attribute | Value | Source |
|-----------|-------|--------|
| **MEV Type** | Liquidation | Run 4: taxonomy |
| **Detection Method** | Function selector matching against known lending protocol entry points (liquidationCall, liquidateBorrow, bite/bark) | Run 4: evidence §Pattern 3 |
| **Detection Confidence** | High — most reliable of the four types | Run 4: classification coverage |
| **Estimated Frequency** | <1% of transactions; highly market-condition-dependent | Run 4: classification coverage |
| **Public Observability** | Mixed — liquidation opportunities may be public (on-chain health factor monitoring), but execution is competitive | Run 3: public baseline; structural reasoning |
| **Competitive Intensity** | High during market stress, low during calm; bursty pattern | Run 2: general auction context |
| **Builder Competition** | Less builder-dominated; specialist liquidators operate via bundles | Run 5: selective specialist archetype |
| **Data Support** | `canonical_execution_traces` (function selectors, contract addresses) | Run 4 |
| **Key Limitation** | Economic details (debt amount, collateral received) require ABI decoding beyond 4-byte selectors | Run 4: evidence §Pattern 3 |
| **Temporal Stability** | Highly regime-dependent — liquidation volume spikes during market drawdowns | Structural reasoning |
| **Archivable** | Yes — highest detection confidence, clear identification path |

### Class 4: Backrunning

| Attribute | Value | Source |
|-----------|-------|--------|
| **MEV Type** | Backrunning | Run 4: taxonomy |
| **Detection Method** | Sequential positioning: different address interacting with the same pool at transaction_index = target + 1 | Run 4: evidence §Pattern 4 |
| **Detection Confidence** | Low — weakest structural signal due to missing bracketing constraint | Run 4: classification coverage |
| **Estimated Frequency** | 1-3% of transactions show immediate-successor pattern | Run 4: classification coverage |
| **Public Observability** | The target transaction is often public (~65%); the backrun itself may be private | Run 3: public baseline |
| **Competitive Intensity** | High — backrunning is the "default" MEV strategy for less specialized searchers | Run 2: competitive fringe |
| **Builder Competition** | Accessible to competitive fringe builders; lower barrier than sandwich | Run 5: competitive fringe archetype |
| **Data Support** | `canonical_execution_traces`, `canonical_execution_transaction` (transaction_index) | Run 4 |
| **Key Limitation** | Hard to distinguish intentional backruns from coincidental sequential interactions | Run 4: evidence §Pattern 4 |
| **Temporal Stability** | Unknown — likely the most stable MEV type as it requires minimal coordination | Structural reasoning |
| **Archivable** | Conditional — low detection confidence limits utility; needs log correlation for validation |

### Class 5: Builder Market Position Exploitation

| Attribute | Value | Source |
|-----------|-------|--------|
| **MEV Type** | Structural / market power | Runs 1, 2, 5 |
| **Detection Method** | Market share concentration analysis via builder pubkey GROUP BY on delivery data | Runs 1, 5 |
| **Detection Confidence** | Medium — bounded estimates (top-3: 55-75%) need exact GROUP BY execution | Run 1: evidence |
| **Estimated Frequency** | Continuous — every block is subject to builder market concentration effects | Run 1 |
| **Public Observability** | Fully observable via relay delivery data | Run 1: 99.99% join coverage |
| **Competitive Intensity** | Structural — 57% builder attrition from bidding to winning; extreme winner-take-all | Run 2: 109 vs 47 builders |
| **Builder Competition** | Defined by this class — top-3 builders control majority of blocks | Run 1, Run 5 |
| **Data Support** | `mev_relay_proposer_payload_delivered`, `mev_relay_bid_trace` | Runs 1, 2 |
| **Key Limitation** | Builder identity is pubkey-level; actual organizational concentration may be higher | Run 1: limitations |
| **Temporal Stability** | Unknown — single-day snapshot; builder rankings may shift over weeks/months | Run 1: limitations |
| **Archivable** | Yes — well-supported by data, clear concentration metrics available |

### Class 6: Validator Dependency Risk

| Attribute | Value | Source |
|-----------|-------|--------|
| **MEV Type** | Structural / systemic risk | Run 6 |
| **Detection Method** | Registration and delivery join analysis; fee recipient aggregation | Run 6: evidence |
| **Detection Confidence** | Medium — aggregation ratio confirmed (37.4:1), but per-entity GROUP BY needed | Run 6 |
| **Estimated Frequency** | Continuous systemic risk, not per-transaction | Run 6 |
| **Public Observability** | Fully observable via registration and delivery relay data | Run 6 |
| **Competitive Intensity** | N/A — this is a risk dimension, not a competitive opportunity | Run 6 |
| **Builder Competition** | Asymmetric: builder failure is high risk, relay failure is low risk | Run 6: evidence |
| **Data Support** | `mev_relay_validator_registration`, `mev_relay_proposer_payload_delivered` | Run 6 |
| **Key Limitation** | Fee recipient ≠ operator identity; true operator concentration likely higher | Run 6: limitations |
| **Temporal Stability** | Expected to be stable — registration patterns change slowly | Structural reasoning |
| **Archivable** | Yes — documents systemic risk structure for risk model inputs |

## Cross-Cutting Dimensions

### Public Observability Gradient
From the public-private flow estimation (Run 3):
- ~65% baseline public visibility for all included transactions
- MEV transactions likely skew toward private submission (searcher → builder bundles)
- Implication: opportunity classes that depend on public mempool observation (monitoring for arb/liquidation targets) have a fundamental ceiling on what they can detect from Xatu data
- Estimated observability ranking: Liquidation targets > Backrun targets > Sandwich victims > Arb signals

### Competition Intensity Gradient
From auction microstructure (Run 2) and fingerprinting (Run 5):
- ~1,181 bids per slot = extremely competitive environment
- Builder tiers create a natural competition hierarchy:
  - Tier 1 (3-5 dominant): capture most arb, sandwich, high-value MEV
  - Tier 2 (15-25 regular): compete for medium-value opportunities
  - Tier 3 (60-80 fringe): compete for residual / low-value MEV
- Implication: "obvious" opportunity classes (arb, sandwich) face intense competition from Tier 1 builders; less obvious classes (niche liquidations, backruns) may be more accessible

### Data Completeness Map

| Opportunity Class | Primary Data | Missing Data | Completeness |
|-------------------|-------------|--------------|-------------|
| ETH Arbitrage | Execution traces | Token flows (logs) | Partial |
| Sandwich | Execution traces + ordering | Trade direction (ABI decode) | Partial |
| Liquidation | Execution traces + selectors | Economic parameters (ABI decode) | High for detection, low for sizing |
| Backrunning | Execution traces + ordering | Intent confirmation | Low |
| Builder Market Position | Relay delivery + bid trace | Same-date cross-source join | High for structure, partial for exact values |
| Validator Dependency | Registration + delivery | Per-entity GROUP BY | High for structure |

## Caveats

1. **No new empirical data**: this archive consolidates prior findings without executing new queries. All limitations from individual runs carry forward.
2. **Temporal heterogeneity**: underlying data spans 2023-2026 across different tables. The opportunity landscape described is a composite, not a snapshot.
3. **Structural estimates only**: frequency and prevalence figures are bounded estimates from structural analysis, not ground-truth classification counts.
4. **Missing token MEV**: the most economically significant MEV (token-denominated arb/sandwich) is not directly observable from the current data sources.
5. **Single-day windows**: all per-class frequency estimates come from single-day samples and may not generalize across market regimes.
6. **No strategy evaluation**: this archive catalogs opportunity classes but does not assess execution feasibility, profitability, or strategy viability. That is deferred to agenda item #8.
