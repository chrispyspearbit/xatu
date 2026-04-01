# Plan: Validator / Proposer Dependency and Concentration Risk

## Research Question

How dependent are Ethereum validators on specific relays and builders for block production, and what concentration risks emerge from these dependencies?

## Hypothesis

Validator relay registration is broadly distributed (most validators register with most relays), but the delivered block pipeline is highly concentrated through a small number of builders. This creates an asymmetric dependency: validators have relay-level redundancy but builder-level concentration risk. Fee recipient aggregation (staking pools) further concentrates the effective decision-making power over relay and builder selection.

## Method

### Step 1: Validator Relay Registration Analysis
- Source: `mev_relay_validator_registration` (2026-03-29)
- Metrics: registration count per relay, validators per relay, relay registration breadth per validator, fee recipient aggregation
- Structural analysis from known scoping data: 917,424 validators, 9 relays, 24,501 fee recipients

### Step 2: Fee Recipient Concentration
- Source: `mev_relay_validator_registration` (2026-03-29)
- Metrics: validators per fee recipient distribution, top-N fee recipient share, fee recipient HHI
- Establishes the effective validator cohort structure (staking pools vs solo validators)

### Step 3: Builder Dependency via Delivered Payloads
- Source: `mev_relay_proposer_payload_delivered` (2026-03-29)
- Join path: proposer_fee_recipient in delivery data links to fee_recipient in registration data
- Metrics: builder concentration per proposer cohort, relay delivery share, single-builder dependency rate

### Step 4: Concentration Risk Scenarios
- What share of blocks would be lost if the top-1, top-3 builders went offline?
- What share of validators would lose relay access if the top-1, top-2 relays went offline?
- How does fee recipient aggregation amplify or dampen these risks?

## Expected Outputs
- Relay registration concentration metrics
- Fee recipient aggregation analysis
- Builder dependency per validator cohort
- Concentration risk scenarios with quantified impact

## Data Window
- Primary: 2026-03-29 (single day, same as prior market map slice)

## Tables
- `mev_relay_validator_registration`
- `mev_relay_proposer_payload_delivered`

## Acceptance Criteria
- Relay registration breadth quantified per validator
- Fee recipient concentration measured (top-N, HHI bounds)
- Builder dependency quantified through delivery data
- At least one concentration risk scenario with quantified impact
- Limitations explicitly documented
