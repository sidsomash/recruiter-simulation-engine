# recruiter-simulation-engine

A modular engine that converts job descriptions into structured, recruiter‑grade simulations and ranks those simulations to prioritize hiring opportunities. The repository contains self-contained "skills" (small agents) that encapsulate deterministic workflows, templates, and reference data used by recruiting automations.

## Core skills

- Simulation skill
  - Location: .github/skills/simulation
  - Purpose: Parse a pasted job description, apply the simulation contract (skill & responsibility mapping, experience/degree mapping, preference checks, recruiter decision), render results using canonical templates, and save outputs to `skills/simulation/simulations/<timestamp>_<slug>.md`.
  - Inputs: single `job_description` string. Deterministic given the same candidate references.

- Ranking skill
  - Location: .github/skills/ranking
  - Purpose: Read all simulation outputs, extract structured fields, compute composite scores using `references/ranking_rules.md`, and return an ephemeral ranked table of roles. Does not modify simulations.
  - Inputs: none (auto-discovers simulations directory).

## Setup

Prerequisites
- Install the GitHub Copilot CLI and follow the official docs: https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli

Quick setup (Copilot CLI)
1. Start an interactive Copilot session from the repository root: `copilot`
2. Authenticate: run `/login` inside the Copilot session and follow the prompts.
3. Initialize repository instructions and register skills: run `/init`.
4. Manage and run skills: use `/skills` to list and invoke available skills. Example flows (interactive):
   - Run a simulation: invoke the `simulation` skill and paste the job description.
   - Run ranking: invoke the `ranking` skill (no inputs) to compute ephemeral rankings.

Using Claude or Gemini instead
- To run the same skill workflows with Claude or Gemini, move or duplicate the skills folder into a model-specific location: `.claude/skills/` or `.gemini/skills/`.
- Add model instruction files at the repo root if needed (CLAUDE.md or GEMINI.md). Copilot recognizes these files and model selection via `/model`.
- In a Copilot session, select the model with `/model claude` or `/model gemini`, run `/init` to register, then use `/skills` as above. The skill invocation pattern and templates remain the same.

## Templates, references & configuration

Each skill uses template files under `assets/templates/` and canonical rules under `references/` to ensure consistent outputs. Key files and editable configuration:

- Simulation templates: `.github/skills/simulation/assets/templates/*.md` — edit these to change output formatting (skill, experience, degree mapping templates).
- Simulation references: `.github/skills/simulation/references/` — this folder contains the candidate artifacts and inputs the Simulation skill consumes (e.g., `candidate_resume.md`, `candidate_profile.md`, `candidate_preferences.md`). Editing these files will change how simulations evaluate the candidate.
- Important: `simulation_contract.md` in the same references folder is canonical and SHOULD NOT be modified unless you understand the contract impact; changing it will change simulation semantics.
- Ranking rules: `.github/skills/ranking/references/ranking_rules.md` — defines the canonical scoring model; treat it as authoritative for ranking behavior.
- Simulation outputs stored in: `.github/skills/simulation/simulations/` — generated, timestamped files produced by the Simulation skill.

When customizing, prefer updating templates and the editable reference files rather than altering skill code; run the Simulation skill afterward to validate effects.
## Intended workflow

1. Run the Simulation skill with a raw JD (paste JD text). The skill validates references, parses the JD, applies the contract, and writes a timestamped markdown simulation to the simulations folder.
2. Run the Ranking skill (no inputs). It loads simulations, applies the canonical scoring model, and returns a ranked evaluation table for prioritization.

## Error handling & notes

- Simulation detects and reports missing reference files or parsing failures. If preferences are missing, preference checks are skipped.
- Ranking skips malformed simulation files and treats missing fields as neutral defaults.
- Both skills are deterministic: same inputs + same references → same outputs.

## Incoming feature

- Resume‑rewrite skill (in flight): planned to add a `resume-rewrite` skill that rewrites candidate résumés to target a JD, producing a tailored resume and signals used by downstream simulations. This feature is being developed and will integrate with the Simulation skill once available.
