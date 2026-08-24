# Resume-Restructure Skill

A deterministic resume rewriting engine that adapts the candidate's résumé to target a specific job description (JD), emphasizing skills, responsibilities, and experiences most relevant to that particular recruiter's needs.

This skill transforms a generic résumé into a tailored, JD-focused version that highlights domain-specific alignment and recruiter-relevant signals.

---

## 📚 References

This skill depends on the following reference files:

- [resume_guidelines.md](references/resume_guidelines.md)  
  Defines the rewriting logic, emphasis strategies, and best practices for tailoring résumés.

- [scripts/fact_guard.py](scripts/fact_guard.py)  
  Deterministic, stdlib-only script that scans a draft tailored résumé for quantitative claims
  not traceable to the original résumé (Step 5).

- Original candidate reference files (from simulation skill):
  - `../simulation/references/candidate_resume.md`  
  - `../simulation/references/candidate_profile.md`  

- Target simulation output (from simulation skill):
  - `../simulation/simulations/<timestamp>_<slugified-role>.md` — required; human-readable
    narrative detail
  - `../simulation/simulations/<timestamp>_<slugified-role>.json` — canonical machine-readable
    metadata (see `../simulation/references/simulation_contract.md` Section 11, "JSON Sidecar");
    preferred source for structured fields (Step 2). If the sidecar is missing (legacy
    simulations), fall back to `.md`-only parsing.

---

## 🧩 Templates

The résumé output is generated using the following template:

- [resume_output_template.md](assets/templates/resume_output_template.md)  
  Ensures consistent structure and formatting across all tailored résumés.

---

## 📝 Inputs

This skill requires:

1. **simulation_file** (string, required): Path or filename of the completed simulation's `.md`
   file (e.g., `20260805_234550_data-engineer-mizuho.md`). Always pass/reference the `.md` file,
   not the `.json` sidecar — the sidecar is located automatically by matching base filename.
   - The skill will auto-discover this from the simulations directory or accept explicit user input.
   - Used to extract JD context (company, role, required skills, responsibilities, domain) — from
     the matching `.json` sidecar where possible, falling back to the `.md` file (see Step 2).

2. **candidate_resume.md** (string, reference): Loaded automatically from `../simulation/references/candidate_resume.md`.

3. **candidate_profile.md** (string, reference): Loaded automatically from `../simulation/references/candidate_profile.md`.

No additional parameters or overrides are supported.

---

## 🧠 Workflow

### **Step 0 — Preflight: Verify Python Is Available**

Fact-checking (Step 5) is performed by a deterministic script (`scripts/fact_guard.py`), not by
the model, so a Python interpreter must be available before invoking it.

- Try `python3 --version`, then fall back to `python --version` if `python3` is not found.
- If neither is available, stop and tell the user: "Python 3.8+ is required to run the
  Resume-Restructure fact guard. Please install Python and try again." Do not attempt to
  hand-verify claims as a substitute — determinism depends on the script running, not the model
  self-grading.
- No virtual environment, `pip install`, or `requirements.txt` is needed —
  `scripts/fact_guard.py` uses only the Python standard library.

---

### **Step 1 — Load References**

Load all required reference and candidate files:

- Original `candidate_resume.md` (source material for rewriting)  
- `candidate_profile.md` (context for domain experience)  
- Target simulation files: both the `.md` file and its matching `.json` sidecar, if present (to
  extract JD context — see Step 2)  
- `resume_guidelines.md` (rewriting strategy)  

This ensures the rewrite uses the latest candidate data and applies consistent strategy.

---

### **Step 2 — Extract JD Context from Simulation**

Read the simulation's `.json` sidecar directly, when present (same base filename as the target
simulation `.md` file — see `../simulation/references/simulation_contract.md` Section 11,
"JSON Sidecar"), for the following fields, instead of re-parsing them out of the Markdown prose:

- **Company name** — `company`
- **Job title** — `title`
- **Degree alignment** — `degree_match` (enum)
- **Aggregate skill alignment** — `skill_alignment` (enum: `high` / `moderate` / `low` /
  `major_gaps`)
- **Experience alignment** — `experience_match` (enum)
- **Overall fit category** — `fit_category` (enum)
- **Recruiter/Interview likelihood** — `recruiter_pct`, `interview_pct`
- **Internship mode** — `internship_mode` (bool)
- **Compensation / Location / Years Required** — `compensation`, `location`, `years_required`

The `.json` sidecar is the canonical machine-readable source for these fields (per
`../simulation/references/simulation_contract.md` Section 11, "JSON Sidecar" and
`../ranking/references/ranking_rules.md` Section 2, "Required Inputs") — reading it directly
avoids re-deriving values the simulation skill already computed once, and avoids inheriting
prose-parsing errors.

**The sidecar does not carry per-skill or narrative detail.** The following must still be read
from the simulation's `.md` file, since the sidecar only stores an aggregate `skill_alignment`
enum, not the individual required/preferred skill list or free-text narrative:

- **Key required skills** (per-skill match detail) — from `.md` Section 2 (Skill & Responsibility
  Mapping, Required Skills table)
- **Preferred technologies/tools** — from `.md` Section 2 (Preferred Skills table)
- **Key responsibilities** — from `.md` Section 2 (Responsibility Alignment)
- **Skill gaps** — from `.md` Section 3 (Skill Gaps)
- **Domain/industry, experience level, and recruiter's likely priorities** — inferred from `.md`
  Section 1 (Recruiter Takeaway) and Section 7 (Recruiter Decision) (these are narrative
  judgments, not structured fields in the sidecar)

If the target simulation has no `.json` sidecar (a pre-`simulation-json-sidecar` legacy file),
fall back to parsing all of the above directly from the `.md` prose, as before.

This creates a "rewrite directive" that guides all subsequent transformations.

---

### **Step 3 — Match Original Resume Sections**

Against the rewrite directive, identify:

- Which **skills** in the original résumé directly map to JD requirements  
- Which **work experiences** (roles, projects) best demonstrate required competencies  
- Which **projects** showcase relevant technical depth  
- Which **education/certifications** reinforce domain alignment  
- Which **tools/technologies** are most relevant to the target role  

---

### **Step 4 — Rewrite Each Section**

Follow the strategy defined in `resume_guidelines.md`:

1. **Contact & Summary (no change)**  
   - Keep name, email, phone, location unchanged  
   - Update or create role-targeted summary if it adds recruiter-relevant context  

2. **Education (minimal rewrite)**  
   - Keep degree, major, minor, dates unchanged  
   - Optionally emphasize coursework or classifications relevant to JD domain  

3. **Skills (aggressive rewrite)**  
   - Reorder skills to prioritize JD-required skills first  
   - Group related skills by domain (e.g., "Data Engineering," "Cloud Platforms")  
   - Emphasize preferred JD technologies  

4. **Work Experience (strategic rewrite)**  
   - For each role, rewrite bullet points to emphasize JD-aligned responsibilities  
   - Highlight metrics, outcomes, and technical decisions relevant to the target role  
   - Reorder bullet points to lead with most relevant accomplishments  
   - Use JD terminology and domain language  
   - **Be detailed yet concise:** Pack maximum recruiter signal into minimum words. Lead with action verb + technical achievement + quantified impact. Avoid filler; every sentence must serve a purpose.  

5. **Projects (selective rewrite)**  
   - Prioritize projects most relevant to JD domain  
   - Rewrite descriptions to emphasize technical alignment and learnings  
   - Optionally de-emphasize or exclude projects with weak relevance  
   - **Be detailed yet concise:** Describe architecture decisions, technical choices, and outcomes in a single focused sentence or two. Show depth without verbosity.  

---

### **Step 5 — Validate Against Resume Guidelines**

Before finalizing, ensure:

- Emphasis matches recruiter's priorities (from simulation)  
- Language and terminology align with JD domain  
- Structure follows the output template  

Then write the current draft (from Steps 3-4) to a temporary Markdown file and run the
deterministic fact guard against it (do not rely on self-grading for factual accuracy — a
hallucinated metric that "sounds right" is a classic LLM failure mode this step exists
specifically to catch):

```
python3 scripts/fact_guard.py <path_to_draft_resume.md>
```

(fall back to `python scripts/fact_guard.py ...` if `python3` is not the resolved command)

The script compares every quantitative claim (percentages, dollar amounts, multipliers, record/
throughput counts, and "reduced/increased/grew/improved/saved/cut by ..." phrasing) in the draft
against the candidate's original `candidate_resume.md`, flagging any claim whose numeric value
isn't traceable to the original.

- **If the script exits 0** (no flagged claims): proceed to Step 6.
- **If the script exits 1** (one or more flagged claims): do not proceed. Either correct each
  flagged claim so its numeric value matches the original résumé, remove the claim, or explicitly
  ask the user to approve it as an intentional exception. Only proceed to Step 6 once no unflagged
  (or user-approved) new claims remain.
- **If the script exits 2** (usage/file error): resolve the underlying issue (e.g., confirm the
  draft file path) and re-run before proceeding.

---

### **Step 6 — Generate Output Using Template**

Populate `resume_output_template.md` with:

- Original sections (contact, education) preserved as-is  
- Rewritten sections (skills, experience, projects) tailored to JD  
- Consistent formatting and structure  

---

### **Step 7 — Save Output File**

Write the tailored résumé to: `skills/resume-restructure/resumes/<timestamp>_<slugified-role>.md`

Where:

- `timestamp` = `YYYYMMDD_HHMMSS`  
- `slugified-role` = lowercase, hyphenated version of the JD role title

Example: `skills/resume-restructure/resumes/20260805_234550_data-engineer-mizuho.md`

---

### **Step 8 — Return Output**

- Write the tailored résumé exclusively to the markdown file at `skills/resume-restructure/resumes/<timestamp>_<slugified-role>.md`.  
- Do NOT print, stream, or otherwise emit the full résumé content to the terminal or assistant response payload.  
- After successfully saving the file, terminal/assistant responses should be restricted to a concise confirmation containing ONLY the relative file path and a one-line status (for example: "Saved: .github/skills/resume-restructure/resumes/20260805_234550_data-engineer-mizuho.md").  
- If an error prevents writing the file, return a brief error message that describes the failure.

---

## ⚠️ Error Handling

- If simulation file is missing → return a message requesting the simulation filename or path.  
- If original candidate_resume.md is missing → return a configuration error (Initialize skill must run first).  
- If resume_guidelines.md is missing → return a reference file error.  
- If Python 3.8+ is unavailable (Step 0) → stop and inform the user; do not hand-verify claims as a substitute for `scripts/fact_guard.py`.  
- If `scripts/fact_guard.py` flags unverifiable claims (Step 5) → do not proceed to Step 6/7 until each is corrected, removed, or explicitly approved by the user as an intentional exception.  
- If rewrite fails to preserve factual accuracy → return a warning and halt output.  

---

## 🧾 Notes

- This skill is **deterministic**: same simulation + same candidate resume → same tailored output.  
- This skill is **non-destructive**: original resume is never modified.  
- This skill **preserves facts**: all accomplishments and experiences are grounded in original resume (no fabrication).  
- This skill **emphasizes context**: the same achievement is described differently depending on recruiter priorities (e.g., "Spark SQL optimization" vs. "enterprise-grade data transformation").  
- This skill **prioritizes conciseness with depth**: descriptions are detailed enough to showcase technical competency but concise enough to maintain recruiter attention. Every word earns its place.  
- Multiple tailored résumés can coexist in the `resumes/` directory for different JDs.  

---

## 🎯 Use Cases

1. **Before applying to a specific role:** Run simulation first, then rewrite resume to maximize impact with that recruiter.  
2. **A/B testing:** Generate tailored résumés for 2–3 target roles and compare emphasis.  
3. **Interview prep:** Use tailored résumé as a talking point outline (what the recruiter is most interested in).  
4. **Portfolio:** Maintain multiple tailored résumés for different career paths (data engineer vs. ML engineer vs. backend engineer).  
