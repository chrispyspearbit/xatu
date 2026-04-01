# Architecture

This repository uses a hybrid design because none of the source systems alone are sufficient.

## Design Synthesis

### From Google AI co-scientist

We take the orchestration shape, not the literal implementation:
- specialist roles instead of one undifferentiated agent
- critique and ranking before execution
- explicit reflection after execution
- persistent memory so later loops compound rather than restart

The useful lesson is that research quality goes up when hypothesis generation, criticism, ranking, and synthesis are separated.

### From ChrisGoesGolfing

We take the research discipline:
- one meaningful step at a time
- append-only memory
- explicit keep/discard/pivot decisions
- hard validation gates before updating the canonical state

That pattern matters even more here because data-heavy research can otherwise drift into vague narrative.

### From Ralph Orchestrator

We take the runtime substrate:
- hats for distinct roles
- events for control flow
- persistent tasks and memories
- worktree-based parallel loops when needed

Ralph is the control plane. The repository state is the durable research memory.

## Two-Layer Agenda

The agenda now has two layers:

1. Fixed spine
   - the human-curated phase structure
   - the seeded items that define the program
2. Derived backlog
   - evidence-backed follow-on items discovered during completed slices
   - recorded first in `state/discovered_backlog.jsonl`
   - promoted into `state/agenda.md` only after curation

This keeps the program expandable without letting it drift into undirected brainstorming.

## Topology

```text
research_slice.start
  -> agenda_manager
  -> ranker
  -> hypothesis_generator
  -> critic
  -> executor
  -> validator
  -> reflector
  -> reporter
  -> agenda_expander
  -> agenda_curator
  -> publisher
  -> RESEARCH_SLICE_COMPLETE
```

The loop is intentionally narrow: one slice, one terminal decision, one ledger update, one publish.

## Why One Slice Per Loop

This domain has expensive joins, partial observability, and meaningful feasibility limits. A long autonomous run that tries to clear an entire program backlog is more likely to:
- mix hypotheses together
- lose provenance
- update shared state prematurely
- produce outputs that cannot be validated cleanly

One slice per loop is slower, but it compounds reliably.

## Hard Validation Contract

Every completed run must produce a bundle under `runs/<run_id>/` with:
- `manifest.json`
- `plan.md`
- `evidence.md`
- `follow_on_candidates.json`
- `metrics.json`
- `report.md`

The validator checks:
- required files exist
- required manifest fields exist
- required metrics fields exist
- decision outcome is explicit
- tables and reproducibility metadata are present
- validation checks inside `metrics.json` all pass

If the bundle fails validation, the slice is either revised or marked `BLOCKED`.

## State Model

Human-readable durable state lives in `state/`:
- `agenda.md`: queue and terminal statuses
- `discovered_backlog.jsonl`: raw discovered follow-on items plus admission outcomes
- `CHANGELOG.md`: narrative reasoning and decisions
- `results.tsv`: compact structured ledger

GitHub is the canonical remote record of that state after each validated slice.

Ralph runtime state is intentionally ephemeral:
- `.ralph/`
- `.agent/`
- `.worktrees/`

That separation keeps the research record reviewable in git while allowing Ralph to manage its own loop state.

## Parallel Execution

Parallel work is allowed, but only under a strict merge policy.

Allowed:
- parallel hypothesis ranking
- independent exploratory runs with separate run directories
- separate worktrees for distinct agenda items

Not allowed:
- concurrent edits to `state/agenda.md`
- concurrent appends to `state/discovered_backlog.jsonl`
- concurrent appends to `state/results.tsv`
- concurrent narrative updates to `state/CHANGELOG.md`
- concurrent pushes of canonical state to `origin`

Parallel loops may create candidate run bundles. The primary loop remains the only writer of canonical state.

## Publishing Contract

Publishing is part of completion, not optional follow-up.

After validation and ledger updates, the publisher stages only:
- `runs/<run_id>/`
- `state/agenda.md`
- `state/discovered_backlog.jsonl`
- `state/CHANGELOG.md`
- `state/results.tsv`

Then it creates a structured commit and pushes the current branch to `origin`.

## Expansion Policy

The system is allowed to expand the agenda, but only under strict rules:
- at most three follow-on candidates per slice
- every candidate must cite evidence from the slice that produced it
- promotion is phase-aware and cannot bypass unfinished earlier phases
- duplicates are filtered against the existing agenda and queued backlog
- rejected or held candidates remain visible in `state/discovered_backlog.jsonl`

## Phase Gating

The research program has real dependencies:
- market structure and public/private flow work should come before strategy feasibility
- realized MEV taxonomy should come before builder fingerprinting
- strategy ideas should be downstream of validated opportunity archives

So the orchestrator is required to finish earlier phases, or explicitly block them, before advancing.
