# recruiter-simulation-engine

A modular engine that converts job descriptions into structured, recruiter‑grade simulations and ranks those simulations to prioritize hiring opportunities. The repository contains self-contained "skills" (small agents) that encapsulate deterministic workflows, templates, and reference data used by recruiting automations.

## 🎯 What Is This?

**recruiter-simulation-engine** helps you evaluate how well you fit a job opportunity by:

1. **Parsing job descriptions** and mapping them to your experience, skills, and preferences
2. **Running deterministic simulations** that answer: "Do I match this role? How well?"
3. **Ranking multiple job opportunities** to see which roles align best with your goals

This is not a resume-matching tool. It's a *simulation* engine that mimics recruiter decision-making: Does your background align with the role? Do the responsibilities match your interests? Are the preferences acceptable?

---

## 👥 Who Should Use This?

- **Job seekers** evaluating multiple offers to find the best fit
- **Recruiters** screening candidates against job descriptions programmatically
- **Hiring managers** testing evaluation logic before scaling to many candidates
- **Career coaches** helping clients understand role fit across multiple opportunities
- **Researchers** studying recruiter decision-making and job-fit signals

---

## 🚀 Quick Start (5 minutes)

### **Step 1: Set up the engine**
```bash
# Clone the repository
git clone https://github.com/sidsomash/recruiter-simulation-engine.git
cd recruiter-simulation-engine

# Install GitHub Copilot CLI (if not already installed)
# See: https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli

# Start a Copilot session
copilot
```

### **Step 2: Initialize your candidate profile (one-time setup — ~10 minutes)**
```
# Inside the Copilot session, use either format:
Initialize my candidate profile
# or
/initialize
```

**Note:** Skills can be invoked with natural language expressions or the `/` prefix. Both work identically.

**What happens:**

1. **Paste your resume** (any format: LinkedIn, PDF text, markdown, plain text)
   - AI automatically extracts structured data:
     - Contact info (name, email, phone, locations, citizenship, LinkedIn)
     - Education (degree, school, graduation, minor, classification)
     - Skills (languages, platforms, frameworks, tools, databases)
     - Work experience (companies, roles, dates, achievements, years)
     - Projects (names, roles, durations, technologies)

2. **Review the extracted resume**
   - AI displays what it found and asks for confirmations or corrections

3. **Answer targeted supplemental questions** (only for missing/unclear fields)
   - Graduation date if not provided
   - Technical summary (1–3 sentences)
   - Top competencies
   - Preferred/avoided roles
   - Location and compensation preferences
   - Defense/clearance stance

4. **Receive your candidate files:**
   - `candidate_resume.md` — Structured work history and education
   - `candidate_profile.md` — Background, location, domain experience
   - `candidate_preferences.md` — Desired roles, locations, compensation, constraints
   - **Pre-populated mobile prompt** — `.github/skills/simulation/one_shot_simulation_prompt.md` (ready to copy and use in ChatGPT/Claude/Gemini)

### **Step 3: Run a simulation**
Paste a job description and say:
```
Simulate this job description
# or
/simulate
```
The engine will generate a timestamped simulation file showing how you fit.

### **Step 4: Rank your results**
After running multiple simulations, say:
```
Rank my simulations
# or
/rank
```
You'll see a ranked table of all opportunities with fit scores.

---

## 📚 Key Concepts & Definitions

### **Simulation**
A deterministic evaluation of a candidate against a specific job description. The simulation applies a decision contract (rules) to answer:
- Do the required skills match your experience?
- Does the work history align with job responsibilities?
- Does the job match your preferences?
- Final decision: Would a recruiter recommend this role?

Each simulation is a **snapshot** — same inputs + same references always produce the same output.

### **Simulation Contract**
The canonical rulebook for how simulations are evaluated. It defines:
- Skill mapping logic (how your skills are matched to the JD)
- Experience mapping (how your work history aligns with responsibilities)
- Degree mapping (educational fit)
- Preference checks (role fit against your preferences)
- Recruiter decision criteria (final recommendation)

**Do not modify** `simulation_contract.md` unless you fully understand the impact on all simulations.

### **Ranking**
An aggregate analysis of multiple simulations. The ranking skill:
- Reads all simulation outputs
- Extracts structured fit data from each
- Applies a scoring model (defined in `ranking_rules.md`)
- Returns a ranked table sorted by overall fit

Ranking is **ephemeral** — it's recalculated each time and not persisted (preserved as snapshots via simulations instead).

### **Recruiter-Grade**
Simulations mimic how a professional recruiter or hiring manager evaluates candidates:
- Beyond keyword matching
- Context-aware (understands experience progression, role fit, constraints)
- Transparent (shows reasoning, not just a score)

### **Deterministic**
Same inputs always produce the same output. If you re-run a simulation on the same JD with the same candidate profile, you get identical results. This enables:
- Reproducibility
- Version control (compare outputs over time)
- Audit trails (see what changed between runs)

---

## 📁 Directory Structure

```
recruiter-simulation-engine/
├── .github/skills/          # GitHub Copilot CLI skills
├── .claude/skills/          # Claude-compatible skills
├── .gemini/skills/          # Gemini-compatible skills
├── README.md                # This file
├── CLAUDE.md                # Claude-specific instructions
├── GEMINI.md                # Gemini-specific instructions
└── pyproject.toml           # Python project config
```

### **Understanding the three skill directories**

- **`.github/skills/`** — Used by the GitHub Copilot CLI (default if using `copilot` command)
- **`.claude/skills/`** — Use these skills with Claude (via Claude API or custom integrations)
- **`.gemini/skills/`** — Use these skills with Google Gemini (via Gemini API or custom integrations)

Each directory contains the same skills with identical logic. Pick the one matching your AI agent platform.

---

## 🏗️ Core Skills

### **1. Initialize Skill**
- **Location:** `.github/skills/initialize/`, `.claude/skills/initialize/`, `.gemini/skills/initialize/`
- **Purpose:** Interactive onboarding that creates your candidate profile (three markdown files)
- **Invocation:** 
  - Natural language: `"Initialize my candidate profile"` or `"Set up my candidate profile"`
  - Slash command: `/initialize`
- **Output:**
  - `candidate_resume.md` — Structured work history and education
  - `candidate_profile.md` — Background, location, constraints
  - `candidate_preferences.md` — Desired roles, skills, environments
  - **Bonus:** Pre-populated mobile simulation prompt for use in any AI app
- **Run this once** before simulating any jobs (other skills depend on it)

#### **Initialize Skill Workflow**

The Initialize Skill uses a two-phase approach optimized for minimal user friction:

**Phase 1: Resume Extraction (5 min)**
- User pastes resume in **any format** (LinkedIn, PDF text, markdown, plain text)
- AI automatically extracts:
  - Contact: name, email, phone, locations, citizenship, LinkedIn
  - Education: degree, school, graduation, minor, classification, level
  - Skills: languages, platforms, frameworks, tools, databases
  - Experience: companies, roles, dates, achievements, years in each skill
  - Projects: names, roles, durations, technologies, outcomes
- AI displays the extracted resume for review/confirmation

**Phase 2: Supplemental Questioning (5 min)**
- AI identifies **gaps** (fields that are missing or unclear)
- AI asks **only necessary questions**:
  - Education details if incomplete
  - Technical summary (1–3 sentences)
  - Top competencies (AI suggests inferred list)
  - Preferred/avoided roles
  - Location and compensation preferences
  - Defense/clearance stance
  - Any additional constraints
- User answers only the questions that apply

**Output:**
- Three candidate reference files (saved to all three platform directories)
- Pre-populated mobile simulation prompt ready to copy/paste into ChatGPT/Claude/Gemini

**Key Benefits:**
- Resume-first approach = less typing for users
- Gap detection = no unnecessary questions
- Mobile-ready = immediate access to simulations from any AI app
- Unified across platforms = same workflow in GitHub, Claude, Gemini

### **2. Simulation Skill**
- **Location:** `.github/skills/simulation/`, `.claude/skills/simulation/`, `.gemini/skills/simulation/`
- **Purpose:** Parse a job description and evaluate fit against your candidate profile
- **Invocation:** 
  - Natural language: `"Run a simulation for this job description"` or `"Simulate this JD"`
  - Slash command: `/simulate`
- **Input:** Raw job description text (paste from LinkedIn, job board, email, etc.)
- **Output:** Timestamped markdown file in `skills/simulation/simulations/` (e.g., `2026-07-09_1245_senior-engineer.md`)
- **What it evaluates:**
  - Skill mapping (required skills vs. your experience)
  - Experience mapping (responsibilities vs. your work history)
  - Degree fit (educational requirements)
  - Preference checks (role aligns with your goals?)
  - Recruiter decision (overall recommendation)

### **3. Ranking Skill**
- **Location:** `.github/skills/ranking/`, `.claude/skills/ranking/`, `.gemini/skills/ranking/`
- **Purpose:** Aggregate all simulations and rank roles by fit score
- **Invocation:** 
  - Natural language: `"Rank my simulations"` or `"Show ranked results"`
  - Slash command: `/rank`
- **Input:** None (auto-discovers all simulations in `skills/simulation/simulations/`)
- **Output:** Ranked table in terminal (ephemeral, not saved)
- **Scoring Model:** Applies rules from `references/ranking_rules.md`
- **Best for:** Comparing 5+ job opportunities to find the best match

### **4. Resume-Restructure Skill**
- **Location:** `.github/skills/resume-restructure/`, `.claude/skills/resume-restructure/`, `.gemini/skills/resume-restructure/`
- **Purpose:** Rewrite your resume to target a specific job description
- **Invocation:** 
  - Natural language: `"Restructure my resume for this JD"`
  - Slash command: `/restructure`
- **Status:** Available for targeted resume optimization
- **Output:** Tailored resume markdown with signals optimized for simulation scoring
- **Note:** Pairs well with Simulation skill to test fit *before* applying

---

## ⚙️ Setup Instructions

### **Prerequisites**
- Install the GitHub Copilot CLI: https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli
- Authentication will be prompted in Step 2

### **Option 1: GitHub Copilot CLI (Recommended)**
```bash
# From the repository root
copilot

# Inside the Copilot session
/login                              # Authenticate with GitHub
/initialize candidate profile       # Create your profile
/simulate <job_description>         # Run a simulation
/rank simulations                   # Rank all results
```

### **Option 2: Using Claude Instead**
1. Ensure `.claude/skills/` directory exists (it does)
2. Start a Claude session (via Claude API, web interface, or custom integration)
3. Point Claude to this repository's `.claude/CLAUDE.md` for instructions
4. Run skills the same way (invocation patterns are identical)

### **Option 3: Using Google Gemini Instead**
1. Ensure `.gemini/skills/` directory exists (it does)
2. Start a Gemini session (via Gemini API, web interface, or custom integration)
3. Point Gemini to this repository's `.gemini/GEMINI.md` for instructions
4. Run skills the same way (invocation patterns are identical)

---

## 📋 First-Time Workflow

### **Day 1: Initialize**
```
You: "Initialize my candidate profile"
Engine: Guides you through 3 interactive prompts
        Creates: candidate_resume.md, candidate_profile.md, candidate_preferences.md
```

### **Day 1-2: Simulate Multiple Jobs**
```
You: [Paste Job Description 1]
     "Run a simulation for this job description"
Engine: Creates: 2026-07-09_1245_senior-engineer.md

You: [Paste Job Description 2]
     "Simulate this JD"
Engine: Creates: 2026-07-09_1530_frontend-engineer.md

You: [Paste Job Description 3]
     "Simulate this JD"
Engine: Creates: 2026-07-09_1800_fullstack-engineer.md
```

### **Day 2: Rank & Decide**
```
You: "Rank my simulations"
Engine: Outputs ranked table:
        1. Senior Engineer (Fit: 92%) — Strong alignment
        2. Fullstack Engineer (Fit: 87%) — Good alignment
        3. Frontend Engineer (Fit: 74%) — Partial alignment
```

---

## 📊 Expected Outputs

### **Sample Simulation Output**
A simulation file (`skills/simulation/simulations/2026-07-09_1245_senior-engineer.md`) contains:

```markdown
# Simulation: Senior Engineer | Acme Corp

## Fit Summary
- Overall Fit: 92%
- Skill Match: 95%
- Experience Fit: 88%
- Preference Alignment: 90%
- Recruiter Decision: ✅ Recommended

## Skill Mapping
### Required Skills (from JD)
- [ ] Python (You: Expert, JD: Required)
- [ ] Kubernetes (You: Intermediate, JD: Preferred)
- [ ] Leadership (You: Advanced, JD: Required)

## Experience Mapping
- Your background aligns with role trajectory ✅
- Responsibility coverage: 90% (7/8 core responsibilities matched)
- Experience level match: Senior ✅

## Preference Checks
- Remote: You want remote, role is hybrid ⚠️
- Salary range: $150-180K (matches your expectation) ✅
- Team size: You prefer <50, team is 35 ✅

## Recruiter Decision
This role is a strong fit. Your senior engineering experience directly aligns
with the leadership expectations, and your technical stack matches well.
```

### **Sample Ranking Output**
```
Rank | Role | Company | Fit | Skills | Experience | Preferences | Recruiter
-----|------|---------|-----|--------|------------|-------------|----------
  1  | Senior Engineer | Acme | 92% |  95%  |   88%    |    90%     | ✅ Yes
  2  | Fullstack Engineer | Beta | 87% |  89%  |   85%    |    86%     | ✅ Yes
  3  | Frontend Engineer | Gamma | 74% |  82%  |   68%    |    72%     | ⚠️ Maybe
```

---

## 🔧 Templates, References & Configuration

Each skill uses template files under `assets/templates/` and canonical rules under `references/` to ensure consistent outputs.

### **Editable Files (Safe to Modify)**
- **Simulation templates:** `.github/skills/simulation/assets/templates/*.md` (and same in `.claude/` and `.gemini/`)
  - `skill_mapping_template.md` — How skills are displayed
  - `experience_mapping_template.md` — How experience is presented
  - `degree_mapping_template.md` — How education fit is shown
  - `simulation_output_template.md` — Overall output format
  - Edit these to customize output formatting; re-run simulations to see changes
  - Safe: Changing templates only affects future simulation output formatting, not logic

- **Candidate reference files:** `.github/skills/simulation/references/` (and same in `.claude/` and `.gemini/`)
  - `candidate_resume.md` — Edit to update your work history or project details
  - `candidate_profile.md` — Edit to update background, technical strengths, domain experience
  - `candidate_preferences.md` — Edit to update role preferences, location, compensation, constraints
  - **Impact:** Editing these changes how *all future* simulations evaluate you
  - **Tip:** Re-run simulations on old JDs after updating to see how your fit has changed

- **Ranking rules:** `.github/skills/ranking/references/ranking_rules.md` (and same in `.claude/` and `.gemini/`)
  - Defines the scoring model for how simulations are ranked
  - Adjust weights to emphasize skills, experience, or preferences differently
  - **Impact:** Changing this re-ranks all existing simulations
  - Only edit if you understand the scoring logic

### **Protected Files (Do Not Modify Unless You Know What You're Doing)**
- **Simulation contract:** `.github/skills/simulation/references/simulation_contract.md` (and same in `.claude/` and `.gemini/`)
  - ⛔ **Critical** — Defines how all simulations evaluate candidates
  - Changing it alters evaluation logic for *all* simulations (past and future)
  - Only modify if you fully understand the consequences and want to change recruiting logic
  - Examples: How skills are mapped, how experience is weighted, degree matching rules, preference violation penalties

### **Generated Files (Read-Only)**
- **Simulation outputs:** `.github/skills/simulation/simulations/<timestamp>_<slug>.md` (and same in `.claude/` and `.gemini/`)
  - Auto-generated by the Simulation skill
  - Preserve these as deterministic snapshots
  - Do not edit (editing breaks reproducibility)
  - Use git to version-control them for audit trails
  - Reference these for historical comparisons

- **Skill definitions:** `.github/skills/*/SKILL.md` (`.claude/` and `.gemini/` versions are identical)
  - Auto-loaded by each AI platform
  - Do not edit unless implementing a new version of the skill
  - Changes propagate to all future skill invocations

---

## ✅ Sanity Check: What to Edit When

| Goal | Edit This | Impact |
|------|-----------|--------|
| Update resume/skills | `candidate_resume.md` | Future simulations re-evaluate you |
| Change role preferences | `candidate_preferences.md` | Future simulations check different preferences |
| Adjust ranking weights | `ranking_rules.md` | Re-ranks all existing simulations |
| Customize output look | Templates in `assets/templates/` | Only affects formatting, not logic |
| Change evaluation rules | `simulation_contract.md` | ⚠️ Changes ALL simulation logic (be careful!) |
| Fix a simulation | Re-run simulation (don't edit file) | Preserves original, creates new snapshot |

---

## 🎯 Intended Workflow (Day-to-Day)

1. **Initialize your profile once** → Creates candidate files
2. **Paste a job description** → Run Simulation skill → Get fit evaluation
3. **Repeat step 2** for each job opportunity
4. **After 3+ simulations** → Run Ranking skill → See ranked results
5. **Review top matches** → Update preferences/resume if needed → Re-simulate

---

## ❓ FAQ

### **Q: How do I invoke skills — do I need to use `/` or natural language?**
A: Both work! Skills accept either format:
- Natural language: `"Run a simulation for this job description"`
- Slash command: `/simulate`
Choose whichever feels more natural to you. Behavior is identical.

### **Q: What's the difference between the mobile prompt and running Copilot CLI?**
A: The mobile prompt (`.github/skills/simulation/one_shot_simulation_prompt.md`) is pre-populated with your candidate data and ready to paste into any AI app (ChatGPT, Claude, Gemini). It's self-contained and doesn't need file infrastructure. The Copilot CLI/Claude/Gemini skills are more powerful because they have file access for persistence. Choose based on where you're working.

### **Q: Can I use the engine without the Initialize skill?**
A: No. The Simulation and Ranking skills require candidate reference files created by Initialize. You must run Initialize first to set up `candidate_resume.md`, `candidate_profile.md`, and `candidate_preferences.md`.

### **Q: What if I don't have preferences — do I have to fill them out?**
A: No. The Initialize skill will create a `candidate_preferences.md` file with your answers. If you skip preference questions or provide "none", the Simulation skill will note "No preference violations evaluated" and skip preference checks.

### **Q: Can I edit my simulations after they're generated?**
A: No. Simulations are deterministic snapshots. Instead, edit your candidate profile (resume, preferences) and re-run the simulation. This preserves the original for comparison.

### **Q: What if my candidate profile is incomplete?**
A: The Simulation skill handles missing data gracefully:
- Missing resume? It skips experience mapping.
- Missing preferences? It skips preference checks.
- You still get a simulation with available data.

### **Q: How is the ranking score calculated?**
A: See `references/ranking_rules.md` for the exact formula. It's a weighted combination of:
- Skill match (40%)
- Experience alignment (35%)
- Preference fit (25%)

Edit this file to adjust weights if needed.

### **Q: Why would I use the Resume-Restructure skill?**
A: To tailor your resume for a specific job before applying. It highlights relevant skills, reorders experience, and optimizes language. Then you can run a simulation on the same JD to test your improved fit score.

### **Q: Can I use this with my own evaluation rules?**
A: Yes. The engine is designed to be customizable:
- **Change output format?** Edit templates in `assets/templates/`.
- **Change scoring?** Edit `references/ranking_rules.md`.
- **Change evaluation logic?** Edit `references/simulation_contract.md` (if you understand the impact).

### **Q: Are simulations reproducible?**
A: Yes. Same candidate profile + same JD = same simulation. This enables:
- Version control (git diff shows what changed)
- A/B testing (change one rule, re-run, compare)
- Audits (prove decisions were consistent)

### **Q: What's the difference between Copilot CLI, Claude, and Gemini versions?**
A: All three contain identical skills with the same logic. Use whichever AI platform you prefer. The output and behavior are the same. Candidate reference files are mirrored across all three directories for consistency.

### **Q: How do I know if a simulation is outdated?**
A: Check the timestamp in the filename (e.g., `2026-07-09_1245_senior-engineer.md`). The timestamp shows when the simulation was created. If your candidate profile has changed since then, the simulation may no longer reflect your current fit.

### **Q: Can I have multiple candidate profiles?**
A: The current system uses one candidate profile at a time. To maintain multiple profiles (e.g., "Data Engineer Siddharth" vs. "Backend Engineer Siddharth"), fork the repository or manually manage separate candidate files. Future versions may support profile switching.

### **Q: What do I do if I get an error about missing reference files?**
A: Run the Initialize skill: `Initialize my candidate profile`. This creates the required `candidate_resume.md`, `candidate_profile.md`, and `candidate_preferences.md` files in all three platform directories.

### **Q: Should I commit my candidate files and simulations to Git?**
A: Yes! Version-controlling them lets you:
- Track how your profile has evolved
- See when you applied to specific roles
- Reproduce old simulations for comparison
- Audit your decision-making process

Treat simulations like snapshots — preserve them.

---

## 🚨 Error Handling & Troubleshooting

### **"Missing reference files" Error**
**Problem:** Simulation skill can't find `candidate_resume.md`, `candidate_profile.md`, or `candidate_preferences.md`

**Solution:**
1. Run the Initialize skill: `Initialize my candidate profile`
2. Or manually create these files in `.github/skills/simulation/references/` (or `.claude/`/`.gemini/` depending on platform)

### **"Malformed simulation file" Error**
**Problem:** Ranking skill skips a simulation file because it's corrupted or incomplete

**Solution:**
1. Check the filename — is it a valid simulation (created by the Simulation skill)?
2. Open it and verify it has required sections (Fit Summary, Skill Mapping, Experience Mapping)
3. Delete the file and re-run the simulation

### **Simulation Output Looks Wrong**
**Problem:** Templates aren't rendering correctly or output is formatted strangely

**Solution:**
1. Check the template files in `assets/templates/`
2. Verify they're valid markdown
3. Re-run the simulation
4. If still wrong, compare against `assets/templates/simulation_output_template.md`

### **Ranking Scores Don't Make Sense**
**Problem:** Ranked results seem inconsistent or unexpected

**Solution:**
1. Review `references/ranking_rules.md` to understand the scoring model
2. Check that all simulations have complete data (Skill Match %, Experience %, Preferences %)
3. Manually recalculate one score to verify the math
4. If you think the rules are wrong, edit `ranking_rules.md`

### **General Troubleshooting Steps**
1. **Verify candidate profile exists:** Check `.github/skills/simulation/references/` for all three candidate files
2. **Check file formats:** Ensure all `.md` files are valid markdown (no encoding issues)
3. **Review logs:** If using Copilot CLI, check output for specific error messages
4. **Rerun the skill:** Simulations and ranking are deterministic; retrying should work if the issue was temporary
5. **Check Git history:** Use `git log --oneline skills/` to see recent changes to reference files

---

## 🔄 Determinism & Reproducibility

Both skills are **fully deterministic**: given the same inputs (candidate profile + JD + scoring rules), they always produce identical outputs. This enables:

- **Version control:** Git tracks all simulations and reference files
- **Reproducibility:** Re-run a simulation months later and get the same result
- **Auditing:** Prove that decisions were consistent and fair
- **A/B testing:** Change one rule, re-run, and compare outputs to measure impact
- **Time travel:** Compare your fit to the same job across different versions of your resume

To preserve this determinism:
- Do not edit reference files mid-evaluation (set them, run simulations, then adjust)
- Do not modify `simulation_contract.md` or `ranking_rules.md` without understanding the impact
- Version-control all changes with meaningful commit messages

---

## 📦 Incoming Features

### **Resume-Rewrite Skill** (Now Available)
A skill that rewrites your resume to target a specific job description. It:
- Highlight relevant skills and responsibilities
- Reorder work history for maximum impact
- Optimize language for ATS and recruiter scanning
- Generate a "signals" document showing what the rewritten resume optimizes for
- Integrate with the Simulation skill for immediate fit testing

Released: Q3 2026

---

## 🤝 Contributing & Customization

This engine is designed to be forked and customized:

### **To modify behavior:**
1. Edit templates in `assets/templates/`
2. Edit reference files (candidate profile, preferences)
3. Edit scoring rules in `references/ranking_rules.md`
4. Run simulations to test changes

### **To add new skills:**
1. Create a new directory in `.github/skills/`, `.claude/skills/`, and `.gemini/skills/`
2. Add a `SKILL.md` file describing the new skill
3. Add necessary templates and references
4. Update this README with the new skill description

### **To report bugs or request features:**
Open an issue on GitHub: https://github.com/sidsomash/recruiter-simulation-engine/issues

---

## 📚 References & Further Reading

- **GitHub Copilot CLI Documentation:** https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli
- **Simulation Contract:** `.github/skills/simulation/references/simulation_contract.md`
- **Ranking Rules:** `.github/skills/ranking/references/ranking_rules.md`
- **Claude Instructions:** `.claude/CLAUDE.md`
- **Gemini Instructions:** `.gemini/GEMINI.md`

---

## 📄 License

See LICENSE file for details.

---

*Last updated: July 9, 2026*
