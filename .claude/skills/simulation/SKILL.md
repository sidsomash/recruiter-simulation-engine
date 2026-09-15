---
name: simulation
description: Evaluates a job description against the candidate’s resume, profile, and preferences using a deterministic simulation contract, then outputs and stores a structured simulation result for ranking.
context: fork
---

# Simulation Skill
A deterministic simulation engine that evaluates a job description (JD) against
the candidate’s resume, profile, and preferences. The skill applies a structured
simulation contract, generates a standardized simulation output, and stores the
result for later ranking.

This skill is deterministic in orchestration and dynamic in interpretation.

---

## 📚 References

This skill depends on the following reference files:

- [simulation_contract.md](references/simulation_contract.md)  
- [degree_domain_map.json](references/degree_domain_map.json) — authoritative degree-domain lookup table (see contract §5.3)  
- [candidate_resume.md](references/candidate_resume.md)  
- [candidate_profile.md](references/candidate_profile.md)  
- [candidate_preferences.md](references/candidate_preferences.md) *(optional)*  
- [validate_simulation_output.py](validate_simulation_output.py) — deterministic post-save validator (stdlib-only, see Step 5)  

These files define the candidate’s background and the rules governing simulation behavior.

---

## 🧩 Templates

The simulation output is generated using the following templates:

- [simulation_output_template.md](assets/templates/simulation_output_template.md)  
- [simulation_output_sidecar_template.json](assets/templates/simulation_output_sidecar_template.json) — required companion JSON schema (see contract §11)  
- [skill_mapping_template.md](assets/templates/skill_mapping_template.md)  
- [experience_mapping_template.md](assets/templates/experience_mapping_template.md)  
- [degree_mapping_template.md](assets/templates/degree_mapping_template.md)  

These templates ensure consistent structure across all simulation outputs.

---

## 📝 Inputs

This skill prompts the user to paste the job description (JD) after invocation and uses that pasted JD as the sole input for the simulation. The skill does not rely on any external context or previously stored JDs.

- **job_description** (string, required): Raw text of the job description — the skill will request this from the user at invocation.

No additional parameters, flags, or overrides are supported.

---

## 🧠 Workflow

### **Step 0 — Preflight: Verify Python Is Available**
Output validation (Step 5) is performed by a deterministic script
(`validate_simulation_output.py`), not by the model, so a Python interpreter
must be available before the simulation can be considered complete.

- Try `python3 --version`, then fall back to `python --version` if `python3`
  is not found.
- If neither is available, stop and tell the user: "Python 3.8+ is required
  to validate the simulation output. Please install Python and try again."
  Do not attempt to hand-validate the output as a substitute — determinism
  depends on the script running, not the model self-checking.
- No virtual environment, `pip install`, or `requirements.txt` is needed —
  `validate_simulation_output.py` uses only the Python standard library.

---

### **Step 1 — Load References**
Load all required reference files:

- simulation contract  
- candidate resume  
- candidate profile  
- candidate preferences (if present)  
- all templates  

This ensures the simulation always uses the latest candidate data.

---

### **Step 2 — Parse the Job Description**
Extract structured information into an explicit, machine-readable job metadata object. At minimum, extract the following fields when present in the JD (use conservative heuristics and fallbacks):

- Company / Employer (explicit organization name or hiring team)  
- Job Title (canonicalized)  
- Posting Date / JD timestamp  
- Job URL or source reference  
- Compensation / Pay Range (salary or hourly)  
- Location(s) (city, state, remote/hybrid flags)  
- Required years of experience (numeric range or "entry/mid/senior")  
- Degree requirements (degree level and domain)  
- Internship enrollment window (if the JD requires ongoing enrollment through a stated future
  cutoff date/term, e.g. "must be enrolled through Fall 2026," "graduating December 2026 or
  later" — record the exact cutoff date/term verbatim, or null if the JD gives no such cutoff)  
- Recent-graduate exception (whether the JD's own text explicitly also accepts recent graduates
  alongside currently-enrolled students — record Yes/No/Not stated; this determines whether
  contract §5.2 Rule H's exception applies)  
- Required skills  
- Preferred skills  
- Responsibilities / duties  
- Clearance / defense requirements  
- Internship indicators ("intern", "internship", "summer", "co‑op")  
- Remote / Onsite / Hybrid expectation  
- Level / seniority (if specified)  

If any field is missing, record a null/empty value rather than failing. Convert the JD into a structured internal representation (metadata + parsed sections) that will be used by the rest of the contract.

---

### **Step 3 — Determine Mode (Full‑Time vs Internship)**

Internship Mode is activated if:

- the JD contains internship indicators **OR**
- the candidate profile indicates enrollment **AND** preferences allow internships

No manual override is supported.

Record this determination verbatim in the output's Metadata section as `Internship Mode: Yes`
or `Internship Mode: No` — do not leave it blank, and do not let downstream tooling infer it
from the job title later.

---

### **Step 4 — Apply Simulation Contract**

Apply the contract as a sequence of discrete, checkable sub-steps, in this exact order. Each
sub-step must produce its stated **output checkpoint** before moving to the next — do not skip
ahead, blend multiple sub-steps into a single unstructured pass, or revisit an earlier
checkpoint once it's locked. This sequencing exists specifically to prevent rule-blending errors:
performing all 8 of the contract's analyses in one pass is the single biggest source of mistakes,
especially for smaller/cheaper models.

#### 4a — Confirm JD Structured Metadata
Finalize the structured JD metadata object built in Step 2 (company, title, posting date/JD
timestamp, job URL/source reference, compensation, location, years required, degree requirement,
internship enrollment window/cutoff (or null), recent-graduate exception (Yes/No/Not stated),
required/preferred skills, responsibilities, clearance/defense flags, internship indicators,
remote/onsite/hybrid, seniority).

**Output checkpoint:** the locked JD metadata object. Every sub-step below reads from this object
only — do not re-parse or second-guess the JD text again after this point.

#### 4b — Confirm Mode
Restate the Step 3 Full-Time vs. Internship determination.

**Output checkpoint:** the locked `Internship Mode: Yes/No` flag. This must not be revisited or
re-derived later — 4d (Degree Mapping) and 4e (Experience Mapping) must apply the §9 Internship
Mode adjustments if and only if this flag is `Yes`.

#### 4c — Skill & Responsibility Mapping + Skill Gaps
Produce:
- Required Skills table (JD skill → Direct / Equivalent / Partial / No Match → evidence)
- Preferred Skills table (same structure)
- Responsibility Alignment table (JD responsibility → Strong / Moderate / Weak → evidence),
  applying §9.2 Internship Mode adjustments if 4b's flag is `Yes` (responsibilities may map to
  coursework/projects/internships, lack of ownership or leadership is not penalized, and depth
  expectations are reduced)
- Skill Gaps list (skills with No Match, or Partial matches worth flagging)

**Output checkpoint:** explicit counts of Direct / Equivalent / Partial / No Match required
skills, plus a single `skill_alignment` tier (`high` / `moderate` / `low` / `major_gaps`) derived
deterministically from those counts per contract §11's thresholds. Both the counts and the tier
are locked here — they are the direct input to 4g's Skill Score and the sidecar's
`skill_alignment` field respectively; do not recompute, re-derive, or second-guess either one
later.

#### 4d — Degree Requirement Mapping
If 4b's Internship Mode flag is `Yes`, first check contract §5.2 Rule H (the enrollment-window
eligibility gate) — this check is unconditional and independent of the JSON lookup/fallback below,
since Rule H governs enrollment-window eligibility, not degree-domain matching. If Rule H applies,
lock ❌ Hard mismatch as the Match Category now and skip the rest of this step.

Otherwise, determine which of the four candidate degree categories in
`references/degree_domain_map.json` applies (`stem_quantitative`, `business_finance_accounting`,
`liberal_arts_humanities`, `social_sciences`, or none of these), using the candidate's degree title
**plus** `candidate_profile.md` (technical strengths, quantitative coursework) and
`candidate_preferences.md` (stated role preferences) when the title alone is ambiguous or
borderline — do not classify from the degree title in isolation. Then look up the JD's required
degree field under that category (see contract §5.2/§5.3). Fall back to Rules A–G only when the
category or JD domain isn't covered by the JSON. If the candidate's degree doesn't match the
JD's field but the candidate has substantial directly relevant professional/project experience
(career-switcher case), apply §6.3 — state the mismatch plainly and cross-reference the relevant
experience.

**Output checkpoint:** a single Match Category label using the contract §5.1 canonical wording
(✔ Direct match / ✔ Equivalent match / ~ Partial match / ✘ No match / ❌ Hard mismatch /
➖ Not specified) — the same labels used in `degree_mapping_template.md` and the §8.1
Degree Score lookup table. This label alone drives both 4g's Degree Score lookup and the §8.4
Hard Reject Override check.

#### 4e — Years-of-Experience Mapping
Compare the JD's stated (or absent) years-of-experience requirement against the candidate's work
history, applying §9.1 Internship Mode adjustments if 4b's flag is `Yes`.

**Output checkpoint:** a single Experience Match label using the contract §6.2 canonical wording
(✔ Meets requirement / ~ Partially meets requirement / ✘ Does not meet requirement) for internal
use and the §8.1 Experience Score lookup table. When populating the `Match` column of
`experience_mapping_template.md`'s Markdown table, write **only the bare glyph** (✔ / ~ / ✘) per
§6.2's note on the legacy `run_ranking.py` fallback parser — the full label text belongs in
prose (e.g. this checkpoint's own record, or the table's Notes column), never in the `Match`
cell itself. This label alone drives 4g's Experience Score lookup.

#### 4f — Preference Violations
Compare the JD against `candidate_preferences.md` (if present) and identify every violation.

**Output checkpoint:** an itemized list of violations, each tagged `minor` / `moderate` / `major`
/ `clearance` (empty list if none, or if no preferences file was provided). This list alone drives
4g's Preference Penalty sum.

#### 4g — Recruiter Decision Synthesis
Using only the checkpoint outputs from 4b–4f (do not re-derive any of them), compute, in order:
1. Check 4d's Match Category label first: if it is ❌ Hard mismatch, apply the §8.4 Hard Reject
   Override — `Recruiter% = 2`, `Interview% = 1` (fixed, deterministic values) — and skip directly
   to step 5 below (step 4, the §8.2/§8.3 formula, is explicitly skipped). Per contract §8.7
   Example C, Skill Score and Experience Score are **not computed** in this case; the override is
   unconditional and independent of them.
2. Otherwise, compute Skill Score, Degree Score, Experience Score (contract §8.1, from
   4c/4d/4e's checkpoints). If 4b's flag is `Yes`, no separate internship penalty is applied here
   — the internship-adjusted Degree and Experience labels 4d/4e already locked (per §9.1/§9.3)
   naturally produce the correct (lighter) Degree/Experience scores; §9.4 is descriptive of that
   effect, not an additional step (see contract §9.4's note). The Skill Score itself is unaffected
   by Internship Mode — per §9.4's note, it is derived purely from 4c's Required Skills counts,
   the same as a full-time role.
3. Preference Penalty: sum the positive point magnitude (5/10/15/20) from the §8.1 Preference
   Penalty table for every violation in 4f's list — this sum is a non-negative number that the
   §8.2/§8.3 formulas subtract directly, per the §8.7 worked examples.
4. Recruiter% and Interview% via the §8.2/§8.3 formulas, clamped per §8.3 (skip this step
   entirely if step 1's Hard Reject Override already applied).
5. The Recruiter/Interview band labels (§8.5), looked up from the computed percentages.
6. The Recruiter Takeaway narrative (output Section 1) — write this **last**, after steps 1–5
   above are complete, even though it is *displayed first* in the final output document. It must
   summarize conclusions already reached in 4b–4g, not introduce new judgments unsupported by
   those checkpoints.

**Output checkpoint:** Recruiter%, Interview%, their band labels, and the Recruiter Takeaway text
— locked inputs to 4h.

#### 4h — Final Fit Summary + Output Assembly
1. Derive the Final Fit Summary category by looking up 4g's computed Recruiter% band in contract
   §10.1's deterministic mapping table — this is a lookup, never chosen independently of it. If
   4b's Internship Mode flag is `Yes`, use §9.5's internship-mode label for that same band in the
   **Markdown output's** Final Fit Summary prose (§9.5's table maps each §10.1 row 1:1 onto its
   internship-mode equivalent) — this is still a lookup, never an independent judgment. The JSON
   sidecar's `fit_category` field always uses the §10.1 **generic** enum value regardless of
   Internship Mode (per §9.5's scope note and §11's schema) — never write an internship-mode
   label or a nonstandard enum value into `fit_category`.
2. Populate `simulation_output_template.md`, `skill_mapping_template.md`,
   `experience_mapping_template.md`, and `degree_mapping_template.md` using the checkpoint
   outputs from 4a–4g. This is pure formatting/assembly — no new analysis happens at this stage.
3. Stamp `Contract Version` in the output's Metadata section with the version number copied
   verbatim from `simulation_contract.md`'s own header (e.g., `v2.4`, from the line
   `# Simulation Contract v2.4 — ...`). Do not paraphrase or infer the version — read it directly
   from the contract file being applied in this Step 4.
4. Populate `simulation_output_sidecar_template.json` (see contract §11 for field definitions and
   enum values). Every field must be derived from the 4a–4g checkpoint outputs already produced —
   do not re-derive or re-interpret values independently; the JSON must agree exactly with the
   corresponding Markdown output (e.g., `recruiter_pct`/`interview_pct` must equal the same
   integers from 4g, `contract_version` must equal the Markdown Metadata's `Contract Version`).

**Output checkpoint:** the complete, validation-ready Markdown + JSON sidecar pair, ready for
Step 5.

---

### **Step 5 — Save Output Files**

Write **two files**, sharing the same base filename, to:

- `skills/simulation/simulations/<timestamp>_<slugified-role>.md` (human-readable, from Step 4h's
  Markdown output)
- `skills/simulation/simulations/<timestamp>_<slugified-role>.json` (machine-readable sidecar,
  from Step 4h's JSON output)

Where:

- `timestamp` = `YYYYMMDD_HHMMSS` (identical value in both filenames)
- `slugified-role` = lowercase, hyphenated version of the JD role title (identical value in both
  filenames)

Example: `skills/simulation/simulations/20260617_153022_data-engineer.md` +
`skills/simulation/simulations/20260617_153022_data-engineer.json`

Both files are required — do not save the Markdown file alone. If the sidecar cannot be written
for any reason, treat this as a save failure per this Step's error handling (do not silently save
only the Markdown file).

**Validate before treating the save as final.** From within `skills/simulation/`, run:

```
python3 validate_simulation_output.py simulations/<timestamp>_<slugified-role>.md
```

(fall back to `python validate_simulation_output.py ...` if `python3` is not the resolved
command, consistent with Step 0's preflight).

- If the script prints `VALID: ...`, the save is complete — proceed to Step 6.
- If the script prints `INVALID: ...` with a list of issues, do **not** return the invalid files
  as final output. Regenerate only the offending section(s)/field(s) named in the issue list
  (re-deriving them from the relevant Step 4 sub-step's checkpoint — do not guess new values),
  rewrite both files, and re-run the validator. Repeat until validation passes.
- If validation still fails after a reasonable retry, stop and return a brief error message
  describing the persistent validation failure (no simulation content) rather than saving
  invalid output.

---

### **Step 6 — Return Output**

- Write the completed simulation output exclusively to the two files at
  `skills/simulation/simulations/<timestamp>_<slugified-role>.md` and
  `skills/simulation/simulations/<timestamp>_<slugified-role>.json`, after they have passed
  Step 5's validation.
- Do NOT print, stream, or otherwise emit any simulation content (full or partial) to the terminal, logs, or assistant response payload. All simulation details must be persisted only to the output files.
- After successfully saving and validating both files, terminal/assistant responses should be restricted to a concise confirmation containing ONLY the two relative file paths and a one-line status (for example: "Saved and validated: skills/simulation/simulations/20260623_093815_role.md + .json"). No simulation content, analysis, or excerpts should be included in the response.
- If an error prevents writing either file, or validation cannot be made to pass, return a brief error message that describes the failure (no simulation content).

---

## ⚠️ Error Handling

- If `candidate_preferences.md` is missing → skip preference violations.  
- If JD parsing fails → return a message requesting a clearer JD.  
- If required reference files are missing → return a configuration error.  

---

## 🧾 Notes

- This skill is deterministic: same JD + same candidate files → same output.  
- This skill is robust to changes in candidate resume/profile/preferences.  
- This skill does not support overrides or optional parameters.  
- This skill does not perform ranking; it only produces simulation outputs.  



