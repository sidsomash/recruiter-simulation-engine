# Claude Instructions for recruiter-simulation-engine

This directory contains Claude-compatible skills for the recruiter-simulation-engine. Claude can use these skills to help candidates evaluate job opportunities, run simulations, and rank fit across roles.

## 📋 Overview

The recruiter-simulation-engine is a modular system that converts job descriptions into structured, recruiter-grade simulations and ranks those simulations to prioritize hiring opportunities.

**Repository:** [recruiter-simulation-engine](https://github.com/sidsomash/recruiter-simulation-engine)

---

## 🧠 Available Skills

Claude has access to the following skills in this directory:

### 1. **Initialize Skill** 
- **Location:** `.claude/skills/initialize/`
- **Purpose:** Guides new users through creating their candidate profile by collecting resume, profile, and preferences data.
- **Invocation:** "Initialize my candidate profile" or "Set up my candidate profile"
- **Output:** Creates three foundational markdown files:
  - `candidate_resume.md` (structured work history and education)
  - `candidate_profile.md` (background, location, constraints)
  - `candidate_preferences.md` (desired roles, skills, environments)

### 2. **Simulation Skill**
- **Location:** `.claude/skills/simulation/`
- **Purpose:** Parses a job description, applies the simulation contract (skill & responsibility mapping, experience/degree mapping, preference checks), and generates a deterministic simulation result.
- **Invocation:** "Run a simulation for this job description" or "Simulate this JD"
- **Input:** Paste raw job description text
- **Output:** Timestamped markdown file saved to `skills/simulation/simulations/`
- **Key References:**
  - `simulation_contract.md` — canonical simulation rules (do not modify)
  - `candidate_resume.md`, `candidate_profile.md`, `candidate_preferences.md` — reference data
- **Templates:** Skill mappings, experience mappings, degree mappings, and final output formatting

### 3. **Ranking Skill**
- **Location:** `.claude/skills/ranking/`
- **Purpose:** Reads all simulation outputs, extracts structured fields, computes composite scores using the canonical ranking rules, and returns a ranked table of roles.
- **Invocation:** "Rank my simulations" or "Show ranked results"
- **Input:** None (auto-discovers simulations directory)
- **Output:** Ephemeral ranked table in terminal response (not persisted)
- **Scoring Model:** `references/ranking_rules.md` (canonical and authoritative)

### 4. **Resume-Restructure Skill**
- **Location:** `.claude/skills/resume-restructure/`
- **Purpose:** Rewrites candidate résumés to target specific job descriptions, producing tailored resumes with signals for downstream simulations.
- **Invocation:** "Restructure my resume for this JD"
- **Status:** Available for targeted resume optimization
- **Key Reference:** `references/resume_guidelines.md`

---

## 🧩 Routing Rules

Claude should run a skill **only when explicitly invoked** by the user. Do not auto-trigger skills when a job description is pasted unless the user explicitly asks for a simulation.

### **Running the Simulation Skill**
Invoke only when the user says:
- "Run a simulation for this job description"
- "Simulate this JD"
- "Generate a simulation for this role"
- "Evaluate this job against my profile"

### **Running the Ranking Skill**
Invoke only when the user requests:
- "Rank my simulations"
- "Aggregate all simulations"
- "Show me the ranked results"
- "Which roles are the best fit?"

### **Running the Initialize Skill**
Invoke when the user says:
- "Initialize my candidate profile"
- "Set up my candidate profile"
- "Create my profile"

---

## 📁 Output Locations

- **Simulation outputs:** `skills/simulation/simulations/` (timestamped markdown files)
- **Ranking outputs:** Ephemeral (printed to terminal, not persisted)
- **Candidate reference files:** Created by Initialize skill and referenced by Simulation skill

---

## 🚫 Prohibited Behavior

Claude should **not**:
- Auto-route job descriptions to the Simulation skill
- Rewrite or modify existing simulation outputs
- Modify scoring rules in `ranking_rules.md`
- Modify canonical templates
- Infer intent without explicit user instruction
- Run skills implicitly

All skill execution must be **explicit** and **requested by the user**.

---

## ✅ Best Practices

1. **Always verify candidate data exists** before running simulations — the Initialize skill should run first if no candidate profile exists.
2. **Preserve simulation outputs** — they are deterministic records of evaluation at a point in time.
3. **Use ranking to prioritize** — after multiple simulations, run the Ranking skill to see which roles fit best.
4. **Reference the contract** — when explaining simulation results, cite the `simulation_contract.md` for transparency.
5. **Validate templates** — if output formatting seems wrong, check the template files in `assets/templates/`.

---

## 📝 Debugging & References

- **Simulation Contract:** `.claude/skills/simulation/references/simulation_contract.md` (defines the deterministic evaluation logic)
- **Ranking Rules:** `.claude/skills/ranking/references/ranking_rules.md` (defines scoring model)
- **Candidate Artifacts:** `.claude/skills/simulation/references/` (candidate_resume.md, candidate_profile.md, candidate_preferences.md)
- **Templates:** `.claude/skills/simulation/assets/templates/` and `.claude/skills/ranking/assets/templates/`

---

## 📚 Related Resources

- Main Repository README: See the repo root `README.md` for full context
- GitHub Copilot CLI Docs: https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli
