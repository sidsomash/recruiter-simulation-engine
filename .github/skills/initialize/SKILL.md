---
name: initialize
description: Guides a new user through initializing their candidate preferences, profile, and resume across .github, .claude, and .gemini directories using structured templates and interactive prompts.
context: fork
---

# Initialize Skill

An onboarding skill that helps new users set up their complete candidate profile by creating structured, standardized markdown files for preferences, profile, and resume. The skill guides users through each section with clear templates and context-aware prompts.

This skill creates a persistent candidate foundation that powers all downstream skills (simulation, ranking, etc.).

---

## 📚 References

This skill does not depend on external reference files but creates the following foundational files:

- [candidate_resume.md](../../simulation/references/candidate_resume.md)  
- [candidate_profile.md](../../simulation/references/candidate_profile.md)  
- [candidate_preferences.md](../../simulation/references/candidate_preferences.md)  

These files are created in `.github/skills/simulation/references/` and mirrored in `.claude/skills/simulation/references/` and `.gemini/skills/simulation/references/`.

---

## 🧩 Templates

The following templates guide user input:

- [resume_input_template.md](#resume-input-template)  
- [profile_input_template.md](#profile-input-template)  
- [preferences_input_template.md](#preferences-input-template)  

---

## 📝 Inputs

This skill operates interactively, collecting user input in three phases:

1. **Resume Phase** — Extract work history, education, skills, and projects
2. **Profile Phase** — Synthesize technical strengths, domain experience, and role alignment  
3. **Preferences Phase** — Collect role preferences, location, compensation, and constraints

No parameters or flags are required; the skill guides the user through each phase.

---

## 🧠 Workflow

### **Step 1 — Confirm Initialization**

Ask the user to confirm they want to initialize a new candidate profile. If they decline, exit gracefully.

---

### **Step 2 — Resume Collection (Interactive)**

Display the resume template and guide the user through:

- **Contact Information** (name, email, phone, locations, citizenship, LinkedIn)
- **Education** (degree, school, graduation date, classification, minor if any)
- **Skills** (languages, platforms, frameworks/tools)
- **Work Experience** (company, role, dates, achievements/bullets)
- **Projects** (project name, role, dates, description)

Prompt the user for each section. Accept free-form input and lightly structure it using the template format.

**Output:** Structured `candidate_resume.md` file.

---

### **Step 3 — Profile Synthesis (Interactive)**

Display the profile template and guide the user through:

- **Summary** (1–3 sentences about technical focus and background)
- **Technical Strengths** (core competencies, languages, tools/platforms)
- **Domain Experience** (industries, verticals, problem spaces)
- **Work History Summary** (brief overview of roles and what was accomplished)
- **Education Summary** (degree level, classification, focus areas)
- **Experience Depth** (years in key skill areas)
- **Role Alignment** (what role types fit best, and what doesn't)
- **Location** (primary locations, remote preferences)
- **Citizenship** (for clearance/restricted roles)

Prompt the user for each section. Draw inspiration from the resume but ask synthesizing questions (e.g., "What are your 3–5 technical strengths?" or "What industries do you want to work in?").

**Output:** Structured `candidate_profile.md` file.

---

### **Step 4 — Preferences Collection (Interactive)**

Display the preferences template and guide the user through:

- **Preferred Role Domains** (data engineering, ML, backend, etc.)
- **Avoided Role Domains** (clearance roles, finance, etc.)
- **Location Preferences** (preferred cities, remote/hybrid/onsite stance)
- **Compensation Preferences** (minimum acceptable, target range)
- **Work Environment Preferences** (remote, hybrid, onsite, travel tolerance)
- **Role Level Preferences** (new grad, early career, senior, etc.)
- **Defense / Clearance Stance** (willing, unwilling, requires clearance)
- **Additional Notes** (openness to emerging roles, constraints, etc.)

Prompt the user for each section. Ask clarifying questions to ensure preferences are specific and actionable (e.g., "What's your minimum acceptable salary?" or "Are you open to fully remote roles?").

**Output:** Structured `candidate_preferences.md` file.

---

### **Step 5 — Save Files Across All Directories**

Write the three generated files to:

1. `.github/skills/simulation/references/`
2. `.claude/skills/simulation/references/`
3. `.gemini/skills/simulation/references/`

**File names:**
- `candidate_resume.md`
- `candidate_profile.md`
- `candidate_preferences.md`

Ensure all three locations have identical copies for consistency.

---

### **Step 6 — Return Confirmation**

Return a concise confirmation summarizing:

- ✅ Files created successfully
- 📂 Locations where files were saved (all three directories)
- 🚀 Next steps (e.g., "You can now run the simulation skill with a job description")

Example output:

```
✅ Candidate profile initialized successfully!

📂 Files saved to:
   • .github/skills/simulation/references/
   • .claude/skills/simulation/references/
   • .gemini/skills/simulation/references/

Created:
   • candidate_resume.md
   • candidate_profile.md
   • candidate_preferences.md

🚀 Next: Run a simulation by pasting a job description with the simulation skill.
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
- If files already exist → ask user if they want to overwrite or update.  

---

## 🧾 Notes

- This skill is interactive and conversational, not automated.  
- All three directories (`.github`, `.claude`, `.gemini`) receive identical copies.  
- Files created by this skill become the foundation for all other skills (simulation, ranking).  
- Users can re-run this skill to update their profile; existing files are overwritten.  
- No validation of resume content is performed; users are trusted to provide accurate information.  

