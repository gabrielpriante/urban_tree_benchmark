# urban_tree_benchmark

Urban tree detection dataset research and model benchmarking.

> **Status: ongoing research.** The evaluation dataset `benchmark_v1` is frozen
> (see below and `docs/decision_log.md`, D-002). Research questions, metrics and
> methods remain provisional. Model results should not be cited until a tagged
> release says they are final.

## Purpose

This repository supports a planned paper for **IGARSS 2027** that evaluates
existing tree-counting and tree-detection models on aerial imagery. The focus
is on **urban forestry**.

The repository is meant to support:

- a systematic investigation of candidate benchmark datasets,
- reproducible evaluation of existing models (not training new ones), and
- clear records of research decisions and how they were made.

## Research objectives (provisional)

1. Identify publicly available aerial-imagery tree datasets suitable for
   independent benchmarking, with attention to urban representation.
2. Evaluate existing tree-detection and counting models on the selected
   datasets.
3. Separate tree-count accuracy from object-localization accuracy, and look at
   repeatability and geographic generalization.
4. Assess how suitable current models are for urban forestry use.

See [docs/research_questions.md](docs/research_questions.md) for the working
questions.

## Planned workflow

1. **Dataset investigation**: record candidates in
   [docs/dataset_registry.md](docs/dataset_registry.md) and check every field
   against primary sources.
2. **Dataset selection**: apply
   [docs/selection_criteria.md](docs/selection_criteria.md) and record the
   outcome in [docs/decision_log.md](docs/decision_log.md).
3. **Method finalization**: fix metrics, sampling, and evaluation protocol in
   [docs/methodology.md](docs/methodology.md).
4. **Environment setup**: dataset pipeline dependencies pinned in
   `requirements.txt`; model versions to be pinned before evaluation.
5. **Evaluation**: run the benchmark with documented configurations.
6. **Reporting**: summarize results for the paper.

## Repository layout

```
urban_tree_benchmark/
├── README.md            Project overview (this file)
├── LICENSE              MIT License (original code and documentation only)
├── requirements.txt     Pinned dependencies for the dataset pipeline
├── scripts/             Five-script pipeline that rebuilds benchmark_v1
├── docs/
│   ├── research_questions.md
│   ├── dataset_registry.md
│   ├── selection_criteria.md
│   ├── methodology.md
│   ├── decision_log.md
│   ├── benchmark_v1_selection.csv   Selected source IDs and source versions
│   ├── benchmark_v1_manifest.csv    Frozen benchmark manifest (exact bytes)
│   └── benchmark_v1_SHA256SUMS      Checksums of every benchmark file
├── data/                Local data (contents not tracked by Git)
├── src/                 Evaluation code (none yet)
└── results/             Experiment outputs (large outputs not tracked)
```

## benchmark_v1 (frozen evaluation dataset)

500 aerial RGB images with their original reference annotations:

| Source | Images | Reference | Ground sampling distance |
|---|---|---|---|
| NeonTreeEvaluation v0.2.2 (22 NEON sites) | 193 | 6,629 crown bounding boxes (original XML) | ~0.10 m |
| Ventura urban tree detection, 2020 imagery (8 California cities) | 307 | 18,308 tree-point records (original CSV) | 0.60 m |

Images and annotations are **not** redistributed here. The repository holds the
code and the records needed to rebuild and verify them from the original sources.

### Rebuild from the original sources

Requires Python 3.12, Git, about 5 GB of disk space and internet access.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt   # Windows: .venv\Scripts\pip
python scripts/fetch_neon.py       # Zenodo 10.5281/zenodo.5914554, MD5-verified
python scripts/prepare_neon.py
python scripts/fetch_ventura.py    # pinned Git revision 78e81bdbb484048472e77cbedd3afb49a6b621c6
python scripts/prepare_ventura.py
python scripts/build_benchmark.py  # offline; refuses output that differs from the selection file
sha256sum -c docs/benchmark_v1_SHA256SUMS
```

Run the Python commands with the environment's interpreter. Annotation checksums
do not depend on library versions. Image checksums assume the pinned Pillow
build: PNG encoding can differ between versions even when pixels are identical.
Selection rules, exclusions and known limitations are documented in
`docs/decision_log.md` (D-002) and [data/README.md](data/README.md).

### Licensing and attribution

This repository does **not** redistribute the 500 source images or their
annotations. It contains scripts and metadata (identifiers, counts, checksums)
for rebuilding the benchmark from the original sources, whose own terms apply.

- **This repository**: the acquisition, preparation and assembly code and the
  project documentation are released under the MIT License (see `LICENSE`).
  The MIT License does not cover the NEON or Ventura imagery and annotations.
- **NeonTreeEvaluation** (https://github.com/weecology/NeonTreeEvaluation):
  the pipeline downloads the pinned Zenodo release v0.2.2,
  https://zenodo.org/records/5914554, whose record lists **CC BY 4.0**. The
  GitHub repository (commit `96b29d5`) carries a **CC0 1.0** licence file. We
  treat the Zenodo CC BY 4.0 terms as applying to the files we use and
  attribute accordingly. Cite: Weinstein, B., Marconi, S., & White, E. (2022).
  *Data for the NeonTreeEvaluation Benchmark* (v0.2.2) [Data set]. Zenodo.
  https://doi.org/10.5281/zenodo.5914554; and Weinstein, B. G. et al. (2021),
  *PLOS Computational Biology* 17(7): e1009180. The imagery originates from
  the National Ecological Observatory Network Airborne Observation Platform;
  NEON's current data policies are not assumed to change the terms of this
  historical release.
- **Ventura urban tree detection**
  (https://github.com/jonathanventura/urban-tree-detection-data): imagery and
  point annotations are the original authors' work; the repository's README
  states **CC BY 4.0**, which requires attribution. Cite: Ventura, J. et al.
  (2024), *International Journal of Applied Earth Observation and
  Geoinformation* 130: 103848. Imagery from the USDA National Agriculture
  Imagery Program (NAIP).

## Data policy

Raw imagery, processed rasters, archives, and large outputs are **not**
committed. See [data/README.md](data/README.md) and
[results/README.md](results/README.md).

## Authorship

Gabriel Penedo, Frontline Labs.
