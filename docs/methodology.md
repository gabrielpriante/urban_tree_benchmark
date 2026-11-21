# Methodology (Provisional Outline)

> **Status: PROVISIONAL OUTLINE.** Metrics, sampling strategies, and
> evaluation protocols are **not final**. They will be set after the dataset
> investigation is complete, and each choice will be recorded in
> `decision_log.md`.

_Last updated: 2026-11-21_

## 1. Scope

- Evaluate **existing** tree-detection and tree-counting models on aerial
  imagery. Training new models is out of scope unless a recorded decision
  changes this.
- Candidate model families (to be confirmed): specialized tree detectors
  (e.g., DeepForest) and vision-language models.
- Datasets: selected from `dataset_registry.md` using `selection_criteria.md`.

## 2. Evaluation dimensions

The benchmark keeps four dimensions separate, because a model can do well on
one and poorly on another (e.g., correct totals from offsetting false
positives and false negatives).

### 2.1 Tree-count accuracy
- **Question:** Does the predicted number of trees per image or area match
  the reference count?
- **Candidate measures (not final):** absolute and relative count error, bias
  (over- or under-counting), and agreement statistics across images.
- **Open issues:** handling contiguous canopy, partially visible trees at tile
  edges, and minimum tree size.

### 2.2 Object localization accuracy
- **Question:** Are individual trees detected in the correct locations?
- **Candidate measures (not final):** precision, recall, and F1 under a
  matching rule. Average precision where box-based outputs allow it.
- **Open issues:** the matching rule (IoU threshold vs. point-in-polygon vs.
  centroid distance), which depends on annotation geometry. Vision-language
  model outputs may not support localization metrics.

### 2.3 Repeatability
- **Question:** Are outputs stable across repeated runs and small
  methodological changes?
- **Candidate factors (not final):** repeated inference (especially for
  vision-language models), tile size and overlap, resampling, confidence
  thresholds, and prompt wording.
- **Open issues:** number of repetitions and which variability statistics to
  report.

### 2.4 Generalization
- **Question:** How does performance change across geographies, canopy
  conditions, and urban vs. non-urban settings?
- **Candidate stratifications (not final):** dataset, site or city, urban
  context, canopy density, and in-distribution vs. independent data (see
  selection criterion C2).
- **Open issues:** defining strata consistently across datasets with
  different metadata.

## 3. Sampling (to be determined)

- Whether to use full test splits or stratified subsets.
- Tile sizes and handling of tile boundaries.
- Whether manual re-annotation or auditing of a subset is needed.

No sampling strategy will be adopted before the dataset investigation is
complete.

## 4. Reproducibility protocol (planned)

- Pin software and model versions, and record checksums for model weights.
- Record dataset versions and access dates.
- Store evaluation configurations alongside results.
- Fix random seeds where applicable, and document any non-determinism.
- Link every reported result to a commit in this repository.

## 5. Relationship to pilot experiments

Earlier pilot experiments (frozen 2026-11-09; not part of this repository) inform which questions
and failure modes to study. Pilot outputs are not reused as benchmark
results. Any methodological lesson taken from the pilot is cited in
`decision_log.md`.
