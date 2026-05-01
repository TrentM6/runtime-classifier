# Runtime Classifier Theory: Why This Works

This document explains the theoretical foundation for runtime-guided generative AI (the core innovation of this project).

---

## The Problem with Fine-Tuning

### Current Approach

When creators want AI to generate in their style, the standard path is:

```
Creator's Portfolio (1000 images)
    ↓
Fine-tuning pipeline
    ↓
Model learns implicit style from data
    ↓
Model generates similar images
```

### Issues with Fine-Tuning

**1. Computational Expense**
- Requires 100-1000+ high-quality training images
- Fine-tuning run takes hours/days
- Retraining needed if style changes
- Scales poorly for multiple creators

**2. Black Box**
- No transparency into what the model learned
- Can't debug failures (why did this not feel like my style?)
- Can't explain to others why image fails
- Hard to iterate rules

**3. Brittleness**
- Model captures statistical noise along with style
- Fails on novel concepts not in training data
- Sensitive to prompt engineering
- Hard to transfer across models

**4. Portability**
- Fine-tuned model locked to one platform/API
- Can't use with different base models
- Can't update without retraining

**5. Iteration**
- To change style, must retrain (expensive)
- No way to isolate which rules to adjust
- Feedback-to-update cycle is slow

---

## The Solution: Runtime Guidance

### New Approach

```
Creator's Philosophy (7 questions)
    ↓
Portfolio Analysis (100 images)
    ↓
Extract Explicit Rules (8 classification rules)
    ↓
VALIDATION (how to score) + GENERATION (how to prompt)
    ↓
Apply Rules at Generation Time (runtime)
    ↓
Score generated images against rules
    ↓
Model generates images in creator's style
```

### Why This Works

**1. Explicit Over Implicit**

Style isn't hidden in statistics. It's **explicit and documentable**:
- "I always look for layered composition" → Rule 2
- "I want warm colors" → Rule 4
- "I capture candid moments" → Rule 1
- "I photograph NYC" → Rule 7

These are *rules*, not statistical patterns.

**2. Rules Are Model-Agnostic**

The 8 rules don't depend on any specific model. They work with:
- DALL-E 3
- Midjourney
- Flux
- GPT-4 Vision
- Any future model

Because rules are prompting guidance, not model internals.

**3. Transparency**

Each generated image gets scored across 8 dimensions. If it fails, we *know why*:
- "Failed Rule 2 (Layering): only 2 depth planes visible"
- "Failed Rule 4 (Warm): skin tones rendered cool"
- "Failed Rule 7 (NYC): generic city, not NYC-specific"

This is **auditable feedback**, not opaque loss values.

**4. Fast Iteration**

To refine style, just edit the rules. No retraining:
- Adjust GENERATION prompt for Rule 4
- Re-run generation
- Images improve immediately

Feedback loop is hours, not days.

**5. Computational Efficiency**

No fine-tuning means:
- No training phase
- Just prompt engineering + scoring
- Works with existing APIs
- Minimal compute overhead

---

## How Runtime Guidance Works

### Step 1: Extract Rules from Portfolio

Given 100 representative images, AI agent identifies patterns:

```
Vision Model analyzes samples:
- What's consistent about composition?
- What's consistent about subjects?
- What's consistent about lighting?
- What's consistent about emotion?

Output: 8 classification rules
```

**Why This Works**: Patterns are visible in portfolio. No training needed, just analysis.

### Step 2: Create VALIDATION Component

For each rule, define how to *evaluate* it:

```
Rule: "Warm Palette"

VALIDATION:
- Are colors warm (oranges, reds, golds)?
- Are skin tones rendered warm?
- Does palette feel cohesive?
- Score 0–1 based on warmth consistency
```

This is evaluable by any vision model.

### Step 3: Create GENERATION Component

For each rule, define how to *instruct* it:

```
Rule: "Warm Palette"

GENERATION:
- Keywords: "warm colors," "golden tones"
- Instruct: "Apply warm color palette throughout"
- Avoid: "Cool tones," "cyan shadows"
```

This goes into the prompt to the generative model.

### Step 4: Generate with Rules

User provides prompt. System synthesizes with all 8 rules:

```
User Prompt: "Couple at farmer's market"

Synthesized Prompt:
"Couple at farmer's market, candid moment (Rule 1), 
layered composition with market stalls visible (Rule 2), 
couple primary focus (Rule 3), 
warm colors and golden light (Rule 4), 
directional light with shadow structure (Rule 5), 
genuine connection and warmth (Rule 6), 
NYC farmer's market setting (Rule 7), 
peak moment captured (Rule 8)"

Generate → Score → Pass or Soft-Retry
```

### Step 5: Score Generated Image

Vision model evaluates generated image against 8 rules:

```
Generated Image
    ↓
[Vision Model]
    ↓
Rule 1 Score: 0.92
Rule 2 Score: 0.88
Rule 3 Score: 0.95
Rule 4 Score: 0.90
Rule 5 Score: 0.85
Rule 6 Score: 0.87
Rule 7 Score: 0.82
Rule 8 Score: 0.90
    ↓
Combined Score: 0.89 ✅ (Pass)
```

### Step 6: Soft Retry on Failure

If combined score <0.75:

```
Generated Image scores:
Rule 2: 0.65 (Layering failed)

Retry Prompt adds emphasis:
"...layered composition with market stalls 
and products visible in distinct depth planes..."

Regenerate → Re-score
```

---

## Why Runtime Guidance Outperforms Fine-Tuning

### Theoretical Comparison

| Aspect | Fine-Tuning | Runtime Guidance |
|--------|------------|------------------|
| **Data Efficiency** | Needs 100-1000 images | 100 images (analysis only) |
| **Compute** | High (training phase) | Low (no training) |
| **Speed** | Days to retrain | Hours to iterate |
| **Transparency** | Black box | Explicit rules + scores |
| **Portability** | Model-specific | Works with any model |
| **Debuggability** | Hard to know why it fails | Know exactly which rules fail |
| **Iteration** | Expensive (retrain) | Cheap (edit rules) |
| **Generalization** | Often overfits to training data | More robust to novelty |
| **Explainability** | Can't explain learned rules | Can show 8 explicit rules |

### Practical Example: photography classifier

**Fine-Tuning Approach**:
- Upload ~100 best images to Replicate/Modal
- Wait 6–12 hours for training
- Test results
- Results don't feel quite right (color cast off, lost setting context)
- Retrain on a different subset (another 6–12 hours)
- Cost: ~$100–300; multi-day iteration

**Runtime Guidance Approach**:
- Analyze ~100 images (20 min)
- Extract 8 rules (10 min)
- Generate test images (15 min)
- Check scores, see that one rule's GENERATION needs adjustment
- Edit that rule's GENERATION block (5 min)
- Regenerate (15 min)
- Cost: ~$5–10; iteration in hours

---

## Why This Generalizes: Music Example

### Music: Runtime Guidance

**Same Process, Different Domain**:

```
Composer's Portfolio (100 audio clips)
    ↓
Analyze 30 representative clips
    ↓
Extract 8 Rules:
  1. Timbre/Instrumentation (warm, organic, not synthetic)
  2. Harmonic Movement (chord progressions used)
  3. Rhythm & Tempo (consistent groove)
  4. Emotional Arc (builds tension/release)
  5. Production Quality (warm, not hyper-compressed)
  6. Vocal Treatment (intimate, forward in mix)
  7. Genre Context (jazz, not electronic)
  8. Decision-Making (confident phrasing, no hesitation)
    ↓
VALIDATION: How to score a generated audio clip
GENERATION: How to instruct music model
    ↓
User Prompt: "Intimate jazz piece with strings"
    ↓
Synthesize with 8 rules → Generate → Score
    ↓
Delivered: Audio that feels authentic to composer's style
```

**Why It Works**: Music has same dimensional structure as photography (composition, subject, texture, palette, context, emotion, execution, authenticity).

---

## Critical Insight: Explicitness Scales

### The Key Realization

When style is **explicit**, it becomes:
- Teachable (can explain to another person)
- Transferable (works across mediums)
- Testable (can verify if it's honored)
- Iterable (can refine without retraining)
- Forkable (others can adapt it)

When style is **implicit** (learned from data), it becomes:
- Black box (can't explain)
- Locked to one model
- Hard to test (no clear criteria)
- Expensive to iterate (retrain needed)
- Can't fork (model is proprietary)

Runtime guidance forces explicitness.

---

## Scoring: Why 0.75 Threshold?

The threshold of **0.75 / 1.0** is calibrated:

- **Too strict (0.85+)**: Reject too many decent images
- **Too loose (<0.70)**: Accept mediocre images
- **0.75**: "Good enough to share"

**Interpretation**:
- 0.90–1.0 = "This could be in a portfolio or publication"
- 0.80–0.89 = "This is solid work, ship it"
- 0.75–0.79 = "This passes the bar but has minor issues"
- <0.75 = "This needs work or retry"

---

## Soft Retry: Why It Works

When generation fails, simply retry with adjusted prompt:

**Original**: "NYC street vendor, afternoon"
- Scores: 0.92, 0.65 (Rule 2 layering failed), 0.88, ...
- Combined: 0.71 ❌

**Retry**: "NYC street vendor with storefront visible behind, layered depth, afternoon"
- Scores: 0.90, 0.88 (Rule 2 now passes), 0.89, ...
- Combined: 0.78 ✅

**Why This Works**:
- We identified exactly which rule failed (Rule 2)
- We adjusted generation prompt to address it specifically
- Model now has better guidance for that dimension
- Retry is inexpensive (just another generation)

No need to retrain or adjust model. Just be more specific in the prompt.

---

## Limitations & Caveats

### When Runtime Guidance Works Best
✅ Well-defined artistic style (photography, music, writing, design)  
✅ 100+ representative portfolio items  
✅ Creator can articulate their philosophy  
✅ Style has clear dimensional breakdown (8 rules)

### When Runtime Guidance Struggles
❌ Highly idiosyncratic or unclear style  
❌ Very small portfolio (<50 items)  
❌ Style that contradicts itself  
❌ Domains where "quality" is hard to define

### When Fine-Tuning Still Wins
❌ Need pixel-perfect replication  
❌ Style is extremely subtle or implicit  
❌ Have massive training dataset (1000+)  
❌ Have unlimited compute budget

---

## The Future: Hybrid Approaches

Future systems might combine approaches:

```
Runtime Guidance (explicit rules)
    +
Fine-Tuning (implicit patterns)
    =
Best of both worlds
```

But for now, **runtime guidance is cheaper, faster, and more transparent**.

---

## Conclusion

**Runtime guidance works because**:
1. Style is explicit, not statistical
2. Rules are model-agnostic
3. Scoring provides transparency
4. Iteration is fast and cheap
5. Process is auditable

**This opens up creative AI to individuals** without access to fine-tuning infrastructure or ML expertise.

You just need:
- Portfolio
- 7 answers about your philosophy
- Our analysis tool

Then you have a classifier you can use, modify, and share.

---

**See Also**:
- [02-THESIS.md](02-THESIS.md) — broader thesis argument
- [06-CLASSIFIER-FORMAT.md](06-CLASSIFIER-FORMAT.md) — file format reference
- [09-EXTENDING-TO-DOMAINS.md](09-EXTENDING-TO-DOMAINS.md) — applying this pattern to art, design, writing, music
