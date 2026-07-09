# Ranked Role Evaluation Results

This document presents the ranked results of all simulation outputs using the scoring model defined in `references/ranking_rules.md`.

---

## 🏆 Final Ranked List

| Rank | Role | Company | Composite Score | Recruiter Screen | Interview | Degree | Skills | Experience | Pref Penalties | Fit Summary |
|------|------|---------|-----------------|------------------|-----------|--------|--------|------------|----------------|-------------|
| 1 | {{role_1}} | {{company_1}} | {{score_1}} | {{screen_1}} | {{interview_1}} | {{degree_1}} | {{skills_1}} | {{exp_1}} | {{prefs_1}} | {{fit_1}} |
| 2 | {{role_2}} | {{company_2}} | {{score_2}} | {{screen_2}} | {{interview_2}} | {{degree_2}} | {{skills_2}} | {{exp_2}} | {{prefs_2}} | {{fit_2}} |
| 3 | {{role_3}} | {{company_3}} | {{score_3}} | {{screen_3}} | {{interview_3}} | {{degree_3}} | {{skills_3}} | {{exp_3}} | {{prefs_3}} | {{fit_3}} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

> **Note:** Composite Score is computed using the weighted multi-factor scoring model defined in `ranking_rules.md`.

---

## 📊 Score Breakdown Summary

### **Top Strengths Across High-Ranking Roles**
- {{top_strength_1}}
- {{top_strength_2}}
- {{top_strength_3}}

### **Common Weaknesses or Penalties**
- {{weakness_1}}
- {{weakness_2}}
- {{weakness_3}}

---

## 🔍 Insights & Interpretation

### **Why the Top Roles Ranked Highly**
- {{insight_top_1}}
- {{insight_top_2}}

### **Why Lower-Ranked Roles Scored Poorly**
- {{insight_low_1}}
- {{insight_low_2}}

---

## 🎯 Final Recommendations

### **Top Roles to Prioritize**
1. {{priority_role_1}}
2. {{priority_role_2}}
3. {{priority_role_3}}

### **Roles to Avoid**
- {{avoid_role_1}}
- {{avoid_role_2}}

### **Roles Worth Applying If Time Permits**
- {{maybe_role_1}}
- {{maybe_role_2}}

---

## 📝 Notes

- All scores are computed using the canonical scoring model in
  `references/ranking_rules.md`.
- This template defines the required output structure for the ranking skill.
- The ranking skill must not alter column order or required sections.

---

## 💾 CSV Export Format (machine-readable)

The ranking skill will persist a CSV file to: `assets/ranking_results.csv` (overwritten on each invocation).
The CSV MUST contain the following header row (columns, in this order):

Rank,Role,Company,Compensation,Location,YearsRequired,Composite,Recruiter,Interview,DegreeScore,SkillScore,ExperienceScore,PrefPenalties,FitScore,FitCategory,FileName,PostingDate

- Rank: integer (1 = top)
- Role: canonical job title
- Company: employer name
- Compensation: raw compensation string from metadata
- Location: metadata Location(s)
- YearsRequired: metadata years field
- Composite: numeric composite score (0–100)
- Recruiter: recruiter screen likelihood (%)
- Interview: interview likelihood (%)
- DegreeScore: normalized numeric score (0–1)
- SkillScore: normalized numeric score (0–1)
- ExperienceScore: normalized numeric score (0–1)
- PrefPenalties: numeric penalty points applied
- FitScore: normalized numeric score (0–1)
- FitCategory: textual final fit category (e.g., "Strong match")
- FileName: source simulation filename
- PostingDate: posting date from metadata (or "Unknown")

This CSV is the canonical persisted artifact for programmatic consumption. The ranking skill implementation must overwrite `assets/ranking_results.csv` each run and ensure the header and column ordering above are preserved exactly.
