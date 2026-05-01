# Methodology: From Creator to Classifier

How to take a creator (or yourself) from a blank page to a finished `[domain].md` classifier. Reuse this for any creative domain — photography, art, graphic design, writing, music, code.

---

## The four phases

```
Phase 1 — Intake          ~30 min   The 7 questions. Capture intent, before looking at the work.
Phase 2 — Portfolio       ~2–3 hr   Analyze ~100 representative items. Surface patterns.
Phase 3 — Synthesis       ~1–2 hr   Convert patterns into 6–10 rules with VALIDATION + GENERATION.
Phase 4 — Validation      iterative Score originals + generated outputs. Refine.
```

The order matters. Doing portfolio analysis first imposes the analyst's lens on the work; doing intake first means patterns are interpreted in the creator's own framing.

---

## Phase 1 — Intake

Send the 7 questions in [04-INTAKE-QUESTIONNAIRE.md](04-INTAKE-QUESTIONNAIRE.md) to the creator. Ask for 2–3 sentences per question — concise beats essay.

The questions move from big picture (philosophy, process) → specific (technique, priorities) → meta (constraints, self-observed patterns). They're domain-agnostic; the wording is photography-flavored but trivially adapts.

For non-photography domains, see `templates/intake/` for pre-adapted versions.

After intake, write down:
- A one-sentence summary of the creator's intent
- 3–5 priorities the creator stated explicitly
- Any non-negotiables ("I never X")
- Patterns the creator already notices in their own work

These become the **predictions** you'll test against the portfolio in Phase 2.

---

## Phase 2 — Portfolio analysis

### Sample size

- **<50 items**: patterns may be noise.
- **~100 items**: enough variation to surface real patterns; the sweet spot.
- **>300 items**: diminishing returns; the same patterns repeat.

### Sampling

Don't cherry-pick — that biases toward the analyst's pre-conception. Use systematic sampling:
- Pull every Nth item from each collection so all collections are represented proportionally.
- Cover the full date/style range, not just recent work.

### What to look for

Across most creative domains, surface patterns in these dimensions:

- **Composition / structure** — how elements are arranged in space (or time, for music/writing)
- **Subjects / content** — what the work is *about*
- **Texture / quality** — sensory rendering (lighting, timbre, prose voice, color, line weight)
- **Palette / constraints** — color, tone, range, intentional limits
- **Emotional intent** — what the work is supposed to make the audience feel
- **Context** — genre, cultural markers, references
- **Decision-making** — why *this* moment / note / word / line
- **Execution** — precision, decisiveness, technical skill

For each dimension, note:
- Frequency: in what % of items does this pattern appear?
- Strength: when present, how strong is it?
- Variation: when does the creator break the pattern, and why?

### Cross-check with intake

The creator predicted certain patterns in Phase 1. Did the portfolio confirm them?

- **Confirmed**: keep as a candidate rule.
- **Stated but absent**: dig deeper. Either the creator misremembers, or the pattern is in their *aspirations* not their work yet — both are useful signals.
- **Present but not stated**: candidate rule the creator hasn't articulated yet. Surface it.

---

## Phase 3 — Rule synthesis

Convert the strongest patterns into rules. Aim for **6–10 rules** total.

- **<6 rules**: usually misses dimensions and lets weak outputs slip through.
- **>12 rules**: rules start overlapping; scoring becomes noisy.
- **8 rules** is a good default — enough to cover all major dimensions.

For each rule, write four things:

1. **Definition** — 1–2 sentences. What does the rule mean?
2. **VALIDATION** — how to score 0–1 whether an output follows this rule. Should be answerable by a vision model (or domain-appropriate evaluator).
3. **GENERATION** — how to instruct a generator to produce work that follows the rule. Keywords + emphasis + things to avoid.
4. **Example** — one concrete example from the portfolio so the rule is grounded.

### Weights

Weights express priority. They must sum to 1.00 so combined scores stay in [0, 1].

A reasonable default for 8 rules:
- 3 "core" rules at 0.14 each (the rules that, if violated, the work fails identity)
- 2 "technical" rules at 0.11 each (important but secondary)
- 3 "context" rules at 0.12 each (specificity, emotion, decisiveness)

= 0.42 + 0.22 + 0.36 = 1.00.

Pick weights based on what the creator emphasized in intake, then verify the weighted score correlates with their qualitative judgment in Phase 4.

### Orthogonality check

Two rules should not be measuring the same thing. Test: can you imagine an output that scores high on rule A but low on rule B (and vice versa)? If not, merge them.

---

## Phase 4 — Validation & iteration

### Score the source portfolio

Run the scoring on the original ~100 items. **Target: ≥90% pass at 0.75 threshold.**

- **<90% pass**: the rules are stricter than the creator's actual work — usually a weight or threshold problem. Refine VALIDATION criteria or relax the threshold.
- **100% pass**: rules are likely too loose. Tighten until you find the boundary.

### Score generated outputs

Generate 20–30 outputs using the GENERATION instructions, then:

1. Score each automatically against all rules.
2. Show outputs to the creator. Ask: *do these feel like your work?*
3. Compare score correlation with creator judgment.

The interesting cases:

- **High score, creator says "no"** → VALIDATION criteria are missing something the creator values. Refine the rule's VALIDATION text.
- **Low score, creator says "yes, this is great"** → either rule weights are wrong, or this output is intentionally outside the documented style (worth noting, not necessarily fixing).

### Lock v1.0

Once score correlates with creator judgment and the source portfolio passes ≥90%, lock the rule set as v1.0. Future changes get versioned and logged.

---

## Common pitfalls

- **Skipping intake.** Going straight to portfolio analysis lets the analyst project assumptions onto the work. The intake exists to anchor interpretation in the creator's own words.
- **Over-fitting to the portfolio.** If a rule only describes the existing portfolio and doesn't generalize, it's a description not a rule. Rules should let *new* work pass even if it's stylistically novel.
- **Vague VALIDATION.** "Captures the mood" isn't scorable. "Direct subject-camera eye contact, OR genuine engagement with another subject/activity" is.
- **Prescriptive GENERATION.** "Set ISO to 400" is too specific. "Film-like grain rendering, not crisp digital noise" lets multiple generators express the same intent.
- **Imbalanced weights.** If one rule is 0.40, the rest barely matter. Keep weights within ~2× of each other unless one is genuinely dominant.

---

## Next

- See [06-CLASSIFIER-FORMAT.md](06-CLASSIFIER-FORMAT.md) for the exact `[domain].md` file format.
- See [08-USER-WORKFLOW.md](08-USER-WORKFLOW.md) for the end-to-end workflow with commands.
