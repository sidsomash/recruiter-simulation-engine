# Resume Rewrite Skill
### (JD-Aligned, Simulation-Driven, ATS-Optimized)

A deterministic resume rewrite engine that tailors the candidate's résumé to a target job
description by consuming a completed simulation output. The skill reorganizes, reframes, and
emphasizes the candidate's existing experience and skills to maximize alignment with the JD
while preserving factual accuracy.

This skill is **dependent on the simulation skill** — it requires a simulation output as input
and does not parse job descriptions independently.

---

## 📚 Dependencies

This skill depends on:

- **Simulation Skill Output**: `skills/simulation/simulations/<timestamp>_<role>.md`
  - Contains parsed JD metadata, skill mapping, fit assessment, and degree/experience alignment
  
- **Candidate Resume**: `skills/simulation/references/candidate_resume.md`
  - The baseline resume to be rewritten

- **Resume Guidelines**: `references/resume_guidelines.md`
  - Defines rewrite principles, formatting rules, and bullet point structure

---

## 📝 Inputs

This skill requires **two inputs**:

### 1. Simulation Output File (Required)
- **Source**: User specifies simulation filename or ID
- **Format**: Markdown file from `skills/simulation/simulations/`
- **Example**: `20260710_070855_junior-data-services-ai-developer.md`
- **Fallback**: If not specified, use the most recent simulation file
- The simulation output must contain:
  - JD metadata (title, company, location, degree requirement, years required, compensation)
  - Skill & Responsibility Mapping (with match categories: Direct/Equivalent/Partial/No Match)
  - Degree Requirement Mapping (alignment category)
  - Years-of-Experience Mapping (alignment status)
  - Final Fit Summary (category: Strong/Moderate/Weak match, etc.)

### 2. Candidate Resume (Implicit)
- **Source**: `skills/simulation/references/candidate_resume.md`
- Automatically loaded; no user input required
- Contains:
  - Work experience (companies, titles, dates, responsibilities)
  - Skills (languages, tools, platforms, frameworks)
  - Projects (descriptions, tools, outcomes)
  - Education (degree, major, minor, institution, graduation date)

---

## 🧠 Workflow

### **Step 1 — Load References**
Load all required inputs:
- Simulation output file (parsed from user-specified path)
- Candidate resume
- Resume rewrite guidelines

---

### **Step 2 — Extract Simulation Context**
From the simulation output, extract:

- **JD Metadata**:
  - Job title, company, location, compensation, posting date
  - Years of experience required
  - Degree requirement
  - Degree alignment category (Direct/Equivalent/Partial/No Match)

- **Skill Mapping**:
  - Required skills (with match category: Direct/Equivalent/Partial/No Match)
  - Preferred skills (with match category)
  - Skill gaps (skills candidate lacks)

- **Experience Alignment**:
  - Years-of-experience requirement vs. candidate's experience
  - Match status (Meets / Partially meets / Does not meet)

- **Overall Fit**:
  - Final fit summary category (Strong/Moderate/Weak match, etc.)
  - Recruiter screen and interview likelihood

---

### **Step 3 — Analyze Resume Content**
Parse the candidate resume to extract:
- Current skills (grouped by category)
- Work experience entries (company, title, dates, bullets)
- Projects (name, tools, outcomes)
- Education (degree, major, institution, graduation)

---

### **Step 4 — Rewrite Resume**

Apply rewrite rules based on simulation insights:

#### **A. Skills Section Rewrite**
1. **Reorder skills** based on JD priority:
   - Rank 1: Required skills with Direct Match (e.g., Python, Spark, SQL)
   - Rank 2: Required skills with Equivalent/Partial Match (e.g., Java for Python role)
   - Rank 3: Preferred skills with Direct Match (e.g., cloud platforms if preferred)
   - Rank 4: Other candidate skills (less relevant to JD)
   - Rank 5: Remove skills that are irrelevant and create noise

2. **Normalize skill names** to match JD terminology:
   - "Spark" → "Apache Spark (PySpark, SQL)" if JD mentions both
   - "Postgres" → "PostgreSQL"
   - "LLM" → "Large Language Models (LLMs)"

3. **Do not add skills** the candidate does not have

#### **B. Experience Section Rewrite**
For each work experience entry:

1. **Prioritize roles** based on JD relevance:
   - Keep roles that demonstrate JD-required/preferred skills
   - Deprioritize unrelated roles (move to bottom or condense)

2. **Rewrite bullets** using the simulation's skill mapping:
   - **For skills marked "Direct Match"**: Emphasize with specific technical details
     - Example: "Engineered ETL pipelines using Spark SQL" (if Spark is Direct Match)
   - **For skills marked "Partial Match"**: Frame as transferable/adjacent
     - Example: "Designed data models using PostgreSQL, transferable to data architecture roles"
   - **For skill gaps**: Do NOT mention; omit entirely
   
3. **Adjust emphasis** based on **Fit Category**:
   - **Strong Match**: Confident, assertive tone; highlight strengths prominently
   - **Moderate Match**: Balanced tone; emphasize relevant skills while acknowledging growth
   - **Weak Match**: Humble, learning-focused tone; show initiative and transferable skills
   
4. **Apply bullet structure** (from resume_guidelines.md):
   - Action verb → What you did → How you did it → Impact (quantified)
   - Keep 3–5 bullets per role
   - Remove generic/filler bullets

#### **C. Projects Section Rewrite**
1. **Filter projects** to include only those demonstrating JD-aligned skills
2. **Rewrite** each project to emphasize:
   - Tools/technologies that match the JD (especially Direct Matches)
   - Architecture or approach relevant to the role
   - Measurable outcomes
3. **If no projects are JD-relevant**: Remove section entirely

#### **D. Education Section (Minimal Rewrite)**
1. Keep education as-is; no rewrite needed
2. If simulation shows degree as "Direct Match" or "Equivalent Match": 
   - Optionally emphasize relevant coursework or minor
3. Do not exaggerate or misrepresent degree

#### **E. Overall Tone & Framing**
1. **Adjust narrative** based on simulation insights:
   - If "Strong Match": Lead with strongest skills/experience; be confident
   - If "Moderate Match": Emphasize transferable skills; show growth trajectory
   - If "Weak Match": Acknowledge learning opportunity; frame as potential/initiative

2. **Use JD language** (without copying verbatim):
   - If JD emphasizes "distributed systems": Reframe candidate's work as "distributed data systems"
   - If JD emphasizes "ownership": Reframe bullets to show autonomy ("Designed independently", "Owned end-to-end")

---

### **Step 5 — Generate Output**

Produce three outputs:

#### **Output 1: Rewritten Resume**
A complete, ATS-optimized résumé with:
- Header (name, contact, location)
- Skills section (reordered by JD priority)
- Experience section (rewritten bullets, reordered by relevance)
- Projects section (filtered to JD-relevant projects)
- Education section (unchanged, or enhanced)
- Format: Markdown or plain text, single-column, ATS-friendly

#### **Output 2: Change Summary**
A structured list of changes made:
```
### Skills Section
- Moved "Python" to position 1 (Direct Match for required skill)
- Moved "SQL" to position 2 (Direct Match for required skill)
- Added emphasis to "Spark" and "Databricks" (required skills)
- Moved "C++" to bottom (not relevant to JD)

### Experience Section
- **CapTech (Data Engineer)**: Rewritten to emphasize ETL pipeline design, Spark, Snowflake
  - Bullet 1: "Engineered ETL pipelines..." → now emphasizes Spark SQL, production scale
  - Bullet 2: Removed, as it focused on unrelated data lineage tool
- **UPS (Internship)**: Rewritten to emphasize AI evaluation frameworks
  - Bullet 1: "Built Agentic Testing Framework..." → now emphasizes GenAI evaluation, accuracy, safety compliance

### Projects Section
- Kept: Mini Wikipedia RAG (demonstrates LlamaIndex, Azure OpenAI, RAG architecture)
- Removed: Ryoko (travel platform, not relevant to data/AI developer role)

### Emphasis Adjustments
- Increased technical specificity for Python, Spark, SQL
- De-emphasized non-relevant tools (e.g., C++, Docker for data-focused roles)
- Adjusted tone: Balanced (Moderate match), not over-confident
```

#### **Output 3: JD Alignment Notes**
Brief explanation of rewrite rationale:
```
### Alignment Strategy
This role prioritizes:
1. Python + AI evaluation frameworks → Your ATF experience is a major strength; emphasized first
2. Data quality and bias auditing → Your CapTech data filtering + ATF work maps directly
3. Financial services domain → Your CapTech + UPS experience is highlighted prominently

### Key Changes
- Reordered skills to lead with Python, SQL, Spark (all Direct Matches)
- Reframed CapTech role to emphasize data infrastructure, not lineage tooling
- Elevated ATF as primary achievement (nearly identical to Citi's "evaluation framework" requirement)
- Adjusted tone to Balanced (Moderate-Strong match) → confident but acknowledging learning curve for MCP/ADK

### Tone Calibration
- Fit category: Strong match → Use assertive language ("Designed", "Built", "Delivered")
- No underselling; no overselling
- Emphasize proven expertise (Spark, Python, evaluation frameworks)
- Show openness to learning (MCP, Anthropic ADK with proven rapid learning track record)
```

---

### **Step 6 — Save Outputs**

Write outputs to persistent files:

1. **Rewritten resume**: `skills/resume-restructure/rewrites/<timestamp>_<slugified-role>_resume.md`
2. **Change summary**: Included as section in markdown
3. **Alignment notes**: Included as section in markdown

File naming convention:
- `<timestamp>_<slugified-role>_resume.md`
- Example: `20260710_070855_junior-data-services-ai-developer_resume.md`

---

### **Step 7 — Return Output**

- Write the rewritten resume, change summary, and alignment notes to the markdown file
- Emit a brief confirmation message with:
  - File path (relative to repo root)
  - One-line status (e.g., "Resume tailored for Citi role; 3 skills reordered, 5 bullets rewritten")
  - Do NOT print full resume content to stdout (too verbose; file is the canonical output)

---

## ⚠️ Error Handling

- **Simulation file not found**: Return error message asking user to:
  1. Run simulation skill first
  2. Provide correct simulation filename
  
- **Simulation output malformed**: Return error describing which sections are missing (Skill Mapping, Fit Summary, etc.)

- **Candidate resume missing**: Return configuration error; check that `skills/simulation/references/candidate_resume.md` exists

- **Resume rewrite guidelines missing**: Return configuration error; check that `skills/resume-restructure/references/resume_guidelines.md` exists

- **Skill overlap detected**: If resume already mentions a skill the simulation marked as "No Match", warn user but do not remove (preserve truthfulness)

---

## 🧾 Notes

- This skill is **deterministic**: same simulation + same resume → same rewritten output
- This skill **preserves truthfulness**: no fabrication, only reframing and reorganization
- This skill is **simulation-dependent**: always run simulation before resume-rewrite
- This skill **does not generate new content**: it reorganizes and reframes existing material
- This skill is **ATS-optimized**: follows formatting rules for applicant tracking systems
- This skill is **candidate-agnostic except for content**: the rewrite logic applies uniformly regardless of candidate profile

---

## 📋 Quick Start for Users

1. **Run simulation**:
   ```
   @copilot /invoke simulation
   [paste job description]
   ```
   Output: `20260710_070855_junior-data-services-ai-developer.md`

2. **Run resume-rewrite** (optional follow-up):
   ```
   @copilot /invoke resume-restructure
   [specify: "Use simulation 20260710_070855" or just "Use latest"]
   ```
   Output: `20260710_070855_junior-data-services-ai-developer_resume.md`

3. **Review tailored resume**:
   - Read the change summary to understand what was rewritten
   - Review alignment notes to see the rationale
   - Export to PDF or Word for final polish

---

## 🔗 Related Skills

- **Simulation Skill** (`skills/simulation/SKILL.md`): Required input; generates the JD analysis
- **Ranking Skill** (`skills/ranking/SKILL.md`): Optional downstream use; ranks multiple simulations (which can have corresponding tailored resumes)

---

## 📖 References

- `resume_guidelines.md`: Canonical resume rewrite rules and formatting
- `../simulation/references/candidate_resume.md`: Baseline candidate resume
- `../simulation/references/simulation_contract.md`: Simulation structure (for parsing skill mapping)
