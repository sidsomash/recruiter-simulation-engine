# Copilot Instructions for This Repository
This repository contains two primary Copilot skills:

1. **Simulation Skill**  
   Generates structured job‑fit simulations from job descriptions.

2. **Ranking Skill**  
   Aggregates and ranks all simulation outputs using the scoring model defined
   in `skills/ranking/references/ranking_rules.md`.

These instructions define how Copilot should behave when interacting with this
repository.

---

## 🧠 Skill Loading Behavior

Copilot must automatically load the following skills when operating inside this
repository:

- `skills/simulation/SKILL.md`
- `skills/ranking/SKILL.md`

No other skills should be auto‑loaded unless explicitly added later.

---

## 📁 File Awareness

Copilot should always be aware of the following reference files:

### Simulation Skill References
- `skills/simulation/references/simulation_contract.md`
- `skills/simulation/assets/templates/simulation_output_template.md`

### Ranking Skill References
- `skills/ranking/references/ranking_rules.md`
- `skills/ranking/assets/templates/ranking_output_template.md`

These files define the canonical rules and templates for each skill.  
Copilot must not duplicate or override their contents.

---

## 🧩 Routing Rules

### **1. Running the Simulation Skill**
Copilot should run the simulation skill **only when explicitly invoked**, such as:

- “Run a simulation for this job description”
- “Simulate this JD”
- “Generate a simulation for this role”

Copilot must **not** auto‑trigger simulations when a job description is pasted.

### **2. Running the Ranking Skill**
Copilot should run the ranking skill when the user explicitly requests:

- “Rank my simulations”
- “Aggregate all simulations”
- “Show me the ranked results”
- “Which roles are the best fit?”

The ranking skill must never run automatically.

---

## 🧱 Output Rules

### Simulation Skill
- Must write outputs to:  
  `skills/simulation/simulations/`
- Must follow the simulation output template exactly.

### Ranking Skill
- Must follow the ranking output template.
- Must not write files; ranking is ephemeral.

---

## 🚫 Prohibited Behavior

Copilot must **not**:

- auto‑route job descriptions to any skill  
- rewrite or modify simulation outputs  
- modify scoring rules  
- modify templates  
- infer intent without explicit user instruction  
- run skills implicitly  

All skill execution must be **explicit**.

---

## 📝 Notes

- Additional skills (e.g., resume‑rewrite) may be added later.  
- This file should be updated when new skills or workflows are introduced.  
- The simulation and ranking skills are the only active skills at this stage.
