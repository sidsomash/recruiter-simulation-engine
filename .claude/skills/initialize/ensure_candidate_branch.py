#!/usr/bin/env python3
"""
ensure_candidate_branch.py

Deterministic git-branch guard for the Initialize skill. Ensures candidate
reference files (candidate_resume.md, candidate_profile.md,
candidate_preferences.md) are only ever written on a dedicated
`candidate/<slug>` branch, never on `main` or any other shared/feature
branch. This keeps `main` a clean, PII-free template and prevents one
candidate's data from being committed onto another candidate's branch or a
skill-development branch.

Usage:
    python3 .github/skills/initialize/ensure_candidate_branch.py "<candidate name>"

Behavior:
    - Determines the current git branch.
    - Slugifies the candidate name into `candidate/<slug>` (lowercase,
      hyphen-separated, alphanumeric only).
    - If already on the correct `candidate/<slug>` branch: no-op, exit 0.
    - If on `main`:
        - Refuses if the working tree has uncommitted changes (so nothing
          unrelated gets carried onto the candidate branch).
        - If `candidate/<slug>` already exists locally: checks it out.
        - Else: creates and checks out a new `candidate/<slug>` branch off
          the current `main` tip.
    - If on any other branch (a different candidate/* branch, or a
      feature/dev branch): refuses and exits non-zero with an explanatory
      message instructing the user to switch to `main` first.
    - Never pushes, merges, fetches, or deletes any branch. Purely local
      branch creation/checkout, scoped to this repository's working copy.
"""

import hashlib
import re
import subprocess
import sys


def run(args):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    if slug:
        return slug
    # Non-ASCII or all-punctuation names (e.g. "李雷", "@@@") sanitize down to an
    # empty string. Falling back to a fixed literal like "candidate" would let
    # multiple such candidates collide onto the same candidate/candidate branch
    # and mix their data. Use a short stable hash of the original name instead,
    # so each distinct input still gets its own unique branch.
    digest = hashlib.sha1(name.strip().encode("utf-8")).hexdigest()[:8]
    return f"candidate-{digest}"


def branch_exists(branch: str) -> bool:
    _, out, _ = run(["branch", "--list", branch])
    return bool(out.strip())


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print(
            "USAGE ERROR: candidate name is required, e.g.\n"
            '  python3 ensure_candidate_branch.py "Jane Doe"',
            file=sys.stderr,
        )
        return 2

    candidate_name = sys.argv[1].strip()
    slug = slugify(candidate_name)
    target_branch = f"candidate/{slug}"

    code, _, err = run(["rev-parse", "--is-inside-work-tree"])
    if code != 0:
        print(f"GIT ERROR: not inside a git repository ({err})", file=sys.stderr)
        return 2

    code, current_branch, err = run(["rev-parse", "--abbrev-ref", "HEAD"])
    if code != 0:
        print(f"GIT ERROR: could not determine current branch ({err})", file=sys.stderr)
        return 2

    if current_branch == target_branch:
        print(f"OK: already on {target_branch}")
        return 0

    if current_branch != "main":
        print(
            "REFUSED: Initialize must be run from `main`, not from "
            f"`{current_branch}`.\n"
            "Candidate data must never be committed onto a non-candidate "
            "branch (e.g. a skill-development branch) or another "
            "candidate's branch.\n"
            "Run `git checkout main` first, then re-run Initialize.",
            file=sys.stderr,
        )
        return 1

    code, status_out, _ = run(["status", "--porcelain"])
    if status_out.strip():
        print(
            "REFUSED: `main` has uncommitted changes. Commit, stash, or "
            "discard them before running Initialize, so no unrelated "
            "changes get carried onto the candidate branch.",
            file=sys.stderr,
        )
        return 1

    if branch_exists(target_branch):
        code, _, err = run(["checkout", target_branch])
        if code != 0:
            print(f"GIT ERROR: could not check out {target_branch} ({err})", file=sys.stderr)
            return 2
        print(f"OK: switched to existing branch {target_branch}")
        return 0

    code, _, err = run(["checkout", "-b", target_branch])
    if code != 0:
        print(f"GIT ERROR: could not create {target_branch} ({err})", file=sys.stderr)
        return 2
    print(f"OK: created and switched to new branch {target_branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
