---
name: simulation
description: Evaluates a job description against the candidate’s resume, profile, and preferences using a deterministic simulation contract, then outputs and stores a structured simulation result for ranking.
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

This skill accepts a single input:

- **job_description** (string): Raw text of the job description.

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
Extract structured information:

- required skills  
- preferred skills  
- responsibilities  
- degree requirements  
- years of experience  
- location  
- clearance requirements  
- internship indicators (“intern”, “internship”, “summer”, “co‑op”)  

Convert the JD into a structured internal representation.

---

### **Step 3 — Determine Mode (Full‑Time vs Internship)**

Internship Mode is activated if:

- the JD contains internship indicators **OR**
- the candidate profile indicates enrollment **AND** preferences allow internships

No manual override is supported.

---

### **Step 4 — Apply Simulation Contract**

Follow the contract exactly:

1. Recruiter Takeaway  
2. Skill & Responsibility Mapping  
3. Skill Gaps  
4. Years‑of‑Experience Mapping  
5. Degree Requirement Mapping  
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

---

### **Step 6 — Save Output File**

Write the completed simulation output to: `skills/simulation/simulations/<timestamp>_<slugified-role>.md`

Where:

- `timestamp` = `YYYYMMDD_HHMMSS`
- `slugified-role` = lowercase, hyphenated version of the JD role title

Example: `skills/simulation/simulations/20260617_153022_data-engineer.md`

---

### **Step 7 — Return Output**

Return the full simulation output to the user.

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



