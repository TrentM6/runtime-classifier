# Documentation Index

The runtime-classifier framework — full docs.

## Read in order

1. [02-THESIS.md](02-THESIS.md) — The core argument: why explicit runtime rules beat fine-tuning for creative style.
2. [03-METHODOLOGY.md](03-METHODOLOGY.md) — How to take a creator from intake to a finished classifier.
3. [04-INTAKE-QUESTIONNAIRE.md](04-INTAKE-QUESTIONNAIRE.md) — The 7-question intake; what each question is for.
4. [05-PORTFOLIO-ANALYSIS.md](05-PORTFOLIO-ANALYSIS.md) — How to analyze ~100 portfolio items into rule patterns.
5. [06-CLASSIFIER-FORMAT.md](06-CLASSIFIER-FORMAT.md) — The `[domain].md` file format — frontmatter, rules, VALIDATION + GENERATION.
6. [07-CLASSIFIER-THEORY.md](07-CLASSIFIER-THEORY.md) — Why this works: the theoretical foundation.
7. [08-USER-WORKFLOW.md](08-USER-WORKFLOW.md) — Step-by-step for someone building their own classifier.
8. [09-EXTENDING-TO-DOMAINS.md](09-EXTENDING-TO-DOMAINS.md) — Cross-domain rule matrix: photography → art, graphic design, writing, music.

## By goal

| You want to… | Read |
|---|---|
| Understand the thesis | `02-THESIS.md` + `07-CLASSIFIER-THEORY.md` |
| Build a classifier for your own domain | `08-USER-WORKFLOW.md` + `templates/` |
| Understand the file format | `06-CLASSIFIER-FORMAT.md` + the example `photography.md` |
| Adapt to a non-photography domain | `09-EXTENDING-TO-DOMAINS.md` + `templates/intake/` |
| Run the worker | top-level `README.md` (Quickstart) |

## The example

The repo ships with a worked example at `photography.md` (root) — a documentary street photography classifier with 8 rules. Treat it as a reference, not as the framework itself: the framework is what's in this folder + `scripts/` + `templates/`.
