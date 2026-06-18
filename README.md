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

## Templates & references

Each skill uses template files under `assets/templates/` and canonical rules under `references/` to ensure consistent outputs. Key files:
- Simulation templates: `assets/templates/*.md` inside the simulation skill
- Ranking rules: `.github/skills/ranking/references/ranking_rules.md`
- Simulation outputs stored in: `.github/skills/simulation/simulations/`

## Intended workflow

1. Run the Simulation skill with a raw JD (paste JD text). The skill validates references, parses the JD, applies the contract, and writes a timestamped markdown simulation to the simulations folder.
2. Run the Ranking skill (no inputs). It loads simulations, applies the canonical scoring model, and returns a ranked evaluation table for prioritization.

## Error handling & notes

- Simulation detects and reports missing reference files or parsing failures. If preferences are missing, preference checks are skipped.
- Ranking skips malformed simulation files and treats missing fields as neutral defaults.
- Both skills are deterministic: same inputs + same references → same outputs.

## Incoming feature

- Resume‑rewrite skill (in flight): planned to add a `resume-rewrite` skill that rewrites candidate résumés to target a JD, producing a tailored resume and signals used by downstream simulations. This feature is being developed and will integrate with the Simulation skill once available.
