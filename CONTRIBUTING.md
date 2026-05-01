# Contributing

Thanks for considering a contribution. This project is a small framework for runtime-guided generative AI — we welcome both code improvements and new domain examples.

## What to contribute

### New domain examples (most useful)

The framework ships with one worked domain (`photography.md`). New domain classifiers — art, graphic design, writing, music, code, video, etc. — are the highest-impact contribution. To submit one:

1. Use one of the intake scaffolds in `templates/intake/` to anchor your rules.
2. Author a `<your-domain>.md` following the format in [docs/06-CLASSIFIER-FORMAT.md](docs/06-CLASSIFIER-FORMAT.md).
3. Validate it against your own ~100-item portfolio (target ≥90% pass at 0.75 threshold). Document the validation in your PR.
4. Open a PR adding `<your-domain>.md` at the repo root (matching where `photography.md` lives). If your domain needs a custom worker, add it under `scripts/` alongside `photography_agent.py`.

### Framework / methodology improvements

- Better intake questions, sharper VALIDATION patterns, clearer rule synthesis guidance — all welcome. Edit the relevant doc in `docs/`.
- If you find a pattern that genuinely changes how the framework should work (not just clarifications), please open an issue first to discuss.

### Worker improvements

`scripts/photography_agent.py` is intentionally small and dependency-light. Useful contributions:

- Workers for non-image domains (audio, text)
- Better cost / latency reporting in the scoring output
- Soft-retry helpers (currently the retry pattern is documented but not automated end-to-end)

Keep the dependency footprint minimal. New deps need a strong justification.

### Documentation

The docs aim for "explanatory, not exhaustive." If something's confusing or wrong, fix it. Big rewrites should be discussed in an issue first.

## Pull request etiquette

- One concern per PR.
- Keep changes focused — restructuring the docs and adding a new domain example are separate PRs.
- For new domain examples, include the validation results in the PR description (combined-score average across your source portfolio, pass rate at 0.75 threshold).
- Tests aren't required for the worker (it's mostly a thin runtime), but if you add new logic that's worth testing, include a small test.

## What's *not* in scope

- Fine-tuning workflows. The whole point of the framework is to *not* fine-tune.
- Vendor-lock SDKs. The worker should keep working if you swap one image API for another.
- Hosted services. This is a self-hosted, local-first project.

## License

By contributing, you agree your contributions are licensed under the MIT License (see `LICENSE`).

## Code of conduct

Be respectful. Disagreements about technical choices are fine; personal attacks aren't. The framework should be welcoming to creators in any domain — including those without a programming background.
