# Research Queue

Status key:
- `[ ]` queued
- `[~]` in progress
- `[K]` validated and kept
- `[X]` validated and discarded
- `[B]` blocked by data or infrastructure limits

## Phase 1 — Foundations

### Seeded Items

1. [K] Builder / Relay Market Map
   Goal: quantify builder share, relay share, overlap, concentration, and churn.
   Core tables: `mev_relay_proposer_payload_delivered`, `mev_relay_validator_registration`, `mev_relay_bid_trace`
   Acceptance: one validated run with explicit market-share metrics and concentration metrics.

2. [K] Auction Microstructure
   Goal: characterize bid timing, competition per slot, and the relationship between bids and delivered outcomes.
   Core tables: `mev_relay_bid_trace`, `mev_relay_proposer_payload_delivered`
   Acceptance: one validated run with slot-level timing distributions and win-pattern analysis.

3. [K] Public-vs-Private Flow Estimation
   Goal: estimate what share of included flow appears in the public mempool and how that varies by context.
   Core tables: `mempool_transaction`, `canonical_execution_transaction`, `mev_relay_proposer_payload_delivered`
   Acceptance: one validated run with coverage estimates, methodology, and caveats.

### Promoted Items

<!-- AUTO-PROMOTED:phase-1:start -->
<!-- AUTO-PROMOTED:phase-1:end -->

## Phase 2 — Extraction and Behavioral Modeling

### Seeded Items

4. [K] Realized MEV Taxonomy
   Goal: classify realized MEV patterns from canonical execution traces and logs.

5. [K] Builder Fingerprinting
   Goal: cluster builders by stable block-construction style and MEV composition.

6. [ ] Validator / Proposer Dependency and Concentration Risk
   Goal: measure relay and builder dependence across validator cohorts.

### Promoted Items

<!-- AUTO-PROMOTED:phase-2:start -->
<!-- AUTO-PROMOTED:phase-2:end -->

## Phase 3 — Opportunity and Portability

### Seeded Items

7. [ ] Opportunity Archive
   Goal: turn validated classifications into a historical opportunity library.

8. [ ] Strategy Feasibility Layer
   Goal: estimate which opportunity classes are recurring, public enough, and not obviously dead on arrival.

9. [ ] Cross-Chain Portability Framework
   Goal: separate chain-specific heuristics from portable research methodology.

### Promoted Items

<!-- AUTO-PROMOTED:phase-3:start -->
<!-- AUTO-PROMOTED:phase-3:end -->
