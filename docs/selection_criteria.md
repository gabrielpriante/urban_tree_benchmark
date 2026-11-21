# Dataset Selection Criteria

> **Status: applied for benchmark_v1.** The criteria below were used to select
> the datasets in benchmark_v1. The selection is recorded in `decision_log.md`
> (D-002); dataset details are in `dataset_registry.md`.

_Last updated: 2026-11-21_

Ratings: **Meets / Partially meets / Does not meet / Unknown**. A dataset rated
**Unknown** on a required criterion is not selected until that criterion is
resolved.

## Required criteria

### C1. Documented ground truth
- Labels come from a documented process (field survey, expert image
  annotation, LiDAR-supported delineation, etc.), not from the outputs of a
  model being evaluated.
- The protocol, including whether every visible tree was labelled, is
  described well enough to judge reliability.

### C2. Model-training overlap
- Determine whether any part of the dataset was used to train, fine-tune, or
  select the models under evaluation.
- Known overlaps are excluded or reported as **in-distribution**.
- For aggregation frameworks (e.g., MillionTrees), assess each component.

### C3. Annotation compatibility
- Annotation geometry can be compared with model outputs without heavy, lossy
  conversion; any matching rule or conversion is documented.
- The annotation unit (individual tree vs. canopy group) matches the counting
  task.

### C4. Data licensing
- The licence allows research use and publication of derived results.
- Where redistribution is limited, only access instructions and derived
  metadata are shared.

### C5. Image resolution
- Ground sampling distance resolves individual crowns, or resampling needs are
  documented.

## Desired criteria

- **C6. Urban representation**: urban scenes are included and documented.
- **C7. Geographic diversity**: multiple regions, climates, or cities.
- **C8. Accessibility and documentation**: stable, versioned public access
  with sensor, date, and georeferencing metadata.
- **C9. Scale and independence**: enough images and annotations, and a
  sample that avoids repeated or overlapping footprints.

## Screening results

| Dataset | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| NEON Tree Evaluation | Meets | Partially meets | Meets | Meets | Meets | Does not meet | Meets | Meets | Partially meets | **Selected** (forest) |
| Ventura Urban Tree Detection | Meets | Meets¹ | Partially meets | Meets | Partially meets | Meets | Partially meets | Meets | Meets | **Selected** (urban) |
| Schütte et al. (2025) | Unknown | Not assessed | Meets | Meets | Meets | Meets | Partially meets | Partially meets | Meets | Not selected for v1 |
| Campo Grande (Zamboni et al. 2021) | Partially meets | Not assessed | Meets | Unknown | Meets | Meets | Does not meet | Partially meets | Does not meet | Not selected for v1 |
| OAM-TCD | Does not meet (for counting) | Not assessed | Partially meets | Partially meets | Meets | Partially meets | Meets | Meets | Not assessed | Not selected |
| DeepTrees-Halle | Unknown | Not assessed | Meets | Meets | Meets | Not assessed | Does not meet | Partially meets | Not assessed | Not selected |
| MillionTrees | Not applicable (framework) | Assess per component | — | — | — | — | — | — | — | Not used; original sources preferred |

"Not assessed" means the dataset was set aside before that criterion was
investigated; it is not a negative finding.

¹ No exposure is documented for the pinned DeepForest checkpoint
(`weecology/deepforest-tree` @ `cc21436b`); models trained on MillionTrees,
which includes Ventura's training split, may have seen Ventura images.

## Why NEON and Ventura were selected

The two datasets complement each other and both provide reference labels that
aim to cover every visible tree, which counting and precision metrics require.
NEON supplies high-resolution forest imagery from many sites; Ventura supplies
urban imagery from several cities. Both are openly licensed, versioned, and
reproducible from pinned sources. Their reference types (boxes vs. points) and
resolutions (0.10 m vs. 0.60 m) differ, so they are evaluated separately.

### NEON Tree Evaluation — selected (primary forest benchmark)
- **Annotation:** crown bounding boxes drawn by visual image interpretation,
  intended to cover every visible tree in each 40 m plot; a second annotator
  relabelled 71 plots. Not an independently field-verified census.
- **Coverage:** 193 images, 6,629 crown boxes, 22 forest sites across the USA;
  about 0.10 m resolution; NeonTreeEvaluation Zenodo v0.2.2.
- **Suitability:** broad geographic and forest-type diversity at the
  resolution DeepForest was developed for.
- **Limitations:** one image with known training overlap (`SJER_016_2018`) is
  excluded; further potential training exposure of DeepForest is unresolved;
  visual QA found apparent omissions of small or shadowed trees; images are
  clustered within sites.

### Ventura Urban Tree Detection — selected (primary urban benchmark)
- **Annotation:** tree-centre points annotated manually on the imagery, seeded
  from municipal inventories and extended to all visible trees including
  private property. Not field-verified coordinates.
- **Coverage:** 1,651 original images of 604 unique locations with 96,547
  point annotations, in eight California cities. benchmark_v1 uses 307 images
  from 2020, one per location, with 18,308 point records (including 19 exact
  duplicate records, preserved unchanged); about 0.60 m resolution.
- **Suitability:** the only verified, openly licensed source with
  comprehensive-intent annotations across several urban settings.
- **Limitations:** coarse resolution for crown detectors; points require a
  documented matching rule for box predictions; same-city tiles are spatially
  clustered. Selected footprints do not overlap (two deterministic
  replacements), and the official splits, which reuse locations across years,
  are not used.

### Schütte et al. (2025), Berlin/Osnabrück — not selected for v1
- **Annotation:** about 14,677 manually delineated crown polygons with
  per-crown urban environment classes, guided by municipal tree registers.
- **Coverage:** 30 large study areas in Berlin and Osnabrück, Germany; 20 cm
  orthophotos.
- **Why not selected:** whether every visible tree was delineated is
  unresolved; Berlin RGB provenance is uncertain; Osnabrück crowns need
  reprojection and class IDs differ between cities.
- **Outlook:** a possible future benchmark for recall and per-environment
  analysis once completeness and RGB provenance are confirmed.

### Campo Grande, Zamboni et al. (2021) — not selected for v1
- **Annotation:** 3,382 manually drawn bounding boxes on 220 RGB patches.
- **Coverage:** 10 cm imagery from two orthomosaics of a single city.
- **Why not selected:** about 575 boxes are fragments of crowns split across
  patch borders; very limited geographic independence; no licence file and
  unclear redistribution terms.

### Other screened datasets
- **OAM-TCD:** global 10 cm imagery, but annotations do not target every tree
  (closed canopy is labelled as groups), so it does not support counting;
  images carry mixed CC BY, CC BY-NC and CC BY-SA licences.
- **DeepTrees-Halle:** a single German city at 20 cm; annotation completeness
  is not documented.
- **MillionTrees:** an aggregation framework that modifies its components
  (tiling, geometry conversion, model-based filtering, re-mapped splits);
  original sources are preferred.
