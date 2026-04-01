#!/bin/zsh
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: scripts/publish_slice.sh <run_id> <agenda item>" >&2
  exit 1
fi

RUN_ID="$1"
shift
AGENDA_ITEM="$*"
RUN_DIR="runs/$RUN_ID"

if [[ ! -d "$RUN_DIR" ]]; then
  echo "Run directory not found: $RUN_DIR" >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository" >&2
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "Git remote 'origin' is not configured" >&2
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ -z "$BRANCH" ]]; then
  echo "Unable to determine current branch" >&2
  exit 1
fi

git add "$RUN_DIR" state/agenda.md state/discovered_backlog.jsonl state/CHANGELOG.md state/results.tsv

if git diff --cached --quiet; then
  echo "No staged changes for slice $RUN_ID" >&2
  exit 1
fi

COMMIT_MSG="research: ${AGENDA_ITEM} (${RUN_ID})"

git commit -m "$COMMIT_MSG"
git push -u origin "$BRANCH"
