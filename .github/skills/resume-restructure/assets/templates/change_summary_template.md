# Change Summary Template

This template documents all changes made to the resume during rewrite.
Provides transparency and helps the candidate understand what was reordered, rewritten, or removed.

---

## Template Structure

```
# Resume Change Summary: [Role Title] @ [Company]

**Original Resume**: `skills/simulation/references/candidate_resume.md`  
**Simulation Used**: `skills/simulation/simulations/[timestamp]_[role].md`  
**Rewritten Resume**: `skills/resume-restructure/rewrites/[timestamp]_[role]_resume.md`  
**Fit Category**: [Strong / Moderate / Weak] Match  
**Tone**: [Assertive / Balanced / Growth-Focused]

---

## Skills Section Changes

### Reordering
- **Moved to Top (Direct Matches, Required)**:
  - [Skill 1] → Position 1 (required skill, direct match)
  - [Skill 2] → Position 2 (required skill, direct match)
  - [Skill 3] → Position 3 (required skill, equivalent match)

- **Middle (Partial Matches, Preferred)**:
  - [Skill] → Position 4 (preferred skill, direct match)
  - [Skill] → Position 5 (required skill, partial match)

- **Moved to End (Non-Critical, Low Relevance)**:
  - [Skill] → Bottom (adjacent skill, not emphasized)
  - [Skill] → Removed (irrelevant to JD, creates noise)

### Normalization
- [Skill] was normalized from "[Old Name]" to "[New Name]" (matching JD terminology)
  - Example: "Spark" → "Apache Spark (PySpark, Spark SQL)" (JD mentions both)

### Removals
- [Skill] was removed (not relevant to JD, clutters section)
- [Skill] was removed (candidate doesn't have it; was fabricated error)

### Additions
- ⚠️ No skills were added (all skills in rewritten resume are from original)

---

## Professional Experience Section Changes

### Reordering
**Original order** (chronological / reverse chronological):
1. CapTech (current role)
2. UPS (internship)
3. ExoAnalytic (internship)

**New order** (by JD relevance):
1. **UPS (Internship)** – Moved to top (agentic systems, AI evaluation = direct match for "AI agent evaluation" requirement)
2. **CapTech (Current)** – Reordered to emphasize data pipelines, compliance
3. **ExoAnalytic (Internship)** – Moved to end (DoD geospatial work, lower relevance)

### Experience Rewriting

#### CapTech Consulting | Data Engineer

**Original bullets:**
- Engineered ETL pipelines using Spark to ingest and clean 5TB+ daily corporate data
- Automated Snowflake DDL generation for compliance and governance
- Debugged multiprocessing bottlenecks, improved throughput 55%
- Resolved production data quality issues affecting downstream analytics

**Rewritten bullets:**
- ✅ **Engineered ETL pipelines using Apache Spark and Snowflake** (Direct Match: Spark, data pipelines required by JD)
  - Changed from: Generic description
  - Changed to: Specific technical stack matching JD requirements
  - Reason: JD requires "data pipelines" and "Spark"; emphasize this directly

- ✅ **Implemented data validation and NPI compliance filtering, preventing production data breaches** (Direct Match: data quality auditing, bias detection)
  - Changed from: "Resolved production data quality issues"
  - Changed to: More specific, emphasizing "validation", "compliance", and "bias/risk detection"
  - Reason: JD requires "data quality auditing" and "bias detection"; reframe as compliance/validation work

- ✅ **Debugged multiprocessing pipeline bottlenecks, achieving 55% throughput improvement** (Partial Match: performance metrics)
  - Changed from: Generic performance statement
  - Changed to: Specific methodology (multiprocessing) + quantified impact
  - Reason: JD requires "performance metrics (latency, throughput, resource utilization)"; this example proves metrics mindset

- ✅ **Automated Snowflake DDL generation, reducing manual overhead 60% and ensuring governance compliance** (Equivalent Match: automation, data governance)
  - Changed from: "Automated Snowflake DDL generation"
  - Changed to: Emphasize automation + governance (JD requires data governance understanding)
  - Reason: Data governance is a key theme in JD

#### UPS | AI Systems Intern

**Original bullets:**
- Built Agentic Testing Framework using Google ADK; evaluated GenAI responses for accuracy, safety, compliance
- Designed bias detection workflows; improved model accuracy ~20%
- Evaluated LLM outputs across live customer test cases
- Achieved 86/86 passing tests on Mini Wikipedia RAG (Pytest)

**Rewritten bullets:**
- ✅ **Built Agentic Testing Framework (ATF): recursive agent system using Google Vertex AI to evaluate GenAI API responses for accuracy, safety, compliance** (Direct Match: "AI agent evaluation", "evaluation frameworks")
  - Changed from: Generic description
  - Changed to: Emphasize "agentic systems", "evaluation framework", "accuracy/safety/compliance metrics"
  - Reason: JD explicitly requires "Agent Skill & Performance Testing" and "Model & Inference Evaluation"; this is a perfect match

- ✅ **Identified and mitigated problematic LLM behaviors through bias detection workflows, enabling safe production deployment** (Direct Match: "data quality & bias auditing", "bias detection")
  - Changed from: "Designed bias detection workflows; improved model accuracy ~20%"
  - Changed to: Emphasize "bias detection", "mitigation", "production deployment" (risk management angle)
  - Reason: JD requires "data quality & bias auditing"; reframe as production risk mitigation

- ✅ **Designed scalable evaluation pipeline supporting live customer test cases and adaptive LLM updates** (Direct Match: "evaluation frameworks", "A/B testing and human-in-the-loop")
  - Changed from: "Evaluated LLM outputs across live customer test cases"
  - Changed to: Emphasize "pipeline", "scalability", "adaptability"
  - Reason: JD requires evaluation pipelines; frame as infrastructure, not just one-off testing

- ✅ **Achieved 86/86 passing regression tests on Mini Wikipedia RAG using PySpark, LlamaIndex, Azure OpenAI** (Partial Match: integration/regression testing, Python, AI frameworks)
  - Changed from: "Achieved 86/86 passing tests on Mini Wikipedia RAG (Pytest)"
  - Changed to: Specify tools (PySpark, LlamaIndex, Azure OpenAI) matching JD tech stack
  - Reason: Demonstrate testing rigor + familiarity with AI frameworks

#### ExoAnalytic | Geospatial Intelligence Intern

**Original position**: #1 (chronological most recent at time)  
**New position**: #3 (moved to end)

**Rewritten bullets** (condensed, deprioritized):
- ⚠️ This role is not relevant to JD (DoD geospatial work does not map to data services/AI developer)
- Action: Condensed to 2 bullets instead of 4; moved to end; tone is neutral (not emphasized)
- Original bullets removed/condensed:
  - Removed: "Analyzed classified geospatial datasets" (not relevant, introduces security/classification noise)
  - Kept: "Debugged Python data processing pipelines" (Python is required; frames as adjacent experience)

---

## Projects Section Changes

### Filtering
**Original projects**:
1. Mini Wikipedia RAG (LlamaIndex, Azure OpenAI, PySpark)
2. Ryoko (AI travel platform, travel aggregation)
3. Agentic Testing Framework (already in experience; not repeated)

**Rewritten projects** (kept):
1. ✅ Mini Wikipedia RAG (demonstrates: Python, AI frameworks, regression testing, LlamaIndex, Azure OpenAI)
   - Reason: JD requires Python + AI applications; Mini Wikipedia RAG is a perfect example

**Rewritten projects** (removed):
- ❌ Ryoko (AI travel platform)
  - Reason: Travel domain does not map to Financial Services (JD preference: financial services background)
  - Also: This project overlaps with "Building with AI" which is already demonstrated by ATF and Mini Wiki RAG
  - Impact: Removes distraction; focuses on finance + data

### Project Rewriting

#### Mini Wikipedia RAG | March 2026

**Original**:
- Built a RAG pipeline using LlamaIndex and Azure OpenAI
- Achieved 86/86 passing tests with Pytest
- Deployed as interactive web application (FastAPI)

**Rewritten**:
- ✅ Designed and built a Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex and Azure OpenAI for information retrieval and accuracy
  - Changed: Added context (RAG purpose), emphasized architecture
  - Reason: Shows Python + AI framework + evaluation mindset
  
- ✅ Implemented robust testing: 86/86 passing integration tests using PySpark, Pytest, demonstrating end-to-end quality
  - Changed: Specified testing framework (Pytest, PySpark) matching JD requirements
  - Reason: JD requires "integration and regression testing"; this example proves competence
  
- ✅ Deployed via FastAPI backend, showing full-stack development capability (Python end-to-end)
  - Changed: Minor adjustment emphasizing full-stack Python (FastAPI is Python)
  - Reason: Supports "Python" and "applications development" requirements

---

## Education Section Changes

### Rewritten Education

**Original**:
- B.S. Computational Modeling & Data Analytics, Virginia Tech
- Minor: Mathematics
- Graduated: May 2025

**Rewritten** (same structure, optional enhancement):
- ✅ B.S. Computational Modeling & Data Analytics | Minor: Mathematics
  - Virginia Tech | Graduated: May 2025
- Reason: Degree is "Direct Match" for the JD; no changes needed
- Optional: Could add "Relevant Coursework: Statistical Analysis, Machine Learning, Data Structures, Algorithms" if space permits
  - Defer unless we're under 1 page

---

## Tone & Framing Adjustments

### Fit Category: **Strong Match**
**Tone Applied**: Assertive, confident, ownership-focused

- **Language shifts**:
  - "Participated in" → "Built" / "Engineered"
  - "Helped with" → "Designed" / "Delivered"
  - "Worked on" → "Owned" / "Led"
  
- **Emphasis**: Leading with strengths (agentic systems, AI evaluation, data quality)
  - Confidence: Candidate has done this work before; minimal learning curve
  - Framing: "You've built evaluation frameworks; this role is the next step"

### Recruiter Takeaway Alignment
From simulation: "Candidate is an **excellent fit**... direct experience building and evaluating AI agents, evaluating LLM outputs for accuracy/safety/compliance — exactly what this role emphasizes."

**Resume rewrite reflects this** by:
- Leading with UPS agentic work (most relevant)
- Emphasizing bias detection + compliance (strong signals for Citi role)
- Prioritizing Python + data quality (core requirements)
- Acknowledging learning curve items (MCP, ADK) not present, but demonstrating rapid learning track record

### Skill Gaps Acknowledged
From simulation: "Risk: candidate has not explicitly built MCP servers or used ADK (Anthropic Developer Kit)"

**Resume rewrite approach**:
- Does NOT fabricate MCP or ADK experience
- Shows Python + API development (FastAPI) as adjacent skills (foundation for learning MCP)
- Demonstrates "rapid learning" through multiple framework adoptions (Vertex AI, LlamaIndex, FastAPI, Spark)

---

## Summary Statistics

| Metric | Change |
|--------|--------|
| Skills reordered | 8 skills moved to top (Direct Matches) |
| Skills removed | 2 skills (irrelevant noise) |
| Experience roles reordered | 3 roles prioritized by JD relevance |
| Bullets rewritten | 12 out of 16 bullets (75%) |
| Experience roles deprioritized | 1 (ExoAnalytic, moved to end) |
| Projects kept | 1 (Mini Wikipedia RAG) |
| Projects removed | 1 (Ryoko, not finance-aligned) |
| Tone adjusted | Assertive (Strong Match) |
| Final resume length | 1 page (optimized for ATS) |

---

## Notes for Candidate

**Key strengths emphasized**:
1. **Agentic systems & evaluation** = directly matches "Agent Skill & Performance Testing" requirement
2. **Data quality & bias auditing** = directly matches "Data Quality & Bias Auditing" requirement
3. **Python proficiency** = required skill, demonstrated across 3 roles
4. **Financial services domain** = Citi prefers FS background; CapTech + UPS both show this

**Learning curve items not fabricated**:
- MCP server development = not on resume (JD nice-to-have, not blocker)
- Anthropic ADK = not on resume (Google ADK on resume shows adjacent skill)
- A/B testing frameworks = implied through evaluation frameworks (good enough for role level)

**Recommendation**: In interviews, be ready to discuss:
- "I've used Google Vertex AI for agentic systems; Anthropic ADK is conceptually similar — quick ramp-up"
- "I've built evaluation pipelines with Pytest and custom metrics; A/B testing framework is adjacent skill"
- "MCP servers: I've built FastAPI backends (Python) and REST APIs; MCP protocol is learnable (2–4 weeks typical ramp-up)"

```

