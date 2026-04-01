#!/usr/bin/env python3
"""Validate a research run bundle."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = {
    "manifest.json",
    "plan.md",
    "evidence.md",
    "metrics.json",
    "report.md",
}

REQUIRED_MANIFEST_KEYS = {
    "run_id",
    "phase",
    "question",
    "hypothesis",
    "status",
    "decision",
    "tables_used",
    "artifacts",
    "reproducibility",
}

REQUIRED_ARTIFACT_KEYS = {"plan", "evidence", "metrics", "report"}
VALID_OUTCOMES = {"KEEP", "DISCARD", "PIVOT", "BLOCKED"}
VALID_CONFIDENCE = {"low", "medium", "high"}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def expect(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_manifest(run_dir: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    missing = sorted(REQUIRED_MANIFEST_KEYS - set(manifest))
    expect(not missing, f"manifest.json missing keys: {', '.join(missing)}", errors)

    decision = manifest.get("decision", {})
    outcome = decision.get("outcome")
    expect(outcome in VALID_OUTCOMES, "decision.outcome must be one of KEEP, DISCARD, PIVOT, BLOCKED", errors)

    tables_used = manifest.get("tables_used")
    expect(isinstance(tables_used, list) and tables_used, "tables_used must be a non-empty list", errors)
    if isinstance(tables_used, list):
        for index, table in enumerate(tables_used):
            expect(isinstance(table, dict), f"tables_used[{index}] must be an object", errors)
            if not isinstance(table, dict):
                continue
            for key in ("name", "date_start", "date_end"):
                expect(bool(table.get(key)), f"tables_used[{index}].{key} is required", errors)

    artifacts = manifest.get("artifacts", {})
    missing_artifacts = sorted(REQUIRED_ARTIFACT_KEYS - set(artifacts))
    expect(not missing_artifacts, f"artifacts missing keys: {', '.join(missing_artifacts)}", errors)
    for key in REQUIRED_ARTIFACT_KEYS:
        artifact_path = artifacts.get(key)
        expect(bool(artifact_path), f"artifacts.{key} must be set", errors)
        if artifact_path:
            expect((run_dir / artifact_path).exists(), f"artifacts.{key} points to missing file: {artifact_path}", errors)

    reproducibility = manifest.get("reproducibility", {})
    expect(bool(reproducibility.get("repo_commit")), "reproducibility.repo_commit is required", errors)
    expect(bool(reproducibility.get("created_at")), "reproducibility.created_at is required", errors)


def validate_metrics(metrics: dict[str, Any], errors: list[str]) -> None:
    expect(isinstance(metrics.get("claim_count"), int) and metrics["claim_count"] >= 0, "metrics.claim_count must be a non-negative integer", errors)
    expect(isinstance(metrics.get("source_count"), int) and metrics["source_count"] >= 0, "metrics.source_count must be a non-negative integer", errors)
    expect(isinstance(metrics.get("row_count_total"), int) and metrics["row_count_total"] >= 0, "metrics.row_count_total must be a non-negative integer", errors)

    join_coverage = metrics.get("join_coverage")
    expect(
        join_coverage is None or isinstance(join_coverage, (int, float)) and 0 <= join_coverage <= 1,
        "metrics.join_coverage must be null or a number between 0 and 1",
        errors,
    )

    expect(metrics.get("confidence") in VALID_CONFIDENCE, "metrics.confidence must be one of low, medium, high", errors)

    validation_checks = metrics.get("validation_checks")
    expect(isinstance(validation_checks, list) and validation_checks, "metrics.validation_checks must be a non-empty list", errors)
    if isinstance(validation_checks, list):
        for index, check in enumerate(validation_checks):
            expect(isinstance(check, dict), f"validation_checks[{index}] must be an object", errors)
            if not isinstance(check, dict):
                continue
            expect(bool(check.get("name")), f"validation_checks[{index}].name is required", errors)
            expect(check.get("status") == "pass", f"validation_checks[{index}] must have status=pass", errors)


def validate_text_file(path: Path, label: str, errors: list[str]) -> None:
    expect(path.exists(), f"{label} is missing", errors)
    if not path.exists():
        return
    expect(bool(path.read_text().strip()), f"{label} is empty", errors)


def validate_run(run_dir: Path) -> list[str]:
    errors: list[str] = []
    expect(run_dir.exists() and run_dir.is_dir(), f"{run_dir} is not a directory", errors)
    if errors:
        return errors

    present_files = {path.name for path in run_dir.iterdir() if path.is_file()}
    missing_files = sorted(REQUIRED_FILES - present_files)
    expect(not missing_files, f"run bundle missing files: {', '.join(missing_files)}", errors)
    if missing_files:
        return errors

    manifest_path = run_dir / "manifest.json"
    metrics_path = run_dir / "metrics.json"

    try:
        manifest = load_json(manifest_path)
        expect(isinstance(manifest, dict), "manifest.json must contain an object", errors)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    try:
        metrics = load_json(metrics_path)
        expect(isinstance(metrics, dict), "metrics.json must contain an object", errors)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    if isinstance(manifest, dict):
        validate_manifest(run_dir, manifest, errors)

    if isinstance(metrics, dict):
        validate_metrics(metrics, errors)

    validate_text_file(run_dir / "plan.md", "plan.md", errors)
    validate_text_file(run_dir / "evidence.md", "evidence.md", errors)
    validate_text_file(run_dir / "report.md", "report.md", errors)

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a research run bundle")
    parser.add_argument("run_dir", help="Path to the run directory, for example runs/2026-03-31-market-map")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = Path(args.run_dir)
    errors = validate_run(run_dir)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

