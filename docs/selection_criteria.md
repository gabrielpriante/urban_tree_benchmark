# Dataset Selection Criteria

> **Status: PROVISIONAL.** These criteria guide dataset screening. Weights and
> thresholds will be finalized after the initial registry verification and
> recorded in `decision_log.md`.

_Last updated: 2026-11-21_

Each candidate in `dataset_registry.md` is assessed against the criteria
below. Ratings: **Meets / Partially meets / Does not meet / Unknown**. A
dataset rated **Unknown** on any required criterion cannot be selected until
that criterion is resolved.

## Required criteria

### C1. Independent ground truth
- Labels come from a documented process (field survey, expert image
  annotation, LiDAR-supported delineation, etc.), not from the outputs of a
  model being evaluated.
- The annotation protocol and quality control are described well enough to
  judge reliability.

### C2. Model-training overlap
- Determine whether any part of the dataset (including the test split) was
  used to train, fine-tune, or select the models under evaluation.
- Overlapping datasets may still be used, but must be reported as
  **in-distribution** and analyzed separately from independent test data.
- For aggregation frameworks (e.g., MillionTrees), assess overlap for each
  component.

### C3. Annotation compatibility
- Annotation geometry (box, point, polygon, mask) can be compared with model
  outputs without heavy, lossy conversion.
- Any conversions (e.g., polygon to box, box to point) are documented and
  their effect on metrics is considered.
- The annotation unit (individual crown vs. canopy group) matches the
  counting task.

### C4. Data licensing
- The license allows research use and publication of derived results.
- Redistribution limits are noted. If redistribution is not allowed, only
  access instructions and derived metrics are shared.

### C5. Image resolution
- Ground sampling distance is fine enough to resolve individual crowns in the
  target setting.
- Resolution is compatible with the models' expected input, or resampling
  needs are documented.

## Desired criteria

### C6. Urban representation
- The dataset includes urban scenes (street trees, parks, residential areas,
  mixed impervious surfaces).
- The amount and type of urban content is documented.

### C7. Geographic diversity
- Coverage of multiple regions, climates, or cities, to support
  generalization analysis.
- The geographic distribution relative to model training data is described.

### C8. Accessibility and documentation
- Data can be obtained through a stable, public channel with versioning.
- Metadata (sensor, acquisition date, georeferencing) is available.

### C9. Scale and split integrity
- There are enough images and annotations for meaningful evaluation.
- Official train/test splits exist and do not leak data (e.g., no spatially
  adjacent tiles across splits).

## Screening record template

| Dataset | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | Decision | Decision log ref |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NEON Tree Evaluation | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | |
| OAM-TCD | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | |
| Urban Tree Detection (Ventura et al.) | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | |
| DeepTrees-Halle | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | |
| MillionTrees (framework; assess per component) | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Pending | |
