# User Workflow: Build Your Own Classifier

End-to-end guide for someone using this framework to build a runtime classifier in their own creative domain.

The example below uses the photography worker (`scripts/photography_agent.py`) which targets OpenAI's image API. If you're working in a non-image domain, the same flow applies — you'll author your own thin worker that reads `[domain].md` and calls a domain-appropriate model. The framework (intake, portfolio analysis, rule synthesis, scoring loop) is identical.

---

## Prerequisites

- Python 3.9+
- An OpenAI API key (for the photography example) — set `OPENAI_API_KEY` in `.env`
- ~100 representative items from your work
- 30–60 minutes for intake + a few hours for portfolio analysis + iteration

---

## Phase 1 — Setup

```bash
# Clone the repo
git clone https://github.com/TrentM6/runtime-classifier.git
cd runtime-classifier

# Set up your API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...

# (Optional) install dependencies
pip install requests
```

Pick a domain intake from `templates/intake/`:
- `templates/intake/photography.md`
- `templates/intake/art.md`
- `templates/intake/graphic-design.md`
- `templates/intake/writing.md`
- `templates/intake/music.md`

Or use the generic `templates/domain-md-template.md` as a starting point if your domain isn't listed.

Answer the 7 questions. Keep answers to 2–3 sentences each. See [04-INTAKE-QUESTIONNAIRE.md](04-INTAKE-QUESTIONNAIRE.md) for guidance on what each question is asking.

---

## Phase 2 — Portfolio analysis

Gather ~100 representative items in a folder. Use systematic sampling — don't cherry-pick. Cover the full range of your work, not just the highlight reel.

For each sampled item, capture observations across the 8 dimensions ([05-PORTFOLIO-ANALYSIS.md](05-PORTFOLIO-ANALYSIS.md)):

1. Composition / structure
2. Subjects / content
3. Texture / quality
4. Palette / constraints
5. Emotional intent
6. Context
7. Decision-making
8. Execution

You can do this manually with a vision model in any chat interface, or write a small loop that batches descriptions via API. The output is one paragraph of observations per item.

Then look for patterns *across* the descriptions. Note frequency, strength, and variation for each candidate pattern.

Cross-check against your intake answers — are predicted patterns present? Are observed patterns predicted?

---

## Phase 3 — Author your `[domain].md`

Copy `templates/domain-md-template.md` to `[your-domain].md` at the repo root.

Fill in:

1. **Frontmatter** — `name`, `version`, `author`, `domain`, `description`, `defaults`, and the `rules` list with 6–10 rules each having `id`, `name`, and `weight`. Weights must sum to 1.00.

2. **Visual / Sonic / Narrative Language Core** — short preamble: Philosophy, Signature, Technical Foundation, Emotional Tone.

3. **For each rule** — write Definition + VALIDATION + GENERATION + Scoring Rubric + Example. See [06-CLASSIFIER-FORMAT.md](06-CLASSIFIER-FORMAT.md) for the exact schema.

The shipped `photography.md` at the repo root is a worked example — read it alongside the format doc.

---

## Phase 4 — Run the worker

For photography (using the included worker):

```bash
# Single image
python3 scripts/photography_agent.py \
  --prompt "Couple at NYC farmer's market, golden hour" \
  --batch-name test-001

# Skip scoring (generate only)
python3 scripts/photography_agent.py --prompt "..." --no-score

# Batch from a file (one prompt per line)
python3 scripts/photography_agent.py \
  --prompts-file my-prompts.txt \
  --batch-name midtown-test
```

Outputs land in `output/generation/<batch-name>/`:
- `images/generated-NN.png`
- `scores.json` — per-image scores, per-rule breakdown, combined score, pass/fail

For non-image domains, write a thin worker that:
1. Reads your `[domain].md` at the repo root
2. Parses frontmatter for rules + weights + defaults
3. Extracts GENERATION blocks per rule
4. Synthesizes a prompt from a base prompt + the GENERATION text
5. Calls your domain's generator
6. Scores the output (using a domain-appropriate evaluator)
7. Writes `output/generation/<batch-name>/scores.json`

`scripts/photography_agent.py` is a small, readable reference for how to do this.

---

## Phase 5 — Validate & iterate

### Score your source portfolio

Run scoring on your original ~100 items. Target: ≥90% pass at the 0.75 threshold.

- **<90% pass**: rules are stricter than your actual work. Refine VALIDATION criteria, lower the threshold, or rebalance weights.
- **100% pass**: rules are too loose. Tighten until you find the boundary.

### Generate test outputs

Create 20–30 generated outputs across a range of prompts. Then:

1. Score each automatically.
2. Show outputs to yourself (or a domain expert). Ask: *do these feel on-style?*
3. Compare combined score to qualitative judgment.

### Refine

The interesting failure modes:

- **High score, looks wrong** — VALIDATION criteria miss something. Refine the rule's VALIDATION text.
- **Low score, looks right** — weights are wrong, or the output is intentionally off-style. Check whether you'd accept this as part of your portfolio; if yes, the rule is over-strict.
- **Specific rule consistently fails** — rewrite the GENERATION block to be more concrete; add things to "Avoid".

Bump version (1.0.1, 1.1.0, etc.) when rules or weights change. Add a Version History entry to the `[domain].md` body.

---

## Phase 6 — Lock and share

Once your source portfolio passes ≥90% and combined scores correlate with your qualitative judgment, you have a v1.0 classifier.

To share:
- Commit your `[domain].md` to a fork of this repo
- Or open a PR adding it under a domain-specific folder
- Or just publish it as a gist — the file format is portable

Other creators can fork your classifier, swap in their own rules and weights, and have a working starting point in their own domain.

---

## Tips

- **Run the photography example end-to-end first** before authoring your own. It surfaces the file format, prompt synthesis, and scoring loop concretely.
- **Don't skip intake.** Going straight to portfolio analysis lets you project assumptions onto the work.
- **Don't over-fit.** A rule that perfectly describes your existing portfolio but doesn't generalize is a description, not a rule.
- **Tune weights last.** Get the rules right first; then balance weights based on creator judgment in Phase 5.
- **Soft retry, don't retrain.** When generation fails a rule, modify the prompt to emphasize that rule and regenerate. Faster and cheaper than rule changes for one-off failures.

---

## Next

- [02-THESIS.md](02-THESIS.md) — why this approach beats fine-tuning.
- [09-EXTENDING-TO-DOMAINS.md](09-EXTENDING-TO-DOMAINS.md) — cross-domain rule matrix.
