---
name: photography
version: 1.0.0
author: Example
domain: photography
description: Example classifier — documentary street photography with 35mm/Portra-400 rendering

# Generation defaults (canonical project preferences; runtimes can override
# any of these via env vars in their own config without editing this file).
defaults:
  image_model: gpt-image-2
  image_size: 1536x1024
  image_quality: high
  vision_model: gpt-4o
  score_threshold: 0.75
  aspect_ratio_pref: "3:2 landscape"

# Classification rules — single machine-readable source of truth. The body
# sections below explain each rule (Definition / VALIDATION / GENERATION /
# Scoring Rubric / Example) for humans; scripts read this block + the
# GENERATION blocks from the body. Do not duplicate weights elsewhere.
rules:
  - id: documentary_honesty
    name: Documentary Honesty
    weight: 0.14
  - id: layered_composition
    name: Layered Composition
    weight: 0.14
  - id: human_centered
    name: Human-Centered
    weight: 0.14
  - id: neutral_wb_lens_char
    name: Neutral-Natural White Balance with 35mm Lens Character
    weight: 0.11
  - id: contrasty_lighting
    name: Contrasty Lighting
    weight: 0.11
  - id: eye_contact_connection
    name: Eye Contact & Connection
    weight: 0.12
  - id: nyc_context
    name: NYC Context
    weight: 0.12
  - id: moment_decisiveness
    name: Moment Decisiveness
    weight: 0.12
---

# Photography Classifier (Example)

Worked example of the runtime-classifier framework, applied to documentary NYC street photography. Use this as a reference when authoring your own `[domain].md` for any creative domain. To adapt: copy this file, replace the rules and visual-language section with your own, and rerun the worker.

---

## Visual Language Core

**Philosophy**: Connect with people and environments by capturing life as it unfolds. Find beauty in everyday life.

**Visual Signature**: Documentary photography of NYC street life and portraiture shot on 35mm, with the characteristic rendering of a Zeiss Biogon lens (slightly warm, rich detail, natural compression, edge character). Layered composition, genuine emotional engagement, and decisive moment capture.

**Technical Foundation**: 
- **Primary Lens**: 35mm Zeiss Biogon (produces slight warmth, rich mid-tones, natural perspective, characteristic edge rendering)
- **Film Stock**: Portra 400 aesthetic (warm tones when exposed in golden/warm light, but neutral white balance in daylight)
- **Shooting Style**: Handheld, natural light, reactive to environment
- **Frame / Aspect Ratio**: **3:2 landscape by default** (35mm sensor proportions). All generation defaults to 3:2 horizontal unless the user explicitly requests a different ratio (e.g. 4:5 vertical, 1:1 square, 16:9 cinematic). API equivalents: `1536x1024` (gpt-image-1/2), `1792x1024` (dall-e-3 closest landscape).
- **Default Generation Model**: **`gpt-image-2`** (OpenAI). Highest fidelity, photorealistic, native 3:2 support. Falls back to `gpt-image-1` (faster) or `dall-e-3` (legacy) if needed. Image quality: `high`.

**Emotional Tone**: Familiar, relatable, dignified, observant, intimate, hopeful.

---

## Classification Rules

### Rule 1: Documentary Honesty (14% weight)

**Definition**: The image feels *captured*, not constructed. Subjects are candid, genuine, unperformed. Technical choices are transparent and natural-looking.

**VALIDATION** (How to evaluate):
- Does the subject's body language feel unguarded and natural?
- Are expressions genuine (not manufactured for camera)?
- Does the image feel like a decisive moment, not a pose?
- Is the technique transparent (not over-processed)?
- Score 0–1: How authentically candid is this image?

**GENERATION** (How to instruct):
- Keywords: "candid," "unposed," "natural," "in-the-moment," "documentary"
- Emphasize: "Capture the subject unaware or naturally engaging, not performing"
- Avoid: "Perfect pose," "model," "studio," "constructed," "artificial"
- Structural: "Moment feels captured, not directed"

**Scoring Rubric**:
- 0.9–1.0: Genuinely candid, no artificiality
- 0.7–0.89: Mostly natural, minor stiffness acceptable
- 0.5–0.69: Some construction visible
- <0.5: Clearly posed or artificial

**Example from Portfolio**: Vendor at street fair, turned away from camera, unaware presence of photographer. Authentic gesture captured mid-action.

---

### Rule 2: Layered Composition (14% weight)

**Definition**: The image has distinct foreground, middle, and background depth planes. Spatial relationships guide the viewer's eye through the frame, creating visual rhythm and compositional strength.

**VALIDATION** (How to evaluate):
- Are there visible foreground/middle/background layers?
- Can you trace a visual pathway through the frame via depth?
- Do converging lines or spatial relationships enhance composition?
- Is the subject spatially integrated with environment?
- Score 0–1: How rich and intentional is the depth layering?

**GENERATION** (How to instruct):
- Keywords: "layered composition," "depth," "foreground-middle-background," "converging lines"
- Emphasize: "Include distinct depth planes," "Place subject in context with environment visible"
- Avoid: "Flat," "one-dimensional," "background blur," "isolated subject"
- Structural: "Environment is visible and contextual, not removed"

**Scoring Rubric**:
- 0.9–1.0: Rich, intentional depth layering with clear spatial progression
- 0.7–0.89: Good depth, clear foreground and background
- 0.5–0.69: Some depth, but layers unclear
- <0.5: Flat, minimal compositional depth

**Example from Portfolio**: Street vendor in foreground, storefront mid-ground, buildings background. Eye travels through frame via depth cues. Converging lines created by street and building angles.

---

### Rule 3: Human-Centered (14% weight)

**Definition**: People are the primary focus and emotional center. Environment is contextual and supporting, not the subject. Work celebrates human presence, not landscape or objects.

**VALIDATION** (How to evaluate):
- Are humans the primary subject or focal point?
- Does the image communicate human emotion/story?
- Is the person/people treated as primary interest?
- Would the image work without human subjects? (If yes, rule fails)
- Score 0–1: How central is the human element?

**GENERATION** (How to instruct):
- Keywords: "human subject," "people-centered," "portrait," "street subject"
- Emphasize: "Human is primary focal point and emotional center"
- Avoid: "Empty street," "landscape," "object," "architecture-focused," "no people"
- Structural: "People essential to image meaning"

**Scoring Rubric**:
- 0.9–1.0: People are clear primary focus, image meaningless without them
- 0.7–0.89: People prominent, clearly important
- 0.5–0.69: People present but secondary
- <0.5: People absent or entirely background

**Example from Portfolio**: Diverse NYC residents, street vendors, pedestrians. Always people first, environment contextual.

---

### Rule 4: Neutral-Natural White Balance with 35mm Lens Character (11% weight)

**Definition**: White balance is neutral and true to the actual lighting conditions (not artificially warm or cool). In daylight, white is white. In golden hour, light is naturally warm because the sun is warm—but the white balance is correct for that light. The 35mm Zeiss Biogon lens character creates a slight inherent warmth and rich mid-tone rendering. Film-like color science (Portra 400 aesthetic), not digital color-grading artifacts.

**VALIDATION** (How to evaluate):
- Is white balance accurate for the actual light source?
- Do colors feel natural and film-like, not digitally manipulated?
- Is there 35mm lens character visible (natural warmth, rich detail)?
- Are skin tones dimensional and naturally rendered?
- Does the image avoid artificial color grading (HSL adjustments, heavy saturation)?
- Score 0–1: How authentic is the color rendering to the actual lighting?

**GENERATION** (How to instruct):**
- Keywords: "neutral white balance," "35mm Zeiss Biogon," "film-like," "Portra 400," "photorealistic color," "natural light rendering"
- Emphasize: "Shot on 35mm Zeiss Biogon. Neutral white balance (true to lighting conditions). Golden hour has golden tones because sunlight is actually golden, not color-graded. Daylight has neutral tones. Film-like color science, not digital manipulation."
- Avoid: "Artificially warm," "color-graded," "saturated," "digital," "HSL adjustments," "plastic-looking colors"
- Technical: "Render with the character of 35mm Zeiss Biogon lens and Portra 400 film stock. Neutral white balance appropriate to lighting."

**Scoring Rubric**:
- 0.9–1.0: Perfect neutral WB with authentic 35mm lens character, film-like colors, no artificial grading
- 0.7–0.89: Mostly natural white balance, minor color shifts acceptable, clear lens character
- 0.5–0.69: Noticeably color-graded or artificial-looking, weak lens character
- <0.5: Heavily manipulated colors, plastic-looking, no lens character

**Example from Portfolio**: Daylight portraits maintain neutral white balance with natural skin tones. Golden hour scenes have warm light because sun is actually warm, but white balance is still correct. All images show 35mm Zeiss Biogon rendering—not overly warm, not artificially graded, just rich and dimensional.

---

### Rule 5: Contrasty Lighting (11% weight)

**Definition**: Visible shadow structure creates visual interest and dimension. Light is defined and directional, not flat. Shadows are flattering and contribute to composition, not obscuring or harsh.

**VALIDATION** (How to evaluate):
- Are shadows visible and structured (not crushed black)?
- Is light directional and creates visual interest?
- Do shadows contribute to composition?
- Are shadows flattering to subjects (not harsh)?
- Score 0–1: How defined and compositionally effective is the lighting?

**GENERATION** (How to instruct):
- Keywords: "contrasty lighting," "defined shadows," "dimensional," "directional light," "shadow structure"
- Emphasize: "Visible shadow structure adds dimension," "Light creates visual interest"
- Avoid: "Flat light," "no shadows," "harsh shadows obscuring faces," "completely shadowed"
- Lighting: "Directional with visible shadow geometry"

**Scoring Rubric**:
- 0.9–1.0: Beautiful shadow structure, visible dimension, flattering to subjects
- 0.7–0.89: Good contrast, clear shadows, effective composition
- 0.5–0.69: Some shadow definition, but light somewhat flat
- <0.5: Flat light, no shadow structure

**Example from Portfolio**: Shadows from umbrellas, buildings, fire escapes create visual rhythm. Shadows define faces, add dimension. Never harsh enough to obscure.

---

### Rule 6: Eye Contact & Connection (12% weight)

**Definition**: Subjects engage genuinely with camera (eye contact, awareness, warmth) OR with activities/other subjects (genuine interaction, unself-conscious presence). Either way, there is human connection/warmth visible.

**VALIDATION** (How to evaluate):
- If subject aware of camera: Is there eye contact and warmth visible?
- If subject unaware: Is there genuine interaction with others or activities?
- Is there emotional openness/vulnerability/connection?
- Do you feel a sense of human warmth from the image?
- Score 0–1: How much genuine human connection is visible?

**GENERATION** (How to instruct):
- Keywords: "eye contact," "genuine connection," "warmth," "intimate," "emotional engagement"
- Emphasize: "Subject engages warmly with camera or is genuinely engaged in activity," "Connection visible between subjects or with camera"
- Avoid: "Detached," "cold," "avoiding camera," "disconnected," "guarded"
- Relational: "Human warmth and connection central"

**Scoring Rubric**:
- 0.9–1.0: Powerful connection visible, genuine warmth/engagement
- 0.7–0.89: Clear connection, warmth visible
- 0.5–0.69: Some engagement, but warmth unclear
- <0.5: Detached, no visible connection

**Example from Portfolio**: Portrait subjects with direct eye contact and visible warmth; street scenes with genuine interaction between subjects. Viewers feel the human warmth.

---

### Rule 7: NYC Context (12% weight)

**Definition**: Image is unmistakably set in New York City. Specific NYC visual markers (streets, storefronts, signage, street culture, bodega aesthetic, specific neighborhoods) ground the image in place. Not generic urban, but specifically NYC.

**VALIDATION** (How to evaluate):
- Are there recognizable NYC elements (storefronts, street signs, architecture)?
- Could this be confused with another city? (If yes, rule fails)
- Is there NYC atmosphere (street culture, bodega vibes, specific energy)?
- Do you sense the specific place?
- Score 0–1: How unmistakably NYC is the setting?

**GENERATION** (How to instruct):
- Keywords: "NYC," "New York," "NYC street," "Crown Heights," "bodega," "NYC storefront"
- Emphasize: "Include recognizable NYC elements," "Street vendor or bodega or NYC-specific architecture"
- Avoid: "Generic city," "could be any urban area," "no place markers"
- Setting: "Distinctly New York City"

**Scoring Rubric**:
- 0.9–1.0: Unmistakably NYC, specific place markers visible
- 0.7–0.89: Clearly NYC, recognizable elements
- 0.5–0.69: Urban, could be NYC but not confirmed
- <0.5: Generic urban, could be anywhere

**Example from Portfolio**: Street vendors, specific storefronts, bodega signage, subway culture references, NYC street style. All three collections are unmistakably NYC.

---

### Rule 8: Moment Decisiveness (12% weight)

**Definition**: The image captures the *peak* moment—gesture fully extended, expression at maximum, action at its height. Timing shows skill and decisiveness, not luck or random capture.

**VALIDATION** (How to evaluate):
- Is the captured moment peak/climactic (not before or after)?
- Do gestures feel complete and full?
- Is expression fully formed (not mid-transition)?
- Does the image feel intentionally timed, not lucky?
- Score 0–1: How decisive and peak-moment is the capture?

**GENERATION** (How to instruct):
- Keywords: "decisive moment," "peak gesture," "maximum expression," "action at height"
- Emphasize: "Capture subject at peak of action or expression," "Timing feels intentional and decisive"
- Avoid: "Before," "after," "mid-action," "unclear timing," "unclear gesture"
- Timing: "Peak moment captured"

**Scoring Rubric**:
- 0.9–1.0: Perfect timing, clearly peak moment, intentional feeling
- 0.7–0.89: Good timing, clear peak, feels decisive
- 0.5–0.69: Decent timing, somewhat unclear if peak
- <0.5: Unclear timing, seems before or after peak

**Example from Portfolio**: Smiles fully formed, hand gestures complete, action at height. Never "almost" captured—always full, decisive moments.

---

## Scoring Framework

### Combined Score Calculation

```
Combined Score = (Rule1 × 0.14) + (Rule2 × 0.14) + (Rule3 × 0.14) 
                 + (Rule4 × 0.11) + (Rule5 × 0.11) + (Rule6 × 0.12) 
                 + (Rule7 × 0.12) + (Rule8 × 0.12)
                 // weights sum to 1.00; combined_score is in [0, 1]
```

Where each rule is scored 0–1 based on VALIDATION criteria.

### Pass Threshold

**0.75 / 1.0** = Minimum acceptable score

- 0.90–1.0 ✅ Exceptional (ship immediately)
- 0.80–0.89 ✅ Strong (publish)
- 0.75–0.79 ✅ Acceptable (meets standard, consider iteration)
- <0.75 ❌ Retry (doesn't meet style standards)

### Soft Retry Protocol

If generated image scores <0.75:

1. **Identify failing rules** (which scored <0.7?)
2. **Adjust prompt** with emphasis on failing rule
3. **Regenerate** with modified instruction
4. **Re-score** and compare

Example:
- Original: "NYC street vendor, afternoon"
- Scores: 0.92, 0.65, 0.88, ... (Rule 2 layering failed)
- Retry: "NYC street vendor with storefront visible behind, layered depth, afternoon"
- New score: 0.78 ✅

---

## Usage Examples

### Example 1: Generating Images

**Prompt**: "Couple at NYC farmer's market, golden hour"

**With Rules Applied**:
```
[Prompt] + [Rule 1: Candid] → "Capture couple unaware, natural interaction, not posing"
[Prompt] + [Rule 2: Depth] → "Include market stalls in background, layered composition"
[Prompt] + [Rule 3: Human] → "Couple is primary focus"
[Prompt] + [Rule 4: Warm] → "Warm color palette, golden hour light, warm skin tones"
[Prompt] + [Rule 5: Light] → "Directional light creating defined shadows, dimensional"
[Prompt] + [Rule 6: Connection] → "Subjects warmly engaged with each other or surroundings"
[Prompt] + [Rule 7: NYC] → "NYC farmer's market setting, recognizable city markers"
[Prompt] + [Rule 8: Decisive] → "Capture peak moment of interaction"
```

**Generate** → **Score** → **Pass or Retry**

### Example 2: Scoring Generated Image

Generated image of "Child playing in NYC park"

**Scoring**:
- Rule 1 (Candid): Child's expression natural, not aware of camera → 0.92
- Rule 2 (Depth): Playground equipment background, child foreground → 0.88
- Rule 3 (Human): Child is clear primary subject → 1.0
- Rule 4 (Warm): Warm color tones, golden hour → 0.91
- Rule 5 (Light): Directional light with shadow definition → 0.85
- Rule 6 (Connection): Joyful expression, engagement visible → 0.87
- Rule 7 (NYC): Park setting, NYC landmarks in background → 0.82
- Rule 8 (Decisive): Peak smile, full expression captured → 0.90

**Combined Score**: 0.89 ✅ (passes threshold)

---

## FAQ

**Q: Can I break these rules?**
A: No — these rules define this example's style. Breaking them creates work that *doesn't* feel like the example. That's fine if it's a different project, but it fails this classifier.

**Q: What if I want a different emotion (cynical, critical, etc.)?**
A: This classifier is specifically for a warm, documentary, connective approach. Different approaches require different classifiers — fork the file and rewrite the rules.

**Q: Why these 8 rules, not more or less?**
A: 8 rules cover all dimensions of creative decision-making: composition (2), subject (3), light/color (4, 5), emotion (6), context (7), execution (8), and authenticity (1). Fewer rules miss nuance. More rules overlap.

**Q: Why weight them differently?**
A: Core narrative rules (1–3) get 14%—if these fail, image fails. Technical rules (4–5) get 11%. Emotional/context rules (6–8) get 12%. (Sum: 1.00.)

**Q: What if my images score high but don't feel right?**
A: Your scoring intuition may not map to these rules. Options: (1) Refine VALIDATION criteria, (2) Adjust weights, (3) Edit rule definitions.

---

## Version History

**v1.0.0** — Initial release
- 8 classification rules with VALIDATION + GENERATION
- Worked photography example for the runtime-classifier framework

---

## Attribution

**Domain**: Documentary photography, NYC street life (example domain)

This file is a worked example. The framework, methodology, and worker are MIT-licensed and free to adapt to any creative domain.

---

## For Contributors

To adapt this classifier for other domains (music, writing, design, art):

1. Copy this file as `[your-domain].md`
2. Replace the 8 rules with domain-specific rules
3. Adapt VALIDATION and GENERATION for the new domain
4. Test on a portfolio of your work
5. Open a PR or share your fork

See `docs/09-EXTENDING-TO-DOMAINS.md` for the cross-domain rule matrix and `templates/intake/` for domain-specific intake questionnaires.
