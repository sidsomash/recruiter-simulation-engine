#!/usr/bin/env python3
"""Sync canonical candidate reference files across skill copies.

The Initialize skill writes candidate_resume.md, candidate_profile.md, and
candidate_preferences.md ONCE to the canonical location
(.github/skills/simulation/references/), then invokes this script to mirror
those files byte-for-byte to the .claude and .gemini copies. This replaces
having the model regenerate the same content three separate times, which
risked subtle drift (a dropped bullet, a reworded sentence) between copies.

Stdlib-only (shutil, pathlib) - no external packages, no virtualenv
required. Requires Python 3.8+.
"""
import sys
from pathlib import Path

FILES = ["candidate_resume.md", "candidate_profile.md", "candidate_preferences.md"]
PLATFORM_DIRS = (".github", ".claude", ".gemini")


def find_repo_root(start):
    """Walk up from this script's location to find the repo root - the
    parent of whichever platform directory (.github/.claude/.gemini) the
    script happens to be running from."""
    for parent in start.parents:
        if parent.name in PLATFORM_DIRS:
            return parent.parent
    return None


def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    if repo_root is None:
        print(
            "Error: could not locate repo root (expected this script to live "
            "under a .github/.claude/.gemini directory)."
        )
        return 1

    source_dir = repo_root / ".github" / "skills" / "simulation" / "references"
    target_dirs = [
        repo_root / ".claude" / "skills" / "simulation" / "references",
        repo_root / ".gemini" / "skills" / "simulation" / "references",
    ]

    missing = [f for f in FILES if not (source_dir / f).exists()]
    if missing:
        print(
            f"Error: canonical source files missing in {source_dir}: "
            f"{', '.join(missing)}. Run the Initialize skill first."
        )
        return 1

    synced = []
    for target_dir in target_dirs:
        target_dir.mkdir(parents=True, exist_ok=True)
        for filename in FILES:
            source_path = source_dir / filename
            target_path = target_dir / filename
            content = source_path.read_text(encoding="utf-8")
            target_path.write_text(content, encoding="utf-8")
            synced.append(str(target_path.relative_to(repo_root)))

    print("Candidate files synced to:")
    for path in synced:
        print(f"  - {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
