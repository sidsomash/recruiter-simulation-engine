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

These rules apply **only when the JD's degree domain is not found** in the authoritative JSON
lookup table (`references/degree_domain_map.json`, see §5.3), or when the candidate's degree does
not fall into a category the JSON covers. Always check the JSON lookup first.

**Determining the candidate's degree category:** Do not classify the candidate's degree from its
literal title alone. Cross-reference `candidate_profile.md` (technical strengths, quantitative
coursework, domain experience) and `candidate_preferences.md` (stated preference for data/
technical/quantitative roles) when the degree title is ambiguous or borderline — e.g., a Business
degree paired with heavy data-analytics coursework and a stated preference for data roles may
warrant treating the candidate closer to the `stem_quantitative` category than the title alone
suggests, or vice versa. When skills/preferences change the categorization call, state that
reasoning explicitly in the Degree Requirement Mapping output.

**Rule A — Bachelor’s Required**  
If JD requires a Bachelor’s in STEM, CS, Math, Engineering, Data Science, or related quantitative field:  
→ Candidate’s STEM/quantitative degree = ✔ Direct or Equivalent match

**Rule B — Business/Finance/Accounting Bachelor’s**  
If JD requires a Bachelor’s in Finance, Accounting, Economics, Business:  
→ Candidate’s STEM degree = ~ Partial match  
Unless JD explicitly allows “related quantitative field,” then → ✔ Equivalent match

> **Note:** §5.3's JSON lookup table currently lists Finance/Accounting as ✘ No match (not ~
> Partial as this rule states) for a `stem_quantitative`-category candidate, and takes precedence
> for those domains since they appear in the table. This is a known discrepancy — Rule B still
> governs any Finance/Accounting/Economics/Business variant not present in the JSON lookup, and
> governs candidates whose own degree is itself in Finance/Accounting/Business (a different
> category not covered by the current JSON).

**Rule C — Master’s Required**  
If JD requires a Master’s degree:  
→ Candidate with only a Bachelor’s = ✘ No match  
Unless JD says “Master’s OR equivalent experience,” then evaluate experience.

**Rule D — PhD Required**  
If JD requires a PhD:  
→ Candidate without PhD = ❌ Hard mismatch

**Rule E — Degree Not Specified**  
→ No penalty, no flag.

**Rule F — Non-STEM Candidate, Matching Non-STEM JD Domain**  
If the candidate's own degree category is non-STEM (e.g., `business_finance_accounting`,
`liberal_arts_humanities`, `social_sciences`) and the JD's required domain matches or is closely
related to that category (e.g., a Finance degree candidate applying to a Finance JD; a
Psychology degree candidate applying to a Psychology-adjacent JD):  
→ ✔ Direct or Equivalent match, per the candidate's matched category table in §5.3.

**Rule G — Non-STEM Candidate, Unrelated or STEM JD Domain**  
If the candidate's own degree category is non-STEM and the JD requires a domain unrelated to
that category (including STEM/quantitative domains such as Computer Science, Data Science, or
Engineering):  
→ ✘ No match, unless the candidate's profile/preferences show quantitative coursework or
experience that upgrades the categorization per the categorization guidance above (in which
case, apply the upgraded category's table instead). Do not apply ❌ Hard mismatch here — that
label is reserved for the advanced-degree cases in Rules C/D (§5.1).

### 5.3 Degree Domain Mapping (Generalized)

**Authoritative source:** `references/degree_domain_map.json`. The model must first determine
which candidate degree category applies — `stem_quantitative`, `business_finance_accounting`,
`liberal_arts_humanities`, `social_sciences`, or none of these (see §5.2's categorization
guidance — this considers the candidate's degree title, skills/profile, and preferences, not the
title alone) — then look up the JD's required degree field under that category in the JSON file.
If the category and domain are both found, use the match category from the JSON verbatim. If
either is not found, fall back to Rules A–G in §5.2.

The tables below are human-readable renderings of the JSON's four categories for quick reference
— if they ever disagree with `degree_domain_map.json`, the JSON wins. See the JSON's
`_meta.known_discrepancy` field for a currently tracked inconsistency with Rule B,
`_meta.categorization_guidance` for how skills/preferences factor into category selection, and
`_meta.career_switcher_guidance` for how a degree mismatch interacts with relevant professional
experience (see also §6.3).

**stem_quantitative**

| JD Field | Match |
|---------|--------|
| Computer Science | ✔ Equivalent |
| Data Science | ✔ Direct |
| Applied Math / Statistics | ✔ Direct |
| Engineering | ~ Partial |
| Finance / Accounting | ✘ No match |
| Economics | ~ Partial |
| AI/ML | ✔ Equivalent |
| Business Analytics | ✔ Equivalent |

**business_finance_accounting**

| JD Field | Match |
|---------|--------|
| Finance | ✔ Direct |
| Accounting | ✔ Direct |
| Economics | ✔ Equivalent |
| Business | ✔ Direct |
| Business Analytics | ✔ Equivalent |
| Applied Math / Statistics | ~ Partial |
| Computer Science / Data Science / Engineering / AI-ML | ✘ No match |

**liberal_arts_humanities**

| JD Field | Match |
|---------|--------|
| Communications / Journalism / English | ✔ Direct |
| Education | ✔ Equivalent |
| Marketing / Business | ~ Partial |
| Computer Science / Data Science / Engineering / Finance / Accounting / Applied Math / Statistics / AI-ML | ✘ No match |

**social_sciences**

| JD Field | Match |
|---------|--------|
| Psychology / Social Sciences / Sociology / Political Science | ✔ Direct |
| Public Policy | ✔ Equivalent |
| Data Science / Statistics / Business | ~ Partial |
| Applied Math / Business Analytics / Computer Science / Engineering / Finance / Accounting / AI-ML | ✘ No match |

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

### 6.3 Degree‑vs‑Experience Interaction (Career Switchers)

A degree mismatch (per §5) and years-of-experience alignment (per §6.1/§6.2) are evaluated
**independently** — the degree match label itself does not change based on experience. However,
when a candidate has a non-matching or ✘ No match degree (per §5's lookup or Rules A–G) **and**
substantial hands-on professional or project experience directly relevant to the JD's field
(e.g., a Liberal Arts graduate with 4+ years of professional software engineering experience
applying to a Computer Science-labeled JD), both sections must be read together in §8 Recruiter
Decision:

- State the degree mismatch plainly in §5's output (do not soften or reclassify the match label
  itself).
- Cross-reference the relevant professional experience in §6's output, explicitly noting that it
  is being weighed against the degree gap.
- The Recruiter Decision in §8 must account for both signals together rather than treating the
  degree mismatch in isolation — heavy, directly relevant professional experience can meaningfully
  offset a non-matching degree in the overall recruiter-realistic assessment, but does not erase
  the mismatch from the record.

See `degree_domain_map.json`'s `_meta.career_switcher_guidance` for the same rule stated from the
degree-lookup side.

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

## 8. Recruiter Decision (Deterministic Formula)

Recruiter Screen Likelihood and Interview Likelihood are **computed**, not estimated or picked
from a range. The same inputs must always produce the same percentages. Round only the **final**
percentage in each formula below — do not round intermediate scores, to avoid rounding-order
ambiguity between runs. Use **round-half-up** (e.g., 96.5 rounds to 97, not 96) — this is the
standard arithmetic rounding convention, not "round half to even"/banker's rounding, which some
tools default to and would otherwise produce a different, non-matching result.

### 8.1 Scoring Inputs (from earlier sections — do not re-derive)

**Skill Score (0–100):** Using only the **Required Skills** table from §4 (skill mapping) — do
not include Preferred Skills in this formula; preferred skills inform the Recruiter Takeaway
narrative only.

```
Skill Score = 100 × (Direct + Equivalent + 0.5 × Partial) / total_required_skills
```

If there are zero required skills listed in the JD, Skill Score = 100.

**Degree Score (0–100):** From the §5 Degree Requirement Mapping match label.

| Degree Match Label (§5.1) | Degree Score |
|---|---|
| ✔ Direct match | 100 |
| ✔ Equivalent match | 100 |
| ~ Partial match | 60 |
| ✘ No match | 25 |
| ❌ Hard mismatch | 0 (also triggers the §8.4 override) |
| Not specified (Rule E) | 100 |

**Experience Score (0–100):** From the §6 Years-of-Experience Mapping match label.

| Experience Match Label (§6.2) | Experience Score |
|---|---|
| ✔ Meets requirement | 100 |
| ~ Partially meets requirement | 55 |
| ✘ Does not meet requirement | 15 |

**Preference Penalty (points subtracted, only if a preferences file was provided — §7):**

| Violation Severity | Penalty |
|---|---|
| Minor (e.g., location) | −5 |
| Moderate (e.g., compensation, domain mismatch) | −10 |
| Major (e.g., on-site/remote mismatch candidate strongly opposes) | −15 |
| Defense/clearance (candidate opts out) | −20 |

Sum the penalty for every applicable violation. If no preferences file was provided, Preference
Penalty = 0.

### 8.2 Recruiter Screen Likelihood Formula

```
Recruiter% = round(0.40 × Skill Score + 0.35 × Degree Score + 0.25 × Experience Score) − Preference Penalty
```

Clamp the result to the range [0, 100].

### 8.3 Interview Likelihood Formula

```
Interview% = round(0.35 × Skill Score + 0.40 × Degree Score + 0.25 × Experience Score) − Preference Penalty
```

Clamp the result to [0, 100], then clamp `Interview% ≤ Recruiter%` — a candidate cannot have a
higher interview probability than recruiter-screen probability, since the interview stage is
conditional on passing the screen.

### 8.4 Hard Reject Override

If the §5 Degree Requirement Mapping label is ❌ **Hard mismatch**:
→ Override both formulas: `Recruiter% = 2`, `Interview% = 1` (fixed, deterministic values — do
not compute via §8.2/§8.3 in this case).

### 8.5 Band Labels (derived from the computed percentage)

The percentage is computed first; the band label is looked up from the percentage, never chosen
independently. Ranges are non-overlapping.

**Recruiter Screen Likelihood band:**

| Range | Band |
|---|---|
| 80–100% | Very High |
| 65–79% | High |
| 45–64% | Moderate |
| 20–44% | Low |
| 5–19% | Very Low |
| 0–4% | Hard Reject |

**Interview Likelihood band:**

| Range | Band |
|---|---|
| 60–100% | High |
| 40–59% | Moderate |
| 20–39% | Low |
| 5–19% | Very Low |
| 0–4% | Hard Reject |

### 8.6 Decision Rules (Narrative Reference)

These restate §8.1's scoring inputs in plain language for the Decision Rationale bullets in the
output — they are descriptive of the formula above, not a separate/independent penalty system:
- Missing required degree (No match/Hard mismatch) → reflected via a low/zero Degree Score
- Missing required years of experience (Does not meet) → reflected via a low Experience Score
- Missing required skills (many No Match rows) → reflected via a low Skill Score
- Preference violations → reflected via the Preference Penalty (only if preferences provided)
- Defense/clearance requirement → penalized only if candidate preferences indicate avoidance
  (via the Preference Penalty table)

### 8.7 Worked Examples

**Example A — Strong match, no preferences file:**
- Required skills: 5 total → Direct=3, Equivalent=1, Partial=1, No Match=0
  → Skill Score = 100 × (3 + 1 + 0.5×1) / 5 = 100 × 4.5 / 5 = 90
- Degree: Equivalent match → Degree Score = 100
- Experience: Meets requirement → Experience Score = 100
- No preferences file → Preference Penalty = 0
- Recruiter% = round(0.40×90 + 0.35×100 + 0.25×100) − 0 = round(96) = **96%** → Very High
- Interview% = round(0.35×90 + 0.40×100 + 0.25×100) − 0 = round(96.5) = 97, clamped to ≤96 →
  **96%** → High

**Example B — Moderate match, one moderate preference violation:**
- Required skills: 4 total → Direct=1, Equivalent=1, Partial=1, No Match=1
  → Skill Score = 100 × (1 + 1 + 0.5×1) / 4 = 100 × 2.5 / 4 = 62.5
- Degree: Partial match → Degree Score = 60
- Experience: Partially meets requirement → Experience Score = 55
- Preferences: 1 moderate violation → Preference Penalty = −10
- Recruiter% = round(0.40×62.5 + 0.35×60 + 0.25×55) − 10 = round(59.75) − 10 = 60 − 10 = **50%** →
  Moderate
- Interview% = round(0.35×62.5 + 0.40×60 + 0.25×55) − 10 = round(59.625) − 10 = 60 − 10 = 50,
  clamped to ≤50 → **50%** → Moderate

**Example C — Hard reject (PhD required, candidate has no PhD):**
- Degree: Hard mismatch (§5.2 Rule D) → §8.4 override applies
- Recruiter% = **2%** → Hard Reject
- Interview% = **1%** → Hard Reject
- (Skill/Experience scores are not computed in this case — the override is unconditional.)

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

---

## 11. JSON Sidecar (Required Companion Output)

Every simulation must produce a `.json` sidecar file alongside the Markdown output (same base
filename, see `simulation/SKILL.md` Steps 4h–5). The Markdown file remains the canonical
**human-readable** record. The JSON sidecar is the canonical **machine-readable** record that the
ranking skill consumes directly (see `ranking_rules.md`), instead of parsing prose strings out of
the Markdown via regex. The sidecar is a required companion, not a replacement for the Markdown
output — both files must always be written together.

**Schema** (see `assets/templates/simulation_output_sidecar_template.json` for the literal
template file):

| Field | Type | Source | Allowed values |
|---|---|---|---|
| `company` | string | §0 Metadata | free text or `"Unknown"` |
| `title` | string | §0 Metadata | free text |
| `posting_date` | string | §0 Metadata | `YYYY-MM-DD` or `"Unknown"` |
| `compensation` | string | §0 Metadata | free text or `"Unknown"` |
| `location` | string | §0 Metadata | free text |
| `years_required` | string | §0 Metadata | free text (e.g. `"3+"`, `"entry-level"`) |
| `degree_match` | string (enum) | §5.1 Degree Match Label | `direct`, `equivalent`, `partial`, `no_match`, `hard_mismatch`, `not_specified` |
| `skill_alignment` | string (enum) | §4.1-derived alignment tier (mirrors `ranking_rules.md` §3.4) | `high`, `moderate`, `low`, `major_gaps` |
| `experience_match` | string (enum) | §6.2 Experience Match Label | `meets`, `partially_meets`, `does_not_meet` |
| `preference_violations` | array of objects | §7 Preference Violations | each `{severity, description}`; `severity` ∈ `minor`, `moderate`, `major`, `clearance`; empty array if none |
| `recruiter_pct` | integer | §8.2 (or §8.4 override) | 0–100, must equal the Markdown's `**Recruiter Screen Likelihood:**` value exactly |
| `interview_pct` | integer | §8.3 (or §8.4 override) | 0–100, must equal the Markdown's `**Interview Likelihood:**` value exactly |
| `fit_category` | string (enum) | §10 Final Fit Summary | `strong_match`, `moderate_match`, `weak_match`, `mismatch`, `hard_reject` |
| `internship_mode` | boolean | §9 / §0 Metadata `Internship Mode` | `true` / `false` |
| `contract_version` | string | this contract's own header | must equal the Markdown Metadata's `Contract Version` exactly |

**Consistency rule:** every field's value must agree exactly with its corresponding Markdown
section — the sidecar is a structured re-encoding of the same computed values, never an
independent re-derivation. If the two ever disagree, that is a bug in output generation, not an
acceptable discrepancy.

**`skill_alignment` derivation:** since §8.1's Skill Score is a continuous 0–100 number (not an
enum), derive the enum for this field only using the same thresholds `run_ranking.py` already
uses for its independent skill-alignment heuristic (documented in `ranking_rules.md` §3.4): `high`
if Skill Score reflects mostly Direct/Equivalent matches with no gaps, `major_gaps` if two or more
required skills are No Match (or the candidate has no Direct/Equivalent/Partial matches at all),
`moderate` or `low` otherwise based on the proportion of strong matches. This keeps the sidecar's
categorical field consistent with the ranking skill's existing categorical scoring, independent of
the continuous Skill Score used only inside the §8 formula.