# Research Decision Log

A chronological record of significant research decisions: dataset selection,
metric choices, scope changes, and protocol changes.

**Rules**
- Add new entries at the bottom, numbered in order (`D-001`, `D-002`, ...).
- Do not edit or delete past entries. To reverse or change a decision, add a
  new entry and set the earlier entry's status to `Superseded by D-XXX`.
- Use ISO dates (`YYYY-MM-DD`).
- Cite evidence (registry entries, papers, pilot results in `tree_boxes` by
  path/commit) rather than repeating it.

---

## Entry template

```markdown
### D-XXX: <Short title>

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by D-XXX | Rejected
- **Decided by:** <name>
- **Related documents:** <e.g., dataset_registry.md#2-oam-tcd, methodology.md §2.2>

**Context**
<What question or problem required a decision?>

**Decision**
<What was decided?>

**Alternatives considered**
1. <Alternative>: <why not chosen>
2. <Alternative>: <why not chosen>

**Justification**
<Reasoning and evidence supporting the decision.>

**Consequences / follow-up**
<Effects on other documents, open tasks, risks.>
```

---

## Entries

### D-001: Establish separate repository for expanded benchmark

- **Date:** 2026-11-21
- **Status:** Accepted
- **Decided by:** Gabriel Penedo
- **Related documents:** README.md, CLAUDE.md

**Context**
Pilot experiments with DeepForest and vision-language models were done in
`tree_boxes`, which was frozen on 2026-11-09. Further work (dataset
investigation, benchmark evaluation, reproducible documentation) needs a home
that leaves the pilot record unchanged.

**Decision**
Create `urban_tree_benchmark` as a separate repository. Pilot outputs are not
copied into it and are cited by reference only.

**Alternatives considered**
1. Continue work in `tree_boxes`: rejected because it would break the
   research freeze.
2. Copy pilot outputs into the new repository: rejected because it would
   duplicate data and blur the line between pilot and benchmark results.

**Justification**
Keeps the frozen pilot record intact and gives the benchmark its own
documentation and data policy.

**Consequences / follow-up**
All references to pilot findings must cite `tree_boxes` explicitly.

### D-002: benchmark_v1 composition and selection rules (193 NEON + 307 Ventura)

- **Date:** 2026-11-21
- **Status:** Proposed (pending maintainer review and full-download validation)
- **Decided by:** Gabriel Penedo
- **Related documents:** data/README.md, docs/benchmark_v1_selection.csv, scripts/

**Context**
The first paper needs a fixed, reproducible evaluation set combining an urban
dataset (Ventura) with a forest dataset (NEON) using only existing reference
labels. File-level reconnaissance established the eligible pools.

**Decision**
1. *NEON* (NeonTreeEvaluation v0.2.2, Zenodo 10.5281/zenodo.5914554): every
   image with both `annotations/<id>.xml` and `evaluation/RGB/<id>.tif`
   (194), minus `SJER_016_2018` = **193 images, 6,629 crown boxes, 22 sites**
   (2017: 3, 2018: 148, 2019: 42). Original XML boxes are kept as references.
2. *Ventura* (urban-tree-detection-data @ `78e81bdbb484048472e77cbedd3afb49a6b621c6`,
   audited as `78e81bd`): 2020 imagery only (604 locations, one image each).
   All Bishop (10) and Eureka (21) locations; 46 per remaining six cities drawn
   with `random.Random(20261121).sample()` from index-sorted candidates, cities
   in alphabetical order = **307 images, 307 locations**. Original CSV points
   are kept as references (18,308 stored points).
3. *Overlap rule (Ventura):* footprints overlapping by more than one pixel in
   both axes (shared borders allowed) are not both kept. Within a city, drawn
   tiles are kept in ascending index order; a tile overlapping a kept tile is
   replaced by the lowest-index unselected tile of the same city that overlaps
   no kept tile. Applied twice: `palm_springs_2020_41` -> `palm_springs_2020_1`
   and `palm_springs_2020_65` -> `palm_springs_2020_2` (verified from TIFF
   georeferencing of all 604 2020 tiles; 6 overlapping pairs exist in 2020).
4. The final list of source IDs and versions is frozen in
   `docs/benchmark_v1_selection.csv`; `build_benchmark.py` refuses any mismatch.

**Alternatives considered**
1. 250 NEON images: rejected; only 194 image-annotated images exist, and
   padding with unannotated other-year copies, field-reference imagery or
   training tiles would not be equivalent evaluation data.
2. Ventura images from all years: rejected; the same locations recur across
   2016/2018/2020 and would inflate apparent independence.
3. Converting Ventura points to boxes: rejected; reference types stay distinct.

**Justification**
Uses only complete reference labels, one image per Ventura location, pinned
source versions and a fixed seed, so the selection is reproducible.

**Known limitations**
- NEON images are clustered within sites (SJER 61 and TEAK 51 of the 194
  eligible images; nearest plots 70-93 m apart); report site-level results and use
  site-resampled confidence intervals.
- NEON training exposure: `SJER_016_2018` (excluded) lies inside hand-annotated
  training tile `2018_SJER_3_258000_4106000_image`. **Unresolved:**
  `2018_SJER_3_252000_4113000_image_323` shares 1 km tile 252000_4113000 with
  training crop `..._image_310`; LiDAR pseudo-label pretraining coverage of
  evaluation plots is undocumented.
- The DeepForest checkpoint used in `tree_boxes` is `weecology/deepforest-tree`
  @ `cc21436bc5d572dde8ff5f93c1e71a32f563cace` (model.safetensors SHA-256
  `d37a7af0b5ba2754282a80d41b4c7b66e8c7149234df5bf3f41bdaf57d329fc8`,
  DeepForest 2.1.0). Its model card documents NEON-based training (LiDAR
  pseudo-labels plus hand annotations from "select sites"); no Ventura exposure
  is documented, but the exact training image list is not published.
- Ventura: 44 border-touching 2020 tile pairs remain allowed; same-city tiles
  are spatially clustered. 10 selected images contain 19 exact duplicate points
  (e.g. `claremont_2020_43`: one point repeated 9 times); labels are unchanged.
  `eureka_2020_3` and `palm_springs_2020_57` have no trees in the source and
  carry header-only CSVs (`annotation_origin = absent_in_source`).
- Resolution differs (NEON ~0.10 m, Ventura 0.60 m) and reference types differ
  (boxes vs points); datasets are analysed separately.

**Consequences / follow-up**
Run the five scripts after approving the full downloads (~3.85 GB NEON
archive, ~450 MB Ventura checkout); confirm the real run reproduces
`docs/benchmark_v1_selection.csv`, then set this entry to Accepted.
