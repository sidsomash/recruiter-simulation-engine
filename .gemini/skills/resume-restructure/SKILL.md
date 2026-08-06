# Resume-Restructure Skill

A deterministic resume rewriting engine that adapts the candidate's résumé to target a specific job description (JD), emphasizing skills, responsibilities, and experiences most relevant to that particular recruiter's needs.

This skill transforms a generic résumé into a tailored, JD-focused version that highlights domain-specific alignment and recruiter-relevant signals.

---

## 📚 References

This skill depends on the following reference files:

- [resume_guidelines.md](references/resume_guidelines.md)  
  Defines the rewriting logic, emphasis strategies, and best practices for tailoring résumés.

- Original candidate reference files (from simulation skill):
  - `../simulation/references/candidate_resume.md`  
  - `../simulation/references/candidate_profile.md`  

---

## 🧩 Templates

The résumé output is generated using the following template:

- [resume_output_template.md](assets/templates/resume_output_template.md)  
  Ensures consistent structure and formatting across all tailored résumés.

---

## 📝 Inputs

This skill requires:

1. **simulation_file** (string, required): Path or filename of the completed simulation (e.g., `20260805_234550_data-engineer-mizuho.md`)
   - The skill will auto-discover this from the simulations directory or accept explicit user input.
   - Used to extract JD context (company, role, required skills, responsibilities, domain).

2. **candidate_resume.md** (string, reference): Loaded automatically from `../simulation/references/candidate_resume.md`.

3. **candidate_profile.md** (string, reference): Loaded automatically from `../simulation/references/candidate_profile.md`.

No additional parameters or overrides are supported.

---

## 🧠 Workflow

### **Step 1 — Load References**

Load all required reference and candidate files:

- Original `candidate_resume.md` (source material for rewriting)  
- `candidate_profile.md` (context for domain experience)  
- Target simulation file (to extract JD context)  
- `resume_guidelines.md` (rewriting strategy)  

This ensures the rewrite uses the latest candidate data and applies consistent strategy.

---

### **Step 2 — Extract JD Context from Simulation**

Parse the simulation output to extract:

- **Company name** (e.g., "Mizuho Financial Group")  
- **Job title** (e.g., "Data Engineer")  
- **Key required skills** (from simulation's skill mapping)  
- **Key responsibilities** (from simulation's responsibility alignment)  
- **Domain/industry** (e.g., financial services, logistics, defense)  
- **Experience level** (entry-level, mid-level, senior)  
- **Preferred technologies/tools** (from simulation's preferred skills)  
- **Recruiter's likely priorities** (inferred from simulation analysis)  

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

- All original content is factually grounded (no fabrication)  
- Emphasis matches recruiter's priorities (from simulation)  
- Language and terminology align with JD domain  
- Metrics and accomplishments are preserved (not exaggerated)  
- Structure follows the output template  

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
- After successfully saving the file, terminal/assistant responses should be restricted to a concise confirmation containing ONLY the relative file path and a one-line status (for example: "Saved: .gemini/skills/resume-restructure/resumes/20260805_234550_data-engineer-mizuho.md").  
- If an error prevents writing the file, return a brief error message that describes the failure.

---

## ⚠️ Error Handling

- If simulation file is missing → return a message requesting the simulation filename or path.  
- If original candidate_resume.md is missing → return a configuration error (Initialize skill must run first).  
- If resume_guidelines.md is missing → return a reference file error.  
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
