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
**Status:** Merged

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
**Status:** Implementation complete, pending PR/merge

**Problem:** Step 9 of the Initialize skill has the model *regenerate* candidate files three
separate times (once per `.github`/`.claude`/`.gemini`). Any subtle drift between passes (a
dropped bullet, reworded sentence) creates silently inconsistent candidate data depending on
which platform later runs Simulation.

**Depends on:** Nothing.

**Checklist:**
1. ✅ Write `sync_candidate_files.py` (stdlib-only: `shutil`/`pathlib`) at
   `.github/skills/initialize/sync_candidate_files.py`, copied identically to
   `.claude/skills/initialize/` and `.gemini/skills/initialize/`. Script copies
   `candidate_resume.md`, `candidate_profile.md`, `candidate_preferences.md` from
   `.github/skills/simulation/references/` to the equivalent `.claude/` and `.gemini/` paths,
   byte-for-byte, using self-relative path resolution (same pattern as `run_ranking.py`).
2. ✅ Updated `initialize/SKILL.md` Step 9 (all 3 copies, renamed "Save Canonical Files, Then
   Sync Copies") — model writes the three canonical files **once** (to
   `.github/skills/simulation/references/` only), then invokes `python3 sync_candidate_files.py`
   (falling back to `python`) to mirror them, instead of regenerating content per directory.
3. ✅ Added an inline preflight to Step 9 (all 3 copies) — verify `python3`/`python` is available
   before invoking the sync script, same pattern as the Ranking skill's Step 0.
4. ✅ Checked `CLAUDE.md` / `GEMINI.md` — found only generic "Candidate Artifacts" references
   without per-directory-generation language; no changes needed there.
5. ✅ Tested: ran the sync script from all three copies against real candidate files; confirmed
   byte-identical output across all three directories via SHA-256 hash comparison. Sync also
   caught and fixed real pre-existing drift between `.github` and the `.claude`/`.gemini` mirrors
   (the `.claude`/`.gemini` resume files were stale relative to `.github`), validating the exact
   problem this branch targets.
6. ✅ Updated `README.md` — Initialize Skill section now notes the write-once + sync approach;
   Prerequisites now says Python is required by both Ranking and Initialize.

---

### Branch: `simulation-contract-versioning`
**Status:** Implementation complete, pending PR/merge

**Problem:** Simulation output files have no tag indicating which version of
`simulation_contract.md` produced them. If the contract changes (e.g., v2.4 → v2.5), old and new
simulation files can be silently mixed in one ranking run with incompatible scoring assumptions.

**Depends on:** Nothing.

**Checklist:**
1. ✅ Added `- Contract Version: <e.g., "v2.4" — copied verbatim from the header of
   simulation_contract.md>` to `simulation_output_template.md` Metadata section (all 3 copies).
2. ✅ Updated `simulation/SKILL.md` Step 5 (all 3 copies) — instructs the model to stamp the
   current contract version, read directly from `simulation_contract.md`'s own header line
   (e.g., `# Simulation Contract v2.4 — ...`), not paraphrased or inferred.
3. ✅ Updated `run_ranking.py` (all 3 copies) — `extract_metadata()` now reads `Contract Version`;
   `main()` prints a non-blocking warning if simulation files in one run span multiple contract
   versions. Field is internal-only (not added to the CSV schema), so no breaking CSV change.
4. ✅ Checked `README.md` — no Metadata section example exists there, so no update needed.
5. ✅ Tested: two sample simulation files stamped `v2.4` and `v2.5` correctly triggered the
   cross-version warning; single-version runs produce no warning.

---

## Tier 1 — Simulation core (build on each other, do in this order)

### Branch: `simulation-degree-lookup-table`
**Status:** Merged

**Problem:** §5.3 of `simulation_contract.md` is a static, 8-row lookup table (JD field → degree
match category) that the model currently has to recall correctly from prose every run. This is a
frequent source of miscategorization (e.g., confusing Finance/Accounting "Partial" with Economics
"Partial" vs. other rows).

**Depends on:** Nothing (but should land before `simulation-json-sidecar` and
`simulation-subskill-breakdown`, which build on cleaner degree logic).

**Checklist:**
1. ✅ Created `simulation/references/degree_domain_map.json` (all 3 copies) — structured JSON with
   a `candidate_degree_categories.stem_quantitative.jd_domains` lookup (JD field → match category),
   plus `match_labels`, and `_meta` notes covering categorization guidance and a known discrepancy
   with Rule B (see below).
2. ✅ Updated `simulation_contract.md` §5.3 (all 3 copies) — replaced the inline table's authority
   with a pointer to the JSON asset as canonical source; kept the markdown table as a
   human-readable rendering only.
3. ✅ Updated `simulation/SKILL.md` Step 4 (all 3 copies) — instructs the model to look up the
   JD's degree field in `degree_domain_map.json` first, falling back to Rules A–E only for
   domains not present in the table.
4. ✅ Updated `simulation_contract.md` §5.2 (all 3 copies) — clarified Rules A–E apply only when
   the JD's degree domain (or candidate's degree category) isn't covered by the JSON lookup.
   Documented a known discrepancy: Rule B says Finance/Accounting = Partial for a STEM candidate,
   but the JSON table says No match — the JSON wins per the user's explicit decision to keep the
   table literal rather than silently changing scoring by aligning it to Rule B.
5. ✅ Tested: JSON lookup hits (Computer Science, Finance, Economics) and a miss (Kinesiology,
   correctly falls back to Rules A–E) verified via a Python script reading the JSON directly.
6. **Scope note (raised during implementation):** the JSON/contract only define one candidate
   degree category, `stem_quantitative` — non-STEM candidate backgrounds (Finance, Business,
   Liberal Arts, etc.) aren't yet covered by structured rules. Per user decision, this is tracked
   as its own follow-up branch, `simulation-degree-lookup-non-stem-coverage` (added to this
   roadmap, depends on this branch), rather than expanding scope here. Also added categorization
   guidance in this branch so degree-category placement considers `candidate_profile.md`
   skills/coursework and `candidate_preferences.md`, not the degree title alone, for borderline
   STEM cases.

---

### Branch: `simulation-degree-lookup-non-stem-coverage`
**Status:** Merged

**Problem:** `degree_domain_map.json` (introduced in `simulation-degree-lookup-table`) only
defines a single candidate degree category, `stem_quantitative`. The engine currently has no
explicit, structured coverage for candidates whose own degree is **not** STEM/quantitative (e.g.,
Finance, Accounting, Business, Liberal Arts, Economics, etc.) — these candidates fall through
entirely to §5.2 Rules A–E, which are themselves only written from the perspective of a STEM
candidate evaluated against a non-STEM JD (Rule B), not the reverse case. This means the engine
is not yet domain-agnostic: a non-STEM candidate applying to a matching non-STEM role, a STEM
role, or a role requiring a related-but-different non-STEM domain has no clear, deterministic
mapping today. Known gaps surfaced while building the STEM table:

1. Non-STEM candidate + matching non-STEM JD (e.g., Finance degree candidate, Finance JD) — no
   explicit rule states this should be a Direct match.
2. Non-STEM candidate + STEM JD (e.g., Business degree candidate, Data Science JD) — outcome
   (No match vs. Hard mismatch) isn't defined.
3. Non-STEM candidate with quantitative minor/coursework (e.g., Business major with a Statistics
   minor) — borderline category-upgrade case, same pattern as the skills/preferences guidance
   added for STEM candidates in `simulation-degree-lookup-table`, but not yet defined for
   non-STEM starting categories.
4. Career switchers — non-STEM degree but substantial hands-on technical/engineering experience —
   the degree-vs-experience interaction isn't called out (may belong partly in §6 Years-of-
   Experience Mapping, but the cross-reference isn't documented anywhere).

**Depends on:** `simulation-degree-lookup-table` (extends the same JSON structure and contract
sections).

**Checklist:**
1. ✅ Added three new `candidate_degree_categories` entries to `degree_domain_map.json` (all 3
   copies): `business_finance_accounting`, `liberal_arts_humanities`, `social_sciences` — each
   with its own `jd_domains` match table analogous to `stem_quantitative` (e.g.,
   `business_finance_accounting.finance = direct`, `.computer science = no_match`;
   `social_sciences.data science = partial`, reflecting common stats/research-methods overlap).
2. ✅ Updated `simulation_contract.md` §5.2 (all 3 copies) — added **Rule F** (non-STEM candidate
   + matching non-STEM JD domain → Direct/Equivalent per the matched category table) and **Rule
   G** (non-STEM candidate + unrelated or STEM JD domain → No match, not Hard mismatch, unless
   skills/preferences upgrade the categorization).
3. ✅ Updated `simulation_contract.md` §5.3 (all 3 copies) — lookup instructions now cover all
   four categories (or "none of these" → fallback to Rules A–G); added human-readable tables for
   all four categories.
4. ✅ Updated `simulation/SKILL.md` Step 4 (all 3 copies) — degree-category determination now
   spans all four categories, references the career-switcher interaction (§6.3), and updates the
   Rules A–E → A–G reference.
5. ✅ Added `simulation_contract.md` §6.3 "Degree-vs-Experience Interaction (Career Switchers)"
   (all 3 copies) — degree match label stays as computed by §5, but §8 Recruiter Decision must
   weigh it alongside substantial directly relevant professional/project experience rather than
   treating the mismatch in isolation. Cross-referenced from the JSON's new
   `_meta.career_switcher_guidance` field.
6. ✅ Tested: verified all four categories resolve correctly for representative hits
   (`stem_quantitative`+CS, `business_finance_accounting`+Finance,
   `liberal_arts_humanities`+Communications, `social_sciences`+Psychology and +Data Science
   partial-match) and a miss (`social_sciences`+Nursing correctly falls back to Rules A–G) via a
   Python script reading the JSON directly.

---

### Branch: `simulation-deterministic-scoring-formula`
**Status:** Merged

**Problem:** §8.1/§8.2 give the model a *range* to pick a number from ("Very High: 80–95%"), with
no formula — so identical inputs can legitimately produce different percentages across runs,
breaking the contract's own "deterministic" claim and directly affecting downstream ranking scores.

**Depends on:** `simulation-degree-lookup-table` (recommended first, since the formula will consume
the now-deterministic degree match category as an input).

**Checklist:**
1. ✅ Designed a point-based formula for Recruiter Screen Likelihood and Interview Likelihood,
   derived from countable factors already produced earlier in the same simulation (Skill Score
   from Required Skills match counts, Degree Score from the §5 match label, Experience Score from
   the §6 match label, Preference Penalty from §7 violation severities) — mirrors the point-value
   conventions already used in `ranking_rules.md`.
2. ✅ Documented the formula explicitly in `simulation_contract.md` §8 (replaced "pick a value in
   this range" language with Scoring Inputs, weighted formulas, a Hard Reject Override, and
   redefined non-overlapping band-label lookup tables).
3. ✅ Updated `simulation/SKILL.md` Step 4 — the Recruiter Decision bullet now instructs the model
   to *compute* (not guess) the percentage using the documented §8 formula.
4. ✅ Added 3 worked numeric examples directly in the contract (strong match, moderate match with
   a preference penalty, and hard reject override) with concrete arithmetic.
5. ✅ Verified determinism: re-ran the formula's arithmetic via a standalone script for both
   worked examples and confirmed the computed percentages match the documented values exactly
   (round-half-up specified explicitly to avoid banker's-rounding ambiguity). Confirmed
   `run_ranking.py`'s `extract_recruiter_interview()` regex (`\*\*Recruiter Screen
   Likelihood:\*\*\s*(\d+)%` / same for Interview) is unaffected — output prose format unchanged.

---

### Branch: `simulation-json-sidecar`
**Status:** Implementation complete, pending PR/merge

**Problem:** `run_ranking.py` depends on exact prose strings (e.g.,
`**Match Category:** ✔ Direct`, `**Recruiter Screen Likelihood:** 85%`). If the model paraphrases
or reformats, parsing silently breaks and the role gets a neutral default score with no warning to
the user.

**Depends on:** `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula`
(sidecar should carry the now-deterministic values from those branches).

**Checklist:**
1. ✅ Added a new required output artifact: `skills/simulation/simulations/<timestamp>_<role>.json`,
   written alongside the existing `.md` file, containing: `company`, `title`, `posting_date`,
   `compensation`, `location`, `years_required`, `degree_match` (enum), `skill_alignment` (enum),
   `experience_match` (enum), `preference_violations` (list of `{severity, description}`),
   `recruiter_pct`, `interview_pct`, `fit_category` (enum), `internship_mode` (bool),
   `contract_version`. Schema documented in new contract §11, with a literal template file at
   `assets/templates/simulation_output_sidecar_template.json`.
2. ✅ Updated `simulation_output_template.md` — added a note documenting the sidecar as a required
   companion file, not a replacement for the markdown (markdown remains the human-readable
   record).
3. ✅ Updated `simulation/SKILL.md` Step 5/6/7 — Step 5 now instructs populating the sidecar
   template alongside the markdown; Step 6 (renamed "Save Output Files") instructs writing both
   files with matching base filenames and treating a missing sidecar as a save failure; Step 7's
   confirmation message now references both files.
4. ✅ Updated `run_ranking.py` (all 3 copies) — added `score_from_json()` which reads the `.json`
   sidecar when present (mapping its enums to the same raw point scales the regex path uses);
   falls back to the existing regex-on-markdown parsing only if no sidecar exists or it's
   unreadable/missing required fields (backward compatibility with pre-existing simulation
   files).
5. ✅ Updated `references/ranking_rules.md` — added a note under §2 Required Inputs establishing
   the JSON sidecar as the canonical machine-readable source, markdown as canonical
   human-readable source.
6. ✅ Tested: created a matched `.md` + `.json` pair and a legacy `.md`-only file with identical
   underlying data, ran `run_ranking.py` — both rows produced byte-identical scores/composite in
   the output CSV, confirming the JSON path and regex-fallback path agree exactly. Test files
   removed after verification.

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
| 1 | `ranking-internship-flag` | — | Merged |
| 1 | `initialize-file-sync` | — | Merged |
| 1 | `simulation-contract-versioning` | — | Merged |
| 1 | `resume-restructure-fact-guard` | — | Not started |
| 1 | `golden-examples-fewshot` | — | Not started |
| 2 | `simulation-degree-lookup-table` | — | Merged |
| 2b | `simulation-degree-lookup-non-stem-coverage` | `simulation-degree-lookup-table` | Merged |
| 3 | `simulation-deterministic-scoring-formula` | `simulation-degree-lookup-table` | Merged |
| 4 | `simulation-json-sidecar` | `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula` | Implementation complete, pending PR/merge |
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
- 2026-08-13: `ranking-internship-flag` merged into `main` (PR #3).
- 2026-08-13: `initialize-file-sync` implemented — added `sync_candidate_files.py` (stdlib-only,
  self-relative path resolution) to all 3 skill copies; Initialize `SKILL.md` Step 9 now writes
  candidate files once to `.github` canonical location and invokes the sync script instead of
  regenerating content 3x; added Python preflight inline; updated README. Verified byte-identical
  output across all 3 directories via hash comparison — sync also fixed real pre-existing drift
  between `.github` and the `.claude`/`.gemini` mirrors. Ready for PR/merge.
- 2026-08-13: `initialize-file-sync` merged into `main` (PR #4).
- 2026-08-13: `simulation-contract-versioning` implemented — added `Contract Version` metadata
  field to simulation output template (all 3 copies); `SKILL.md` Step 5 instructs stamping the
  version verbatim from `simulation_contract.md`'s header; `run_ranking.py` reads the field and
  prints a non-blocking warning if a ranking run spans multiple contract versions. Verified with
  sample files at v2.4/v2.5 triggering the warning correctly. Ready for PR/merge.
- 2026-08-13: `simulation-contract-versioning` merged into `main` (PR #5).
- 2026-08-13: `simulation-degree-lookup-table` implemented — added `degree_domain_map.json` (all
  3 copies) as authoritative source for §5.3, replacing model-recalled prose table; contract §5.2
  now clarifies Rules A–E only apply on JSON miss; documented known Rule B vs. JSON discrepancy
  (Finance/Accounting) per explicit user decision to keep the JSON literal. Also added
  categorization guidance so degree-category placement weighs `candidate_profile.md` skills and
  `candidate_preferences.md`, not just the degree title, for borderline STEM cases. Verified
  lookup hit/miss/fallback behavior via script. Added a new follow-up branch,
  `simulation-degree-lookup-non-stem-coverage`, to track full non-STEM-candidate support (raised
  during implementation, scoped out of this branch per user decision). Ready for PR/merge.
- 2026-08-14: `simulation-degree-lookup-table` merged into `main` (PR #6).
- 2026-08-14: `simulation-degree-lookup-non-stem-coverage` implemented — added
  `business_finance_accounting`, `liberal_arts_humanities`, and `social_sciences` categories to
  `degree_domain_map.json` (all 3 copies), each with its own JD-domain match table; added Rule F
  (non-STEM candidate + matching non-STEM JD → Direct/Equivalent) and Rule G (non-STEM candidate +
  unrelated/STEM JD → No match, not Hard mismatch) to contract §5.2; extended §5.3 lookup
  instructions and tables to all four categories; added §6.3 Degree-vs-Experience Interaction for
  career switchers, cross-referenced from the JSON's `_meta.career_switcher_guidance`. Updated
  `simulation/SKILL.md` Step 4 accordingly. Verified all four categories resolve correctly for
  representative hits and a miss (correct fallback) via script. Ready for PR/merge.
- 2026-08-14: `simulation-degree-lookup-non-stem-coverage` merged into `main` (PR #7).
- 2026-08-14: `simulation-deterministic-scoring-formula` implemented — replaced contract §8's
  "pick a value from this range" band language with a computed point-based formula: Skill/Degree/
  Experience Scores (0-100) derived from existing §4/§5/§6 match labels, weighted formulas for
  Recruiter Screen Likelihood (0.40/0.35/0.25) and Interview Likelihood (0.35/0.40/0.25, capped
  at ≤ Recruiter%), a Preference Penalty table, a fixed Hard Reject Override (Recruiter%=2,
  Interview%=1), redefined non-overlapping band-label tables, and an explicit round-half-up rule
  to avoid banker's-rounding ambiguity. Added 3 worked numeric examples. Updated
  `simulation/SKILL.md` Step 4 to instruct computing (not guessing) via the formula. Verified all
  3 worked examples' arithmetic independently via script; confirmed `run_ranking.py`'s
  recruiter/interview regex extraction is unaffected (output prose format unchanged). Also
  corrected two stale "pending PR/merge" statuses in this pass for
  `simulation-degree-lookup-non-stem-coverage` (own section + summary table), which was already
  confirmed merged as PR #7. Ready for PR/merge.
- 2026-08-17: `simulation-deterministic-scoring-formula` merged into `main` (PR #8).
- 2026-08-17: `simulation-json-sidecar` implemented — added a required `.json` sidecar output
  (same base filename as the `.md` output) documented in new contract §11 and a literal template
  at `assets/templates/simulation_output_sidecar_template.json`; sidecar carries `company`,
  `title`, `posting_date`, `compensation`, `location`, `years_required`, `degree_match` (enum),
  `skill_alignment` (enum), `experience_match` (enum), `preference_violations` (list of
  `{severity, description}`), `recruiter_pct`, `interview_pct`, `fit_category` (enum),
  `internship_mode` (bool), `contract_version`. Updated `simulation_output_template.md` with a
  note documenting the sidecar as a required companion, not a replacement. Updated
  `simulation/SKILL.md` Steps 5-7 to populate/save/confirm both files together, treating a
  missing sidecar as a save failure. Updated `run_ranking.py` (all 3 copies) with
  `score_from_json()`, which reads the sidecar directly when present and falls back to the
  existing regex-on-markdown parsing only when no sidecar exists or it's unreadable/incomplete.
  Updated `ranking_rules.md` §2 to document the sidecar as the canonical machine-readable source.
  Verified parity: built a matched `.md`+`.json` pair and a legacy `.md`-only file with identical
  underlying data, ran `run_ranking.py`, and confirmed both rows scored identically in the output
  CSV. Ready for PR/merge.
