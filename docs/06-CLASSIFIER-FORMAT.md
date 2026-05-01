# Classifier File Format

The `[domain].md` file is the canonical single source of truth for a classifier. It contains:

- A YAML frontmatter block (machine-readable: rules + weights + defaults)
- A human-readable body explaining each rule with VALIDATION + GENERATION

The included worker (`scripts/photography_agent.py`) reads this file at runtime — no rules or weights are duplicated in code.

---

## File structure

```markdown
---
name: photography
version: 1.0.0
author: Example
domain: photography
description: One-sentence description

defaults:
  image_model: gpt-image-2
  image_size: 1536x1024
  image_quality: high
  vision_model: gpt-4o
  score_threshold: 0.75
  aspect_ratio_pref: "3:2 landscape"

rules:
  - id: rule_one_id
    name: Rule One Name
    weight: 0.14
  - id: rule_two_id
    name: Rule Two Name
    weight: 0.14
  # ... 6–10 rules total; weights must sum to 1.00
---

# Title

## Visual Language Core
**Philosophy**: …
**Visual Signature**: …
**Technical Foundation**: …
**Emotional Tone**: …

## Classification Rules

### Rule 1: Rule One Name (14% weight)

**Definition**: 1–2 sentence definition.

**VALIDATION** (How to evaluate):
- Bullet criteria
- Score 0–1: how to score

**GENERATION** (How to instruct):
- Keywords: "x", "y"
- Emphasize: "..."
- Avoid: "..."

**Scoring Rubric**:
- 0.9–1.0: …
- 0.7–0.89: …
- 0.5–0.69: …
- <0.5: …

**Example**: concrete reference from the portfolio.

---
### Rule 2: …
```

---

## Frontmatter

### `name`, `version`, `author`, `domain`, `description`

Top-level metadata. `version` follows semver; bump when rules or weights change. `domain` is a free-form string (`photography`, `music`, `writing`, etc.).

### `defaults`

Generation defaults. The worker reads these unless overridden by environment variables. Override priority: CLI flag > env var > `.env` file > `defaults` block > built-in fallback.

For non-image domains, replace these with whatever the worker for that domain expects (e.g., `audio_model`, `text_model`).

### `rules`

A list of rule entries. Each entry has:

- `id` — short snake_case identifier; used as the key in score JSON.
- `name` — human-readable name; appears in the body.
- `weight` — float in [0, 1]. **All weights must sum to exactly 1.00.**

The body's `### Rule N: <name> (NN% weight)` headers are matched by name to these frontmatter entries. Don't duplicate weights between frontmatter and body — frontmatter is authoritative.

---

## Body sections

### Visual Language Core

A short human-readable preamble. Four labeled paragraphs:

- **Philosophy** — the creator's intent.
- **Visual Signature** (or Sonic / Narrative Signature for other domains) — what makes the work recognizable.
- **Technical Foundation** — specific technical choices (medium, instruments, tools).
- **Emotional Tone** — list of emotions the work evokes.

This section is reference material, not parsed by code. Keep it concise.

### Each rule

Every rule needs five blocks in this order:

1. **Definition** — 1–2 sentences. The "what."
2. **VALIDATION** — bulleted criteria for scoring 0–1. Should be answerable by a vision model (or domain analyzer). End with "Score 0–1: …"
3. **GENERATION** — bulleted instructions for *generating* work that follows this rule. Keywords, emphasis, things to avoid.
4. **Scoring Rubric** — four bands (0.9–1.0, 0.7–0.89, 0.5–0.69, <0.5) describing what each looks like.
5. **Example** — one concrete reference from the portfolio.

The worker extracts the GENERATION block to synthesize prompts and the rule list to score outputs. The Definition / Scoring Rubric / Example are for humans.

### Scoring framework, FAQ, version history, attribution

Standard sections. Update version history when rules change.

---

## Weights

Weights must sum to **exactly 1.00**. Combined score = sum of (rule_score × rule_weight).

A reasonable default for 8 rules:
- 3 "core" rules at 0.14 each
- 2 "technical" rules at 0.11 each
- 3 "emotion / context" rules at 0.12 each

= 0.42 + 0.22 + 0.36 = 1.00.

Adjust based on creator priority. The example `photography.md` ships with this distribution.

---

## Pass threshold

**0.75** is the default minimum for "passes the style." Rationale:

- 0.90–1.0 → exceptional, ship.
- 0.80–0.89 → strong, publish.
- 0.75–0.79 → acceptable, consider iterating.
- <0.75 → retry generation.

Threshold is set in the `defaults` block (`score_threshold`). Override per project as needed.

---

## How the worker reads it

`scripts/photography_agent.py` (which is generic — name is example-flavored, but the code is domain-agnostic):

1. Reads `[domain].md` at the repo root.
2. Parses the frontmatter for rules + weights + defaults.
3. Extracts per-rule GENERATION blocks from the body.
4. Synthesizes a prompt by combining the user's base prompt + each rule's GENERATION text.
5. Calls the image model with that synthesized prompt.
6. Scores the output via vision model against the rule list.
7. Computes the combined weighted score and writes results to `output/generation/<batch-name>/`.

The worker is a thin runtime — all the *creative direction* lives in the `.md` file.

---

## Authoring tips

- Keep VALIDATION criteria bulleted and binary-ish. "Are there ≥2 visible depth planes?" beats "How layered is the composition?"
- Keep GENERATION concrete and short. The worker compresses bullets into a single line per rule when synthesizing prompts.
- One rule, one dimension. If you find yourself writing "and also" in a rule, split it into two.
- Rule weights are an editable, versionable opinion. Tune them after Phase 4 validation, not before.
