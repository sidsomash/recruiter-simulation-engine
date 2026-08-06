# Resume Rewriting Guidelines v1.0

This document defines the strategy and rules for rewriting a candidate's résumé to target a specific job description. The goal is to emphasize relevant experience while preserving factual accuracy.

---

## 1. Core Principles

### 1.1 Honesty First
- **Never fabricate** skills, roles, or accomplishments.
- **Never exaggerate** metrics or timelines.
- **Always ground** claims in the original résumé.
- **Reframe, don't reinvent:** Present existing content in JD-relevant language.

### 1.2 Context Over Content
- Same skill/accomplishment → described differently for different recruiters.
- Example: "Optimized Spark SQL queries" (for data engineer) vs. "Reduced query latency by 40%" (for performance engineer).
- Use JD terminology and domain language naturally.

### 1.3 Emphasis and Omission
- **Prioritize:** Lead with JD-relevant accomplishments.
- **Reorder:** Rearrange bullet points to emphasize recruiter priorities.
- **Minimize:** De-emphasize or softly exclude accomplishments with weak relevance (but never delete facts).
- **Group:** Organize skills and experiences by domain/function.

### 1.4 Consistency
- Keep names, dates, and core facts unchanged.
- Maintain the structure and flow of the original résumé.
- Use consistent terminology and tone.

---

## 2. Section-by-Section Rewriting Strategy

### 2.1 Contact & Header
**Rewrite Level:** Minimal

- Keep name, email, phone, locations unchanged.
- Keep LinkedIn URL and citizenship status unchanged.
- Do NOT modify or add false information.

**Example:** No changes needed.

---

### 2.2 Education
**Rewrite Level:** Minimal

- Keep degree name, major, minor, university, and graduation date unchanged.
- Keep classification (STEM, quantitative, etc.) unchanged.
- Optionally highlight relevant coursework or classifications if they strengthen JD alignment.

**Example Original:**
```
B.S. in Computational Modeling & Data Analytics (CMDA)
Minor: Mathematics
Virginia Tech — Blacksburg, VA
Graduation: May 2025
Classification: STEM, quantitative, data‑science‑aligned
```

**Example Tailored (for Data Engineering role):**
```
B.S. in Computational Modeling & Data Analytics (CMDA)
Minor: Mathematics
Virginia Tech — Blacksburg, VA
Graduation: May 2025

Classification: STEM, quantitative, data-science-aligned. Strong foundation in 
applied mathematics, statistical modeling, and computational methods directly 
applicable to data engineering and pipeline architecture.
```

**Rewriting Rules:**
- Add 1–2 sentences explaining how the degree aligns with the JD if it significantly strengthens the candidate's profile.
- Never modify degree name or dates.
- Keep all original information intact.

---

### 2.3 Skills
**Rewrite Level:** Aggressive

#### 2.3.1 Reordering
- **Priority 1:** Required skills from JD (e.g., SQL, Python, Databricks).
- **Priority 2:** Preferred skills from JD (e.g., PySpark, Azure).
- **Priority 3:** Complementary skills that reinforce domain depth (e.g., testing frameworks, CI/CD).
- **Priority 4:** Adjacent skills with lower relevance.

#### 2.3.2 Grouping
Organize skills by functional domain:

**Original (Flat List):**
```
### Languages
Python, Java, R, SQL, C#, C

### Cloud / Platforms
AWS, GCP, Azure, Databricks, Snowflake, Docker
```

**Tailored (Data Engineering Role):**
```
### Core Data Engineering
Python, SQL, Databricks, Apache Spark, PySpark

### Cloud Platforms
AWS (S3, Airflow), GCP (Vertex AI), Azure (OpenAI services)

### Data Warehousing & Storage
Snowflake, PostgreSQL, MySQL, Supabase

### Backend & DevOps
FastAPI, Docker, Jenkins, Linux, Git
```

#### 2.3.3 Emphasis
- **List JD-required skills first** in each category.
- **Add brief context** if a skill deserves emphasis (e.g., production vs. coursework).
- **Remove or minimize** skills with zero relevance to the JD (but never delete them if the candidate actually has them).

**Example:**
```
### Languages
**Python** (advanced; production ETL scripts, data pipelines, ML frameworks)
**SQL** (advanced; Spark SQL, Snowflake DDL, complex transformations)
Java, R, C#, C (supporting languages)
```

---

### 2.4 Work Experience
**Rewrite Level:** Strategic

#### 2.4.1 Role Selection
- **Keep all roles** from the original résumé (do not omit jobs).
- **Reorder** roles if a less-recent role is more relevant to the JD.
- **Emphasize** roles that best demonstrate JD competencies.

#### 2.4.2 Bullet Point Rewriting

**Rule 1: Lead with JD Relevance**
- First 2–3 bullet points should directly address JD responsibilities.
- Use JD terminology and domain language.

**Original Bullet:**
```
Engineered ETL pipelines for high‑volume S3 datasets using YAML configs, 
Spark SQL transformations, Airflow DAGs, and Bogie job configs to orchestrate 
Databricks jobs triggered via Jenkins and Shairflow.
```

**Tailored (for Data Engineer role emphasizing pipeline architecture):**
```
Engineered production ETL pipelines for high-volume S3 datasets using Databricks 
Spark SQL transformations and Airflow DAGs, orchestrating enterprise-scale data 
ingestion and transformations aligned with medallion architecture patterns.
```

**Rule 2: Emphasize Metrics and Outcomes**
- If the original bullet includes metrics (% improvement, # of records), emphasize them.
- Add metrics if they strengthen relevance (grounded in original résumé).
- Use domain-relevant metrics (e.g., "query optimization," "schema design," "SLA uptime").

**Original Bullet:**
```
Deployed Snowflake DDL automation for QA and production sinks using a Python‑based 
Databricks script that filters NPI and credit‑sensitive attributes and generates 
compliant `.avsc` schemas. Reduced union‑view deployment time by 70% and drove 
program‑wide adoption.
```

**Tailored (for Data Engineering role):**
```
Deployed Snowflake DDL automation and schema generation at scale, filtering 
sensitive data attributes and ensuring compliance. Reduced deployment time by 70% 
and enabled team-wide adoption of standardized schema practices.
```

**Rule 3: Adapt Language to JD Domain**
- Use keywords from the JD naturally (e.g., "medallion architecture," "Bronze/Silver/Gold").
- Translate technical accomplishments into recruiter-relevant language.
- Maintain honesty but frame differently.

**Example:**
- JD focuses on "data product ownership" → frame experience as "owning data pipeline quality and schema integrity."
- JD emphasizes "scalability" → highlight "processed X records/sec," "optimized for 10x data growth."

**Rule 4: Reorder Bullet Points**
- Move JD-aligned bullet points to the top.
- Deprioritize accomplishments with weak relevance (but keep them).

**Original Order (generic role):**
1. Built a Copilot Skill–driven workflow…
2. Engineered ETL pipelines…
3. Deployed Snowflake DDL automation…

**Tailored Order (Data Engineering role):**
1. Engineered ETL pipelines… (directly addresses JD responsibility)
2. Deployed Snowflake DDL automation… (schema expertise)
3. Built a Copilot Skill–driven workflow… (auxiliary project)

---

### 2.5 Projects
**Rewrite Level:** Selective

#### 2.5.1 Project Selection
- **Prioritize** projects most relevant to the JD domain.
- **Rewrite descriptions** to emphasize technical alignment.
- **Optionally de-emphasize** projects with weak relevance (but keep all original facts).

**Rule 1: Reorder Projects**
- List most JD-relevant projects first.

**Rule 2: Rewrite Project Descriptions**
- Lead with the technical problem and domain relevance.
- Emphasize tools/technologies used that match the JD.

**Original Project Description:**
```
### **Mini Wikipedia RAG Q&A System**  
**CapTech — March 2026**

- Built a 3‑stage RAG pipeline using HuggingFace Wikipedia passages, LlamaIndex 
StorageContext, and Azure OpenAI GPT‑4o.
- Delivered 6 FastAPI endpoints for ingestion, retrieval, generation, and workflow 
execution with observability and Jupyter notebooks for debugging.
- Achieved 86/86 passing pytest tests across unit, API, workflow, and integration 
layers.
```

**Tailored (for Data Engineering role):**
```
### **Mini Wikipedia RAG Q&A System**  
**CapTech — March 2026**

- Architected a production-grade data pipeline combining retrieval-augmented 
generation (RAG) with FastAPI backend services and comprehensive testing coverage.
- Designed efficient data ingestion and workflow orchestration, achieving 86/86 
passing tests across unit, API, and integration test layers.
- Developed schema and data flow design for scaling retrieval and generation 
operations.
```

---

## 3. Recruiter Perspective: What to Emphasize

### 3.1 Common JD Priorities

| Priority | What Recruiters Look For | How to Highlight |
|----------|-------------------------|-----------------|
| **Technical Skills Match** | Core tools (Python, SQL, Databricks) | Lead bullets; list first in skills |
| **Hands-On Experience** | Production systems, real data, scale | Use specific examples; cite metrics |
| **Ownership & Initiative** | Led design, built from scratch | Active verbs ("Engineered," "Designed," "Architected") |
| **Domain Depth** | Industry-specific knowledge | Use JD terminology; mention domain experience |
| **Scalability & Performance** | Large datasets, optimization, SLAs | Emphasize metrics ("10x data growth," "70% reduction") |
| **Collaboration** | Cross-team work, communication | Mention working with senior engineers, teams |
| **Learning Agility** | Mastered new tools quickly | Cite rapid adoption (e.g., "Quickly mastered Databricks") |

### 3.2 Red Flags to Avoid

- **Vague language:** "Helped with data tasks" → "Engineered ETL pipelines for S3 datasets"
- **Buzzwords without substance:** "Big data expert" → "Processed 10M records/day at CapTech"
- **Irrelevant projects:** Bury low-relevance projects; don't lead with them
- **Missing metrics:** "Optimized queries" → "Optimized queries by 40%, reducing latency from 8s to 5s"
- **Passive voice:** "Pipelines were developed" → "Engineered and deployed production pipelines"

---

## 4. Rewrite Checklist

Before finalizing a tailored résumé, verify:

- [ ] All facts are grounded in the original résumé (no fabrication)
- [ ] Emphasis matches JD priorities (from simulation analysis)
- [ ] JD terminology is used naturally (not forced)
- [ ] Metrics and accomplishments are preserved
- [ ] Skill section leads with JD-required skills
- [ ] Work experience bullets are reordered to emphasize JD alignment
- [ ] Projects are prioritized by JD relevance
- [ ] Names, dates, and core facts are unchanged
- [ ] Structure follows the resume output template
- [ ] Tone is consistent with original résumé

---

## 5. Example: Full Role Rewrite

### Original Resume (Generic)

**Skills (Original):**
```
### Languages
Python, Java, R, SQL, C#, C

### Cloud / Platforms
AWS, GCP, Azure, Databricks, Snowflake, Docker
```

**Work Experience Bullet (Original):**
```
Engineered ETL pipelines for high‑volume S3 datasets using YAML configs, 
Spark SQL transformations, Airflow DAGs, and Bogie job configs to orchestrate 
Databricks jobs triggered via Jenkins.
```

### Tailored Resume (for Data Engineer @ Mizuho)

**Skills (Tailored):**
```
### Data Engineering & Pipelines
Python (advanced), SQL (advanced), Databricks, Apache Spark, Airflow

### Cloud Platforms & Data Storage
AWS (S3, Airflow), Azure, Snowflake (production DDL, schema design)

### Backend & DevOps
FastAPI, Docker, Jenkins, Git, Linux
```

**Work Experience Bullet (Tailored):**
```
Engineered production ETL pipelines for enterprise-scale S3 datasets using 
Databricks Spark SQL transformations and Airflow DAG orchestration, delivering 
high-volume data ingestion aligned with medallion architecture patterns and 
Snowflake sink optimization.
```

### Analysis

- **Skills:** Reordered to lead with "Data Engineering," then "Cloud Platforms," deprioritizing "Backend."
- **Bullet:** Reframed to emphasize enterprise-scale delivery, medallion patterns (aligned with Mizuho JD), and Snowflake (which candidate has experience with).
- **Facts:** Unchanged; all original technologies and accomplishments preserved.
- **Language:** Uses JD terminology ("medallion architecture," "enterprise-scale," "sink optimization").

---

## 6. Notes

- Rewriting is an art + science: there is no single "correct" tailored résumé for every JD.
- Different recruiters prioritize different things; tailor accordingly.
- Multiple tailored résumés for different roles is encouraged (portfolio approach).
- The simulation output provides the "rewrite directive"—use it as a guide for emphasis.

