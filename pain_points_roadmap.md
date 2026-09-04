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
**Status:** Merged

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
**Status:** Merged

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
**Status:** Merged

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
**Status:** Merged

**Problem:** Nothing currently checks a generated simulation output against the required
structure/enum values before it's saved — malformed output is only discovered later, downstream,
when ranking silently mis-scores it.

**Depends on:** `simulation-json-sidecar` (validator checks the JSON schema primarily, markdown
secondarily).

**Checklist:**
1. ✅ Wrote `validate_simulation_output.py` (stdlib-only, all 3 copies) — checks: all 8 required
   Markdown sections present; empty Preference Violations section without the required "no
   preferences" statement; Recruiter/Interview Likelihood are integer percentages; JSON sidecar
   has all required keys and is valid JSON; enum fields (`degree_match`, `skill_alignment`,
   `experience_match`, `fit_category`, violation `severity`) match one of the allowed values;
   `recruiter_pct`/`interview_pct` are 0–100 integers with `interview_pct` not exceeding
   `recruiter_pct` (contract §8.3); `internship_mode` is a real boolean; plus a cross-file check
   that the Markdown's percentages/Contract Version agree exactly with the JSON sidecar (contract
   §11's consistency rule).
2. ✅ Updated `simulation/SKILL.md` Step 6 (Save Output Files) — instructs running the validator
   against the just-written files before treating the save as final; on failure, regenerate only
   the offending section(s)/field(s) (re-derived from Step 4, not guessed) and re-validate, rather
   than saving invalid output. Step 7's confirmation message now says "Saved and validated".
3. ✅ Added a Step 0 preflight (python3/python check) to `simulation/SKILL.md`, mirroring the
   Ranking skill's existing Step 0 pattern exactly. Added the validator script to the References
   list.
4. ✅ Tested with a deliberately malformed sample `.md`+`.json` pair (missing 5 Markdown sections,
   non-numeric percentage string, invalid `degree_match`/`severity` enums, non-boolean
   `internship_mode`, `interview_pct` > `recruiter_pct`) — validator correctly caught all 10
   issues with clear, specific messages. Also confirmed a valid matched pair passes cleanly. Test
   files removed after verification.

---

### Branch: `simulation-subskill-breakdown`
**Status:** Ready for review (all checklist items complete)

**Problem:** Step 4 ("Apply Simulation Contract") asks the model to perform 8 distinct analyses in
one pass, each with its own branching rules — the single biggest source of rule-blending errors,
especially for smaller/cheaper models.

**Depends on:** `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula`,
`simulation-json-sidecar`, `simulation-output-validator` (this is the biggest structural change and
should land last, once the target schema/formulas/validation are stable).

**Checklist:**
1. ✅ Restructured `simulation/SKILL.md` Step 4 into explicit sequential sub-steps, each producing
   a discrete, checkable output before moving to the next:
   - 4a. JD parser → structured metadata (already partially Step 2; formalize as JSON)
   - 4b. Mode classifier (Full-time vs. Internship) — isolated decision, recorded before anything
     else depends on it
   - 4c. Skill & Responsibility mapping
   - 4d. Degree mapping (using the JSON lookup table)
   - 4e. Experience mapping
   - 4f. Preference violation check
   - 4g. Recruiter decision synthesis (using the deterministic formula)
   - 4h. Final fit summary + output assembly (markdown + JSON sidecar)
   Old Step 5 (Generate Output) folded into 4h; old Steps 6/7 renumbered to 5/6. Propagated
   identically to all three platform copies.
2. ✅ Updated `simulation_contract.md`'s cross-reference to the new step numbering ("Steps 5–6" →
   "Steps 4h–5" for the JSON sidecar description).
3. Consider whether any sub-steps warrant becoming their own slash-invocable skills vs. remaining
   internal steps of one skill — default recommendation is to keep them as one skill with
   explicit internal checkpoints (simpler UX), only splitting into separate skills if a sub-step
   needs independent reuse (e.g., the JD parser being reused by Resume-Restructure). (Not
   pursued — kept as one skill per the default recommendation.)
4. ✅ Tested end-to-end with 3 real, varied JDs against the candidate's actual (if slightly
   outdated) résumé data on `candidate/sid-somashekar`, applying the restructured 4a-4h
   sub-steps by hand and validating the resulting Markdown + JSON sidecar pairs with the
   unchanged `validate_simulation_output.py`:
   - **Mizuho Data Engineer** (full-time, direct STEM-degree/skill match, one moderate
     compensation preference violation) → Strong match, Recruiter 90% / Interview 90%.
   - **Amazon Automation Engineer Intern** (internship; JD requires *current* enrollment
     through a Dec 2027-Aug 2028 graduation window, but the candidate already graduated and
     is employed full-time) → classified as ❌ Hard mismatch (closest analogous rule to
     §5.1's Master's/PhD case, since the JD's specific "already-graduated-but-JD-requires-
     ongoing-enrollment" scenario isn't explicitly named in the contract — flagged as a
     future contract-refinement candidate), triggering the §8.4 override → Hard reject,
     Recruiter 2% / Interview 1%.
   - **ICF Early Talent Acquisition Associate** (full-time, unspecified degree field per
     Rule E, but a full domain shift into HR/recruiting with a 2+ year recruiting-specific
     experience requirement the candidate doesn't meet, plus an explicit avoided-domain
     preference violation) → Weak match, Recruiter 35% / Interview 35%.
   All three pairs passed `validate_simulation_output.py` (structural sections, enum values,
   percentage ranges, and cross-file Markdown/JSON consistency). Independently recomputed all
   three Recruiter%/Interview% formulas in a separate script and confirmed exact agreement
   (90/90, 2/1, 35/35) with no rounding-order discrepancies. Test artifacts were scratch-only
   (not committed to any branch) since the resume used was known to be somewhat outdated;
   confirms output parity and correct checkpoint-sequencing behavior across a full-time
   direct-match case, an internship hard-reject edge case, and a full-time domain-mismatch
   case.

---

## Tier 2 — Resume-Restructure

### Branch: `resume-restructure-fact-guard`
**Status:** Merged (PR #12; follow-up doc fix PR #13)

**Problem:** The skill's "aggressive rewrite" / "maximum recruiter signal" instructions create
fabrication pressure — a classic LLM failure mode is inventing a metric that "sounds right." Step 5
("Validate Against Resume Guidelines") is self-graded by the same model/pass that wrote the
rewrite, so hallucinations aren't reliably caught.

**Depends on:** Nothing (standalone script, can be done in parallel with Tier 1).

**Checklist:**
1. ✅ Wrote `scripts/fact_guard.py` (stdlib-only: `re`, `sys`, `pathlib`) — scans the tailored
   resume output for quantitative claims (`%`, `$`, `\d+x`, record/throughput counts, "reduced/
   increased/grew/improved/saved/cut by ...") and checks each numeric token against the original
   `candidate_resume.md` text; flags any claim not traceable to the source. Placed under
   `scripts/` (not skill root) per the canonical skill directory structure
   (`SKILL.md`/`scripts/`/`references/`/`assets/`), matching the convention `run_ranking.py`
   should also follow (noted as a separate future cleanup, not in scope here).
2. ✅ Updated `resume-restructure/SKILL.md` Step 5 — replaced the self-graded-only validation with
   an explicit invocation of `scripts/fact_guard.py` against the draft output; only proceed to
   Step 6/7 if no unflagged (or user-approved) new claims remain. Also updated References (added
   the script) and Error Handling (Python-unavailable and flagged-claims cases).
3. ✅ Added a Step 0 preflight (python3/python check), consistent with the Ranking skill's Step 0
   pattern.
4. ✅ Tested with a deliberately embellished sample rewrite (fabricated 95% reliability boost,
   $2.3M savings, 3x throughput, 10M records/day) — all 4 correctly flagged; and with a faithful
   rewrite using only claims from the original résumé — 0 false positives, exit code 0. Verified
   the script runs correctly from all 3 propagated copies (`.github`, `.claude`, `.gemini`).
   Test files removed after verification.

---

### Branch: `resume-restructure-shared-context`
**Status:** Merged

**Problem:** The skill currently re-derives JD context (skills, priorities, domain) from the
simulation's *prose*, inheriting any parsing errors from that prose and duplicating extraction
logic that the Simulation skill already did once.

**Depends on:** `simulation-json-sidecar` (needs the sidecar to exist as the shared source of
truth).

**Checklist:**
1. ✅ Update `resume-restructure/SKILL.md` Step 2 ("Extract JD Context from Simulation") — read the
   simulation's `.json` sidecar directly instead of re-parsing the `.md` prose.
2. ✅ Update `resume-restructure/references/resume_guidelines.md` if it references specific prose
   patterns from simulation output that no longer need to be regex-matched. (Reviewed in full —
   no specific prose/regex patterns tied to simulation markdown structure were found; no edit
   needed.)
3. ✅ Test: run Resume-Restructure against a simulation with a sidecar, confirm identical or
   improved context extraction vs. the prior prose-parsing approach. (Verified with a sample
   sidecar + matching `.md` — all structured fields listed in the new Step 2 load correctly from
   JSON.)

**Implementation notes:** Also updated References (added `.json` sidecar as a required target
simulation output, noted as canonical/preferred per `simulation_contract.md` Section 11, "JSON
Sidecar"), Inputs (item 1 now notes sidecar-first extraction), and Step 1 (now loads both `.md`
and `.json` sidecar).
Step 2 explicitly documents which fields come from the sidecar (aggregate/enum fields: company,
title, degree_match, skill_alignment, experience_match, fit_category, recruiter_pct/interview_pct,
internship_mode, compensation/location/years_required) vs. which still require `.md` prose parsing
(per-skill required/preferred tables, responsibility alignment, skill gaps, narrative priorities —
none of which the sidecar carries). Includes a fallback: simulations without a sidecar (legacy,
pre-`simulation-json-sidecar`) fall back to full `.md`-prose parsing as before, mirroring the same
pattern used in `run_ranking.py`'s `score_from_json()` fallback. Propagated to all three platform
copies (`.github`, `.claude`, `.gemini`), preserving each copy's own platform-specific Step 8
example path (the one pre-existing intentional drift point in this file).

---

## Tier 3 — Cross-cutting (independent, can be done anytime)

### Branch: `candidate-branch-isolation`
**Status:** Merged

**Problem:** Candidate PII (résumé, profile, preferences, and by extension simulation/résumé
outputs derived from them) has historically been committed directly onto `main` and other
shared branches, with no enforcement preventing it. This has already caused real incidents this
session: two different candidates' data got mixed into uncommitted changes on `main`, requiring
manual git archaeology to untangle into separate branches after the fact. There was also no
structural guarantee that a skill-development branch (like `simulation-subskill-breakdown`)
couldn't accidentally inherit or carry real candidate PII.

**Depends on:** Nothing (independent of Simulation/Ranking/Resume-Restructure internals).

**Checklist:**
1. ✅ Wrote `.github/skills/initialize/ensure_candidate_branch.py` (mirrored identically to
   `.claude/skills/initialize/` and `.gemini/skills/initialize/`; stdlib-only, no external
   packages) — a deterministic git-branch guard. Given a candidate's name, it slugifies it into
   `candidate/<slug>`, and:
   - No-ops if already on that exact branch.
   - Refuses (exit 1) if the current branch isn't `main` (prevents writing candidate data onto
     a feature branch or a *different* candidate's branch).
   - Refuses (exit 1) if `main` has uncommitted changes (prevents carrying unrelated work onto
     a new candidate branch).
   - Otherwise checks out the branch if it already exists, or creates it fresh off `main`.
   - Never pushes, merges, fetches, or deletes branches — purely local checkout/creation.
   Propagated identically to all three platform copies (`.github`, `.claude`, `.gemini`).
2. ✅ Updated `.github/skills/initialize/SKILL.md` (and its `.claude`/`.gemini` mirrors) — added
   new **Step 5.5** (runs immediately after Step 5's supplemental questioning, before Step 6
   starts building any file content) that invokes the script and handles all three outcomes
   (`OK`/`REFUSED`/`GIT ERROR`). Updated References (added the script), Error Handling (three
   new bullet points for the guard's failure modes), and Notes (documents the `candidate/<slug>`
   branch strategy and that branches are local-only unless the user explicitly pushes).
   Propagated identically to all three platform copies.
3. ✅ Reset `.github/skills/simulation/references/candidate_resume.md`, `candidate_profile.md`,
   and `candidate_preferences.md` on `main` (and the `.claude`/`.gemini` mirrors) back to the
   blank fill-in-the-blank templates from `initialize/SKILL.md`'s own Input Templates section,
   removing real candidate PII that had been committed directly to `main`. Confirmed
   `one_shot_simulation_prompt.md` and the `simulations/`/`resumes/` output directories on
   `main` were already free of committed candidate data (verified via `git show HEAD:<path>`
   before making changes).
4. ✅ Updated root `README.md`: new "Candidate Branch" concept entry, new "🌿 Candidate Data &
   Git Branches" section explaining the full workflow (why, how it works, publishing is opt-in),
   updated Quick Start Step 2 / First-Time Workflow / Intended Workflow to reflect the
   branch-per-candidate flow, updated Prerequisites (git required), updated the Initialize Skill
   summary bullet list, and rewrote two now-outdated FAQ answers ("Can I have multiple candidate
   profiles?", "Should I commit my candidate files to Git?") plus added a new FAQ entry
   explaining the `REFUSED` error states.
5. ✅ Applied the same candidate-file template reset to `simulation-subskill-breakdown`, the one
   pre-existing non-candidate branch that had inherited PII before this branch existed (it
   branched off `main` prior to this cleanup) — done as a follow-up commit directly on that
   branch (`50955f8`).
6. ✅ End-to-end tested `ensure_candidate_branch.py` in an isolated scratch git repo (outside this
   repository, to avoid touching real `main`/candidate branches): verified all 5 code paths —
   (1) happy-path branch creation from `main`, (2) no-op when already on the target branch,
   (3) checkout of an already-existing candidate branch from `main`, (4) refusal when run from a
   non-`main`/non-candidate branch, (5) refusal when `main` has uncommitted changes. All 5
   behaved exactly as documented.

**Implementation notes:** This branch does **not** rewrite existing git history — old commits on
`main` prior to this branch still contain the previously-committed PII in their diffs/blobs.
Purging that would require a history rewrite (`git filter-repo` or similar), which is invasive
(breaks any existing local clones/forks) and out of scope here; flagged as a possible future
follow-up if full historical purge is ever required. This branch only ensures **going forward**,
`main`'s current/working-tree state stays clean and Initialize can't write real data anywhere but
a dedicated candidate branch.

---

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
| 1 | `resume-restructure-fact-guard` | — | Merged |
| 1 | `golden-examples-fewshot` | — | Not started |
| 1 | `candidate-branch-isolation` | — | Merged |
| 2 | `simulation-degree-lookup-table` | — | Merged |
| 2b | `simulation-degree-lookup-non-stem-coverage` | `simulation-degree-lookup-table` | Merged |
| 3 | `simulation-deterministic-scoring-formula` | `simulation-degree-lookup-table` | Merged |
| 4 | `simulation-json-sidecar` | `simulation-degree-lookup-table`, `simulation-deterministic-scoring-formula` | Merged |
| 5 | `simulation-output-validator` | `simulation-json-sidecar` | Merged |
| 5 | `resume-restructure-shared-context` | `simulation-json-sidecar` | Merged |
| 6 | `simulation-subskill-breakdown` | all Tier 1 branches above | Ready for review |

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
- 2026-08-17: `simulation-json-sidecar` merged into `main` (PR #9).
- 2026-08-17: `simulation-output-validator` implemented — added `validate_simulation_output.py`
  (stdlib-only, all 3 copies) checking: all 8 required Markdown sections present; empty
  Preference Violations section without the required "no preferences" statement; Recruiter/
  Interview Likelihood are integer percentages; JSON sidecar has all required keys and is valid
  JSON; enum fields (`degree_match`, `skill_alignment`, `experience_match`, `fit_category`,
  violation `severity`) match allowed values; `recruiter_pct`/`interview_pct` are 0-100 integers
  with the §8.3 `interview_pct ≤ recruiter_pct` clamp enforced; `internship_mode` is a real
  boolean; plus a cross-file check that Markdown percentages/Contract Version agree exactly with
  the JSON sidecar (contract §11's consistency rule). Added a Step 0 preflight (python3/python
  check) to `simulation/SKILL.md`, mirroring the Ranking skill's existing pattern. Updated Step 6
  to run the validator before treating a save as final, regenerating offending section(s) on
  failure rather than saving invalid output; Step 7's confirmation now says "Saved and
  validated". Tested with a deliberately malformed sample pair (10 injected issues across missing
  sections, bad enums, bad types, and the interview/recruiter clamp) — validator caught all of
  them with specific messages; confirmed a valid pair passes cleanly. Test files removed after
  verification. Ready for PR/merge.
- 2026-08-17: `simulation-output-validator` merged into `main` (PR #10).
- 2026-08-17: `resume-restructure-shared-context` implemented — rewrote Resume-Restructure Step 2
  ("Extract JD Context from Simulation") to read the simulation's `.json` sidecar directly for
  structured/aggregate fields (`company`, `title`, `degree_match`, `skill_alignment`,
  `experience_match`, `fit_category`, `recruiter_pct`/`interview_pct`, `internship_mode`,
  `compensation`/`location`/`years_required`), avoiding re-derivation from prose. Documented that
  per-skill match tables, responsibility alignment, skill gaps, and narrative priorities/domain
  inference still require the `.md` prose (the sidecar only stores an aggregate enum, not
  per-skill detail), with a fallback to full `.md`-only parsing for legacy simulations lacking a
  sidecar (mirroring `run_ranking.py`'s `score_from_json()` pattern). Updated References (added
  `.json` sidecar as a required target simulation output), Inputs (item 1), and Step 1 (now loads
  both files) accordingly. Reviewed `resume_guidelines.md` — no prose-pattern-specific references
  found, no edit needed. Verified field extraction against a sample sidecar+`.md` pair (removed
  after testing). Propagated to all 3 platform copies, preserving each copy's own
  platform-specific Step 8 example path (the file's one pre-existing intentional drift point).
  Ready for PR/merge.
- 2026-08-18: `resume-restructure-shared-context` merged into `main` (PR #11), after several
  Copilot PR review rounds addressing internal contradictions ("both required" vs. legacy
  fallback wording in References and Step 2), replacing non-standard `§N` section references with
  the docs' actual `## N. Title` heading format, and adding explicit relative paths when citing
  `simulation_contract.md`/`ranking_rules.md`. Also corrected two stale "pending PR/merge"
  statuses in this pass for `initialize-file-sync` (PR #4) and `simulation-contract-versioning`
  (PR #5), both already confirmed merged earlier in the session.
- 2026-08-18: `resume-restructure-fact-guard` implemented — added `scripts/fact_guard.py`
  (stdlib-only, all 3 copies) which scans a draft tailored résumé for quantitative claims
  (percentages, dollar amounts, multipliers, record/throughput counts, and "reduced/increased/
  grew/improved/saved/cut by ..." phrasing) and flags any whose numeric value doesn't appear in
  the original `candidate_resume.md`. Placed under `scripts/` per the canonical skill directory
  structure (`SKILL.md`/`scripts/`/`references/`/`assets/`) — noted that `run_ranking.py` in the
  Ranking skill doesn't yet follow this convention (sits at skill root); scoped that move to a
  separate future branch per user decision. Updated `resume-restructure/SKILL.md`: added Step 0
  preflight (python3/python check, mirroring Ranking's pattern), rewrote Step 5 to write the
  draft to a file and invoke the script (proceed only on exit 0; correct/remove/get user approval
  on exit 1), added the script to References, and added two Error Handling entries (Python
  unavailable; flagged claims blocking Step 6/7). Tested with a deliberately embellished sample
  (fabricated 95% reliability, $2.3M savings, 3x throughput, 10M records/day — all 4 correctly
  flagged) and a faithful sample (0 false positives, exit 0); verified the script runs correctly
  from all 3 propagated copies. Ready for PR/merge.
- 2026-08-24: `resume-restructure-fact-guard` — fixed an overlap-detection bug in
  `scripts/fact_guard.py`'s `find_claims()` flagged by Copilot PR review: the prior boundary-based
  check (`s[0] <= span[0] < s[1] or s[0] < span[1] <= s[1]`) missed the case where a new match span
  fully encloses an already-seen span while extending past it on both sides (e.g., seen `(5,10)`,
  new `(3,12)`), which could double-report the same underlying claim as two separate flagged
  entries. Replaced with a standard general interval-overlap test
  (`span[0] < s[1] and s[0] < span[1]`). Verified the fix directly (old check returned `False`,
  new check returns `True`, for the enclosing-span case) and re-ran both existing regression
  scenarios (faithful sample: 0 false positives; embellished sample: same 4 correctly flagged
  claims) with no change in behavior. Propagated the fix to all 3 copies (byte-identical after).
- 2026-08-24: `resume-restructure-fact-guard` — addressed a second Copilot PR review round with
  three fixes across all 3 copies. (1) Fixed a substring-matching false-negative in
  `check_claims()`: the prior verification (`normalize(token) in normalized_original`) could
  falsely "verify" a fabricated numeric token that happened to be a substring of an unrelated,
  longer genuine number (e.g., fabricated "1M" matching inside a genuine "11M"). Replaced with a
  new `is_verified()` helper using a digit-boundary-guarded regex search
  (`(?<!\d)` + token + `(?!\d)`) so a match only counts if not immediately adjacent to another
  digit. Verified directly: "1M" vs. original "11M" → correctly unverified; "11M" vs. original
  "11M" → correctly verified; re-ran both faithful (0 flagged, exit 0) and embellished (4 flagged,
  exit 1) regression samples with no behavior change. (2) Corrected an inaccurate exit-code
  docstring claiming "0 - no unverifiable quantitative claims found (or resumes are empty)" —
  an empty original résumé with claims present actually (correctly) exits 1, not 0; docstring now
  just states "no unverifiable quantitative claims found in the tailored résumé." (3) Restored
  Step 5's manual factual-grounding checklist bullets ("All original content is factually
  grounded", "Metrics and accomplishments are preserved") that were dropped when Step 5 was
  rewritten around the script invocation — the script only catches quantitative claims, so
  non-quantitative fabrication (fake responsibilities/technologies/skills) still needs explicit
  manual review; also added a note clarifying the script should be run from the
  `resume-restructure` skill directory (or with an explicit original-résumé path) so its default
  relative path resolves correctly. All fixes propagated to `.github`/`.claude`/`.gemini`,
  verified byte-identical (`scripts/fact_guard.py`) and content-identical apart from the
  pre-existing platform-specific Step 8 path (`SKILL.md`).
- 2026-08-25: `resume-restructure-fact-guard` merged (PR #12). A final post-merge Copilot review
  found Step 5's documented default original-résumé path was wrong
  (`../simulation/references/candidate_resume.md` instead of the actual
  `../../simulation/references/candidate_resume.md`, per `SCRIPT_DIR.parent.parent` in the
  script) and misleadingly implied the default depends on the current working directory, when in
  fact `Path(__file__).resolve()` makes it directory-independent. Fixed the wording in all 3
  copies on branch `resume-restructure-fact-guard-path-doc-fix` (doc-only, no script logic
  changed); merged as PR #13. Local `main` synced, both feature branches deleted. Branch and
  todo now closed.
- 2026-09-02: `simulation-subskill-breakdown` implemented (uncommitted on branch → committed):
  restructured `simulation/SKILL.md` Step 4 into checkpointed sub-steps 4a–4h, folded old Step 5
  into 4h, renumbered old Steps 6/7 to 5/6, updated `simulation_contract.md`'s cross-reference.
  Propagated to all 3 platform copies. End-to-end JD testing still pending; status set to
  "In progress".
- 2026-09-02: Started `candidate-branch-isolation` (new Tier 3 branch, added to roadmap). Wrote
  `initialize/ensure_candidate_branch.py` (deterministic git-branch guard: creates/checks out
  `candidate/<slug>` off `main`, refuses on any other branch or a dirty `main`). Updated
  `initialize/SKILL.md` with new Step 8.5 invoking the guard before any candidate file writes.
  Reset `main`'s `candidate_resume.md`/`candidate_profile.md`/`candidate_preferences.md` (all 3
  platform copies) to blank templates, removing previously-committed real candidate PII. Updated
  root `README.md` with a new "Candidate Data & Git Branches" section and refreshed related
  FAQ/workflow text. All changes propagated to `.github`/`.claude`/`.gemini`. Remaining: apply
  the same template reset to `simulation-subskill-breakdown` (which branched off the pre-cleanup
  `main`), and run a full Initialize-skill dry run to validate the branch guard end-to-end.
- 2026-09-03: `candidate-branch-isolation` completed remaining items — applied the PII template
  reset to `simulation-subskill-breakdown`, and end-to-end tested `ensure_candidate_branch.py`
  in an isolated scratch repo (all 5 code paths verified). Status set to "Ready for review".
  Two Copilot review rounds followed, both addressed on the branch: (1) fixed a slug-collision
  risk (non-ASCII/all-punctuation names falling back to a shared `candidate/candidate` branch —
  now hashes to a unique slug instead), corrected README wording implying the guard blocks *any*
  non-`main` branch (it's actually a no-op on the candidate's own branch), and fixed a stale
  roadmap checklist module list; (2) fixed `ensure_candidate_branch.py` crashing with an
  unhandled `FileNotFoundError` when git isn't on PATH (now returns a deterministic `GIT ERROR`),
  fixed silent truncation of unquoted multi-word candidate names (now joins all of `sys.argv[1:]`
  instead of reading only `argv[1]`), moved the branch guard from Step 8.5 to **Step 5.5** in
  `initialize/SKILL.md` so it unambiguously precedes Step 8's file-writing instructions, and
  corrected a README example that said `candidate/<your-name>` instead of `candidate/<slug>`.
  All fixes verified with dedicated scratch-repo tests (git hidden from PATH, unquoted name,
  two colliding non-ASCII names) and propagated identically to `.github`/`.claude`/`.gemini`.
- 2026-09-03: `candidate-branch-isolation` — two more Copilot review rounds addressed: (3) fixed
  `git status --porcelain`'s exit code being silently discarded in the dirty-`main` check (a
  failing git command was treated as "clean" and let the guard proceed anyway), fixed a
  residual Unicode slug-collision risk where ASCII-folding via a plain regex silently dropped
  diacritics (e.g. differently-accented names could fold to the same base slug) — now uses
  `unicodedata.normalize("NFKD", ...)` plus a stable hash suffix appended whenever the input
  contains any non-ASCII character, and closed an unclosed Markdown backtick span plus reworded
  a guard-behavior description in `README.md` that contradicted the no-op-on-candidate-branch
  behavior. Several subsequent review comments (backtick fix, anchor-link warnings) were
  confirmed stale/false-positive: the intra-README anchors (`#-candidate-data--git-branches`)
  were verified correct against GitHub's actual slug-generation algorithm (emoji-prefixed
  headings get a leading `-`; `&` surrounded by spaces produces a double hyphen). PR merged;
  remote branch deleted. Status set to **Merged**.
- 2026-09-04: `simulation-subskill-breakdown` — closed the last remaining checklist item
  (end-to-end testing). Ran 3 real, varied JDs (Mizuho Data Engineer full-time, Amazon
  Automation Engineer Intern, ICF Early Talent Acquisition Associate) through the restructured
  4a-4h sub-steps against the candidate's real (if slightly outdated) résumé/profile/
  preferences on `candidate/sid-somashekar`, producing Strong match / Hard reject / Weak match
  results respectively. All three Markdown+JSON sidecar pairs passed
  `validate_simulation_output.py`, and the Recruiter%/Interview% formulas were independently
  recomputed and matched exactly (90/90, 2/1, 35/35). The Amazon internship case surfaced a
  genuine contract gap worth a future follow-up: §5.1's Hard Mismatch definition only names the
  Master's/PhD scenario explicitly, not "JD requires ongoing enrollment through a future
  graduation window, candidate already graduated" — handled by analogy this round, flagged for
  a possible future contract refinement rather than silently resolved. Status set to
  **Ready for review**.
