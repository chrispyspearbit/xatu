# Report: Validator / Proposer Dependency and Concentration Risk

## Summary

This study measures relay and builder dependence across the Ethereum validator set using Xatu public relay data from 2026-03-29. The key finding is an **asymmetric dependency structure**: validators have broad relay registration redundancy (average 6.35 of 9 relays) but face significant builder concentration risk (top-3 builders estimated at 55-75% of delivered blocks). Fee recipient aggregation (37.4 validators per fee recipient) means a small number of staking pool operators hold outsized leverage over the relay and builder ecosystem.

## Key Findings

### 1. Relay Registration Is Broadly Distributed

Validators register with an average of 6.35 out of 9 available relays (70.6% breadth). This provides substantial relay-level redundancy: losing 1-2 relays would leave most validators covered. The estimated relay registration HHI is 0.11-0.14, indicating low concentration.

One relay (9th) accepts registrations but delivered no winning blocks on the sample day, functioning as a registration sink.

### 2. Fee Recipient Aggregation Creates Leverage Concentration

The 917,424 registered validators map to only 24,501 fee recipients — a 37.4:1 aggregation ratio. The top-5 fee recipients likely control 50-65% of registered validators, and the top-20 likely control 75-85%.

This means relay and builder ecosystem viability depends on the configuration decisions of a small number of staking pool operators. A single large operator changing their MEV-Boost configuration affects thousands of validators simultaneously.

### 3. Builder Dependency Is the Primary Concentration Risk

From prior validated evidence (Entry #1), the builder market is moderately to highly concentrated:
- Top-1 builder: estimated 20-35% of delivered blocks
- Top-3 builders: estimated 55-75%
- Builder HHI: estimated 0.15-0.25

Validators do not choose builders — MEV-Boost auctions select the highest bidder. But this means all validators share the same builder dependency. If the top builder goes offline, all proposers lose 20-35% of potential MEV revenue with no individual recourse.

### 4. Relay Failure Is Low Risk; Builder Failure Is High Risk

| Scenario | Estimated Impact | Recovery |
|----------|-----------------|----------|
| Top-1 relay offline | <5% block disruption | Rapid (6+ alternative relay paths per block) |
| Top-2 relays offline | 5-15% block disruption | Moderate (most blocks still have 4+ paths) |
| Top-1 builder offline | 20-35% revenue impact | Slow (remaining builders may bid lower) |
| Top-3 builders offline | 55-75% temporary capacity loss | Severe (may trigger local block production fallback) |

The asymmetry is structural: relays are substitutable routing infrastructure, but builders provide unique MEV extraction value that cannot be easily replaced.

### 5. The Dependency Graph Is Three-Layered

```
Staking Pool Operators (24,501 fee recipients)
  ↓ control relay selection for
Validators (917,424 registered)
  ↓ receive blocks from
Builders (47 active) via Relays (8 delivering)
```

Concentration risk compounds across layers: a few operators control relay access for most validators, and a few builders produce most blocks. The relay layer provides genuine redundancy, but the operator and builder layers do not.

## Limitations

1. Single-day window (2026-03-29); all metrics are point-in-time
2. Bounded estimates only — no per-entity GROUP BY queries executed
3. Fee recipient ≠ operator identity (understates true concentration)
4. No revenue/value weighting; block count is the unit
5. Builder identity ambiguity (pubkey ≠ organization)
6. Registration breadth ≠ delivery preference
7. Static analysis; dependencies shift with market conditions

## Decision

**KEEP** — establishes the three-layer dependency structure (operators → validators → builders), quantifies the asymmetric relay vs builder risk, and documents concentration risk scenarios. Serves as a foundation for deeper per-entity analysis in follow-on slices.

## Confidence

**Medium** — structural analysis is well-grounded in observed data dimensions, but all concentration metrics are bounded estimates rather than exact computed values. The qualitative findings (asymmetric risk, operator leverage) are robust; the quantitative bounds need per-entity query execution to narrow.
