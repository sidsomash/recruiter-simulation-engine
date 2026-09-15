#!/usr/bin/env python3
"""Verify (and optionally fix) that skill-definition files are mirrored
identically across the .github, .claude, and .gemini platform copies.

Every skill's logic (SKILL.md, references/*, assets/templates/*, and any
deterministic helper scripts) must be byte-for-byte identical across all
three platform directories, since each AI platform (GitHub Copilot CLI,
Claude, Gemini) reads its own copy independently. There is currently no
automatic propagation for these files (unlike candidate data files, which
are synced by initialize/sync_candidate_files.py) - skill-file edits must be
applied to all three copies by hand, and drift between copies has been a
recurring source of bugs (stale cross-references, inconsistent wording,
etc.). This script exists to catch that drift instead of relying on manual
`Compare-Object`/`diff` calls after every edit.

Usage:
    # Report-only (the default when no flag is given): scan every skill
    # file and print any drift. Exits 1 if any file differs across copies
    # or is missing from some copy (unless explicitly allowed - see
    # ALLOWED_EXCEPTIONS below). Safe to run in CI or as a pre-commit check.
    python3 tools/check_skill_sync.py

    # Fix ONE specific file: mirror it byte-for-byte from the canonical
    # .github copy to .claude and .gemini. Path is relative to
    # <platform>/skills/ (e.g. simulation/SKILL.md, NOT skills/simulation/SKILL.md).
    python3 tools/check_skill_sync.py --sync simulation/SKILL.md

    # Sync every canonical (.github) file to .claude/.gemini in one pass.
    # This can only copy FROM .github - a file that exists only in .claude
    # or .gemini (missing from .github) is NOT created/copied; it is
    # reported as an unresolved warning and the command exits 1 so it isn't
    # silently ignored. Use with care - review the diff before committing.
    python3 tools/check_skill_sync.py --sync-all

--sync and --sync-all are mutually exclusive.

Stdlib-only (pathlib, sys, argparse) - no external packages, no virtualenv
required. Requires Python 3.8+.
"""
import argparse
import ntpath
import sys
from pathlib import Path, PurePosixPath

PLATFORM_DIRS = (".github", ".claude", ".gemini")
CANONICAL_DIR = ".github"

# Files/patterns that are *intentionally* not mirrored across all three
# copies. Anything matched here is skipped by both the default check and
# --sync-all. Keep this list short and well-justified - if in doubt, a file
# should be mirrored, not excluded.
ALLOWED_EXCEPTIONS = (
    # Mobile one-shot prompt: canonical-only by design (see initialize
    # SKILL.md Step 8/9) - Claude/Gemini users don't need their own copy.
    "simulation/one_shot_simulation_prompt.md",
)

# Generated/output directories - never part of the skill *definition*, so
# they're excluded from sync checks entirely (their contents are expected
# to differ per-platform-copy, per-run, or be entirely absent).
EXCLUDED_DIR_PARTS = (
    "simulations",  # generated simulation Markdown/JSON pairs
    "resumes",  # generated tailored resumes (resume-restructure output)
)
EXCLUDED_FILENAMES = (
    "ranking_results.csv",  # generated ranking output, overwritten per run
)


def is_excluded(rel_path: Path) -> bool:
    if str(rel_path).replace("\\", "/") in ALLOWED_EXCEPTIONS:
        return True
    if rel_path.name in EXCLUDED_FILENAMES:
        return True
    if any(part in EXCLUDED_DIR_PARTS for part in rel_path.parts):
        return True
    # Python bytecode caches are interpreter/version-specific artifacts, not
    # skill-definition source - never part of the sync contract.
    if "__pycache__" in rel_path.parts or rel_path.suffix == ".pyc":
        return True
    return False


def find_repo_root(start: Path):
    """Walk up from this script's location to find the repo root."""
    for parent in [start] + list(start.parents):
        if all((parent / d).is_dir() for d in (".github", ".claude", ".gemini")):
            return parent
    return None


def collect_relative_paths(repo_root: Path):
    """All skill-relative paths (relative to <platform>/skills/) that exist
    in at least one platform copy, excluding generated/excluded content."""
    rel_paths = set()
    for platform in PLATFORM_DIRS:
        skills_dir = repo_root / platform / "skills"
        if not skills_dir.is_dir():
            continue
        for path in skills_dir.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(skills_dir)
            if is_excluded(rel):
                continue
            rel_paths.add(rel)
    return sorted(rel_paths, key=lambda p: str(p))


def check(repo_root: Path):
    rel_paths = collect_relative_paths(repo_root)
    missing_issues = []
    diff_issues = []
    type_conflict_issues = []

    for rel in rel_paths:
        full_paths = {
            platform: repo_root / platform / "skills" / rel for platform in PLATFORM_DIRS
        }
        # Only count actual files as "existing" - a path that is a file in
        # one platform copy but a directory (or other non-file entry) in
        # another is itself a form of drift, not something read_bytes() can
        # safely handle, so it must never be treated as present here.
        existing = {p: fp for p, fp in full_paths.items() if fp.is_file()}
        non_file = [p for p, fp in full_paths.items() if fp.exists() and not fp.is_file()]

        if non_file:
            type_conflict_issues.append((rel, non_file))
            continue

        if len(existing) < len(PLATFORM_DIRS):
            missing_from = [p for p in PLATFORM_DIRS if p not in existing]
            missing_issues.append((rel, missing_from))
            continue

        contents = {p: fp.read_bytes() for p, fp in existing.items()}
        if len(set(contents.values())) > 1:
            diff_issues.append(rel)

    if missing_issues:
        print(f"MISSING in some copy ({len(missing_issues)}):")
        for rel, missing_from in missing_issues:
            print(f"  - skills/{rel}  (absent from: {', '.join(missing_from)})")

    if type_conflict_issues:
        print(f"FILE/DIRECTORY TYPE CONFLICT ({len(type_conflict_issues)}):")
        for rel, non_file in type_conflict_issues:
            print(
                f"  - skills/{rel}  (is a file in some copies, but a directory or "
                f"other non-file entry in: {', '.join(non_file)})"
            )

    if diff_issues:
        print(f"CONTENT DIFFERS across copies ({len(diff_issues)}):")
        for rel in diff_issues:
            print(f"  - skills/{rel}")

    if not missing_issues and not diff_issues and not type_conflict_issues:
        print(f"OK - {len(rel_paths)} skill files checked, all copies identical.")
        return 0

    print(
        "\nIf this drift is intentional, add the path to ALLOWED_EXCEPTIONS in "
        "tools/check_skill_sync.py. Otherwise fix it with:\n"
        "  python3 tools/check_skill_sync.py --sync <relative-path>\n"
        "  python3 tools/check_skill_sync.py --sync-all"
    )
    return 1


def normalize_sync_path(raw: str) -> Path:
    """Validate and normalize a user-supplied --sync path.

    Accepts paths relative to <platform>/skills/ (the documented form, e.g.
    'simulation/SKILL.md'), and also tolerates an accidental leading
    'skills/' prefix (e.g. 'skills/simulation/SKILL.md') by stripping it,
    so the command works regardless of which form the user copies from
    docs. Rejects absolute paths (POSIX-style, e.g. '/etc/passwd', and
    Windows drive-qualified, e.g. 'C:/tmp/x' or 'C:\\tmp\\x' - PurePosixPath
    alone does not treat a drive-qualified path as absolute, so it is
    checked explicitly here) and any '..' component, to prevent writing
    outside the intended skill trees.
    """
    normalized_raw = raw.replace("\\", "/")
    # ntpath.splitdrive() is used explicitly (rather than os.path.splitdrive)
    # so a Windows drive-qualified path (e.g. 'C:/tmp/x') is rejected even
    # when this script runs on a POSIX host, where os.path.splitdrive()
    # would never detect a drive and PurePosixPath("C:/tmp/x").is_absolute()
    # is also False - without this explicit check such a path could pass
    # both checks below and Path(*parts) could later preserve the drive,
    # escaping the repo root.
    drive, _ = ntpath.splitdrive(normalized_raw)
    if drive:
        raise ValueError(f"--sync path must be relative, got a drive-qualified path: {raw}")
    posix = PurePosixPath(normalized_raw)
    if posix.is_absolute():
        raise ValueError(f"--sync path must be relative, got absolute path: {raw}")
    if ".." in posix.parts:
        raise ValueError(f"--sync path must not contain '..' components: {raw}")
    parts = posix.parts
    if parts and parts[0] == "skills":
        parts = parts[1:]
    if not parts:
        raise ValueError(f"--sync path is empty after normalization: {raw}")
    return Path(*parts)


def sync_one(repo_root: Path, rel: Path):
    source = repo_root / CANONICAL_DIR / "skills" / rel
    if not source.exists():
        print(f"Error: canonical source file does not exist: {source}")
        return 1
    if not source.is_file():
        print(f"Error: canonical source path is not a regular file (e.g. a directory): {source}")
        return 1
    content = source.read_bytes()
    synced = []
    for platform in PLATFORM_DIRS:
        if platform == CANONICAL_DIR:
            continue
        target = repo_root / platform / "skills" / rel
        if target.exists() and not target.is_file():
            print(
                f"Error: target path exists but is not a regular file (e.g. a "
                f"directory), refusing to overwrite: {target}"
            )
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        synced.append(str(target.relative_to(repo_root)))
    print(f"Synced {rel} to:")
    for path in synced:
        print(f"  - {path}")
    return 0


def sync_all(repo_root: Path):
    canonical_skills_dir = repo_root / CANONICAL_DIR / "skills"
    rel_paths = {
        p.relative_to(canonical_skills_dir)
        for p in canonical_skills_dir.rglob("*")
        if p.is_file() and not is_excluded(p.relative_to(canonical_skills_dir))
    }

    # Files that exist in a non-canonical copy but are absent from the
    # canonical .github copy can't be fixed by copying *from* .github - flag
    # them instead of silently leaving them unresolved (previously this case
    # was neither synced nor reported, so `check()` would still report drift
    # right after sync-all claimed success).
    all_rel_paths = set(collect_relative_paths(repo_root))
    canonical_missing = sorted(all_rel_paths - rel_paths, key=str)

    total_synced = 0
    type_conflicts = []
    for rel in sorted(rel_paths, key=str):
        source = canonical_skills_dir / rel
        content = source.read_bytes()
        for platform in PLATFORM_DIRS:
            if platform == CANONICAL_DIR:
                continue
            target = repo_root / platform / "skills" / rel
            if target.exists() and not target.is_file():
                # A directory (or other non-file entry) occupying the same
                # path as a canonical file is a drift condition that can't
                # be resolved by writing bytes over it - report it instead
                # of letting read_bytes()/write_bytes() raise.
                type_conflicts.append(str(target.relative_to(repo_root)))
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() == content:
                continue
            target.write_bytes(content)
            total_synced += 1
            print(f"  - wrote {target.relative_to(repo_root)}")
    print(f"Done. {total_synced} file(s) written/updated from {CANONICAL_DIR}.")

    exit_code = 0
    if type_conflicts:
        print(
            f"\nWARNING: {len(type_conflicts)} target path(s) are a directory (or "
            "other non-file entry) where a canonical file was expected - NOT "
            "resolved automatically:"
        )
        for path in type_conflicts:
            print(f"  - {path}")
        exit_code = 1

    if canonical_missing:
        print(
            f"\nWARNING: {len(canonical_missing)} file(s) exist in a non-canonical "
            f"copy but are MISSING from {CANONICAL_DIR} - these were NOT resolved "
            "(sync-all only copies canonical -> other copies). Add them to "
            f"{CANONICAL_DIR} manually, then re-run:"
        )
        for rel in canonical_missing:
            print(f"  - skills/{rel}")
        exit_code = 1
    return exit_code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--sync",
        metavar="RELATIVE_PATH",
        help="Mirror one file (relative to skills/, e.g. simulation/SKILL.md) "
        "from the canonical .github copy to .claude and .gemini.",
    )
    group.add_argument(
        "--sync-all",
        action="store_true",
        help="Mirror every non-excluded file from the canonical .github copy "
        "to .claude and .gemini in one pass.",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        print(
            "Error: could not locate repo root (expected .github/, .claude/, "
            "and .gemini/ directories as siblings)."
        )
        return 1

    if args.sync:
        try:
            rel = normalize_sync_path(args.sync)
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
        return sync_one(repo_root, rel)
    if args.sync_all:
        return sync_all(repo_root)
    return check(repo_root)


if __name__ == "__main__":
    sys.exit(main())
