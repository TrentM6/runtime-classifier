# Extending to Other Domains

The 8-rule structure isn't specific to photography. The same dimensional breakdown applies to any creative domain where style can be explicitly documented.

This doc shows the cross-domain rule matrix and how the 8 rules from the photography example translate to art, graphic design, writing, and music. Treat it as a starting point — your specific rules will diverge based on intake answers and portfolio analysis.

---

## The 8 dimensions

Most creative domains have rules that fall into these dimensions. Names and rule weights vary; the dimensions are stable.

| # | Dimension              | What it measures                                            |
|---|------------------------|--------------------------------------------------------------|
| 1 | **Authenticity / Documentary quality** | How "captured" vs. "constructed" the work feels |
| 2 | **Composition / Structure** | How elements are arranged in space or time           |
| 3 | **Subject focus**       | What the work is *about*; primary vs. background           |
| 4 | **Texture / Quality**   | Sensory rendering — light, color, line, timbre, voice      |
| 5 | **Palette / Constraints** | Tonal/color/dynamic-range discipline                     |
| 6 | **Emotional connection** | Engagement, intimacy, vulnerability                       |
| 7 | **Context / Setting**   | Genre, cultural markers, place specificity                 |
| 8 | **Decisiveness / Execution** | Peak moment, intentional timing, technical precision  |

---

## Cross-domain matrix

Each row is a dimension. Each column is how that dimension typically manifests in a domain. The "Photography" column is the actual rule from `photography.md`; the others are starting suggestions.

| Dimension | Photography (example shipped) | Art / Painting | Graphic Design | Writing | Music |
|---|---|---|---|---|---|
| 1. Authenticity | Documentary Honesty (candid, unposed, captured) | Direct Mark-Making (visible process, no over-finish) | Honest Hierarchy (no manipulative dark-pattern visuals) | Authorial Voice (consistent register, no AI sheen) | Live Feel (performance grit, not over-quantized) |
| 2. Composition | Layered Composition (foreground/middle/background) | Pictorial Structure (figure/ground, depth, balance) | Grid + Hierarchy (clear visual reading order) | Paragraph Flow (rising/falling rhythm, not flat) | Layered Arrangement (instruments in conversation) |
| 3. Subject focus | Human-Centered (people primary) | Subject Centrality (clear focal subject vs. ambient) | Message Primacy (core message reads first) | Protagonist Clarity (whose story this is) | Vocal/Lead Forward (lead voice mixed prominently) |
| 4. Texture / Quality | Neutral WB + 35mm Lens Character | Surface / Brushwork (visible material character) | Type Character (specific typographic texture) | Prose Texture (sentence-level voice, diction) | Timbre / Production (warm vs. clinical rendering) |
| 5. Palette / Constraints | Contrasty Lighting (defined shadow structure) | Restricted Palette (intentional color discipline) | Color System (limited, systematic palette) | Vocabulary Discipline (avoiding showy diction) | Dynamic Range (compressed vs. natural) |
| 6. Emotional connection | Eye Contact & Connection | Emotional Charge (does it land emotionally?) | Empathy / Tone (warmth vs. corporate detachment) | Reader Resonance (does it hit personally?) | Emotional Intimacy (vulnerability, openness) |
| 7. Context / Setting | NYC Context (specific place markers) | Genre Markers (period, school, references) | Brand Coherence (fits the brand world) | Setting Specificity (concrete place/time markers) | Genre Context (jazz vs. ambient vs. punk) |
| 8. Decisiveness | Moment Decisiveness (peak gesture) | Confident Mark (no hesitation, no muddiness) | Decisive Layout (no compromise/committee feel) | Confident Phrasing (no hedging) | Confident Phrasing (no hesitant timing) |

---

## Adapting per domain

### Photography → Art / Painting

The photography rules already lean into observable visual properties — most translate directly to painting. The interesting differences:

- "Documentary Honesty" becomes "Direct Mark-Making" — the painterly version of *captured-not-constructed* is *visible-process-not-over-finished*.
- "Lens Character" becomes "Surface / Brushwork" — the rendering signature is the artist's hand, not the lens.
- "NYC Context" becomes "Genre Markers" — period, school, references, art-historical context.

### Photography → Graphic Design

Design adds intent: every piece exists to communicate. Adjust:

- Add "Message Primacy" as the dominant rule (often the highest weight).
- "Composition" splits into "Grid + Hierarchy" (structural) and "Reading Order" (sequential).
- "Palette / Constraints" usually deserves higher weight in design than in photography — color systems matter more.
- Skip "Documentary Honesty" or replace with "Honest Hierarchy" (no manipulative visual tricks).

### Photography → Writing

Writing is sequential rather than spatial — composition becomes flow, palette becomes vocabulary. Suggested adaptations:

- "Authorial Voice" replaces "Documentary Honesty" — voice consistency over candidness.
- "Paragraph Flow" replaces "Layered Composition" — rhythm of sentence/paragraph length.
- "Prose Texture" — sentence-level voice (Hemingway short, McCarthy run-on, Didion observational).
- "Vocabulary Discipline" — color-palette-equivalent for words.
- "Setting Specificity" — concrete place/time markers replace "NYC Context."

For writing, scoring shifts from vision-model evaluation to text-model evaluation (e.g., GPT-4 reading prose against rules).

### Photography → Music

Music is temporal rather than spatial. Suggested adaptations:

- "Live Feel" — performance grit, breath, room sound vs. over-quantized perfection.
- "Layered Arrangement" — instruments in conversation across the stereo field and frequency range.
- "Vocal/Lead Forward" — clear lead voice, supporting parts in service.
- "Timbre / Production" — warmth vs. clinical, analog vs. digital character.
- "Dynamic Range" — natural breathing vs. brick-walled.
- "Emotional Intimacy" — vulnerability, openness in performance.
- "Genre Context" — jazz era, smoky club, lo-fi bedroom, etc.

For music, scoring requires an audio-aware evaluator. Vision-model APIs won't work — use audio embeddings, music-genre classifiers, or human evaluation in early iterations.

---

## What stays the same across domains

- The **8-rule structure** with weights summing to 1.00.
- **VALIDATION + GENERATION blocks** for each rule.
- The **0.75 default threshold** for "passes the style."
- The **soft-retry pattern** — when an output fails on rule N, regenerate with emphasis on rule N's GENERATION text.
- The **methodology** — intake, portfolio analysis, rule synthesis, validation. See [03-METHODOLOGY.md](03-METHODOLOGY.md).

---

## What changes across domains

- The **specific rule names and content** (obviously).
- The **evaluator** — vision model for images, text model for writing, audio classifier for music, etc.
- The **GENERATION targets** — different generators take different prompt formats. The synthesizer in `scripts/photography_agent.py` is one example; you may need a thin custom worker.
- **Sample size norms** — 100 items is reasonable for photography or graphic design; for writing, "100 items" might mean 100 paragraphs or 100 short stories depending on grain.

---

## Starting points

For each non-photography domain, this repo ships:

- An intake questionnaire scaffold at `templates/intake/<domain>.md`
- The generic file template at `templates/domain-md-template.md`

Use the intake to anchor your rules in your own intent, then adapt the matrix above to your domain. The rules in the matrix are *suggestions* based on what's worked for the photography example — your portfolio analysis will surface your own.
