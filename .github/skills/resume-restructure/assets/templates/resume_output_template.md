# Resume Output Template

This template defines the structure of a rewritten, ATS-optimized résumé.

---

## Template Structure

```
# [Candidate Full Name]
[Email] | [Phone] | [Location: City, State]

---

## Skills
[Organized by category, reordered by JD priority]

### [Category 1: e.g., Languages]
- [Primary skill with Direct Match] (confidence: advanced/intermediate/proficient)
- [Secondary skill with Direct/Equivalent Match]
- [Supplementary skill]

### [Category 2: e.g., Tools & Platforms]
- [Tool 1] (Direct Match - required by JD)
- [Tool 2] (Equivalent Match - transferable)

### [Category 3: e.g., Methodologies]
- [Methodology 1]

---

## Professional Experience

### [Company Name] | [Title] | [Dates: Month Year – Month Year]
[1–2 sentence context: company, domain, team context]

- [Bullet 1: Quantified achievement with JD-aligned skill(s)]
- [Bullet 2: Direct Match skill emphasis]
- [Bullet 3: Impact-oriented bullet with metrics]
- [Bullet 4: (Optional) Transferable skill or adjacent experience]

### [Company Name] | [Title] | [Dates]
[Context sentence]

- [Bullets reordered by JD relevance]

---

## Projects
[Only if projects demonstrate JD-aligned skills; omit if none are relevant]

### [Project Name] | [Dates / Status]
[1 sentence: what it is and why it matters]

- Built with: [Technologies matching JD requirements]
- Key achievement: [Outcome demonstrating JD-aligned skill]
- Impact: [Metric or learning]

---

## Education

### Bachelor of Science in [Major] | [Minor (if included)]
[Institution Name] | Graduated: [Month Year]

[Optional: GPA (if 3.5+), relevant coursework, honors, etc.]

---

## [Optional: Additional Sections]
[e.g., Certifications, Publications, Open Source Contributions]
[Only include if relevant to JD]

---

## Formatting Rules (ATS-Friendly)

1. **Single column, no tables, no images**
2. **Simple markdown headings** (# ## ###)
3. **Bullet points** for readability, not sub-bullets
4. **Standard fonts** (avoid decorative elements)
5. **Plain text dates** (Month Year, not "07/10/26" or date ranges)
6. **Contact info** (email, phone; LinkedIn optional)
7. **No headers/footers** (some ATS systems strip them)
8. **Max 1–2 pages** (for mid-level roles)

---

## Content Rules

### Skills Section
- **Reorder by priority**: Required + Direct Match → Required + Equivalent Match → Preferred + Direct Match → Other
- **Normalize terminology** to match JD (e.g., "Apache Spark" if JD uses that; "Spark" if JD is casual)
- **Do NOT add skills** candidate doesn't have
- **Remove noise**: skills irrelevant to JD that clutter the section

### Experience Section
- **Reorder roles** by JD relevance (not chronological)
- **Rewrite bullets** to emphasize Direct Match skills
- **Use action verbs** (Designed, Built, Engineered, Optimized, etc.)
- **Structure**: [Verb] [What] [How/Tool] [Impact/Metric]
  - Example: "Engineered ETL pipelines using Spark SQL, processing 5TB+ daily data with 70% deployment time reduction"
- **Deemphasize non-relevant bullets**: move to end or condense
- **Omit**: skill gaps (things candidate doesn't have)

### Projects Section
- **Filter**: Keep only projects demonstrating JD-aligned skills
- **Rewrite**: Emphasize tools/architecture matching JD
- **Omit**: Projects with no JD overlap (to reduce noise)
- **If no relevant projects**: Omit section entirely

### Education Section
- **Minimal changes**: Keep as-is unless degree fit is "Direct Match"
- **Enhance (optional)**: If degree is strong match, consider adding 1–2 relevant courses or emphasis

### Tone
- **Strong Match (Final Fit = Strong)**: Assertive, confident, ownership-focused
  - Language: "Designed", "Built", "Delivered", "Led"
- **Moderate Match (Final Fit = Moderate)**: Balanced, demonstrating growth
  - Language: "Engineered", "Contributed", "Developed", "Collaborated"
- **Weak Match (Final Fit = Weak)**: Growth-focused, emphasizing learning and initiative
  - Language: "Learned", "Developed", "Explored", "Rapidly adapted"

---

## Example Output

```
# Alex Chen
alex.chen@email.com | (201) 555-1234 | Jersey City, NJ

---

## Skills

### Languages & Frameworks
- Python (advanced, primary language)
- Java (Spring Boot, JUnit)
- SQL

### AI & Data Technologies
- Apache Spark (PySpark, Spark SQL)
- Databricks
- LlamaIndex, Vertex AI, Azure OpenAI
- Snowflake

### Tools & Platforms
- FastAPI, Jenkins, Git
- Pytest, JUnit

---

## Professional Experience

### CapTech Consulting | Data Engineer | July 2025 – Present
Leading data infrastructure projects for a top-5 U.S. financial institution, designing ETL pipelines and ensuring data quality for NPI-sensitive production systems.

- Engineered ETL pipelines using Apache Spark and Snowflake, processing 5TB+ daily with 70% deployment time reduction
- Implemented data validation and NPI compliance filtering, preventing production data breaches while maintaining 99.9% data accuracy
- Debugged multiprocessing pipeline bottlenecks, achieving 55% throughput improvement on core ingestion workflows
- Automated Snowflake DDL generation and attribute filtering, reducing manual overhead by 60% and ensuring governance compliance

### UPS | AI Systems Intern (2024–2025)
Built and evaluated agentic systems for logistics optimization, designing evaluation frameworks to test GenAI outputs for accuracy, safety, and policy compliance.

- Built Agentic Testing Framework (ATF): recursive decision-tree agent system using Google Vertex AI to automatically evaluate GenAI API responses for accuracy, safety, and compliance
- Identified and mitigated problematic LLM behaviors before production deployment by designing bias detection workflows
- Designed scalable evaluation pipeline supporting live customer test cases and adaptive LLM updates
- Achieved 86/86 passing regression tests (Mini Wikipedia RAG) with PySpark, LlamaIndex, and Azure OpenAI; demonstrated rapid learning on new frameworks

---

## Projects

### Agentic Testing Framework (ATF) | 2024–2025
Designed and built a recursive agent system using Google Vertex AI to evaluate GenAI API outputs for accuracy, safety, and compliance in production scenarios.

- Built with: Python, Google Vertex AI (ADK), FastAPI, Pytest (86/86 passing tests)
- Detected problematic LLM behaviors; model tuning improved accuracy by ~20%
- Key achievement: Enabled safe GenAI deployment in enterprise environments

---

## Education

### Bachelor of Science in Computational Modeling & Data Analytics | Minor: Mathematics
Virginia Tech | Graduated: May 2025
```

# Tailored Résumé

## 0. Metadata
- Original Simulation: <simulation filename>
- Target Company: <company name>
- Target Role: <job title>
- Generation Date: <YYYYMMDD_HHMMSS>
- Tailoring Strategy: <brief description of emphasis areas>

---

## Contact
- Name: <name>
- Email: <email>
- Phone: <phone>
- Locations: <locations>
- LinkedIn: <url>
- Citizenship: <citizenship>

---

## Education
<degree and classification, optionally with role-specific context>

---

## Skills

### <Category 1 — JD-Aligned Domain>
<skills prioritized for this JD>

### <Category 2>
<skills>

### <Category N>
<skills>

---

## Work Experience

### **<Company>**  
**<Role>** — <Location>  
**<Dates>**

- <JD-aligned bullet point>
- <JD-aligned bullet point>
- <supporting bullet point>
- <optional additional bullet>

### **<Company>**  
**<Role>** — <Location>  
**<Dates>**

- <bullets rewritten for JD fit>

---

## Projects

### **<Project Name>**  
**<Context/Company> — <Date>**

- <JD-relevant description>
- <technical/architectural detail>
- <outcome or skill demonstrated>

---

## Tailoring Notes

**JD Alignment Summary:**  
<brief explanation of how this résumé emphasizes JD-aligned skills and experiences>

**Key Emphasis Areas:**
- <emphasis 1>
- <emphasis 2>
- <emphasis 3>

**Original Content Preserved:**  
All facts, dates, roles, and accomplishments are grounded in the candidate's original résumé. This version reorganizes and reframes content to maximize alignment with the target JD.
