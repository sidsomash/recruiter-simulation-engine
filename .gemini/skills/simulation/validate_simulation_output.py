#!/usr/bin/env python3
"""Simulation output validator.

Validates a completed simulation output (its .md file and required .json
sidecar, see simulation_contract.md §11) BEFORE the files are treated as
final, so malformed output is caught immediately instead of being discovered
later, downstream, when the ranking skill silently mis-scores it.

Usage:
    python3 validate_simulation_output.py <path-to-md-or-json-or-base>

`<path>` may be the .md file, the .json file, or the shared base path
without an extension (e.g. "simulations/20260617_153022_data-engineer").
Both the .md and .json files (same base filename) must exist alongside
each other.

Exit code 0 = valid. Exit code 1 = invalid (details printed to stdout).

Stdlib-only (json, re, sys, pathlib) - no external packages, no virtualenv
required. Requires Python 3.8+.
"""
import json
import re
import sys
from pathlib import Path

REQUIRED_MD_SECTIONS = [
    "## 0. Metadata",
    "## 1. Recruiter Takeaway",
    "## 2. Skill & Responsibility Mapping",
    "## 3. Skill Gaps",
    "## 4. Years-of-Experience Mapping",
    "## 5. Degree Requirement Mapping",
    "## 6. Preference Violations",
    "## 7. Recruiter Decision",
    "## 8. Final Fit Summary",
]

REQUIRED_JSON_KEYS = [
    "company", "title", "posting_date", "compensation", "location",
    "years_required", "degree_match", "skill_alignment", "experience_match",
    "preference_violations", "recruiter_pct", "interview_pct",
    "fit_category", "internship_mode", "contract_version",
]

# Allowed enum values, mirroring simulation_contract.md §11 and the
# JSON_*_POINTS maps in run_ranking.py — keep these in sync with both.
ALLOWED_DEGREE_MATCH = {"direct", "equivalent", "partial", "no_match", "hard_mismatch", "not_specified"}
ALLOWED_SKILL_ALIGNMENT = {"high", "moderate", "low", "major_gaps"}
ALLOWED_EXPERIENCE_MATCH = {"meets", "partially_meets", "does_not_meet"}
ALLOWED_FIT_CATEGORY = {"strong_match", "moderate_match", "weak_match", "mismatch", "hard_reject"}
ALLOWED_SEVERITY = {"minor", "moderate", "major", "clearance"}


def resolve_paths(raw_path):
    """Given a .md path, .json path, or extension-less base path, return
    (md_path, json_path) — both Path objects, regardless of which was given."""
    p = Path(raw_path)
    if p.suffix == ".md":
        return p, p.with_suffix(".json")
    if p.suffix == ".json":
        return p.with_suffix(".md"), p
    return p.with_suffix(".md"), p.with_suffix(".json")


def validate_markdown(md_path):
    errors = []
    if not md_path.exists():
        return [f"Markdown file not found: {md_path}"]

    text = md_path.read_text(encoding="utf-8")
    for section in REQUIRED_MD_SECTIONS:
        if section not in text:
            errors.append(f"Missing required Markdown section: '{section}'")

    if "No preference file provided" not in text:
        violations_block = re.search(
            r"## 6\. Preference Violations(.*?)(?:\n---|\Z)", text, re.S)
        if violations_block and not violations_block.group(1).strip():
            errors.append(
                "Section 6 (Preference Violations) is empty and does not state "
                "'No preference file provided — no violations evaluated.'"
            )

    recruiter_m = re.search(r"\*\*Recruiter Screen Likelihood:\*\*\s*(\S+)", text)
    interview_m = re.search(r"\*\*Interview Likelihood:\*\*\s*(\S+)", text)
    if not recruiter_m:
        errors.append("Missing '**Recruiter Screen Likelihood:**' value in section 7.")
    elif not re.fullmatch(r"\d+%", recruiter_m.group(1)):
        errors.append(
            f"Recruiter Screen Likelihood value '{recruiter_m.group(1)}' is not an "
            "integer percentage (e.g. '70%')."
        )
    if not interview_m:
        errors.append("Missing '**Interview Likelihood:**' value in section 7.")
    elif not re.fullmatch(r"\d+%", interview_m.group(1)):
        errors.append(
            f"Interview Likelihood value '{interview_m.group(1)}' is not an "
            "integer percentage (e.g. '65%')."
        )

    return errors


def _check_percentage(errors, data, key):
    if key not in data:
        return
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"'{key}' must be an integer 0-100 (got {value!r}).")
        return
    if not (0 <= value <= 100):
        errors.append(f"'{key}' must be within 0-100 (got {value}).")


def validate_json(json_path):
    errors = []
    if not json_path.exists():
        return [f"JSON sidecar not found: {json_path}"]

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON sidecar is not valid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["JSON sidecar root must be an object."]

    for key in REQUIRED_JSON_KEYS:
        if key not in data:
            errors.append(f"Missing required JSON key: '{key}'")

    def _check_enum(key, allowed):
        if key in data and data[key] not in allowed:
            errors.append(
                f"'{key}' value {data[key]!r} is not one of the allowed values: "
                f"{sorted(allowed)}"
            )

    _check_enum("degree_match", ALLOWED_DEGREE_MATCH)
    _check_enum("skill_alignment", ALLOWED_SKILL_ALIGNMENT)
    _check_enum("experience_match", ALLOWED_EXPERIENCE_MATCH)
    _check_enum("fit_category", ALLOWED_FIT_CATEGORY)

    _check_percentage(errors, data, "recruiter_pct")
    _check_percentage(errors, data, "interview_pct")

    if "internship_mode" in data and not isinstance(data["internship_mode"], bool):
        errors.append(
            f"'internship_mode' must be a boolean (got {data['internship_mode']!r})."
        )

    if "preference_violations" in data:
        violations = data["preference_violations"]
        if not isinstance(violations, list):
            errors.append("'preference_violations' must be a list.")
        else:
            for i, v in enumerate(violations):
                if not isinstance(v, dict):
                    errors.append(f"preference_violations[{i}] must be an object.")
                    continue
                if "severity" not in v or "description" not in v:
                    errors.append(
                        f"preference_violations[{i}] must have 'severity' and 'description' keys."
                    )
                    continue
                if v["severity"] not in ALLOWED_SEVERITY:
                    errors.append(
                        f"preference_violations[{i}].severity {v['severity']!r} is not one "
                        f"of the allowed values: {sorted(ALLOWED_SEVERITY)}"
                    )

    # recruiter_pct must be present to compare against interview_pct's clamp rule.
    if (
        isinstance(data.get("recruiter_pct"), int)
        and isinstance(data.get("interview_pct"), int)
        and not isinstance(data.get("recruiter_pct"), bool)
        and not isinstance(data.get("interview_pct"), bool)
        and data["interview_pct"] > data["recruiter_pct"]
    ):
        errors.append(
            f"'interview_pct' ({data['interview_pct']}) must not exceed "
            f"'recruiter_pct' ({data['recruiter_pct']}) per contract §8.3."
        )

    return errors


def validate_cross_file(md_path, json_path, md_errors, json_errors):
    """Only run if both files independently parsed without structural errors —
    checks that sidecar values agree exactly with the Markdown (contract §11's
    consistency rule)."""
    if md_errors or json_errors or not md_path.exists() or not json_path.exists():
        return []

    errors = []
    text = md_path.read_text(encoding="utf-8")
    data = json.loads(json_path.read_text(encoding="utf-8"))

    recruiter_m = re.search(r"\*\*Recruiter Screen Likelihood:\*\*\s*(\d+)%", text)
    interview_m = re.search(r"\*\*Interview Likelihood:\*\*\s*(\d+)%", text)
    if recruiter_m and int(recruiter_m.group(1)) != data.get("recruiter_pct"):
        errors.append(
            f"Markdown Recruiter Screen Likelihood ({recruiter_m.group(1)}%) does not match "
            f"JSON recruiter_pct ({data.get('recruiter_pct')})."
        )
    if interview_m and int(interview_m.group(1)) != data.get("interview_pct"):
        errors.append(
            f"Markdown Interview Likelihood ({interview_m.group(1)}%) does not match "
            f"JSON interview_pct ({data.get('interview_pct')})."
        )

    version_m = re.search(r"-\s*Contract Version:\s*(.+)", text)
    if version_m and version_m.group(1).strip() != data.get("contract_version"):
        errors.append(
            f"Markdown Contract Version ({version_m.group(1).strip()!r}) does not match "
            f"JSON contract_version ({data.get('contract_version')!r})."
        )

    return errors


def validate(raw_path):
    md_path, json_path = resolve_paths(raw_path)
    md_errors = validate_markdown(md_path)
    json_errors = validate_json(json_path)
    cross_errors = validate_cross_file(md_path, json_path, md_errors, json_errors)
    all_errors = md_errors + json_errors + cross_errors
    return all_errors, md_path, json_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_simulation_output.py <path-to-md-or-json-or-base>")
        return 1

    errors, md_path, json_path = validate(sys.argv[1])

    if not errors:
        print(f"VALID: {md_path.name} + {json_path.name} pass all structural, enum, and "
              "cross-file consistency checks.")
        return 0

    print(f"INVALID: {md_path.name} + {json_path.name} — {len(errors)} issue(s) found:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
