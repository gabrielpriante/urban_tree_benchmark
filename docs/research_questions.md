# Research Questions

> **Status: PROVISIONAL.** These questions are working drafts. They will be
> refined after the dataset investigation, and any change should be recorded
> in `decision_log.md`.

_Last updated: 2026-11-21_

## Central question (provisional)

**RQ0.** How accurately and reliably do existing, publicly available
tree-detection and tree-counting models perform on aerial imagery when tested
against independent ground truth, especially in urban settings?

## Secondary questions (provisional)

### RQ1: Accuracy
How close are model-predicted tree counts to reference counts, and how does
count accuracy compare with object-level detection accuracy?

### RQ2: Counting consistency
Are model outputs consistent across repeated runs, small input changes (tile
size, overlap, resampling), and inference settings? For vision-language
models, how much do outputs vary between runs?

### RQ3: Geographic generalization
How does performance change across regions, biomes, and cities, especially
outside the geographic distribution of each model's training data?

### RQ4: Canopy complexity
How does performance depend on canopy conditions such as crown overlap,
canopy closure, tree size, species mix, shadows, and contiguous canopy
compared with isolated trees?

### RQ5: Urban applicability
Do models validated mostly on natural or managed forests work in urban
environments (street trees, parks, residential areas, mixed impervious
surfaces), and what failure modes appear?

## Open issues to resolve

- Define "tree count" for contiguous canopy, where individual crowns may be
  hard to separate.
- Decide which model families are in scope (e.g., specialized detectors such
  as DeepForest, general-purpose vision-language models).
- Determine how pilot findings from `tree_boxes` (frozen 2026-11-09) inform,
  but do not substitute for, these questions.
