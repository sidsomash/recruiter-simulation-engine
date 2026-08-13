# Simulation Contract v2.4 — Recruiter‑Strict Edition  
### (Bias‑Free, Candidate‑Agnostic, Internship‑Compatible)

## 1. Purpose
A simulation is a recruiter‑realistic fit analysis that:

- Maps the job description (JD) to the candidate’s résumé  
- Identifies skill matches, partial matches, and gaps  
- Evaluates responsibility alignment  
- Evaluates years‑of‑experience alignment  
- Evaluates degree requirement alignment  
- Identifies preference violations (based on candidate-provided preferences)  
- Outputs a recruiter‑style decision likelihood  

A simulation **does not** predict final hiring outcomes.  
It models the **initial recruiter screen** using strict, rule‑based evaluation.

---

## 2. Required Inputs

### 2.1 Job Description (JD)
Raw or cleaned JD text containing:
- Responsibilities  
- Required skills  
- Preferred skills  
- Degree requirements  
- Years of experience  
- Location  
- Compensation (if available)  
- Clearance or defense requirements (if any)

### 2.2 Candidate Résumé
Structured résumé text containing:
- Skills  
- Responsibilities  
- Tools/technologies  
- Years of experience  
- Education  
- Projects  
- Certifications  

### 2.3 Candidate Profile
A structured profile containing:
- Work history  
- Domain experience  
- Technical stack  
- Location  
- Compensation expectations  
- Role preferences  

### 2.4 Candidate Degree Information
A structured degree object containing:
- Degree name  
- Major  
- Minor (optional)  
- Classification (STEM / non‑STEM)  
- Domain equivalencies  
- Degree level (Bachelor’s / Master’s / PhD)  
- Enrollment status (for internships)

### 2.5 Candidate Preferences (Optional)
A structured preferences file containing:
- Preferred roles  
- Avoided roles  
- Location preferences  
- Compensation minimums  
- Remote/hybrid/on‑site preferences  
- Defense/clearance stance  

If omitted, **no preference violations are applied**.

---

## 3. Required Output Sections

Every simulation must output **exactly** these sections in order:

1. **Recruiter Takeaway**  
2. **Skill & Responsibility Mapping**  
3. **Skill Gaps**  
4. **Years‑of‑Experience Mapping**  
5. **Degree Requirement Mapping**  
6. **Preference Violations**  
7. **Recruiter Decision**  
8. **Final Fit Summary**

Each section must be present, even if empty.

---

## 4. Skill & Responsibility Mapping Rules

### 4.1 Skill Match Categories
- **Direct Match** — Candidate explicitly has the skill  
- **Equivalent Match** — Candidate has a recognized equivalent  
- **Partial Match** — Candidate has adjacent or related experience  
- **No Match** — Candidate lacks the skill entirely  

### 4.2 Responsibility Mapping
Responsibilities are mapped using:
- Direct experience  
- Adjacent experience  
- Transferable experience  

---

## 5. Degree Requirement Mapping (Mandatory)

Every simulation must include a strict mapping of:

**(A) Degree required by the JD**  
vs.  
**(B) Candidate’s actual degree or enrollment status**

### 5.1 Degree Match Labels

- ✔ **Direct match** — Degree exactly matches or is explicitly listed  
- ✔ **Equivalent match** — Degree is a STEM/quantitative equivalent  
- ~ **Partial match** — Degree is adjacent but not explicitly listed  
- ✘ **No match** — Degree is not relevant to the required field  
- ❌ **Hard mismatch** — JD requires Master’s/PhD with no “or equivalent experience” clause  

### 5.2 Degree Mapping Rules

**Rule A — Bachelor’s Required**  
If JD requires a Bachelor’s in STEM, CS, Math, Engineering, Data Science, or related quantitative field:  
→ Candidate’s STEM/quantitative degree = ✔ Direct or Equivalent match

**Rule B — Business/Finance/Accounting Bachelor’s**  
If JD requires a Bachelor’s in Finance, Accounting, Economics, Business:  
→ Candidate’s STEM degree = ~ Partial match  
Unless JD explicitly allows “related quantitative field,” then → ✔ Equivalent match

**Rule C — Master’s Required**  
If JD requires a Master’s degree:  
→ Candidate with only a Bachelor’s = ✘ No match  
Unless JD says “Master’s OR equivalent experience,” then evaluate experience.

**Rule D — PhD Required**  
If JD requires a PhD:  
→ Candidate without PhD = ❌ Hard mismatch

**Rule E — Degree Not Specified**  
→ No penalty, no flag.

### 5.3 Degree Domain Mapping (Generalized)

| JD Field | Candidate Degree | Match |
|---------|------------------|--------|
| Computer Science | STEM quantitative | ✔ Equivalent |
| Data Science | STEM quantitative | ✔ Direct |
| Applied Math / Statistics | STEM quantitative | ✔ Direct |
| Engineering | STEM quantitative | ~ Partial |
| Finance / Accounting | STEM quantitative | ✘ No match |
| Economics | STEM quantitative | ~ Partial |
| AI/ML | STEM quantitative | ✔ Equivalent |
| Business Analytics | STEM quantitative | ✔ Equivalent |

---

## 6. Years‑of‑Experience Mapping

### 6.1 Experience Interpretation (Full‑Time Roles)
- Professional experience counts fully  
- Internships count partially  
- Academic projects count lightly  
- Missing required years → moderate/heavy penalty  

### 6.2 Experience Match Labels
- ✔ Meets requirement  
- ~ Partially meets requirement  
- ✘ Does not meet requirement  

---

## 7. Preference Violations

Preference violations are applied **only if the candidate provides a preferences file**.

Possible violations include:
- Location mismatch  
- Compensation below candidate minimum  
- Role outside candidate’s preferred domains  
- Defense/clearance requirement (only if candidate opts out)  
- On‑site/remote mismatch  

If no preferences are provided:  
→ This section must state **“No preference file provided — no violations evaluated.”**

---

## 8. Recruiter Decision (Strict)

### 8.1 Likelihood of Recruiter Screen
- **Very High:** 80–95%  
- **High:** 65–80%  
- **Moderate:** 45–65%  
- **Low:** 20–45%  
- **Very Low:** 5–20%  
- **Hard Reject:** 0–5%  

### 8.2 Likelihood of First‑Round Interview
- **High:** 60–80%  
- **Moderate:** 40–60%  
- **Low:** 20–40%  
- **Very Low:** 5–20%  
- **Hard Reject:** 0–5%  

### 8.3 Decision Rules
- Missing required degree → **heavy penalty**  
- Missing required years of experience → **moderate/heavy penalty**  
- Missing required skills → **heavy penalty**  
- Preference violations → **moderate penalty** (only if preferences provided)  
- Defense/clearance requirement → **penalized only if candidate preferences indicate avoidance**  

---

## 9. Internship Mode (Optional)

If the JD is identified as an internship, the simulation must adjust the evaluation rules:
The Step 3 mode determination (Full-Time vs. Internship) must be recorded verbatim in the
output's Metadata section as `Internship Mode: Yes` or `Internship Mode: No` — this is the
authoritative flag downstream tooling (e.g., the ranking skill) relies on, so it must always be
set explicitly rather than left blank or inferred later from the job title.

### 9.1 Experience Interpretation (Internships)
- Coursework counts as experience  
- Academic projects count as experience  
- Research counts as experience  
- Hackathons count as experience  
- Personal projects count as experience  
- Missing “years of experience” is **not penalized**  
- Professional experience is a bonus, not a requirement  

### 9.2 Responsibility Mapping (Internships)
- Responsibilities are mapped to coursework, projects, and internships  
- Lack of ownership or leadership is **not penalized**  
- Depth expectations are reduced  

### 9.3 Degree Requirements (Internships)
- “Pursuing a degree in X” is treated as:  
  ✔ Direct match if candidate is enrolled in that field  
  ✔ Equivalent match if enrolled in a related STEM field  
- Degree completion is **not required**  

### 9.4 Recruiter Decision Adjustments (Internships)
- Missing required skills → moderate penalty (not heavy)  
- Missing required experience → light penalty  
- Degree mismatch → evaluated based on enrollment, not completion  

### 9.5 Internship Fit Summary Labels
- Strong internship match  
- Moderate internship match  
- Weak internship match  
- Mismatch  

---

## 10. Final Fit Summary

One of:

- **Strong match**  
- **Moderate match**  
- **Weak match**  
- **Mismatch**  
- **Hard reject** (only if recruiter logic or candidate preferences dictate)

The summary must reflect the recruiter decision logic above.