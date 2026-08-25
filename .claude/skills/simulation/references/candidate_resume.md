# Candidate Résumé

## Contact
- Name: Siddharth Somashekar
- Email: sidsomash@gmail.com
- Phone: (201) 870-8763
- Locations: NYC, Washington DC
- Citizenship: US Citizen
- LinkedIn: https://www.linkedin.com/in/siddharth-somashekar-8394aa220/

---

## Education
**B.S. in Computational Modeling & Data Analytics (CMDA)**  
Minor: Mathematics  
Virginia Tech — Blacksburg, VA  
Graduation: May 2025

Classification: STEM, quantitative, data‑science‑aligned  
Degree Level: Bachelor’s

---

## Skills

### Languages
Python, Java, R, SQL, C#, C

### Cloud / Platforms
AWS, GCP, Azure, Databricks, Snowflake, Docker

### Frameworks / Tools
Spark, FastAPI, Spring Boot, Supabase, PostgreSQL, MySQL, JUnit, Jira, Linux, Git, Jenkins, Airflow

---

## Work Experience

### **CapTech**  
**Data Engineer** — Reston, VA  
**July 2025 – Present**

- Engineered ETL pipelines for high‑volume S3 datasets using YAML configs, Spark SQL transformations, Airflow DAGs, and Bogie job configs to orchestrate Databricks jobs triggered via Jenkins and Shairflow. Delivered production data into Snowflake warehouses for a top‑5 U.S. financial institution.
- Owned end-to-end migration of mission-critical financial datasets with regulatory compliance requirements (U.S. government fine risk if not delivered on schedule). Validated S3 source locations, configured YAML files with correct schema mappings, executed pre-write validation (Databricks notebooks for schema alignment), orchestrated Spark SQL transformations via Airflow UI, and performed post-write validation in Snowflake. Created ad-hoc pre-write validation when datasets lacked standard metadata, enabling successful ingestion. Delivered results ahead of schedule with weekend execution and zero data quality issues; communicated outcomes to PMs and DAs for end-to-end validation.
- Deployed Snowflake DDL automation for QA and production sinks using a Python‑based Databricks script that filters NPI and credit‑sensitive attributes and generates compliant `.avsc` schemas. Reduced union‑view deployment time by 70% and drove program‑wide adoption.
- Built a Copilot Skill–driven workflow to extract source‑table lineage from complex SQL transformations. Validated Skill performance with deterministic Python/regex scripts and produced reliability metrics used by engineering leads. Integrated into developer tooling to eliminate redundant utilities and reduce manual lineage checks from hours to minutes.

---

### **UPS**  
**Enterprise Data Analytics Intern** — Mahwah, NJ  
**June 2024 – Aug 2024; June 2025 – July 2025**

- Developed an AI tool using Google Agent Builder in Vertex AI Studio for MLOps, enabling retrieval from 1000+ page documents via a Flask app deployed on Google Cloud Run.
- Created the Agentic Testing Framework (ATF) — a recursive decision‑tree agent system using Google ADK to evaluate GenAI API responses for accuracy, safety, and policy compliance. Identified problematic LLM behaviors enabling model tuning before production deployment. Designed to scale across live customer test cases and adapt to LLM updates.

---

### **ExoAnalytic Solutions**  
**Software Developer Intern** — Arlington, VA  
**May 2023 – Aug 2023**

- Developed satellite image anomaly‑detection algorithms using NumPy, Pandas, Pillow, and multiprocessing to support high‑volume preprocessing for GAN training pipelines.
- Improved image‑processing throughput by 55% through parallelization, enabling faster dataset generation for ML experimentation.
- Collaborated with senior engineers and Intelligence Community analysts to validate model outputs and brief DoD teams on findings and operational implications.

---

## Projects

### **Recruiter Simulation Engine**  
**Founder & Architect** — June 2026 – Present

- Architected a multi-agent job‑fit simulation platform with modular skills deployed across GitHub Copilot CLI, Claude, and Gemini environments. Designed deterministic simulation contracts that evaluate job descriptions against candidate profiles using structured reference files and templates.
- Built the **Simulation Skill** — a deterministic evaluation engine that parses JDs, applies recruiter decision logic, produces skill/responsibility/degree mappings, and generates standardized simulation outputs stored for ranking and resume tailoring.
- Engineered the **Resume-Restructure Skill** — an intelligent resume rewriting system that tailors candidate résumés for specific job opportunities by strategically reordering skills by JD relevance, rewriting experience bullets to emphasize recruiter priorities, and preserving factual accuracy while maximizing alignment. Includes comprehensive rewriting guidelines covering principles (honesty, context over content, emphasis/omission) and validation checklists.
- Implemented the **Ranking Skill** — an aggregation engine applying weighted multi-factor scoring models to rank all simulations, enabling data-driven role prioritization.
- Designed the **Initialize Skill** — an onboarding workflow that guides users through building candidate preferences, profiles, and resumes across all three agent platforms with structured templates and interactive prompts.
- Produced deterministic, reproducible outputs enabling same JD + same candidate = identical simulation, ensuring consistency across all skill invocations and agent environments.

---

### **Mini Wikipedia RAG Q&A System**  
**CapTech — March 2026**

- Built a 3‑stage RAG pipeline using HuggingFace Wikipedia passages, LlamaIndex StorageContext, and Azure OpenAI GPT‑4o.
- Delivered 6 FastAPI endpoints for ingestion, retrieval, generation, and workflow execution with observability and Jupyter notebooks for debugging.
- Achieved 86/86 passing pytest tests across unit, API, workflow, and integration layers.

