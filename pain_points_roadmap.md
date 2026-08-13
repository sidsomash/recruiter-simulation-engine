# Pain Points Roadmap

This document tracks known pain points across the Initialize, Simulation, Ranking, and
Resume-Restructure skills, and organizes the fixes into independently branchable units of
work. Each section below = one branch. Branches are ordered by dependency (earlier branches
should be merged before later ones that depend on them), but branches within the same
"tier" are independent of each other and can be worked in any order / in parallel.

Every branch must touch all three skill copies (`.github/`, `.claude/`, `.gemini/`) to keep
them in sync, unless explicitly noted otherwise.

**Status legend:** `Not started` / `In progress` / `Blocked` / `Merged`

This file is the durable source of truth for progress (it survives across sessions/branches,
unlike any session-local tracker). Update the status marker on a branch's heading and the
summary table row whenever work starts, gets blocked, or merges. Add a dated entry to the
**Progress Log** at the bottom whenever a branch's status changes.

---

## Tier 0 — Independent, low-risk fixes

### Branch: `ranking-internship-flag`
**Status:** In progress (implementation complete, pending PR/merge)

**Problem:** `run_ranking.py` currently guesses internship mode via a regex on the job title/text
(`is_internship()`), duplicating logic the Simulation skill's own Step 3 already decided
authoritatively. The two heuristics can disagree (e.g., "Internship Program **Manager**" title
false-positives as an internship role).

**Depends on:** Nothing.

**Checklist:**
1. Update `simulation_output_template.md` (all 3 copies) — add `- Internship Mode: Yes/No` to the
   `## 0. Metadata` section.
2. Update `simulation/references/simulation_contract.md` — note that the Step 3 mode decision
   must be recorded verbatim in the output Metadata section.
3. Update `simulation/SKILL.md` Step 3/Step 5 — instruct the model to populate the new metadata
   field with its own mode determination.
4. Update `ranking/run_ranking.py` (all 3 copies) — read `Internship Mode` from `extract_metadata()`
   instead of calling `is_internship()` on title/text; keep the keyword-regex function only as a
   fallback for older simulation files that lack the field (log a warning when falling back).
5. Regenerate/verify with a sample simulation file containing the new metadata field.
6. Update `README.md` if the Metadata section example needs the new field mentioned.

---

### Branch: `initialize-file-sync`
**Status:** Not started

**Problem:** Step 9 of the Initialize skill has the model *regenerate* candidate files three
separate times (once per `.github`/`.claude`/`.gemini`). Any subtle drift between passes (a
dropped bullet, reworded sentence) creates silently inconsistent candidate data depending on
which platform later runs Simulation.

**Depends on:** Nothing.

**Checklist:**
1. Write `sync_candidate_files.py` (stdlib-only: `shutil`, `pathlib`) at a shared location
   (e.g., `.github/skills/initialize/sync_candidate_files.py`, copied to `.claude`/`.gemini` like
   the ranking script). Script copies `candidate_resume.md`, `candidate_profile.md`,
   `candidate_preferences.md` from `.github/skills/simulation/references/` to the equivalent
   `.claude/` and `.gemini/` paths, byte-for-byte.
2. Update `initialize/SKILL.md` Step 9 — model writes the three canonical files **once** (to
   `.github/skills/simulation/references/` only), then invokes
   `python3 sync_candidate_files.py` to mirror them, instead of regenerating content per directory.
3. Add a Step 0 preflight to `initialize/SKILL.md` (same pattern as ranking) — verify
   `python3`/`python` is available before invoking the sync script.
4. Update `CLAUDE.md` / `GEMINI.md` — reflect that `.claude`/`.gemini` candidate files are now
   synced copies, not independently generated.
5. Test: run Initialize end-to-end, confirm all three directories are byte-identical
   (`Compare-Object`/`diff`).
6. Update `README.md` Initialize section if it describes the old per-directory generation process.

---

### Branch: `simulation-contract-versioning`
**Status:** Not started

**Problem:** Simulation output files have no tag indicating which version of
`simulation_contract.md` produced them. If the contract changes (e.g., v2.4 → v2.5), old and new
simulation files can be silently mixed in one ranking run with incompatible scoring assumptions.

**Depends on:** Nothing.

**Checklist:**
1. Add `- Contract Version: v2.4` (or current version) to `simulation_output_template.md`
   Metadata section (all 3 copies).
2. Update `simulation/SKILL.md` Step 5 — instruct the model to stamp the current contract version
   from `simulation_contract.md`'s own header into the output.
3. Optionally: update `run_ranking.py` to surface a warning if simulation files in one run span
   multiple contract versions (non-blocking, informational only).
4. Update `README.md` if Metadata section example needs the new field.

---

## Tier 1 — Simulation core (build on each other, do in this order)

### Branch: `simulation-degree-lookup-table`
**Status:** Not started

**Problem:** §5.3 of `simulation_contract.md` is a static, 8-row lookup table (JD field → degree
match category) that the model currently has to recall correctly from prose every run. This is a
frequent source of miscategorization (e.g., confusing Finance/Accounting "Partial" with Economics
"Partial" vs. other rows).

**Depends on:** Nothing (but should land before `simulation-json-sidecar` and
`simulation-subskill-breakdown`, which build on cleaner degree logic).

**Checklist:**
1. Create `simulation/references/degree_domain_map.json` (all 3 copies) — literal structured
   version of the §5.3 table: `{"computer science": "equivalent", "data science": "direct", ...}`.
2. Update `simulation_contract.md` §5.3 — replace the inline markdown table with a pointer to the
   JSON asset as the canonical source (keep a human-readable rendering of the table for reference,
   but mark the JSON as authoritative).
3. Update `simulation/SKILL.md` Step 4/Degree Mapping — instruct the model to look up the JD's
   degree field in `degree_domain_map.json` first, falling back to Rules A–E judgment only for
   domains not present in the table.
4. Update `references/simulation_contract.md` §5.2 Rules A–E — clarify these rules apply only when
   the JD's degree domain isn't found in the JSON lookup.
5. Test with 2–3 sample JDs covering table hits (CS, Finance) and a table miss (e.g., "Kinesiology")
   to confirm fallback-to-rules behavior still works.

---

### Branch: `simulation-deterministic-scoring-formula`
**Status:** Not started

**Problem:** §8.1/§8.2 give the model a *range* to pick a number from ("Very High: 80–95%"), with
no formula — so identical inputs can legitimately produce different percentages across runs,
breaking the contract's own "deterministic" claim and directly affecting downstream ranking scores.

**Depends on:** `simulation-degree-lookup-table` (recommended first, since the formula will consume
the now-deterministic degree match category as an input).

**Checklist:**
1. Design a point-based formula for Recruiter Screen Likelihood and Interview Likelihood, derived
   from countable factors already produced earlier in the same simulation (# Direct/Equivalent
   skill matches, # gaps, degree match tier, experience match tier, preference violation count) —
   mirror the style already used in `ranking_rules.md`'s composite formula.
2. Document the formula explicitly in `simulation_contract.md` §8 (replace "pick a value in this
   range" language with "compute using this formula, then map the result into the corresponding
   band label").
3. Update `simulation/SKILL.md` Step 4 — instruct the model to compute (not guess) the percentage
   using the documented formula.
4. Add 2–3 worked numeric examples directly in the contract so the model has concrete
   arithmetic to pattern-match against.
5. Test: run the same JD/resume pair twice, confirm identical recruiter/interview percentages.

---

### Branch: `simulation-json-sidecar`
**Status:** Not started

**Problem:** `run_ranking.py` depends on exact prose strings (e.g.,
`**Match Category:** ✔ Direct`, `**Recruiter Screen Likelihood:** 85%`). If the model paraphrases
or reformats, parsing silently breaks and the role gets a neutral default score with no warning to
the user.

**Depends on:** `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula`
(sidecar should carry the now-deterministic values from those branches).

**Checklist:**
1. Add a new required output artifact: `skills/simulation/simulations/<timestamp>_<role>.json`,
   written alongside the existing `.md` file, containing: `company`, `title`, `posting_date`,
   `compensation`, `location`, `years_required`, `degree_match` (enum), `skill_alignment` (enum),
   `experience_match` (enum), `preference_violations` (list of `{severity, description}`),
   `recruiter_pct`, `interview_pct`, `fit_category` (enum), `internship_mode` (bool),
   `contract_version`.
2. Update `simulation_output_template.md` — document the sidecar as a required companion file,
   not a replacement for the markdown (markdown remains the human-readable record).
3. Update `simulation/SKILL.md` Step 5/6 — instruct the model to write both files with matching
   base filenames.
4. Update `run_ranking.py` (all 3 copies) — prefer reading the `.json` sidecar when present; fall
   back to the existing regex-on-markdown parsing only if no sidecar exists (backward
   compatibility with pre-existing simulation files).
5. Update `references/ranking_rules.md` — note the JSON sidecar as the canonical machine-readable
   source of truth, markdown as the canonical human-readable source.
6. Test: generate a sample sidecar + run `run_ranking.py`, confirm it reads JSON values directly
   and produces identical CSV output to the regex path on the same inputs.

---

### Branch: `simulation-output-validator`
**Status:** Not started

**Problem:** Nothing currently checks a generated simulation output against the required
structure/enum values before it's saved — malformed output is only discovered later, downstream,
when ranking silently mis-scores it.

**Depends on:** `simulation-json-sidecar` (validator checks the JSON schema primarily, markdown
secondarily).

**Checklist:**
1. Write `validate_simulation_output.py` (stdlib-only) — checks: all 8 required markdown sections
   present; JSON sidecar has all required keys; enum fields (`degree_match`, `fit_category`, etc.)
   match one of the allowed values; percentages are 0–100 integers.
2. Update `simulation/SKILL.md` Step 6 (Save Output File) — instruct the model to run the
   validator against the just-written files before returning its confirmation message; if
   validation fails, regenerate the offending section(s) rather than saving invalid output.
3. Add a Step 0 preflight (python3/python check) to `simulation/SKILL.md`, consistent with the
   Ranking skill's pattern.
4. Test with a deliberately malformed sample file to confirm the validator catches it.

---

### Branch: `simulation-subskill-breakdown`
**Status:** Not started

**Problem:** Step 4 ("Apply Simulation Contract") asks the model to perform 8 distinct analyses in
one pass, each with its own branching rules — the single biggest source of rule-blending errors,
especially for smaller/cheaper models.

**Depends on:** `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula`,
`simulation-json-sidecar`, `simulation-output-validator` (this is the biggest structural change and
should land last, once the target schema/formulas/validation are stable).

**Checklist:**
1. Restructure `simulation/SKILL.md` Step 4 into explicit sequential sub-steps, each producing a
   discrete, checkable output before moving to the next:
   - 4a. JD parser → structured metadata (already partially Step 2; formalize as JSON)
   - 4b. Mode classifier (Full-time vs. Internship) — isolated decision, recorded before anything
     else depends on it
   - 4c. Skill & Responsibility mapping
   - 4d. Degree mapping (using the JSON lookup table)
   - 4e. Experience mapping
   - 4f. Preference violation check
   - 4g. Recruiter decision synthesis (using the deterministic formula)
   - 4h. Final fit summary + output assembly (markdown + JSON sidecar)
2. Update `simulation_contract.md` to explicitly reference this sub-step ordering (contract logic
   itself doesn't change, only the orchestration granularity).
3. Consider whether any sub-steps warrant becoming their own slash-invocable skills vs. remaining
   internal steps of one skill — default recommendation is to keep them as one skill with
   explicit internal checkpoints (simpler UX), only splitting into separate skills if a sub-step
   needs independent reuse (e.g., the JD parser being reused by Resume-Restructure).
4. Test end-to-end with 2–3 varied JDs (full-time, internship, ambiguous degree) to confirm output
   parity with the pre-refactor monolithic version.

---

## Tier 2 — Resume-Restructure

### Branch: `resume-restructure-fact-guard`
**Status:** Not started

**Problem:** The skill's "aggressive rewrite" / "maximum recruiter signal" instructions create
fabrication pressure — a classic LLM failure mode is inventing a metric that "sounds right." Step 5
("Validate Against Resume Guidelines") is self-graded by the same model/pass that wrote the
rewrite, so hallucinations aren't reliably caught.

**Depends on:** Nothing (standalone script, can be done in parallel with Tier 1).

**Checklist:**
1. Write `fact_guard.py` (stdlib-only: `re`) — scans the tailored resume output for quantitative
   claims (`%`, `$`, `\d+x`, "reduced by", "increased by", "grew", etc.) and fuzzy-matches each
   against the original `candidate_resume.md` text; flags any claim not traceable to the source.
2. Update `resume-restructure/SKILL.md` Step 5 — replace/augment the self-graded validation with
   an explicit invocation of `fact_guard.py` against the draft output; only proceed to Step 6/7 if
   no unflagged (or user-approved) new claims remain.
3. Add a Step 0 preflight (python3/python check), consistent with other scripted skills.
4. Test with a deliberately embellished sample rewrite to confirm flags are raised correctly, and
   with a faithful rewrite to confirm no false positives.

---

### Branch: `resume-restructure-shared-context`
**Status:** Not started

**Problem:** The skill currently re-derives JD context (skills, priorities, domain) from the
simulation's *prose*, inheriting any parsing errors from that prose and duplicating extraction
logic that the Simulation skill already did once.

**Depends on:** `simulation-json-sidecar` (needs the sidecar to exist as the shared source of
truth).

**Checklist:**
1. Update `resume-restructure/SKILL.md` Step 2 ("Extract JD Context from Simulation") — read the
   simulation's `.json` sidecar directly instead of re-parsing the `.md` prose.
2. Update `resume-restructure/references/resume_guidelines.md` if it references specific prose
   patterns from simulation output that no longer need to be regex-matched.
3. Test: run Resume-Restructure against a simulation with a sidecar, confirm identical or improved
   context extraction vs. the prior prose-parsing approach.

---

## Tier 3 — Cross-cutting (independent, can be done anytime)

### Branch: `golden-examples-fewshot`
**Status:** Not started

**Problem:** Skills currently only provide fill-in-the-blank templates, not fully worked examples.
Few-shot examples are typically a bigger lever for weaker-model compliance than additional prose
rules.

**Depends on:** Nothing.

**Checklist:**
1. Add `simulation/references/example_simulation_output.md` — one complete, realistic worked
   example (with plausible JD + resume) showing correct section formatting, enum usage, and
   reasoning style.
2. Add `resume-restructure/references/example_tailored_resume.md` — one worked example showing
   appropriate emphasis-shifting without fabrication.
3. Update both skills' `SKILL.md` References sections to point to the new example files and
   instruct the model to use them as a formatting/style reference (not to copy content).
4. Keep examples anonymized/generic (no real company or personal data).

---

## Suggested Branch Order Summary

| Order | Branch | Depends on | Status |
|---|---|---|---|
| 1 | `ranking-internship-flag` | — | In progress |
| 1 | `initialize-file-sync` | — | Not started |
| 1 | `simulation-contract-versioning` | — | Not started |
| 1 | `resume-restructure-fact-guard` | — | Not started |
| 1 | `golden-examples-fewshot` | — | Not started |
| 2 | `simulation-degree-lookup-table` | — | Not started |
| 3 | `simulation-deterministic-scoring-formula` | `simulation-degree-lookup-table` | Not started |
| 4 | `simulation-json-sidecar` | `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula` | Not started |
| 5 | `simulation-output-validator` | `simulation-json-sidecar` | Not started |
| 5 | `resume-restructure-shared-context` | `simulation-json-sidecar` | Not started |
| 6 | `simulation-subskill-breakdown` | all Tier 1 branches above | Not started |

Rows sharing the same "Order" number have no dependency on each other and can be branched/worked
in parallel.

---

## Progress Log

Add a dated entry here every time a branch's status changes (started, blocked, merged). Keep
entries short — one line per event.

- 2026-08-13: `ranking-internship-flag` implemented — added `Internship Mode` metadata field to
  simulation output template/contract/SKILL.md; `run_ranking.py` now reads it directly with a
  keyword-based fallback (+ warning) for older simulation files lacking the field. Verified with
  sample files covering both paths. Ready for PR/merge.
