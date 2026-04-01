# Xatu MEV Autoresearch

Produce one validated research slice for the highest-priority unresolved agenda item in `state/agenda.md`.

## Objective

Use Xatu public data to build grounded research outputs around MEV market structure, public-vs-private flow, and realized extraction patterns.

This loop is not for speculative strategy writing. It is for evidence-backed research artifacts that can survive scrutiny.

## Inputs You Must Read First

- `research/data-scope.md`
- `research/program.md`
- `specs/phase-01-foundations.spec.md`
- `state/agenda.md`
- `state/discovered_backlog.jsonl`
- `state/CHANGELOG.md`
- `state/results.tsv`
- `docs/architecture.md`

## Operating Model

You are executing exactly one agenda item per run.

### Required flow

1. Read the state files and choose the highest-priority unresolved item in the earliest unfinished phase.
2. Create a run directory at `runs/<run_id>/`.
3. Write a concrete experiment contract:
   - `plan.md`
   - `manifest.json`
4. Execute the research and produce:
   - `evidence.md`
   - `metrics.json`
   - `report.md`
5. Run `python3 scripts/validate_run.py runs/<run_id>`.
6. If validation passes, update:
   - `state/agenda.md`
   - `state/discovered_backlog.jsonl`
   - `state/CHANGELOG.md`
   - `state/results.tsv`
7. Generate and process evidence-backed follow-on candidates:
   - write `runs/<run_id>/follow_on_candidates.json`
   - record all candidates in `state/discovered_backlog.jsonl`
   - promote only admitted candidates into `state/agenda.md`
8. Publish the validated slice to GitHub:
   - run `scripts/publish_slice.sh <run_id> "<agenda item>"`
   - confirm the push to `origin` succeeded
9. Stop after that single agenda item reaches a terminal state.

## Hard Constraints

1. One agenda item per run. Do not combine items.
2. Do not make claims that the Xatu public data cannot support.
3. Every claim must tie back to exact datasets, date ranges, and evidence files.
4. Shared ledgers in `state/` are append-only. Add entries; do not rewrite history.
5. If the data is insufficient, say so and mark the item `BLOCKED` rather than hallucinating a result.
6. Parallel work is allowed only if it writes to isolated `runs/<run_id>/` directories. Shared ledgers are updated only after validation.
7. A slice is not complete until the validated run bundle and updated state have been committed and pushed to GitHub.
8. New agenda items must come from evidence in the completed slice, not generic brainstorming.
9. Propose at most three follow-on candidates per slice.

## Run Bundle Contract

Every run directory must contain:

- `manifest.json`
- `plan.md`
- `evidence.md`
- `follow_on_candidates.json`
- `metrics.json`
- `report.md`

### `manifest.json`

Must include:
- `run_id`
- `phase`
- `question`
- `hypothesis`
- `status`
- `decision`
- `tables_used`
- `artifacts`
- `reproducibility`

### `metrics.json`

Must include:
- `claim_count`
- `source_count`
- `row_count_total`
- `join_coverage`
- `confidence`
- `validation_checks`

## Decision Policy

Every completed slice must end with one outcome:

- `KEEP`: the result is valid and should inform future work
- `DISCARD`: the result is valid but not useful enough to keep as a building block
- `PIVOT`: the result is valid and shows the question should be reframed
- `BLOCKED`: the question cannot currently be answered with available data or infrastructure

## Success Criteria

The loop is complete when:
- one agenda item was taken from `state/agenda.md`
- a run bundle was created under `runs/<run_id>/`
- `scripts/validate_run.py` passed, or the item was explicitly marked `BLOCKED`
- `state/agenda.md`, `state/discovered_backlog.jsonl`, `state/CHANGELOG.md`, and `state/results.tsv` were updated
- `runs/<run_id>/follow_on_candidates.json` was written and processed
- the validated slice was committed and pushed to `origin`

Output `RESEARCH_SLICE_COMPLETE` only after all of the above are true.
