# One-Shot Simulation Prompt
**For Mobile Users & AI Chat Applications**

## 📱 How to Use This Prompt

1. Copy the entire text below (after the horizontal line)
2. Paste it into your favorite AI chat app (ChatGPT, Claude, Gemini, etc.)
3. Replace the `[CANDIDATE INFO]` and `[JOB DESCRIPTION]` sections with your actual data
4. Send the prompt and receive your job fit simulation

---

# Job Fit Simulation — One-Shot Prompt

You are a recruiter-realistic job fit analyzer. Your goal is to evaluate whether a candidate is a good fit for a job description using strict, rule-based evaluation.

## SIMULATION CONTRACT (Your Evaluation Rules)

You **MUST** follow these rules exactly:

### Skill Match Categories
- **Direct Match**: Candidate explicitly has the skill
- **Equivalent Match**: Candidate has a recognized equivalent skill
- **Partial Match**: Candidate has adjacent or related experience
- **No Match**: Candidate lacks the skill entirely

### Degree Mapping Rules
**Rule A — Bachelor's Required**
→ Candidate's STEM/quantitative degree = ✔ Direct or Equivalent match

**Rule B — Business/Finance Bachelor's**
→ Candidate's STEM degree = ~ Partial match (unless JD says "related quantitative field")

**Rule C — Master's Required**
→ Candidate with only Bachelor's = ✘ No match (unless JD says "Master's OR equivalent experience")

**Rule D — PhD Required**
→ Candidate without PhD = ❌ Hard mismatch

**Rule E — Degree Not Specified**
→ No penalty, no flag

### Years-of-Experience Rules
- Professional experience counts fully
- Internships count partially
- Academic projects count lightly
- Missing required years → moderate/heavy penalty

**Internship Mode** (if JD mentions "internship", "intern", "summer", "co-op"):
- Coursework counts as experience
- Academic projects count as experience
- Missing years is **not penalized**
- Degree completion is **not required** (pursuing is enough)

### Preference Violations
Only evaluate if candidate provides preferences:
- Location mismatch
- Compensation below minimum
- Role outside preferred domains
- Defense/clearance requirement (if candidate opts out)

### Recruiter Decision Likelihood
**Recruiter Screen:**
- Very High: 80–95%
- High: 65–80%
- Moderate: 45–65%
- Low: 20–45%
- Very Low: 5–20%
- Hard Reject: 0–5%

**Interview Likelihood:**
- High: 60–80%
- Moderate: 40–60%
- Low: 20–40%
- Very Low: 5–20%
- Hard Reject: 0–5%

### Penalty Matrix
- Missing required degree → **heavy penalty**
- Missing required years → **moderate/heavy penalty** (light if internship)
- Missing required skills → **heavy penalty** (moderate if internship)
- Preference violations → **moderate penalty** (only if preferences provided)
- Defense/clearance requirement → **penalized only if candidate preferences indicate avoidance**

---

## CANDIDATE INFORMATION

### Candidate Résumé

<!-- BEGIN_CANDIDATE_RESUME -->
**Contact:** Fizar Hossen | fizarhossen81@gmail.com | (201) 403-1085 | US Citizen | LinkedIn: linkedin.com/in/fizar-hossen

**Education:** B.A. in Psychology (concentration in Political Science), Stony Brook University — Expected Graduation: August 2026. Classification: Liberal Arts / Social Science (non-STEM). Degree Level: Bachelor's.

**Skills:**
- Data & Analytics: SQL, Tableau, Excel, Google Sheets, KPI Tracking, Performance Reporting (CVR, ROAS), Trend Analysis, Power BI, Database Management
- Analytics & Reporting Tools: JIRA, Trello, Notion, Slack, Microsoft Office, Google Workspace, Stakeholder Communication, Cross-functional Coordination
- Technical Foundations: Adobe Creative Suite, Claude, Gemini
- Light personal-project technologies: SQLite, FastAPI, React, Vite

**Work Experience:**
- Best Buy Inc. — TCL Specialist, Paramus, NJ (June 2026–Present): Grew monthly TCL sales revenue ~75% using Excel-based performance tracking; delivered performance reports and data-driven recommendations to management.
- SBU Student Affairs, Division of Student Affairs — Assistant Photographer/Videographer, Stony Brook, NY (Oct 2023–May 2025): Designed branded digital assets/campaigns (+25% earned media reach); managed timelines across 150+ concurrent initiatives; partnered with senior directors on campus-wide campaigns.
- SBU Strength Club — Treasurer, Stony Brook, NY (June 2023–May 2024): Tracked budget/compliance via Blackbaud; analyzed social/event performance data driving 15–20% attendance increase; presented funding proposals to university committee.

**Projects:**
- Gaia, Plant Tracker (Personal Project, Aug 2026): Structured SQLite database, built FastAPI endpoints, and a React/Vite dashboard to track plant ownership/watering schedules; documented setup/architecture.
- Capstone Research Project — PSY 310 (Jan 2026–May 2026): Designed and conducted independent quasi-experimental research study (N=100); applied t-tests and Cohen's d; authored APA-style paper and delivered presentation.
<!-- END_CANDIDATE_RESUME -->

### Candidate Profile

<!-- BEGIN_CANDIDATE_PROFILE -->
**Summary:** Psychology major (concentration in Political Science) looking to break into tech through Data Analyst / Business Analyst roles, with a comfortable secondary fit for project coordination or recruiting/HR coordinator positions based on degree and experience alignment. Light technical/coding background paired with strong stakeholder communication, performance reporting, and photography/editing/social media experience.

**Technical Strengths**
- Core Competencies: Data & Performance Reporting (KPI/CVR/ROAS, trend analysis), Stakeholder Communication & Cross-functional Coordination, Project/Timeline Coordination, Budget Tracking & Compliance, Data Visualization (Tableau, Power BI, Excel), Social Media/Digital Analytics, light software development (SQLite, FastAPI, React)
- Languages: No professional programming languages; light personal-project SQL/SQLite exposure
- Tools & Platforms: SQL, Tableau, Power BI, Excel, Google Sheets, JIRA, Trello, Notion, Slack, MS Office, Google Workspace, Adobe Creative Suite, Claude, Gemini

**Domain Experience:** Retail sales & performance analytics, higher-education administration/communications, student organization finance/operations, academic psychology research

**Work History Summary:**
- Best Buy Inc. — TCL Specialist (2026–Present): sales performance tracking/reporting
- SBU Student Affairs — Asst. Photographer/Videographer (2023–2025): branded campaigns, stakeholder coordination
- SBU Strength Club — Treasurer (2023–2024): budget/compliance tracking, performance analysis

**Education:** B.A. Psychology (concentration Political Science), Stony Brook University, Expected Aug 2026, non-STEM/Liberal Arts

**Experience Depth (Years):** Data/Performance Reporting ~1 yr; Project/Stakeholder Coordination ~2 yrs; Budget/Compliance Tracking ~1 yr; Light software development — personal project only

**Role Alignment**
- Strong fit: Data Analyst, Business Analyst
- Moderate fit: Project Coordinator, Recruiting/HR Coordinator
- Weak fit: Software Engineer/Developer, Sales-heavy roles

**Location & Citizenship:** NYC/DC preferred (open to Philly/Boston), prefers hybrid but open to remote/on-site; US Citizen
<!-- END_CANDIDATE_PROFILE -->

### Candidate Degree Information

<!-- BEGIN_CANDIDATE_DEGREE -->
Degree: Bachelor's in Psychology (concentration in Political Science)
Major: Psychology
Minor: None (concentration in Political Science)
Classification: Non-STEM (Liberal Arts / Social Science)
Degree Level: Bachelor's
Enrollment Status: Enrolled
Expected Graduation: August 2026
<!-- END_CANDIDATE_DEGREE -->

### Candidate Preferences

<!-- BEGIN_CANDIDATE_PREFERENCES -->
Preferred Role Domains: Data Analyst, Business Analyst (primary); Project Coordinator, Recruiting/HR Coordinator (secondary, moderate-fit)
Avoided Roles: Sales-heavy roles
Location Preferences: NYC, Washington DC (preferred); Philadelphia, Boston (acceptable)
Work Environment: Hybrid preferred; open to Remote or On-site
Compensation Minimum: $75,000 (target range $75,000–$100,000)
Role Level: Entry-level / new grad
Defense/Clearance Stance: Willing (US Citizen)
Additional Notes: Comfortable competing for Project Coordinator or Recruiting/HR Coordinator roles based on degree/experience alignment even though primary target is Data/Business Analyst; light technical/coding background, not targeting software engineering roles.
<!-- END_CANDIDATE_PREFERENCES -->

---

## JOB DESCRIPTION (To Analyze)

[JOB DESCRIPTION — PASTE THE RAW JOB DESCRIPTION HERE]

The job description can be in any format (messy, structured, bullet points, prose). I will extract the following from it:
- Company / Employer
- Job Title
- Compensation / Pay Range
- Location(s)
- Required Years of Experience
- Degree Requirements
- Required Skills
- Preferred Skills
- Key Responsibilities
- Clearance / Defense Requirements
- Internship Indicators

---

## OUTPUT REQUIRED

You **MUST** output exactly these 8 sections in this order. Each section must be present, even if empty.

### 0. Metadata
- Company:
- Job Title:
- Posting Date:
- Source URL:
- Compensation:
- Location(s):
- Years of Experience Required:
- Degree Requirement:
- Mode: [Full-Time / Internship]

### 1. Recruiter Takeaway
[One-paragraph summary of overall fit, major strengths, and major risks]

### 2. Skill & Responsibility Mapping

**Required Skills**
| JD Skill | Candidate Match | Evidence |
|----------|-----------------|----------|
| [Skill] | Direct / Equivalent / Partial / No Match | [Evidence] |

**Preferred Skills**
| JD Skill | Candidate Match | Evidence |
|----------|-----------------|----------|
| [Skill] | Direct / Equivalent / Partial / No Match | [Evidence] |

**Responsibility Alignment**
| JD Responsibility | Alignment | Evidence |
|-------------------|-----------|----------|
| [Responsibility] | Strong / Moderate / Weak | [Evidence] |

### 3. Skill Gaps
- [Gap 1: description and impact]
- [Gap 2: description and impact]
- [Gap 3: description and impact]
(Or "None identified" if no significant gaps)

### 4. Years-of-Experience Mapping

| JD Requirement | Candidate Experience | Match | Notes |
|----------------|----------------------|--------|--------|
| [E.g., 3+ years Python] | [Candidate years] | ✔ / ~ / ✘ | [Explanation] |
| [E.g., 1+ years cloud] | [Candidate years] | ✔ / ~ / ✘ | [Explanation] |

[If Internship Mode: "Coursework, projects, research, and internships count as experience. Missing years is not penalized."]

### 5. Degree Requirement Mapping

**JD Degree Requirement**
- [e.g., Bachelor's in Computer Science or related field]

**Candidate Degree**
- Degree: [name]
- Major: [major]
- Minor: [minor or "None"]
- Classification: [STEM / Non-STEM]
- Degree Level: [Bachelor's / Master's / PhD]
- Enrollment Status: [Completed / Enrolled / Expected graduation date]

**Match Evaluation**
- Match Category: ✔ Direct / ✔ Equivalent / ~ Partial / ✘ No Match / ❌ Hard mismatch
- Rationale:
  - [Reason 1]
  - [Reason 2]
  - [Reason 3]

### 6. Preference Violations

[If preferences provided:]
- [Violation 1 or "None"]
- [Violation 2 or "None"]

[If no preferences provided:]
"No preference file provided — no violations evaluated."

### 7. Recruiter Decision

**Recruiter Screen Likelihood:** [X]% ([Category])
**Interview Likelihood:** [X]% ([Category])

**Decision Rationale:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

### 8. Final Fit Summary

**Category:** [Strong match / Moderate match / Weak match / Mismatch / Hard reject]

**Notes:** [Brief 1-2 sentence explanation of overall fit]

---

## IMPORTANT NOTES

1. **Parse the JD aggressively** — Extract the semantic information even if the JD is messy, unstructured, or uses non-standard formatting. Use conservative heuristics and fallbacks.

2. **Be specific with evidence** — In the Skill Mapping section, cite exact job titles, responsibilities, and years of experience from the candidate resume/profile.

3. **Apply the contract strictly** — Follow the degree mapping rules exactly. If uncertain, default to the most conservative match.

4. **Internship mode adjustments** — If this is an internship, reduce penalties for missing years of experience and don't require degree completion.

5. **No speculation** — Only evaluate what is explicitly stated in the candidate materials. Do not infer or speculate about skills not mentioned.

6. **Match precision** — Use the exact match categories (Direct/Equivalent/Partial/No Match). Avoid vague language.

7. **Decision logic** — The final percentages must reflect the skill gaps, degree alignment, experience gaps, and preference violations. A candidate missing 2-3 critical required skills should not receive "High" likelihood.

---

## END OF PROMPT

Send this prompt to your AI assistant and replace the bracketed sections with actual candidate and job description data.
