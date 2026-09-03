---
name: initialize
description: Guides candidates through profile initialization by collecting resume first, then asking targeted supplemental questions to fill gaps. Creates candidate_resume.md, candidate_profile.md, candidate_preferences.md, and populates the one_shot_simulation_prompt.md for mobile use.
context: fork
---

# Initialize Skill

An onboarding skill that helps new candidates set up their complete, reusable profile. The skill prioritizes extracting information from a pasted resume, then asks targeted supplemental questions to fill missing profile and preference data. All collected data is saved as structured markdown files across `.github`, `.claude`, and `.gemini` directories, and is also embedded in an interactive simulation prompt for mobile users.

This skill creates a persistent candidate foundation that powers all downstream skills (simulation, ranking, resume restructuring, etc.).

---

## 📚 References

This skill does not depend on external reference files but creates the following foundational files:

- [candidate_resume.md](../../simulation/references/candidate_resume.md)  
- [candidate_profile.md](../../simulation/references/candidate_profile.md)  
- [candidate_preferences.md](../../simulation/references/candidate_preferences.md)  
- [one_shot_simulation_prompt.md](../one_shot_simulation_prompt.md) ← populated with candidate data  

These files are written **once** to `.github/skills/simulation/references/`
(the canonical location), then mirrored byte-for-byte into
`.claude/skills/simulation/references/` and
`.gemini/skills/simulation/references/` by running
`sync_candidate_files.py` — a deterministic script, not model regeneration.
This avoids the drift risk of the model rewriting the same content three
separate times.

- [ensure_candidate_branch.py](ensure_candidate_branch.py) — deterministic,
  stdlib-only git-branch guard (see Step 8.5). Ensures candidate files are
  only ever written on a dedicated `candidate/<slug>` branch, never on
  `main` or any other shared/feature branch, keeping `main` a clean,
  PII-free template.

The `one_shot_simulation_prompt.md` is populated once and remains in `.github/skills/simulation/` for mobile user access.

---

## 🧩 Templates

The following templates guide extraction and formatting:

- [resume_input_template.md](#resume-input-template)  
- [profile_input_template.md](#profile-input-template)  
- [preferences_input_template.md](#preferences-input-template)  

---

## 📝 Inputs

This skill operates in **two phases**:

**Phase 1 — Resume Extraction:**
- User pastes raw resume (text, LinkedIn-style, PDF-converted, etc.)
- Skill automatically extracts structured fields and builds `candidate_resume.md`
- Skill identifies gaps in extracted data

**Phase 2 — Supplemental Questioning:**
- Skill asks targeted questions for missing or unclear fields
- Questions are context-aware (e.g., only ask about graduation date if education is incomplete)
- Candidate fills in remaining profile and preference details
- Skill builds `candidate_profile.md` and `candidate_preferences.md`

No parameters or flags are required; the skill guides the user through both phases.

---

## 🧠 Workflow

### **Step 1 — Confirm Initialization**

Greet the user and ask to confirm they want to initialize their candidate profile. If they decline, exit gracefully.

---

### **Step 2 — Request Resume Paste (Critical First Step)**

Display this prompt:

```
📋 **Paste Your Resume Below**

Please paste your resume in any format (LinkedIn text, PDF-converted text, Markdown, plain text, etc). 
The skill will extract and structure it automatically.

Resume formats accepted:
- Pasted from LinkedIn
- Plain text exported from resume
- PDF-to-text conversions
- Markdown-formatted resumes
- Any text-based resume

Paste here:
```

**Important:** This is the **primary data source**. The skill extracts as much as possible from this input.

---

### **Step 3 — Parse Resume Automatically**

Extract the following fields from the pasted resume using conservative heuristics:

**Contact Information:**
- Name (from header or first mention)
- Email (regex: xxx@xxx.xxx)
- Phone (regex: (XXX) XXX-XXXX or similar)
- Locations (cities, states mentioned)
- Citizenship (if mentioned)
- LinkedIn URL (if present)

**Education:**
- Degree name (e.g., "B.S. in Computer Science")
- School / University name
- Graduation date / Expected graduation
- Minor or secondary focus (if listed)
- Degree classification (infer from major: STEM, quantitative, liberal arts, etc.)
- Degree level (Bachelor's, Master's, PhD)

**Skills:**
- Programming languages (extract keywords: Python, Java, JavaScript, etc.)
- Cloud platforms (AWS, GCP, Azure, etc.)
- Frameworks & tools (FastAPI, Docker, Spark, React, etc.)
- Databases (PostgreSQL, Snowflake, MongoDB, etc.)

**Work Experience:**
- Company name
- Job title
- Location
- Employment dates (start/end year or "present")
- Bullet-point achievements (extract verbatim or paraphrase)
- Count years of experience in key areas

**Projects:**
- Project name
- Role (if specified)
- Duration
- Key technologies used
- Outcomes

**Record gaps:** Track which fields were not found or are unclear.

---

### **Step 4 — Display Extracted Resume**

Show the candidate the extracted `candidate_resume.md` in formatted markdown. Ask: **"Does this look correct? Any additions or corrections needed?"**

Allow the candidate to:
- Confirm it's correct as-is
- Provide corrections for specific sections
- Add missing details

This ensures accuracy before moving forward.

---

### **Step 5 — Supplemental Questioning (Targeted Phase)**

Based on gaps identified in Step 3, ask **targeted questions only**. Do NOT ask about fields already captured in the resume.

**Questions to ask (if needed):**

1. **If education is incomplete:**
   - "What's your graduation date or expected graduation?"
   - "Did you complete a minor or secondary focus?"
   - "What degree level is this? (Bachelor's, Master's, PhD)"

2. **If contact info is missing:**
   - "What's your primary phone number?"
   - "What's your best email for recruiters to contact you?"
   - "Are you a US citizen? (Relevant for clearance-required roles)"

3. **For profile synthesis (draw from resume but ask clarifying questions):**
   - "In 1–3 sentences, how would you describe your technical focus and background?"
   - "What are your top 5 technical competencies?" (suggest inferred list from resume)
   - "What industries or problem spaces have you worked in?" (suggest inferred list)
   - "Years of experience in [key skill from resume]?" (ask for any skills with unclear duration)

4. **For role preferences:**
   - "What role types do you want to pursue?" (suggest: Data Engineer, ML Engineer, Backend, etc.)
   - "Are there role types you want to avoid?" (suggest: Defense/DoD, Finance, Sales, etc.)

5. **For location & compensation:**
   - "What are your preferred work locations or regions?"
   - "Remote, hybrid, or on-site preference?"
   - "What's your minimum acceptable base salary?"
   - "What's your target salary range?"

6. **For constraints:**
   - "Are you willing to work on defense/clearance-required roles?"
   - "Any other preferences or constraints?" (open-ended)

**Implementation:** Use a structured question flow. Only ask questions for gaps. Skip sections if the resume provided complete information.

---

### **Step 6 — Build Candidate Profile**

From the resume and supplemental answers, construct `candidate_profile.md`:

```markdown
# Candidate Profile

## Summary
[1–3 sentence summary from supplemental Q or inferred from resume]

## Technical Strengths
### Core Competencies
- [5–7 inferred or stated competencies]

### Languages
[From resume]

### Tools & Platforms
[From resume]

## Domain Experience
- [Industries/verticals from work history]

## Work History Summary
[Brief summaries of key roles, inferred from resume]

## Education
- Degree: [from resume]
- School: [from resume]
- Graduation: [from resume or supplemental Q]
- Classification: [inferred STEM/non-STEM]

## Experience Depth (Years)
- [Skill]: X years

## Role Alignment
[Inferred from supplemental Q or stated preferences]

## Location
[From supplemental Q or resume]

## Citizenship
[From resume or supplemental Q]
```

---

### **Step 7 — Build Candidate Preferences**

From supplemental answers, construct `candidate_preferences.md`:

```markdown
# Candidate Preferences

## 1. Preferred Role Domains
- [From supplemental Q]

## 2. Avoided Role Domains
- [From supplemental Q]

## 3. Location Preferences
Preferred:
- [From supplemental Q or resume]

Acceptable:
- [Remote/hybrid/onsite stance]

Avoided:
- [From supplemental Q]

## 4. Compensation Preferences
Minimum acceptable base salary:
- [From supplemental Q]

Target compensation:
- [From supplemental Q]

## 5. Work Environment Preferences
Preferred:
- [Remote/hybrid/onsite]

Avoided:
- [High travel, etc.]

## 6. Role Level Preferences
Preferred:
- [New grad, early career, senior, etc.]

## 7. Defense / Clearance Stance
[Willing / Unwilling / Requires clearance]

## 8. Additional Notes
[Open-ended constraints or opportunities]
```

---

### **Step 8 — Populate one_shot_simulation_prompt.md**

Replace the placeholder sections in `.github/skills/simulation/one_shot_simulation_prompt.md` with extracted candidate data:

**Sections to populate:**
- `[CANDIDATE INFO — REPLACE THIS WITH THE CANDIDATE'S RESUME]` → Use formatted `candidate_resume.md`
- `[CANDIDATE INFO — REPLACE THIS WITH THE CANDIDATE'S PROFILE]` → Use formatted `candidate_profile.md`
- `[CANDIDATE INFO — REPLACE THIS WITH DEGREE DETAILS]` → Extract from degree info
- `[CANDIDATE INFO — REPLACE THIS WITH PREFERENCES OR STATE "NO PREFERENCES PROVIDED"]` → Use formatted `candidate_preferences.md`

This creates a **pre-filled simulation prompt** that mobile users can immediately copy and paste into any AI app.

---

### **Step 8.5 — Ensure Candidate Git Branch (Required Before Writing Any Files)**

Candidate reference files must never be written directly onto `main` or any other shared/
feature branch — `main` stays a clean, generic template with no real candidate PII, and each
candidate's full data/simulation/résumé history lives on its own dedicated local
`candidate/<slug>` branch (branched off `main`, never pushed unless the user explicitly asks
to do so).

**Preflight — verify Python is available** (same as Step 9's preflight below; check once,
Python is needed for both this script and `sync_candidate_files.py`).

Run the branch guard, passing the candidate's full name as extracted in Step 3/confirmed in
Step 4:

```bash
python3 .github/skills/initialize/ensure_candidate_branch.py "<Candidate Full Name>"
# or, if python3 is not found:
python .github/skills/initialize/ensure_candidate_branch.py "<Candidate Full Name>"
```

- **If the script prints `OK: ...`**: the working copy is now on the correct
  `candidate/<slug>` branch (created fresh off `main`, or an existing one that was checked
  out). Proceed to Step 9 — all file writes in Step 9 happen on this branch, not on `main`.
- **If the script prints `REFUSED: ...` because the current branch isn't `main`**: stop and
  relay the message to the user verbatim — they must switch to `main` themselves (or confirm
  which branch they intended) before Initialize can proceed. Do not attempt to write candidate
  files anyway as a workaround.
- **If the script prints `REFUSED: ...` because `main` has uncommitted changes**: stop and
  ask the user to commit, stash, or discard those changes first, so nothing unrelated gets
  carried onto the new candidate branch.
- **If the script exits with a `GIT ERROR`**: relay the message; this usually means git isn't
  installed/initialized. Do not proceed without a working git branch guard — do not fall back
  to writing files on whatever branch happens to be checked out.
- This skill never pushes, merges, or deletes branches — it only creates/checks out a local
  `candidate/<slug>` branch. Publishing (pushing, opening a PR) is always the user's explicit,
  separate decision.

---

### **Step 9 — Save Canonical Files, Then Sync Copies**

Write the generated files **once** to the canonical location, on the `candidate/<slug>`
branch confirmed in Step 8.5 (never on `main`):

1. `.github/skills/simulation/references/`

**File names:**
- `candidate_resume.md`
- `candidate_profile.md`
- `candidate_preferences.md`

**Also update:**
- `.github/skills/simulation/one_shot_simulation_prompt.md` (populated version)

**Preflight — verify Python is available:** the `.claude` and `.gemini`
mirrors are produced by a deterministic script (`sync_candidate_files.py`),
not by the model regenerating content, so a Python interpreter must be
available before invoking it.
- Try `python3 --version`, then fall back to `python --version` if `python3`
  is not found.
- If neither is available, stop and tell the user: "Python 3.8+ is required
  to sync candidate files across skill directories. Please install Python
  and try again." Do not attempt to hand-copy or retype the files as a
  substitute — doing so risks subtle drift (a dropped bullet, a reworded
  sentence) between the `.github`, `.claude`, and `.gemini` copies.
- No virtual environment, `pip install`, or `requirements.txt` is needed —
  `sync_candidate_files.py` uses only the Python standard library.

**Run the sync script** to mirror the canonical files byte-for-byte into
`.claude/skills/simulation/references/` and
`.gemini/skills/simulation/references/`:

```bash
python3 .github/skills/initialize/sync_candidate_files.py
# or, if python3 is not found:
python .github/skills/initialize/sync_candidate_files.py
```

The script copies `candidate_resume.md`, `candidate_profile.md`, and
`candidate_preferences.md` from the canonical `.github` location to both
mirrors, and prints the list of files it wrote. This replaces having the
model regenerate the same three files three separate times.

---

### **Step 10 — Return Confirmation**

Return a confirmation message summarizing:

- ✅ Files created successfully
- 📂 Locations where files were saved
- 📱 Mobile simulation prompt ready at `.github/skills/simulation/one_shot_simulation_prompt.md`
- 🚀 Next steps (e.g., "You can now run the simulation skill or copy the mobile prompt")

Example output:

```
✅ Candidate profile initialized successfully!

📂 Canonical files written to:
   • .github/skills/simulation/references/

🔄 Synced (byte-for-byte) to:
   • .claude/skills/simulation/references/
   • .gemini/skills/simulation/references/

Created:
   • candidate_resume.md
   • candidate_profile.md
   • candidate_preferences.md

📱 Mobile simulation prompt ready:
   • .github/skills/simulation/one_shot_simulation_prompt.md
   (Pre-populated with your data — ready to copy and share)

🚀 Next:
   1. Run "Simulate this JD" with a job description
   2. Copy the mobile prompt and use it in ChatGPT/Claude/Gemini
   3. Run "Rank my simulations" after multiple JDs
```

---

## 📋 Input Templates

### Resume Input Template

```markdown
# Candidate Résumé

## Contact
- Name: 
- Email: 
- Phone: 
- Locations: 
- Citizenship: 
- LinkedIn: (optional)

---

## Education
**Degree & Field**  
School — Location  
Graduation: Month Year

Classification: (e.g., STEM, quantitative, liberal arts)
Degree Level: (Bachelor's, Master's, etc.)
Minor/Focus: (optional)

---

## Skills

### Languages
(Comma-separated: Python, Java, etc.)

### Cloud / Platforms
(AWS, GCP, Azure, etc.)

### Frameworks / Tools
(FastAPI, Docker, SQL, etc.)

---

## Work Experience

### **Company Name**
**Role Title** — Location  
**Dates**

- Bullet point achievement 1
- Bullet point achievement 2
- Bullet point achievement 3

---

## Projects

### **Project Name**
**Role** — Dates

- Brief description of project
- Key technologies or outcomes
```

### Profile Input Template

```markdown
# Candidate Profile

## Summary
(1–3 sentences about your technical focus and background)

---

## Technical Strengths

### Core Competencies
- (List 5–7 key areas)

### Languages
(Ranked by proficiency)

### Tools & Platforms
(Key technologies)

---

## Domain Experience
- (Industry / vertical 1)
- (Industry / vertical 2)
- (Problem space or technology focus)

---

## Work History Summary

### Company — Role (Year–Year)
(1–2 lines about what you accomplished)

---

## Education
- Degree level and field
- School
- Graduation year
- Classification (e.g., STEM, quantitative)

---

## Experience Depth (Years)
- Skill area 1: X years
- Skill area 2: X years

---

## Role Alignment

Strong alignment with:
- (Role type 1)
- (Role type 2)

Moderate alignment with:
- (Role type 3)

Weak alignment with:
- (Role type 4)

---

## Location
- Preferred regions

---

## Citizenship
(For clearance-required roles)
```

### Preferences Input Template

```markdown
# Candidate Preferences

## 1. Preferred Role Domains
- (Role domain 1)
- (Role domain 2)
- (etc.)

## 2. Avoided Role Domains
- (Domain to avoid 1)
- (Domain to avoid 2)

## 3. Location Preferences
Preferred:
- (City / Region 1)
- (City / Region 2)

Acceptable:
- (Remote, hybrid, etc.)

Avoided:
- (Full-time onsite outside preferred regions, etc.)

## 4. Compensation Preferences
Minimum acceptable base salary:
- $(Amount)

Target compensation:
- $(Amount)–$(Amount)+

## 5. Work Environment Preferences
Preferred:
- (Remote, hybrid, onsite, etc.)

Avoided:
- (High travel, etc.)

## 6. Role Level Preferences
Preferred:
- (Full-time, new grad, early career, etc.)

Avoided:
- (Senior 5+, managerial, etc.)

## 7. Defense / Clearance Stance
(Willing / Unwilling / Requires clearance)

If unwilling: Flag defense-oriented JDs as preference violations.

## 8. Additional Notes
(Any other constraints, preferences, or opportunities)
```

---

## ⚠️ Error Handling

- If user cancels at any phase → abort gracefully and explain that they can re-run the skill later.  
- If a required field is missing → prompt again or mark as incomplete.  
- If file write fails → return an error and suggest manual creation.  
- If files already exist on the current candidate branch → ask user if they want to overwrite or update.  
- If `ensure_candidate_branch.py` (Step 8.5) refuses because the current branch isn't `main` → relay the message verbatim and stop; do not write candidate files on a non-candidate branch as a workaround.  
- If `ensure_candidate_branch.py` refuses because `main` has uncommitted changes → ask the user to commit/stash/discard them first, then re-run.  
- If git is not installed/initialized (`GIT ERROR` from the script) → stop and inform the user; do not fall back to writing files on whatever branch happens to be checked out.  

---

## 🧾 Notes

- This skill is interactive and conversational, not automated.  
- All three directories (`.github`, `.claude`, `.gemini`) receive identical copies.  
- Files created by this skill become the foundation for all other skills (simulation, ranking).  
- Users can re-run this skill to update their profile; existing files are overwritten.  
- No validation of resume content is performed; users are trusted to provide accurate information.  
- **Candidate data lives on `candidate/<slug>` branches, never on `main`.** Each candidate gets
  their own local branch (created/checked out automatically by Step 8.5), keeping `main` a
  clean, generic template safe to branch skill-development work from without carrying anyone's
  PII along. These candidate branches are local-only by default — pushing/publishing them is
  always a separate, explicit user decision, not something this skill does automatically.  

