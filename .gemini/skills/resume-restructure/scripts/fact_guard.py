#!/usr/bin/env python3
"""Resume-Restructure fact guard.

Scans a tailored résumé Markdown file for quantitative claims (percentages,
dollar amounts, multipliers, record/throughput counts, and "reduced/increased/
grew/improved/saved/cut by ..." phrasing) and flags any claim whose numeric
value cannot be traced back to the candidate's original résumé.

This exists because Step 4's "aggressive rewrite" / "maximum recruiter
signal" instructions create fabrication pressure, and Step 5's self-graded
validation (same model/pass that wrote the rewrite) is not a reliable check
against hallucinated metrics. This script provides a deterministic,
independent check instead.

Usage:
    python3 fact_guard.py <tailored_resume.md> [original_resume.md]

If <original_resume.md> is omitted, defaults to the canonical candidate
résumé at ../../simulation/references/candidate_resume.md (relative to this
script).

Exit codes:
    0 - no unverifiable quantitative claims found (or resumes are empty).
    1 - one or more quantitative claims in the tailored résumé could not be
        traced to the original résumé; details are printed to stdout.
    2 - usage/file error (missing file, etc.).

Stdlib-only (re, sys, pathlib) - no external packages, no virtualenv
required. Requires Python 3.8+.
"""
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ORIGINAL_RESUME = (
    SCRIPT_DIR.parent.parent / "simulation" / "references" / "candidate_resume.md"
)

# --- Quantitative claim patterns -------------------------------------------
# Each pattern captures a self-contained numeric claim. Surrounding wording
# may legitimately be reworded by the rewrite; the *numeric value + unit* is
# what must be traceable to the original résumé, since that's the part that
# is either true (grounded) or fabricated.
CLAIM_PATTERNS = [
    # Percentages: "70%", "12.5 %"
    re.compile(r"\d+(?:\.\d+)?\s?%"),
    # Dollar amounts: "$3.2M", "$500,000", "$1.5B"
    re.compile(r"\$\d[\d,]*(?:\.\d+)?\s?[KMB]?\b"),
    # Multipliers: "10x", "3.5x"
    re.compile(r"\b\d+(?:\.\d+)?x\b", re.IGNORECASE),
    # Record/throughput counts: "10M records", "500K users", "1,000+ requests"
    re.compile(
        r"\d[\d,]*(?:\.\d+)?\s?[KMB]?\+?\s*"
        r"(?:records|rows|users|requests|datasets|transactions|customers|"
        r"documents|tests|endpoints|passing|files|queries)",
        re.IGNORECASE,
    ),
    # "reduced/increased/grew/improved/saved/cut ... by <number>"
    re.compile(
        r"(?:reduced|increased|grew|improved|saved|cut|decreased)\s+"
        r"(?:\w+\s+){0,3}by\s+\d+(?:\.\d+)?\s?[%x]?",
        re.IGNORECASE,
    ),
]

# Characters to strip when normalizing a claim for substring comparison.
_NORMALIZE_STRIP = re.compile(r"[\s,]")


def normalize(text: str) -> str:
    """Lowercase and strip whitespace/commas for tolerant substring matching."""
    return _NORMALIZE_STRIP.sub("", text.lower())


def extract_numeric_token(claim: str) -> str:
    """Extract the core numeric+unit token from a claim match.

    For phrase-style matches (e.g. "reduced deployment time by 70%"), pulls
    just the trailing "70%" portion so it can be checked against the
    original résumé independent of the surrounding phrasing.
    """
    m = re.search(r"\$?\d[\d,]*(?:\.\d+)?\s?[KMB%x]?", claim, re.IGNORECASE)
    return m.group(0) if m else claim


def find_claims(text: str):
    """Return a list of (claim_text, line_number, line_text) tuples."""
    claims = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        seen_spans = set()
        for pattern in CLAIM_PATTERNS:
            for match in pattern.finditer(line):
                span = match.span()
                # Avoid double-flagging overlapping matches on the same line.
                if any(s[0] <= span[0] < s[1] or s[0] < span[1] <= s[1] for s in seen_spans):
                    continue
                seen_spans.add(span)
                claims.append((match.group(0).strip(), line_no, line.strip()))
    return claims


def check_claims(tailored_text: str, original_text: str):
    """Return (verified, flagged) claim lists.

    Each entry is a dict with keys: claim, numeric_token, line_no, line_text.
    A claim is "verified" if its normalized numeric token appears anywhere in
    the normalized original résumé text; otherwise it's "flagged".
    """
    normalized_original = normalize(original_text)
    verified, flagged = [], []
    for claim_text, line_no, line_text in find_claims(tailored_text):
        numeric_token = extract_numeric_token(claim_text)
        entry = {
            "claim": claim_text,
            "numeric_token": numeric_token,
            "line_no": line_no,
            "line_text": line_text,
        }
        if normalize(numeric_token) and normalize(numeric_token) in normalized_original:
            verified.append(entry)
        else:
            flagged.append(entry)
    return verified, flagged


def main(argv):
    if len(argv) < 2:
        print(
            "Usage: python3 fact_guard.py <tailored_resume.md> [original_resume.md]",
            file=sys.stderr,
        )
        return 2

    tailored_path = Path(argv[1])
    original_path = Path(argv[2]) if len(argv) > 2 else DEFAULT_ORIGINAL_RESUME

    if not tailored_path.is_file():
        print(f"Error: tailored resume file not found: {tailored_path}", file=sys.stderr)
        return 2
    if not original_path.is_file():
        print(f"Error: original resume file not found: {original_path}", file=sys.stderr)
        return 2

    tailored_text = tailored_path.read_text(encoding="utf-8")
    original_text = original_path.read_text(encoding="utf-8")

    verified, flagged = check_claims(tailored_text, original_text)

    print(f"Fact Guard: scanned {tailored_path.name} against {original_path.name}")
    print(f"  Quantitative claims found: {len(verified) + len(flagged)}")
    print(f"  Verified (traceable to original): {len(verified)}")
    print(f"  Flagged (not traceable to original): {len(flagged)}")

    if flagged:
        print("\nFlagged claims requiring review or correction:")
        for entry in flagged:
            print(
                f"  - Line {entry['line_no']}: \"{entry['claim']}\" "
                f"(numeric value: {entry['numeric_token']})"
            )
            print(f"    Context: {entry['line_text']}")
        print(
            "\nEach flagged claim's numeric value does not appear anywhere in the "
            "original resume. Either correct it to match the original, remove it, "
            "or have the user explicitly approve it as an acceptable exception "
            "before proceeding to Step 6/7."
        )
        return 1

    print("\nNo unverifiable quantitative claims found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
