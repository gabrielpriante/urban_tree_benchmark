# Dataset Registry

Verified status of candidate datasets for tree-detection benchmarking.
Selection rules and limitations for benchmark_v1 are recorded in
`decision_log.md` (D-002). Unresolved items are labelled as such.

_Last updated: 2026-11-21_

## Summary

| Dataset | Status | Reference type | Role |
|---|---|---|---|
| NEON Tree Evaluation | Verified, selected, prepared | Crown bounding boxes (image-annotated) | benchmark_v1: 193 images |
| Ventura Urban Tree Detection | Verified, selected, prepared | Tree points (image-annotated) | benchmark_v1: 307 images |
| Schütte et al. (2025), Berlin/Osnabrück | Evaluated, not selected for v1 | Crown polygons | Possible future dataset |
| Campo Grande, Zamboni et al. (2021) | Evaluated, not selected for v1 | Bounding boxes | Deprioritized |
| OAM-TCD, DeepTrees-Halle, MillionTrees | Desk review only | Mixed | Not selected (see bottom) |

---

## 1. NEON Tree Evaluation — verified, selected, prepared

| Field | Value |
|---|---|
| Source | Zenodo release v0.2.2, https://doi.org/10.5281/zenodo.5914554 (record lists CC BY 4.0); GitHub https://github.com/weecology/NeonTreeEvaluation (CC0 1.0 licence file) |
| Publication | Weinstein, B. G. et al. (2021), *PLOS Computational Biology* 17(7): e1009180 |
| Geography | NEON field sites across the USA; forests and woodlands (not urban) |
| Eligible pool | 194 RGB images with image-annotated XML (226 XMLs, 2,289 RGB TIFFs in the archives) |
| Selected (benchmark_v1) | **193 images, 6,629 crown boxes, 22 sites** (2017: 3, 2018: 148, 2019: 42) |
| Imagery | 3-band 8-bit RGB GeoTIFF, mostly 400 × 400 px, approximately 0.10 m GSD |
| Ground truth | Visual image annotation intended to cover every visible tree in each plot (paper); a second annotator relabelled 71 plots. Not an independently field-verified census |
| Exclusion | `SJER_016_2018`: lies inside hand-annotated training tile `2018_SJER_3_258000_4106000_image` |
| Unresolved | `2018_SJER_3_252000_4113000_image_323` may overlap training crop `..._image_310`; LiDAR pseudo-label coverage of evaluation plots in DeepForest's training is undocumented |
| Limitations | Images are clustered within sites (SJER and TEAK dominate); visual QA found apparent omissions of small or shadowed trees (e.g. `2018_TEAK_3_318000_4103000_image_261`, `JERC_056_2018`); source orthorectification distortion in some crowns. Published totals differ from the files (e.g. 207 images / 6,926 trees in Weinstein et al. 2021, *eLife*; 6,490 trees in the dataset paper); counts here come from the files |

## 2. Ventura Urban Tree Detection — verified, selected, prepared

| Field | Value |
|---|---|
| Source | https://github.com/jonathanventura/urban-tree-detection-data @ `78e81bdbb484048472e77cbedd3afb49a6b621c6` (CC BY 4.0 per README) |
| Publication | Ventura, J. et al. (2024), *Int. J. Applied Earth Observation and Geoinformation* 130: 103848 |
| Geography | Eight California cities: Bishop, Chico, Claremont, Eureka, Long Beach, Palm Springs, Riverside, Santa Monica |
| Available | 1,651 images (NAIP 2016/2018/2020) of **604 distinct locations**; **96,547** point annotations in the files (README states 95,972; paper 96,425) |
| Selected (benchmark_v1) | **307 images from 2020**, one per location (Bishop 10, Eureka 21, 46 per other city; seed 20261121) |
| Selected references | **18,308 point records, 18,289 unique coordinates** (19 exact duplicates in 10 images, preserved unchanged) |
| Imagery | 256 × 256 px NAIP, 4 bands (R, G, B, NIR); bands 1–3 used; approximately 0.60 m GSD |
| Ground truth | Manual image annotation seeded from municipal inventories and extended to all visible trees, including private property (paper §2.2). Not field-verified coordinates |
| Selection safeguards | Overlapping footprints (>1 pixel) replaced deterministically: `palm_springs_2020_41` → `_1`, `_65` → `_2`. Shared borders allowed |
| Limitations | Official splits reuse locations across years (not used); same-city tiles are spatially clustered; 60 cm imagery is coarse for crown detectors trained at about 10 cm; two selected images contain no trees in the source |

## 3. Schütte et al. (2025), Berlin/Osnabrück — evaluated, not selected for v1

| Field | Value |
|---|---|
| Source | Zenodo v2, https://doi.org/10.5281/zenodo.17721877 (CC BY 4.0); publication doi:10.1109/JSTARS.2025.3626942 |
| Content | 30 study areas (Berlin 24, Osnabrück 6), Germany; 14,677 crown polygons with per-crown urban environment classes (7 in Berlin, 5 in Osnabrück) |
| Imagery | 20 cm orthophotos (Berlin 2020, Osnabrück 2023), false-colour and RGB renderings |
| Open questions | Annotation completeness (all visible trees vs. inventory-guided trees) unresolved; Berlin RGB provenance uncertain (red/green differ from the false-colour rendering; blue lacks a typical vegetation signature); mixed 8/16-bit RGB files |
| Preprocessing notes | Osnabrück crowns (EPSG:25833) must be reprojected to the rasters (EPSG:25832); class IDs differ between cities |
| Assessment | Possible future urban dataset for recall and per-environment analysis once completeness and RGB provenance are confirmed with the authors |

## 4. Campo Grande, Zamboni et al. (2021) — evaluated, not selected for v1

| Field | Value |
|---|---|
| Source | https://github.com/pedrozamboni/individual_urban_tree_crown_detection (no licence file); publication doi:10.3390/rs13132482 |
| Content | 220 RGB patches (512 × 512 px, 10 cm) from two 2013 orthoimages of one city; 3,382 bounding boxes |
| Findings | About 575 boxes are halves of crowns split across patch borders, so at most about 2,807 distinct trees; patches are not georeferenced (grid layout reconstructable); 29 zero-area slivers; repeated random folds |
| Reasons deprioritized | Unclear redistribution and licensing terms; very limited geographic independence (one city, one date, about 0.58 km²); crown fragmentation complicates counting |

## Other candidates (desk review only)

| Dataset | Finding |
|---|---|
| OAM-TCD (Restor, 2024) | Global 10 cm imagery, 5,072 tiles; annotations do not target every tree (closed canopy labelled as groups), so unsuitable for counting |
| DeepTrees-Halle (2026) | Halle, Germany; 241 tiles at 20 cm with tree/cluster/unsure polygon classes; completeness not documented |
| MillionTrees | Aggregation framework, not an independent source; modifies its components (tiling, geometry conversion, model-based filtering, re-mapped splits); original sources preferred |
