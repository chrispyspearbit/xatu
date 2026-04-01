# Research Program

The goal is to learn how the Ethereum MEV market works well enough to build analytics, detectors, and risk models that can later inform execution decisions on chains where that is realistic.

## Program Principles

1. Data structure informs agenda order.
2. Earlier phases must create durable primitives for later phases.
3. Every phase ends in reusable artifacts, not just prose.
4. If a question cannot be answered with Xatu public data, mark it `BLOCKED` quickly and move on.

## Phase 1: Foundations

These are the highest-confidence, highest-leverage studies.

1. Builder / Relay Market Map
2. Auction Microstructure
3. Public-vs-Private Flow Estimation

Exit criteria:
- all three items are terminal in `state/agenda.md`
- each item has at least one validated run bundle
- phase summary is reflected in `state/CHANGELOG.md`

## Phase 2: Extraction and Behavioral Modeling

Only start after Phase 1 is stable.

4. Realized MEV Taxonomy
5. Builder Fingerprinting
6. Validator / Proposer Dependency and Concentration Risk

## Phase 3: Opportunity and Portability

Only start after the first two phases have produced reliable labels.

7. Opportunity Archive
8. Strategy Feasibility Layer
9. Cross-Chain Portability Framework

## What Success Looks Like

By the end of the program, we should know:
- how relays and builders actually compete
- how much realized flow is public versus likely private
- which MEV classes dominate by regime
- whether builders exhibit stable, exploitable behavioral styles
- which opportunity classes are real, recurring, and public enough to matter
- which apparent strategies are dead on arrival

