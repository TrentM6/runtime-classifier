# Portfolio Analysis

How to systematically analyze ~100 portfolio items and surface the patterns that become rules.

---

## Inputs

- The creator's intake answers ([04-INTAKE-QUESTIONNAIRE.md](04-INTAKE-QUESTIONNAIRE.md))
- ~100 representative items from the creator's work
- A vision-capable model (or domain-appropriate analyzer) for batch description

---

## Sample selection

### How many?

- **<50 items**: not enough variation to separate patterns from noise.
- **~100 items**: the sweet spot. Enough to surface real recurring patterns; few enough that you can think about each one.
- **>300 items**: same patterns repeat. Diminishing returns.

### How to sample

Don't cherry-pick. Cherry-picking biases toward the analyst's pre-conception of the creator's style. Use systematic sampling:

- If the creator has multiple distinct collections or projects, draw proportionally from each.
- Cover the full date range — early work and recent work, not just the most recent batch.
- Include known "best work" *and* known "B-sides." A classifier should describe what the creator's work actually *is*, not just the highlight reel.

---

## What to capture per item

For each sampled item, record observations across these dimensions:

1. **Composition / structure** — how elements are arranged (space for visual work, time for music, layout for written/designed work)
2. **Subjects / content** — what the work depicts or is about
3. **Texture / quality** — sensory rendering (light, color, line, timbre, voice)
4. **Palette / constraints** — color, tone, range, intentional limits
5. **Emotional intent** — what mood or feeling
6. **Context** — genre, cultural markers, references, setting
7. **Decision-making / decisiveness** — why *this* moment / note / line / element
8. **Execution** — precision, intentionality, technical character

For each dimension, note one short phrase of what you see. Don't editorialize at this stage — describe.

---

## Surfacing patterns

After you've described all ~100 items, look for patterns *across* the descriptions. Don't trust your memory; use the actual notes.

For each candidate pattern, measure:

- **Frequency**: in what % of items does this appear?
- **Strength**: when present, is the signal subtle or strong?
- **Variation**: when does the creator break the pattern, and why?

A useful pattern is **frequent enough to feel intentional** (≥60% in most domains) and **strong enough to be measurable** (a vision model could distinguish present vs. absent).

A pattern that appears in 95% of items but is weak when present is probably an unconscious habit — still useful, but lower-weight.

A pattern that appears in 30% of items but is striking when present is a *signature move* — often worth a dedicated rule with a moderate weight.

---

## Cross-check with intake

The intake (Phase 1) generated predictions about what patterns should appear. Now check:

- **Predicted + present**: strong rule candidate. The creator named it, the work shows it.
- **Predicted but absent**: investigate. Either the creator misremembers their own work, or the pattern is aspirational. Both are useful — sometimes the gap *is* the rule ("the creator wants this but isn't there yet").
- **Present but not predicted**: the creator has unconscious habits. Surface these. Often the most interesting rules.
- **Neither predicted nor present**: not a rule. Move on.

---

## From patterns to rule candidates

Group the strongest patterns into 6–10 candidate rules. Each rule should:

- **Have a clear name** (2–4 words, semantic)
- **Be measurable** (a vision model or domain analyzer can score 0–1)
- **Be orthogonal to other rules** (you can imagine an output that scores high on rule A and low on rule B)
- **Be grounded in the portfolio** (you can point to specific items as examples)

Take these candidates into Phase 3 (rule synthesis) and write each one up in the [06-CLASSIFIER-FORMAT.md](06-CLASSIFIER-FORMAT.md) format with VALIDATION + GENERATION blocks.

---

## What "good" looks like

When this phase is done, you should have:

- A document listing 6–10 candidate rules with:
  - Name
  - Frequency in portfolio
  - Strength when present
  - 2–3 portfolio items as concrete examples
  - Mapping back to intake answers (which question this rule traces to)
- A short note on **outliers** — items that broke the pattern and why
- A short note on **gaps** — patterns the creator predicted but the portfolio doesn't show

That document is the input to rule synthesis (Phase 3, see [03-METHODOLOGY.md](03-METHODOLOGY.md)).
