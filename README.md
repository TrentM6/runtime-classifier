# Runtime Classifier

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **New here?** Read the [Getting Started guide](docs/08-USER-WORKFLOW.md) for full setup and usage instructions.

**A thesis, proved out:** explicit style classification rules applied at runtime can substitute for fine-tuning when generating creative work. Cheaper, transparent, model-agnostic, easy to iterate — and the same pattern works across creative domains.

This repo is the framework, the methodology, a **worked photography example** at [`photography.md`](photography.md), intake scaffolds for art / graphic design / writing / music, and a minimal Python worker (~540 lines, one runtime dep) that proves the pipeline end-to-end.

---

## Why

Fine-tuning to capture a creator's style is expensive (hours of training, $100s of compute), opaque (no insight into what the model actually learned), brittle (often loses the style on novel prompts), and locked to the model you trained.

Style is *explicit* — a creator can articulate why they chose a frame, a color, a moment. So encode it explicitly:

- **Intake** — 7 questions anchor the work in the creator's own words
- **Portfolio analysis** — ~100 representative items surface real patterns
- **Synthesis** — patterns become 6–10 rules with VALIDATION + GENERATION blocks
- **Runtime** — at generation time, rules synthesize into the prompt; outputs are scored against the same rules; failures soft-retry

Same `[domain].md` works with any image / text / audio model. Iteration is in hours, not days. See [docs/02-THESIS.md](docs/02-THESIS.md) for the full argument.

---

## Quickstart (the photography example)

```bash
git clone https://github.com/TrentM6/runtime-classifier.git
cd runtime-classifier

# One-time setup: pip install requests + copy .env.example → .env
bash install.sh

# Edit .env: set OPENAI_API_KEY=sk-...

# Generate + score one image
python3 scripts/photography_agent.py \
  --prompt "Couple at NYC farmer's market, golden hour" \
  --batch-name first-test
```

Outputs land in `output/generation/first-test/` — generated PNG plus `scores.json` with per-rule breakdown.

The worker reads `photography.md` at runtime — rules, weights, and generation defaults all live there. Edit the `.md`, regenerate, and behavior changes immediately. No retraining.

---

## Build a classifier for your own domain

The framework isn't photography-specific. The same 8-dimension structure applies to art, graphic design, writing, music, code, and more.

To build your own:

1. Pick an intake from [`templates/intake/`](templates/intake/) — `photography`, `art`, `graphic-design`, `writing`, or `music`. Answer the 7 questions.
2. Analyze ~100 portfolio items ([docs/05-PORTFOLIO-ANALYSIS.md](docs/05-PORTFOLIO-ANALYSIS.md)).
3. Author your `[your-domain].md` using [`templates/domain-md-template.md`](templates/domain-md-template.md). Format reference: [docs/06-CLASSIFIER-FORMAT.md](docs/06-CLASSIFIER-FORMAT.md).
4. For non-image domains, write a thin worker that reads your `.md` and calls a domain-appropriate generator (the photography worker is a ~540-line reference: [scripts/photography_agent.py](scripts/photography_agent.py)).
5. Validate against your portfolio (target ≥90% pass at the 0.75 threshold).

Full walkthrough: [docs/08-USER-WORKFLOW.md](docs/08-USER-WORKFLOW.md).

---

## Extending to other domains

The 8 dimensions translate across creative domains. Excerpt — full matrix in [docs/09-EXTENDING-TO-DOMAINS.md](docs/09-EXTENDING-TO-DOMAINS.md):

| Dimension | Photography (shipped example) | Art | Graphic Design | Writing | Music |
|---|---|---|---|---|---|
| Authenticity | Documentary Honesty | Direct Mark-Making | Honest Hierarchy | Authorial Voice | Live Feel |
| Composition | Layered Composition | Pictorial Structure | Grid + Hierarchy | Paragraph Flow | Layered Arrangement |
| Subject focus | Human-Centered | Subject Centrality | Message Primacy | Protagonist Clarity | Vocal/Lead Forward |
| Texture | Neutral WB + 35mm Lens Character | Surface / Brushwork | Type Character | Prose Texture | Timbre / Production |
| Palette | Contrasty Lighting | Restricted Palette | Color System | Vocabulary Discipline | Dynamic Range |
| Connection | Eye Contact & Connection | Emotional Charge | Empathy / Tone | Reader Resonance | Emotional Intimacy |
| Context | NYC Context | Genre Markers | Brand Coherence | Setting Specificity | Genre Context |
| Decisiveness | Moment Decisiveness | Confident Mark | Decisive Layout | Confident Phrasing | Confident Phrasing |

What changes per domain: rule names, the evaluator (vision model → text model → audio classifier), and the generator. What stays the same: the 8-dimension structure, the VALIDATION + GENERATION block pattern, the 0.75 default threshold, and the soft-retry loop.

---

## Repo layout

```
runtime-classifier/
├── README.md                 — this file
├── LICENSE                   — MIT
├── CONTRIBUTING.md           — how to contribute new domains or framework changes
├── install.sh                — minimal installer (Python deps + .env)
├── .env.example              — config template
├── photography.md            — worked example: documentary photography classifier
│
├── docs/                     — framework documentation
│   ├── 01-README.md          — index
│   ├── 02-THESIS.md          — the core argument
│   ├── 03-METHODOLOGY.md     — intake → analysis → synthesis → validation
│   ├── 04-INTAKE-QUESTIONNAIRE.md
│   ├── 05-PORTFOLIO-ANALYSIS.md
│   ├── 06-CLASSIFIER-FORMAT.md  — the [domain].md file format
│   ├── 07-CLASSIFIER-THEORY.md  — why this works
│   ├── 08-USER-WORKFLOW.md      — end-to-end build guide
│   └── 09-EXTENDING-TO-DOMAINS.md  — cross-domain matrix
│
├── scripts/
│   └── photography_agent.py  — the worker (reads photography.md, generates, scores)
│
└── templates/
    ├── domain-md-template.md   — generic [domain].md scaffold
    └── intake/                 — 7-question intakes per domain
        ├── photography.md
        ├── art.md
        ├── graphic-design.md
        ├── writing.md
        └── music.md
```

---

## How the worker works

`scripts/photography_agent.py` is intentionally small (~540 lines, one runtime dep). At a glance:

1. Reads `photography.md` at the repo root.
2. Parses the YAML frontmatter for rules + weights + defaults.
3. Extracts each rule's GENERATION block from the body.
4. For each prompt, synthesizes a full prompt: base prompt + per-rule GENERATION text + a style preamble.
5. Calls the image API (default: `gpt-image-2` at 1536×1024).
6. Calls a vision model (default: `gpt-4o`) to score the output against each rule, 0–1.
7. Computes a weighted combined score; flags pass/retry vs. the threshold.
8. Writes `scores.json` with per-image breakdown.

No rules or weights live in the code. The `.md` is the canonical source of truth.

**The models are swappable defaults, not requirements.** The shipped photography example was tested end-to-end with `gpt-image-2` (generation) and `gpt-4o` (scoring), but both are configurable via `.env` or per-domain `defaults` in your `[domain].md`. Swap the image model for any prompt-driven generator — including a video model, audio model, or text model — and swap the vision model for whatever evaluator fits the output medium. The framework only cares that each step takes a prompt and returns something scoreable.

---

## What this is not

- **Not fine-tuning.** No model training, no GPU rental. The runtime is the API call.
- **Not a hosted service.** Self-hosted, local-first.
- **Not a vendor SDK.** The example happens to use OpenAI; the framework works with any image/text/audio generator that takes a prompt.
- **Not a chat agent.** It's a generation+scoring pipeline. You can wrap it in an agent if you want.

---

## License

MIT — see [LICENSE](LICENSE).

## Contributing

PRs welcome, especially new domain examples. See [CONTRIBUTING.md](CONTRIBUTING.md).
