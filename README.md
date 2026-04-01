# Xatu MEV Autoresearch

Autonomous research harness for learning Ethereum MEV market structure from Xatu public data, then turning that understanding into analytics, detectors, and risk models.

This repository is deliberately opinionated:
- Google AI co-scientist contributes the orchestration pattern: generate, critique, rank, execute, reflect.
- ChrisGoesGolfing contributes the operating discipline: one validated step at a time, append-only memory, hard keep/discard gates.
- Ralph Orchestrator contributes the runtime: hats, events, persistent tasks/memories, and optional worktree-based parallel loops.

## What This Repo Is For

We are not trying to trade directly off the public parquet feed. The public export is delayed and partial. We are using it to build a durable research substrate around questions that the data can actually answer:
- builder / relay market structure
- auction microstructure
- public-vs-private flow estimation
- realized MEV taxonomy
- builder fingerprinting
- validator / proposer dependency and concentration risk

The current design assumes one validated research slice per Ralph run. That keeps the loop disciplined and compatible with hard validation.

## Core Rules

1. One agenda item per loop.
2. Every run must end in `KEEP`, `DISCARD`, `PIVOT`, or `BLOCKED`.
3. Every substantive claim must have evidence tied to exact tables, date ranges, and reproducibility metadata.
4. Shared ledgers are append-only.
5. Parallel execution is allowed only for isolated runs that write to separate `runs/<run_id>/` directories and merge back after validation.

## Repository Layout

```text
.
├── PROMPT.md                  # Ralph task prompt for one research slice
├── ralph.yml                  # Ralph orchestration config
├── Makefile                   # Common commands
├── docs/
│   └── architecture.md        # Design rationale and orchestration topology
├── research/
│   ├── data-scope.md          # What Xatu can and cannot support
│   └── program.md             # Phase ordering and long-horizon agenda
├── runs/                      # One directory per validated experiment
├── scripts/
│   ├── publish_slice.sh       # Stages, commits, and pushes one validated slice
│   └── validate_run.py        # Hard validation for run bundles
├── specs/
│   └── phase-01-foundations.spec.md
└── state/
    ├── agenda.md              # Current queue and statuses
    ├── CHANGELOG.md           # Append-only research narrative
    └── results.tsv            # Append-only structured result ledger
```

## Operating Loop

1. Read `research/data-scope.md`, `research/program.md`, and the files in `state/`.
2. Select the highest-priority unresolved item from `state/agenda.md`.
3. Turn it into a concrete experiment contract in `runs/<run_id>/`.
4. Execute the analysis and produce the required run bundle.
5. Run `python3 scripts/validate_run.py runs/<run_id>`.
6. If validation passes, update `state/CHANGELOG.md`, `state/results.tsv`, and `state/agenda.md`.
7. Commit and push the validated slice to GitHub.
8. Stop after that single research slice is resolved.

GitHub is the canonical remote record of validated slices, not just a backup of local work.

## Commands

```bash
# Run one autonomous research slice
ralph run --config ralph.yml

# Validate a completed run bundle
make validate-run RUN=runs/<run_id>

# Publish a completed slice manually, if needed
scripts/publish_slice.sh <run_id> "<agenda item>"
```

## Parallel Execution Policy

Use Ralph's parallel loops sparingly.

Good candidates:
- low-cost hypothesis generation or ranking
- independent agenda items that touch different output directories
- exploratory branches that write only to `runs/<run_id>/`

Bad candidates:
- competing edits to shared ledgers in `state/`
- overlapping long-running analyses on the same question
- anything that depends on an unresolved validation result

The merge boundary is simple: parallel loops may create or update their own run bundles, but only the primary loop updates `state/agenda.md`, `state/CHANGELOG.md`, `state/results.tsv`, and performs the final publish to GitHub.
