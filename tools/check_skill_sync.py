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
    # Refuses generated/excluded paths (see EXCLUDED_DIR_PARTS/
    # EXCLUDED_FILENAMES/ALLOWED_EXCEPTIONS below) - those are intentionally
    # outside the sync contract and must never be propagated across copies.
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
import os
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
    symlink_issues = []

    for rel in rel_paths:
        full_paths = {
            platform: repo_root / platform / "skills" / rel for platform in PLATFORM_DIRS
        }

        # A symlinked path component (the file itself, or any ancestor
        # directory) is drift regardless of what content it resolves to -
        # Path.is_file()/read_bytes() both follow symlinks, so without this
        # check a symlink pointing at byte-identical content in all three
        # trees would be silently reported as "synchronized" even though
        # --sync/--sync-all (validate_sync_target/validate_sync_source)
        # would reject that same path outright.
        symlinked = {
            p: fp for p, fp in full_paths.items()
            if find_symlink_component(repo_root, fp) is not None
        }
        if symlinked:
            symlink_issues.append((rel, sorted(symlinked)))
            continue

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

    if symlink_issues:
        print(f"SYMLINKED PATH COMPONENT ({len(symlink_issues)}):")
        for rel, platforms in symlink_issues:
            print(
                f"  - skills/{rel}  (symlinked path component under: "
                f"{', '.join(platforms)} - not a plain file/directory, refused by --sync)"
            )

    if diff_issues:
        print(f"CONTENT DIFFERS across copies ({len(diff_issues)}):")
        for rel in diff_issues:
            print(f"  - skills/{rel}")

    if not missing_issues and not diff_issues and not type_conflict_issues and not symlink_issues:
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


def find_symlink_component(repo_root: Path, path: Path):
    """Return the first path component between repo_root and `path`
    (inclusive of both ends) that is itself a symlink, or None if none are.

    Containment checks based on os.path.realpath()/commonpath() alone are
    not sufficient: a symlink whose resolved target still happens to land
    inside the expected root passes those checks, but write_bytes()/
    read_bytes() would still follow it and mutate/read the *link's target*
    rather than the path that was actually requested - e.g. a final target
    that is a symlink to a different regular file inside the same skills
    root would pass containment yet cause `--sync` to silently overwrite
    that other file while leaving the requested path as an untouched link;
    an ancestor directory symlinked to a different directory inside the
    root would let mkdir()/write_bytes() write into that aliased directory
    instead of the intended one; and `<platform>/skills` (or the platform
    directory, or repo_root itself) being a symlink would make every
    containment check below trivially "consistent" against whatever
    external location the link resolves to. Rejecting every symlinked
    component outright - regardless of where it resolves to - closes all
    of these cases at once, rather than trying to special-case each one.
    """
    try:
        rel = path.relative_to(repo_root)
    except ValueError:
        rel = None
    if repo_root.is_symlink():
        return repo_root
    current = repo_root
    if rel is not None:
        for part in rel.parts:
            current = current / part
            if current.is_symlink():
                return current
        return None
    # `path` isn't under repo_root at all (e.g. repo_root itself resolved
    # oddly) - fall back to checking path's own component chain directly.
    chain = list(reversed(path.parents)) + [path]
    for component in chain:
        if component.is_symlink():
            return component
    return None


def validate_sync_target(repo_root: Path, platform: str, rel: Path):
    """Validate that writing `content` to <platform>/skills/<rel> is safe.

    Returns None if safe, or an error message string if not. Checks:
    - no component from repo_root down to the final target (the platform
      directory, <platform>/skills/ itself, every ancestor under it, and
      the target itself) may be a symlink - see find_symlink_component()
      for why containment checks alone can't safely replace this;
    - <platform>/skills/ itself, and every ancestor directory component
      under it, must be a real directory (not a file, and not a broken
      symlink) wherever something already exists at that path - otherwise
      mkdir(parents=True) would raise an unhandled FileExistsError instead
      of a clear error;
    - the final target, if anything already exists at that path (including
      a broken symlink), must be a regular file (not a directory or other
      non-file entry);
    - the resolved real path of <platform>/skills/ itself must remain
      under the resolved repo_root, and the resolved real path of the
      target must remain under the resolved skills root - kept as
      defense-in-depth alongside the symlink rejection above (e.g. for
      reparse points/junctions that is_symlink() may not catch on every
      platform).

    Path.exists() is deliberately avoided for these existence checks since
    it returns False for a broken symlink (it follows the link and reports
    based on the link's target) - that would let a broken symlink slip past
    this validation and only fail later, inside mkdir()/write_bytes(), with
    an unhandled OSError. os.path.lexists() reports based on the path entry
    itself, so broken symlinks are correctly treated as "something is
    already here" and checked against is_dir()/is_file() (which do follow
    symlinks, but return False for a broken one, correctly flagging it as
    a conflict rather than a usable directory/file).
    """
    skills_root = repo_root / platform / "skills"
    target = skills_root / rel

    symlink_hit = find_symlink_component(repo_root, target)
    if symlink_hit is not None:
        return (
            f"path component is a symlink, refusing to write through it "
            f"(syncing one path must not be able to alias/modify another): "
            f"{symlink_hit}"
        )

    # skills_root itself must be a directory (not a file/broken symlink) if
    # anything exists there at all - previously only rel.parts[:-1] below
    # was checked, so a <platform>/skills path that is itself a file passed
    # validation and the first mkdir(parents=True) call raised instead.
    if os.path.lexists(skills_root) and not skills_root.is_dir():
        return (
            f"path component exists but is not a directory, refusing to "
            f"write under it: {skills_root}"
        )

    # Walk every remaining ancestor from skills_root down to target's
    # parent, and confirm any that already exist are directories (not
    # files/broken symlinks/symlinks to files) - this is what would
    # otherwise make mkdir(parents=True) raise.
    ancestor = skills_root
    for part in rel.parts[:-1]:
        ancestor = ancestor / part
        if os.path.lexists(ancestor) and not ancestor.is_dir():
            return (
                f"path component exists but is not a directory, refusing to "
                f"write under it: {ancestor}"
            )

    if os.path.lexists(target) and not target.is_file():
        return (
            f"target path exists but is not a regular file (e.g. a directory), "
            f"refusing to overwrite: {target}"
        )

    # Containment check (defense-in-depth alongside the symlink rejection
    # above): resolve whatever part of the path already exists (realpath
    # does not require the full path to exist - it resolves as far as it
    # can and appends the remaining, necessarily nonexistent, components
    # literally) and confirm skills_root itself is under repo_root, and the
    # target is under skills_root.
    real_repo_root = os.path.realpath(str(repo_root))
    real_root = os.path.realpath(str(skills_root))
    try:
        root_common = os.path.commonpath([real_repo_root, real_root])
    except ValueError:
        root_common = None
    if root_common != real_repo_root:
        return (
            f"platform skills root resolves outside the repository (possible "
            f"symlink escape): {skills_root} -> {real_root}"
        )
    real_target = os.path.realpath(str(target))
    try:
        common = os.path.commonpath([real_root, real_target])
    except ValueError:
        common = None
    if common != real_root:
        return (
            f"target path resolves outside the platform's skills root (possible "
            f"symlink escape): {target} -> {real_target}"
        )
    return None


def validate_sync_source(repo_root: Path, source: Path):
    """Validate that reading `source` (the canonical .github file) is safe.

    Returns None if safe, or an error message string if not. `--sync <path>`
    is caller-supplied and only textually validated (no '..'/absolute/drive
    components) by normalize_sync_path() - it does not by itself prevent a
    symlink placed inside .github/skills from pointing at an arbitrary file
    outside the repo. source.is_file()/read_bytes() both follow symlinks,
    so without this check a symlinked source could be used to read (and
    then copy into .claude/.gemini) any file the process can access.
    """
    canonical_root = repo_root / CANONICAL_DIR / "skills"

    symlink_hit = find_symlink_component(repo_root, source)
    if symlink_hit is not None:
        return (
            f"path component is a symlink, refusing to read through it: {symlink_hit}"
        )

    real_repo_root = os.path.realpath(str(repo_root))
    real_root = os.path.realpath(str(canonical_root))
    try:
        root_common = os.path.commonpath([real_repo_root, real_root])
    except ValueError:
        root_common = None
    if root_common != real_repo_root:
        return (
            f"canonical skills root resolves outside the repository (possible "
            f"symlink escape): {canonical_root} -> {real_root}"
        )
    real_source = os.path.realpath(str(source))
    try:
        common = os.path.commonpath([real_root, real_source])
    except ValueError:
        common = None
    if common != real_root:
        return (
            f"canonical source path resolves outside the canonical skills root "
            f"(possible symlink escape): {source} -> {real_source}"
        )
    return None


def write_targets_transactionally(targets_content):
    """Write every (target_path, content_bytes) pair in `targets_content`.

    Returns None on full success, or an error message string if any write
    failed. On failure, every target already written *during this call* is
    rolled back - restored to its prior content if it existed before, or
    deleted if it didn't - so a mid-batch OSError (e.g. permission denied on
    a later destination) cannot leave some destinations updated and others
    stale. This is scoped to the current call only: it cannot undo writes
    from a previous, already-returned invocation, but preflight validation
    (validate_sync_target/validate_sync_source) is what prevents foreseeable
    conflicts from reaching this point at all - this rollback specifically
    covers unforeseeable failures (disk full, permissions, concurrent
    external modification) that preflight checks can't detect in advance.
    """
    written = []
    try:
        for target, content in targets_content:
            existed = target.exists()
            prior = target.read_bytes() if existed else None
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            written.append((target, existed, prior))
    except OSError as exc:
        for target, existed, prior in reversed(written):
            try:
                if existed:
                    target.write_bytes(prior)
                else:
                    target.unlink()
            except OSError:
                pass
        return (
            f"write failed ({exc}); rolled back {len(written)} already-written "
            "destination(s) from this operation"
        )
    return None


def sync_one(repo_root: Path, rel: Path):
    if is_excluded(rel):
        print(
            f"Error: '{rel}' is excluded from the sync contract (generated output, or a "
            f"canonical-only ALLOWED_EXCEPTIONS file) and must not be propagated across "
            f"platform copies: {rel}"
        )
        return 1
    source = repo_root / CANONICAL_DIR / "skills" / rel
    if not source.exists():
        print(f"Error: canonical source file does not exist: {source}")
        return 1
    if not source.is_file():
        print(f"Error: canonical source path is not a regular file (e.g. a directory): {source}")
        return 1
    source_error = validate_sync_source(repo_root, source)
    if source_error:
        print(f"Error: {source_error}")
        return 1
    content = source.read_bytes()

    targets = [
        repo_root / platform / "skills" / rel
        for platform in PLATFORM_DIRS if platform != CANONICAL_DIR
    ]
    # Preflight every target before writing any of them, so a conflict on
    # (say) the .gemini copy can't leave .claude written and .gemini stale -
    # a partially-synced state would otherwise result from validating and
    # writing each destination in the same loop.
    for platform in PLATFORM_DIRS:
        if platform == CANONICAL_DIR:
            continue
        error = validate_sync_target(repo_root, platform, rel)
        if error:
            print(f"Error: {error}")
            return 1

    synced = []
    targets_content = [(target, content) for target in targets]
    write_error = write_targets_transactionally(targets_content)
    if write_error:
        print(f"Error: {write_error}")
        return 1
    synced = [str(target.relative_to(repo_root)) for target in targets]
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

    # Preflight every (rel, platform) pair - source containment and target
    # safety - before writing anything at all. Without this upfront pass,
    # writing as we iterate could leave the trees partially synchronized if
    # a later rel/platform pair fails validation (earlier files already
    # written, command still exits nonzero).
    type_conflicts = []
    plan = []
    for rel in sorted(rel_paths, key=str):
        source = canonical_skills_dir / rel
        source_error = validate_sync_source(repo_root, source)
        if source_error:
            type_conflicts.append(f"skills/{rel} - {source_error}")
            continue
        rel_ok = True
        for platform in PLATFORM_DIRS:
            if platform == CANONICAL_DIR:
                continue
            error = validate_sync_target(repo_root, platform, rel)
            if error:
                type_conflicts.append(f"{platform}/skills/{rel} - {error}")
                rel_ok = False
        if rel_ok:
            plan.append(rel)

    total_synced = 0
    if type_conflicts:
        # Full-batch abort: if ANY (rel, platform) pair failed validation,
        # write nothing at all - not even the conflict-free entries -
        # rather than partially applying the sync and reporting a warning
        # afterward. Preflighting-but-still-writing-the-rest would leave
        # the three trees in a mixed state (some paths freshly
        # synchronized, others still stale because of the conflict) every
        # time any single path in the whole tree has a problem, which is
        # exactly the inconsistent partial-sync state this function is
        # meant to avoid.
        print(
            f"Aborting: {len(type_conflicts)} target path(s) failed validation - "
            "writing nothing (not even conflict-free paths) so the sync stays "
            "all-or-nothing:"
        )
        for path in type_conflicts:
            print(f"  - {path}")
    else:
        targets_content = []
        for rel in plan:
            source = canonical_skills_dir / rel
            content = source.read_bytes()
            for platform in PLATFORM_DIRS:
                if platform == CANONICAL_DIR:
                    continue
                target = repo_root / platform / "skills" / rel
                if target.exists() and target.read_bytes() == content:
                    continue
                targets_content.append((target, content))
        write_error = write_targets_transactionally(targets_content)
        if write_error:
            print(f"Error: {write_error}")
            return 1
        for target, _ in targets_content:
            print(f"  - wrote {target.relative_to(repo_root)}")
            total_synced += 1
    print(f"Done. {total_synced} file(s) written/updated from {CANONICAL_DIR}.")

    exit_code = 0
    if type_conflicts:
        print(
            f"\nWARNING: {len(type_conflicts)} target path(s) could not be validated as "
            "safe to write - NOT resolved automatically:"
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

    if args.sync is not None:
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
