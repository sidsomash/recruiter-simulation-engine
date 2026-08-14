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

These files define the candidate’s background and the rules governing simulation behavior.

---

## 🧩 Templates

The simulation output is generated using the following templates:

- [simulation_output_template.md](assets/templates/simulation_output_template.md)  
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

Follow the contract exactly:

1. Recruiter Takeaway  
2. Skill & Responsibility Mapping  
3. Skill Gaps  
4. Years‑of‑Experience Mapping  
5. Degree Requirement Mapping — determine which of the four candidate degree categories in
   `references/degree_domain_map.json` applies (`stem_quantitative`,
   `business_finance_accounting`, `liberal_arts_humanities`, `social_sciences`, or none of these),
   using the candidate's degree title **plus** `candidate_profile.md` (technical strengths,
   quantitative coursework) and `candidate_preferences.md` (stated role preferences) when the
   title alone is ambiguous or borderline — do not classify from the degree title in isolation.
   Then look up the JD's required degree field under that category (see contract §5.2/§5.3). Fall
   back to Rules A–G only when the category or JD domain isn't covered by the JSON. If the
   candidate's degree doesn't match the JD's field but the candidate has substantial directly
   relevant professional/project experience (career-switcher case), apply §6.3 — state the
   mismatch plainly, cross-reference the relevant experience, and let §8's Recruiter Decision
   weigh both together.
6. Preference Violations  
7. Recruiter Decision  
8. Final Fit Summary  

This produces a structured evaluation of candidate fit.

---

### **Step 5 — Generate Output Using Templates**

Populate:

- simulation_output_template.md  
- skill_mapping_template.md  
- experience_mapping_template.md  
- degree_mapping_template.md  

This ensures consistent formatting across all simulations.

Stamp `Contract Version` in the output's Metadata section with the version number copied
verbatim from `simulation_contract.md`'s own header (e.g., `v2.4`, from the line
`# Simulation Contract v2.4 — ...`). Do not paraphrase or infer the version — read it directly
from the contract file being applied in Step 4. This lets old and new simulation files be
distinguished if the contract is revised later.

---

### **Step 6 — Save Output File**

Write the completed simulation output to: `skills/simulation/simulations/<timestamp>_<slugified-role>.md`

Where:

- `timestamp` = `YYYYMMDD_HHMMSS`
- `slugified-role` = lowercase, hyphenated version of the JD role title

Example: `skills/simulation/simulations/20260617_153022_data-engineer.md`

---

### **Step 7 — Return Output**

- Write the completed simulation output exclusively to the markdown file at `skills/simulation/simulations/<timestamp>_<slugified-role>.md`.
- Do NOT print, stream, or otherwise emit any simulation content (full or partial) to the terminal, logs, or assistant response payload. All simulation details must be persisted only to the output file.
- After successfully saving the file, terminal/assistant responses should be restricted to a concise confirmation containing ONLY the relative file path and a one-line status (for example: "Saved: .github/skills/simulation/simulations/20260623_093815_role.md"). No simulation content, analysis, or excerpts should be included in the response.
- If an error prevents writing the file, return a brief error message that describes the failure (no simulation content).

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



