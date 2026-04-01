#!/usr/bin/env python3
"""Record and promote curated follow-on agenda candidates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DISCOVERED_PATH = Path("state/discovered_backlog.jsonl")
AGENDA_PATH = Path("state/agenda.md")

PHASE_MARKERS = {
    "Phase 1 — Foundations": (
        "<!-- AUTO-PROMOTED:phase-1:start -->",
        "<!-- AUTO-PROMOTED:phase-1:end -->",
    ),
    "Phase 2 — Extraction and Behavioral Modeling": (
        "<!-- AUTO-PROMOTED:phase-2:start -->",
        "<!-- AUTO-PROMOTED:phase-2:end -->",
    ),
    "Phase 3 — Opportunity and Portability": (
        "<!-- AUTO-PROMOTED:phase-3:start -->",
        "<!-- AUTO-PROMOTED:phase-3:end -->",
    ),
}

REQUIRED_CANDIDATE_KEYS = {
    "title",
    "phase",
    "why_now",
    "parent_run_id",
    "depends_on",
    "tables_needed",
    "feasibility",
    "expected_value",
    "admission",
}

VALID_FEASIBILITY = {"low", "medium", "high"}
VALID_EXPECTED_VALUE = {"low", "medium", "high"}
VALID_ADMISSION = {"promote", "hold", "reject"}


def normalize_title(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def load_discovered_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text().splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number} is not valid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number} must contain a JSON object")
        records.append(record)
    return records


def extract_existing_titles(agenda_text: str, discovered_records: list[dict[str, Any]]) -> set[str]:
    titles: set[str] = set()
    for line in agenda_text.splitlines():
        match = re.match(r"^(?:\d+\.\s+|-\s+)\[[^\]]+\]\s+(.*)$", line.strip())
        if match:
            titles.add(normalize_title(match.group(1)))
    for record in discovered_records:
        title = record.get("title")
        if isinstance(title, str) and record.get("status") in {"promoted", "queued"}:
            titles.add(normalize_title(title))
    return titles


def validate_candidates(candidates: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(candidates, list):
        return ["candidate file must contain a JSON array"]
    if len(candidates) > 3:
        errors.append("candidate file may contain at most 3 candidates")
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            errors.append(f"candidate[{index}] must be an object")
            continue
        missing = sorted(REQUIRED_CANDIDATE_KEYS - set(candidate))
        if missing:
            errors.append(f"candidate[{index}] missing keys: {', '.join(missing)}")
        if candidate.get("phase") not in PHASE_MARKERS:
            errors.append(f"candidate[{index}].phase must match a known phase heading")
        if candidate.get("feasibility") not in VALID_FEASIBILITY:
            errors.append(f"candidate[{index}].feasibility must be one of low, medium, high")
        if candidate.get("expected_value") not in VALID_EXPECTED_VALUE:
            errors.append(f"candidate[{index}].expected_value must be one of low, medium, high")
        if candidate.get("admission") not in VALID_ADMISSION:
            errors.append(f"candidate[{index}].admission must be one of promote, hold, reject")
        if not isinstance(candidate.get("depends_on"), list):
            errors.append(f"candidate[{index}].depends_on must be a list")
        if not isinstance(candidate.get("tables_needed"), list):
            errors.append(f"candidate[{index}].tables_needed must be a list")
    return errors


def render_promoted_item(candidate: dict[str, Any]) -> str:
    depends_on = ", ".join(candidate["depends_on"]) if candidate["depends_on"] else "none"
    tables = ", ".join(candidate["tables_needed"]) if candidate["tables_needed"] else "none"
    return "\n".join(
        [
            f"- [ ] {candidate['title']}",
            f"  Goal: {candidate['why_now']}",
            f"  Source: derived from `{candidate['parent_run_id']}`",
            f"  Depends on: {depends_on}",
            f"  Tables: {tables}",
        ]
    )


def insert_between_markers(text: str, start_marker: str, end_marker: str, block: str) -> str:
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    if start_index == -1 or end_index == -1 or start_index > end_index:
        raise ValueError(f"unable to find marker pair: {start_marker} / {end_marker}")

    insert_at = start_index + len(start_marker)
    existing = text[insert_at:end_index]
    prefix = "\n" if not existing.startswith("\n") else ""
    suffix = "\n" if not block.endswith("\n") else ""
    return text[:insert_at] + prefix + block + suffix + text[end_index:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record and promote follow-on agenda candidates")
    parser.add_argument("candidate_file", help="Path to runs/<run_id>/follow_on_candidates.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidate_path = Path(args.candidate_file)
    if not candidate_path.exists():
        print(f"FAIL: candidate file not found: {candidate_path}", file=sys.stderr)
        return 1

    try:
        candidates = load_json(candidate_path)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate_candidates(candidates)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    try:
        discovered_records = load_discovered_records(DISCOVERED_PATH)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    agenda_text = AGENDA_PATH.read_text()
    known_titles = extract_existing_titles(agenda_text, discovered_records)
    now = datetime.now(timezone.utc).isoformat()

    backlog_records: list[dict[str, Any]] = []
    promoted_blocks: dict[str, list[str]] = {phase: [] for phase in PHASE_MARKERS}

    for candidate in candidates:
        normalized = normalize_title(candidate["title"])
        record = dict(candidate)
        record["candidate_id"] = f"{candidate['parent_run_id']}::{normalized}"
        record["recorded_at"] = now

        if normalized in known_titles:
            record["status"] = "duplicate"
        elif candidate["admission"] == "promote":
            record["status"] = "promoted"
            promoted_blocks[candidate["phase"]].append(render_promoted_item(candidate))
            known_titles.add(normalized)
        elif candidate["admission"] == "hold":
            record["status"] = "queued"
            known_titles.add(normalized)
        else:
            record["status"] = "rejected"

        backlog_records.append(record)

    if backlog_records:
        with DISCOVERED_PATH.open("a", encoding="utf-8") as handle:
            for record in backlog_records:
                handle.write(json.dumps(record, sort_keys=True) + "\n")

    updated_agenda = agenda_text
    for phase, blocks in promoted_blocks.items():
        if not blocks:
            continue
        start_marker, end_marker = PHASE_MARKERS[phase]
        block_text = "\n\n".join(blocks)
        updated_agenda = insert_between_markers(updated_agenda, start_marker, end_marker, block_text)

    if updated_agenda != agenda_text:
        AGENDA_PATH.write_text(updated_agenda)

    print(f"PASS: processed {len(candidates)} candidates from {candidate_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
