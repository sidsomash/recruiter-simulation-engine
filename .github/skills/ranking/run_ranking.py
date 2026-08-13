#!/usr/bin/env python3
"""Ranking skill runner.

Reads all simulation outputs from ../simulation/simulations/*.md, scores them
using the composite formula defined in references/ranking_rules.md, and
persists a ranked CSV to assets/ranking_results.csv (overwritten each run).

Stdlib-only (re, csv, pathlib, glob) - no external packages, no virtualenv
required. Requires Python 3.8+.

Preflight (interpreter availability) is handled by the calling skill
(SKILL.md instructs trying `python3` then `python` before invoking this
script); this file assumes it is already running under a valid interpreter.
"""
import csv
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SIM_DIR = SCRIPT_DIR.parent / "simulation" / "simulations"
OUT_CSV = SCRIPT_DIR / "assets" / "ranking_results.csv"

CSV_HEADER = [
    "Rank", "Role", "Company", "Compensation", "Location", "YearsRequired",
    "Composite", "Recruiter", "Interview", "DegreeScore", "SkillScore",
    "ExperienceScore", "PrefPenalties", "FitScore", "FitCategory",
    "FileName", "PostingDate",
]

# --- Raw point scales from ranking_rules.md, with normalization ranges ---
DEGREE_POINTS = {
    "hard mismatch": -5,
    "no match": -2,
    "partial": 1,
    "equivalent": 2,
    "direct": 3,
}
DEGREE_RANGE = (-5, 3)  # min, max possible raw points

FIT_POINTS = {
    "hard reject": -5,
    "mismatch": -2,
    "weak match": 1,
    "moderate match": 2,
    "strong match": 3,
}
FIT_RANGE = (-5, 3)

SKILL_RANGE = (-2, 3)     # Major gaps=-2 .. High alignment=+3
EXPERIENCE_RANGE = (-2, 2)  # Does not meet=-2 .. Meets=+2

PENALTY_POINTS = {
    "minor": 1,
    "moderate": 2,
    "major": 3,
    "clearance": 4,
}


def normalize(raw, value_range):
    """Map a raw point value onto a 0-100 scale given its (min, max) range."""
    lo, hi = value_range
    if hi == lo:
        return 50.0
    pct = (raw - lo) / (hi - lo) * 100.0
    return max(0.0, min(100.0, pct))


def extract_metadata(text):
    meta = {
        "Company": "Unknown", "Title": "Unknown", "Posting": "Unknown",
        "Comp": "Unknown", "Loc": "Unknown", "Years": "Unknown",
        "Degree": "Unknown", "InternshipMode": "Unknown",
    }
    block_match = re.search(r"## 0\. Metadata(.*?)(?:\n---|\Z)", text, re.S)
    block = block_match.group(1) if block_match else ""
    patterns = {
        "Company": r"-\s*Company:\s*(.+)",
        "Title": r"-\s*Job Title:\s*(.+)",
        "Posting": r"-\s*Posting Date:\s*(.+)",
        "Comp": r"-\s*Compensation:\s*(.+)",
        "Loc": r"-\s*Location\(s\):\s*(.+)",
        "Years": r"-\s*Years of Experience Required:\s*(.+)",
        "Degree": r"-\s*Degree Requirement:\s*(.+)",
        "InternshipMode": r"-\s*Internship Mode:\s*(.+)",
    }
    for key, pattern in patterns.items():
        m = re.search(pattern, block)
        if m:
            meta[key] = m.group(1).strip()
    return meta


def extract_recruiter_interview(text):
    re_m = re.search(r"\*\*Recruiter Screen Likelihood:\*\*\s*(\d+)%", text)
    int_m = re.search(r"\*\*Interview Likelihood:\*\*\s*(\d+)%", text)
    recruiter = int(re_m.group(1)) if re_m else 50
    interview = int(int_m.group(1)) if int_m else 50
    return recruiter, interview



def extract_degree_score(text):
    m = re.search(r"\*\*Match Category:\*\*\s*(.+)", text)
    if not m:
        return 0, "Unknown"
    label = m.group(1).strip()
    lower = label.lower()
    for key, points in DEGREE_POINTS.items():
        if key in lower:
            return points, label
    return 0, label


def extract_skill_score(text):
    section_m = re.search(
        r"## 2\. Skill & Responsibility Mapping(.*?)(?:\n## 3\.|\Z)", text, re.S)
    section = section_m.group(1) if section_m else ""

    # Only count rows within the "Required Skills" table (weighted most heavily).
    required_m = re.search(
        r"## Required Skills(.*?)(?:## Preferred Skills|## Responsibility Alignment|\Z)",
        section, re.S)
    required = required_m.group(1) if required_m else section

    direct = len(re.findall(r"\|\s*(Direct|Equivalent)\s*\|", required))
    partial = len(re.findall(r"\|\s*Partial\s*\|", required))
    no_match = len(re.findall(r"\|\s*No Match\s*\|", required))
    total = direct + partial + no_match

    if total == 0:
        return 0, "Unknown"
    ratio_direct = direct / total
    if no_match >= 2 or (total > 0 and direct == 0 and partial == 0):
        return -2, "Major skill gaps"
    if ratio_direct >= 0.7 and no_match == 0:
        return 3, "High alignment"
    if ratio_direct >= 0.4 or (direct + partial) / total >= 0.6:
        return 2, "Moderate alignment"
    return 1, "Low alignment"


def extract_experience_score(text):
    section_m = re.search(
        r"## 4\. Years-of-Experience Mapping(.*?)(?:\n## 5\.|\Z)", text, re.S)
    section = section_m.group(1) if section_m else ""
    rows = re.findall(r"\|[^\n|]*\|[^\n|]*\|\s*(✔|~|✘)\s*\|", section)
    if not rows:
        return 0, "Unknown"
    if "✘" in rows:
        return -2, "Does not meet requirement"
    if "~" in rows:
        return 1, "Partially meets requirement"
    return 2, "Meets requirement"


def extract_fit_score(text):
    m = re.search(r"## 8\. Final Fit Summary\s*\n\*\*Category:\*\*\s*(.+)", text)
    if not m:
        return 0, "Unknown"
    label = m.group(1).strip()
    lower = label.lower()
    for key, points in FIT_POINTS.items():
        if key in lower:
            return points, label
    return 0, label


def extract_preference_penalty(text):
    section_m = re.search(
        r"## 6\. Preference Violations(.*?)(?:\n## 7\.|\Z)", text, re.S)
    section = section_m.group(1) if section_m else ""
    penalty = 0
    lower = section.lower()
    if "clearance" in lower and "violation" in lower:
        penalty += PENALTY_POINTS["clearance"]
    penalty += PENALTY_POINTS["major"] * len(re.findall(r"major violation", lower))
    penalty += PENALTY_POINTS["moderate"] * len(re.findall(r"moderate violation", lower))
    penalty += PENALTY_POINTS["minor"] * len(re.findall(r"minor violation", lower))
    return penalty


def is_internship_from_metadata(internship_mode_value):
    """Read the authoritative Internship Mode flag the Simulation skill records in
    Metadata (per simulation_contract.md section 9). Returns True/False, or None if
    the field is missing/unrecognized (e.g. simulation files predating this field)."""
    value = (internship_mode_value or "").strip().lower()
    if value in ("yes", "true", "y"):
        return True
    if value in ("no", "false", "n"):
        return False
    return None


def is_internship_from_keywords(title, text):
    """Fallback heuristic for simulation files that predate the Internship Mode
    metadata field. Only used when that field is missing/unrecognized."""
    haystack = f"{title}\n{text}".lower()
    return bool(re.search(r"\bintern(ship)?\b|\bco-?op\b", haystack))


def score_file(path):
    text = path.read_text(encoding="utf-8")
    meta = extract_metadata(text)
    recruiter, interview = extract_recruiter_interview(text)
    degree_raw, _ = extract_degree_score(text)
    skill_raw, _ = extract_skill_score(text)
    exp_raw, _ = extract_experience_score(text)
    fit_raw, fit_category = extract_fit_score(text)
    penalty = extract_preference_penalty(text)

    degree_norm = normalize(degree_raw, DEGREE_RANGE) / 100.0
    skill_norm = normalize(skill_raw, SKILL_RANGE) / 100.0
    exp_norm = normalize(exp_raw, EXPERIENCE_RANGE) / 100.0
    fit_norm = normalize(fit_raw, FIT_RANGE) / 100.0

    composite = (
        recruiter * 0.45
        + interview * 0.20
        + degree_norm * 100 * 0.15
        + skill_norm * 100 * 0.10
        + exp_norm * 100 * 0.05
        + fit_norm * 100 * 0.05
        - penalty
    )
    composite = round(max(0.0, min(100.0, composite)), 2)

    hard_reject = "hard reject" in fit_category.lower()

    internship = is_internship_from_metadata(meta["InternshipMode"])
    if internship is None:
        print(
            f"Warning: {path.name} has no valid 'Internship Mode' metadata field; "
            "falling back to keyword detection on title/text."
        )
        internship = is_internship_from_keywords(meta["Title"], text)

    return {
        "Role": meta["Title"],
        "Company": meta["Company"],
        "Compensation": meta["Comp"],
        "Location": meta["Loc"],
        "YearsRequired": meta["Years"],
        "Composite": composite,
        "Recruiter": recruiter,
        "Interview": interview,
        "DegreeScore": round(degree_norm, 2),
        "SkillScore": round(skill_norm, 2),
        "ExperienceScore": round(exp_norm, 2),
        "PrefPenalties": penalty,
        "FitScore": round(fit_norm, 2),
        "FitCategory": fit_category,
        "FileName": path.name,
        "PostingDate": meta["Posting"],
        "_hard_reject": hard_reject,
        "_internship": internship,
    }


def sort_key(row):
    # Hard rejects always sink to the bottom, ordered by recruiter likelihood
    # among themselves (rules 5.3). Otherwise sort by composite score desc,
    # then the documented tie-breaker chain (rules 5.2).
    return (
        row["_hard_reject"],
        -row["Composite"],
        -row["Recruiter"],
        -row["Interview"],
        -row["DegreeScore"],
        row["PrefPenalties"],
        -row["SkillScore"],
        -row["ExperienceScore"],
    )


def build_ranked_rows(rows):
    ranked = sorted(rows, key=sort_key)
    out = []
    for i, r in enumerate(ranked, start=1):
        row = {k: r[k] for k in CSV_HEADER if k != "Rank"}
        row["Rank"] = i
        out.append(row)
    return out


def write_csv(rows, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in CSV_HEADER})


def main():
    if not SIM_DIR.exists():
        print(f"No simulation files found in {SIM_DIR}")
        return 1
    files = sorted(SIM_DIR.glob("*.md"))
    if not files:
        print(f"No simulation files found in {SIM_DIR}")
        return 1

    scored = [score_file(f) for f in files]
    full_time = [r for r in scored if not r["_internship"]]
    interns = [r for r in scored if r["_internship"]]

    ranked_full_time = build_ranked_rows(full_time) if full_time else []
    ranked_interns = build_ranked_rows(interns) if interns else []

    # Full-time ranking is the canonical CSV; if only internships exist,
    # persist those instead so the CSV is never silently empty.
    primary = ranked_full_time if ranked_full_time else ranked_interns
    write_csv(primary, OUT_CSV)

    print(f"Ranking persisted to {OUT_CSV}")
    if ranked_full_time and ranked_interns:
        print(
            f"Note: {len(ranked_interns)} internship role(s) were ranked "
            "separately per rules 5.4 and are not included in the CSV above."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
