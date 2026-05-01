#!/usr/bin/env python3
"""
Runtime Classifier — photography example worker.

Reference implementation of the runtime-classifier pattern, scoped to the
photography example shipped at the repo root (``photography.md``). Single
source of truth for rules + weights + defaults: ``photography.md``. This
script reads that file at runtime and never embeds its own copy of the
rules. For non-image domains, copy this file as a starting point and swap
out the generation + scoring API calls.

Configuration (resolution order: CLI flag > env var > .env file > defaults
in photography.md frontmatter > built-in fallback):

    OPENAI_API_KEY        required; from env or .env at repo root
    IMAGE_MODEL           default: gpt-image-2
    IMAGE_SIZE            default: 1536x1024 (3:2 landscape)
    IMAGE_QUALITY         default: high
    VISION_MODEL          default: gpt-4o
    SCORE_THRESHOLD       default: 0.75
    OPENAI_BASE           default: https://api.openai.com/v1

Usage:
    python3 scripts/photography_agent.py \\
        --prompt "Couple at NYC farmers market, golden hour" \\
        --batch-name batch-005 \\
        --count 3

    python3 scripts/photography_agent.py \\
        --prompts-file prompts.txt \\
        --batch-name midtown-test

    python3 scripts/photography_agent.py --prompt "..." --no-score
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
PHOTOGRAPHY_MD = REPO_ROOT / "photography.md"
ENV_FILE = REPO_ROOT / ".env"
OUTPUT_BASE = REPO_ROOT / "output" / "generation"

BUILTIN_DEFAULTS = {
    "IMAGE_MODEL": "gpt-image-2",
    "IMAGE_SIZE": "1536x1024",
    "IMAGE_QUALITY": "high",
    "VISION_MODEL": "gpt-4o",
    "SCORE_THRESHOLD": "0.75",
    "OPENAI_BASE": "https://api.openai.com/v1",
}


# ---------------------------------------------------------------------------
# .env loader (no python-dotenv dep)
# ---------------------------------------------------------------------------

def load_env_file(path: Path = ENV_FILE) -> None:
    """Populate os.environ from a .env file if present (without overriding
    values already set in the real environment)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def cfg(name: str, fallback: str | None = None) -> str:
    return os.environ.get(name) or (fallback if fallback is not None else BUILTIN_DEFAULTS.get(name, ""))


def require_api_key() -> str:
    key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not key:
        sys.exit(
            "ERROR: OPENAI_API_KEY not found.\n"
            f"  Set it in your shell, or create {ENV_FILE} with:\n"
            "    OPENAI_API_KEY=sk-proj-...\n"
        )
    return key


# ---------------------------------------------------------------------------
# photography.md parser
# ---------------------------------------------------------------------------

def _parse_yaml_value(v: str) -> Any:
    """Best-effort scalar parser (avoids a YAML dep)."""
    v = v.strip().strip('"').strip("'")
    if v in ("true", "True", "yes"):
        return True
    if v in ("false", "False", "no"):
        return False
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def _parse_frontmatter(text: str) -> dict:
    """Hand-parse the simple YAML frontmatter we use in photography.md.

    Supports: top-level scalars; nested mappings (e.g. ``defaults``); and a
    list of mappings (e.g. ``rules:`` with ``- id: ...``). No anchors,
    multi-line strings, or other fancy YAML.
    """
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not m:
        sys.exit(f"ERROR: no YAML frontmatter found in {PHOTOGRAPHY_MD}")
    body = m.group(1)

    out: dict = {}
    cur_block_key: str | None = None  # name of nested mapping we're inside
    cur_block: dict | None = None
    cur_list_key: str | None = None  # name of list-of-mappings we're inside
    cur_list: list | None = None
    cur_item: dict | None = None

    def commit_item() -> None:
        nonlocal cur_item
        if cur_item is not None and cur_list is not None:
            cur_list.append(cur_item)
            cur_item = None

    def flush_block() -> None:
        nonlocal cur_block_key, cur_block, cur_list_key, cur_list
        if cur_block_key is not None and cur_block is not None:
            out[cur_block_key] = cur_block
            cur_block_key = None
            cur_block = None
        if cur_list_key is not None and cur_list is not None:
            commit_item()
            out[cur_list_key] = cur_list
            cur_list_key = None
            cur_list = None

    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # Top-level key (no leading whitespace)
        if not raw.startswith((" ", "\t")):
            flush_block()
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v == "":
                # Could be the start of a nested block OR a list. Decide on
                # the next non-empty line.
                cur_block_key = k
                cur_block = {}
            else:
                out[k] = _parse_yaml_value(v)
        else:
            stripped = line.strip()
            # List item: "- key: value"
            if stripped.startswith("- "):
                # Promote pending nested-mapping block to a list if needed
                if cur_block_key is not None:
                    cur_list_key = cur_block_key
                    cur_list = []
                    cur_block_key = None
                    cur_block = None
                if cur_list is None:
                    continue  # malformed — ignore
                commit_item()
                cur_item = {}
                kv = stripped[2:]
                if ":" in kv:
                    k, v = kv.split(":", 1)
                    cur_item[k.strip()] = _parse_yaml_value(v.strip())
            elif cur_item is not None and ":" in stripped:
                k, v = stripped.split(":", 1)
                cur_item[k.strip()] = _parse_yaml_value(v.strip())
            elif cur_block is not None and ":" in stripped:
                k, v = stripped.split(":", 1)
                cur_block[k.strip()] = _parse_yaml_value(v.strip())

    flush_block()
    return out


def _extract_generation_blocks(text: str) -> dict[str, str]:
    """Map rule-id → joined GENERATION text from the photography.md body.

    Body sections look like:
        ### Rule 1: Documentary Honesty (14% weight)
        ...
        **GENERATION** (How to instruct):
        - bullet
        - bullet
        ...
        **Scoring Rubric**:           ← end of GENERATION

    We slug the rule name to match frontmatter ids when possible; if a slug
    doesn't match any known id, we still keep it keyed by slug so the caller
    can decide.
    """
    rule_chunks: list[tuple[str, str]] = []
    rule_re = re.compile(r"^###\s+Rule\s+\d+:\s*(.+?)\s*\(\s*\d+\s*%\s*weight\s*\)\s*$",
                         re.MULTILINE)
    matches = list(rule_re.finditer(text))
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        rule_chunks.append((name, text[start:end]))

    out: dict[str, str] = {}
    for name, chunk in rule_chunks:
        gen_match = re.search(
            r"\*\*GENERATION\*\*[^\n]*\n(.*?)(?=\n\*\*[A-Z][^\n]*\n|\n###\s+Rule|\n---|\Z)",
            chunk, re.DOTALL,
        )
        gen = gen_match.group(1).strip() if gen_match else ""
        slug = _slug(name)
        out[slug] = gen
        out[f"__name__::{slug}"] = name
    return out


def _slug(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def load_rules() -> tuple[list[dict], dict]:
    """Returns (rules, defaults) from photography.md.

    rules: list of {id, name, weight, generation} dicts in canonical order.
    defaults: dict from the ``defaults`` frontmatter block.
    """
    if not PHOTOGRAPHY_MD.exists():
        sys.exit(f"ERROR: {PHOTOGRAPHY_MD} not found")
    text = PHOTOGRAPHY_MD.read_text()
    fm = _parse_frontmatter(text)
    if "rules" not in fm or not isinstance(fm["rules"], list):
        sys.exit("ERROR: photography.md frontmatter has no 'rules:' list")

    gen_blocks = _extract_generation_blocks(text)

    # Match generation blocks to rules. Try id-as-slug first, then name slug.
    rules: list[dict] = []
    for r in fm["rules"]:
        rid = r.get("id")
        name = r.get("name", "")
        weight = r.get("weight")
        if not rid or weight is None:
            sys.exit(f"ERROR: rule entry missing id or weight: {r}")
        gen = gen_blocks.get(rid) or gen_blocks.get(_slug(name)) or ""
        rules.append({"id": rid, "name": name, "weight": float(weight), "generation": gen})

    defaults = fm.get("defaults", {}) or {}
    return rules, defaults


# ---------------------------------------------------------------------------
# Prompt synthesis & API calls
# ---------------------------------------------------------------------------

def synthesize_prompt(base_prompt: str, rules: list[dict], aspect_ratio_pref: str) -> str:
    """Build the full prompt sent to the image model. Pulls per-rule
    GENERATION text directly from photography.md."""
    lines = []
    for i, r in enumerate(rules, start=1):
        body = r["generation"].strip() or "see photography.md for full guidance"
        # Compress multi-line bullets into a single line per rule for the prompt.
        compact = " ".join(line.strip(" -•\t").strip() for line in body.splitlines() if line.strip())
        lines.append(f"Rule {i} ({r['name']}): {compact}")

    style_line = (
        "Photography style: 35mm documentary street photography, Portra 400 "
        f"film-like rendering, handheld natural light. Default frame: {aspect_ratio_pref} "
        "(35mm sensor proportions). Avoid: HDR, oversaturation, color-graded look, "
        "plastic skin, posed-studio feel, square crops."
    )
    return f"{base_prompt}.\n\n" + "\n".join(lines) + "\n\n" + style_line


def generate_image(prompt: str, api_key: str) -> bytes:
    resp = requests.post(
        f"{cfg('OPENAI_BASE')}/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": cfg("IMAGE_MODEL"),
            "prompt": prompt,
            "n": 1,
            "size": cfg("IMAGE_SIZE"),
            "quality": cfg("IMAGE_QUALITY"),
        },
        timeout=600,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"image API {resp.status_code}: {resp.text[:500]}")

    data = resp.json()["data"][0]
    if "b64_json" in data:
        return base64.b64decode(data["b64_json"])
    if "url" in data:
        img_resp = requests.get(data["url"], timeout=60)
        img_resp.raise_for_status()
        return img_resp.content
    raise RuntimeError(f"unexpected image response shape: {list(data.keys())}")


def build_scoring_prompt(rules: list[dict]) -> str:
    """Build the JSON-schema scoring prompt dynamically from rules."""
    lines = ["You are evaluating a photograph against this project's classification rules.",
             "",
             "For EACH rule, score 0.0–1.0 where 1.0 = perfectly follows the rule, 0.5 = partial, 0.0 = not at all.",
             "",
             "Rules:"]
    for i, r in enumerate(rules, start=1):
        body = r["generation"].strip() or r["name"]
        compact = " ".join(line.strip(" -•\t").strip() for line in body.splitlines() if line.strip())
        lines.append(f"{i}. {r['id']} — {r['name']}: {compact[:400]}")
    lines += [
        "",
        "RESPOND ONLY WITH JSON, no other text. Schema:",
        "{",
    ]
    for r in rules:
        lines.append(f'  "{r["id"]}": 0.0-1.0,')
    lines.append('  "reasoning": "brief explanation of the scores"')
    lines.append("}")
    return "\n".join(lines)


def score_image(png_bytes: bytes, rules: list[dict], api_key: str) -> dict:
    b64 = base64.b64encode(png_bytes).decode("ascii")
    resp = requests.post(
        f"{cfg('OPENAI_BASE')}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": cfg("VISION_MODEL"),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": build_scoring_prompt(rules)},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"},
                        },
                    ],
                }
            ],
            "max_tokens": 800,
            "response_format": {"type": "json_object"},
        },
        timeout=120,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"vision API {resp.status_code}: {resp.text[:500]}")
    return json.loads(resp.json()["choices"][0]["message"]["content"])


def combined_score(scores: dict, rules: list[dict]) -> float:
    total = 0.0
    for r in rules:
        s = scores.get(r["id"], 0.0)
        try:
            s = float(s)
        except (TypeError, ValueError):
            s = 0.0
        total += s * r["weight"]
    return round(total, 4)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Runtime Classifier — photography example worker")
    p.add_argument("--prompt", help="Single base prompt (ignored if --prompts-file is set)")
    p.add_argument("--prompts-file", help="Path to a file containing one prompt per line")
    p.add_argument("--batch-name", default=None,
                   help="Output subfolder under output/generation/ (default: batch-NNN auto)")
    p.add_argument("--count", type=int, default=1,
                   help="Number of images to generate per prompt (default 1)")
    p.add_argument("--no-score", action="store_true",
                   help="Skip vision scoring (generate only)")
    return p.parse_args()


def auto_batch_name() -> str:
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    existing = [p.name for p in OUTPUT_BASE.iterdir()
                if p.is_dir() and p.name.startswith("batch-")]
    nums = []
    for n in existing:
        m = re.match(r"batch-(\d+)$", n)
        if m:
            nums.append(int(m.group(1)))
    return f"batch-{(max(nums) + 1) if nums else 1:03d}"


def collect_prompts(args: argparse.Namespace) -> list[str]:
    if args.prompts_file:
        path = Path(args.prompts_file)
        if not path.exists():
            sys.exit(f"ERROR: prompts file not found: {path}")
        return [ln.strip() for ln in path.read_text().splitlines()
                if ln.strip() and not ln.strip().startswith("#")]
    if args.prompt:
        return [args.prompt] * args.count
    sys.exit("ERROR: provide --prompt or --prompts-file")


def main() -> int:
    load_env_file()
    api_key = require_api_key()
    rules, defaults = load_rules()

    # Apply photography.md defaults to env without overriding existing env.
    for k, env_k in [
        ("image_model", "IMAGE_MODEL"),
        ("image_size", "IMAGE_SIZE"),
        ("image_quality", "IMAGE_QUALITY"),
        ("vision_model", "VISION_MODEL"),
        ("score_threshold", "SCORE_THRESHOLD"),
    ]:
        if k in defaults and env_k not in os.environ:
            os.environ[env_k] = str(defaults[k])

    args = parse_args()
    prompts = collect_prompts(args)
    batch_name = args.batch_name or auto_batch_name()

    batch_dir = OUTPUT_BASE / batch_name
    images_dir = batch_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    scores_path = batch_dir / "scores.json"

    aspect_ratio_pref = str(defaults.get("aspect_ratio_pref", "3:2 landscape"))
    threshold = float(cfg("SCORE_THRESHOLD"))

    print(f"=== {batch_name} — {cfg('IMAGE_MODEL')} ===")
    print(f"Output: {batch_dir}")
    print(f"Rules: {len(rules)} (sum of weights: {sum(r['weight'] for r in rules):.4f})")
    print(f"Generating {len(prompts)} image(s){' (no scoring)' if args.no_score else ''}\n")

    results = []
    for i, base in enumerate(prompts, start=1):
        print(f"[{i}/{len(prompts)}] {base[:80]}")
        synth = synthesize_prompt(base, rules, aspect_ratio_pref)

        try:
            png = generate_image(synth, api_key)
        except Exception as e:
            print(f"  GENERATE FAILED: {e}")
            results.append({"id": i, "base_prompt": base, "error": f"generate: {e}"})
            continue

        img_path = images_dir / f"generated-{i:02d}.png"
        img_path.write_bytes(png)
        print(f"  saved: {img_path.name} ({len(png) // 1024} KB)")

        record: dict = {
            "id": i,
            "filename": img_path.name,
            "base_prompt": base,
            "synthesized_prompt": synth,
        }

        if not args.no_score:
            try:
                scores = score_image(png, rules, api_key)
            except Exception as e:
                print(f"  SCORE FAILED: {e}")
                record["error"] = f"score: {e}"
                results.append(record)
                continue
            cs = combined_score(scores, rules)
            passed = cs >= threshold
            print(f"  combined: {cs:.3f}  {'PASS' if passed else 'RETRY'}")
            record["scores"] = scores
            record["combined_score"] = cs
            record["pass"] = passed

        results.append(record)

    summary = {
        "batch": batch_name,
        "image_model": cfg("IMAGE_MODEL"),
        "image_size": cfg("IMAGE_SIZE"),
        "image_quality": cfg("IMAGE_QUALITY"),
        "vision_model": cfg("VISION_MODEL"),
        "score_threshold": threshold,
        "rules_source": "photography.md (canonical)",
        "rules": {r["id"]: r["weight"] for r in rules},
        "timestamp": time.time(),
        "num_images": len(results),
        "pass_rate": (sum(1 for r in results if r.get("pass")) / len(results)) if results else 0.0,
        "average_score": (
            sum(r.get("combined_score", 0.0) for r in results) / len(results)
            if results else 0.0
        ),
        "images": results,
    }
    scores_path.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {scores_path.relative_to(REPO_ROOT)}")
    if not args.no_score:
        print(f"pass rate: {summary['pass_rate']:.0%}  avg: {summary['average_score']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
