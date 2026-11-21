# data/

Local working directory for datasets. **Contents are not tracked by Git**;
only this README is committed (see `.gitignore`).

## Policy

- Do not commit raw imagery, processed rasters, annotations downloaded from
  third parties, or archives.
- Record each dataset's source, version, license, and access date in
  `docs/dataset_registry.md`.
- Keep downloaded data unchanged. Write derived data to a separate subfolder.

## Pipeline (benchmark_v1)

Run from the project root (Python 3.12, `pip install -r requirements.txt`,
Git on PATH):

```powershell
python scripts/fetch_neon.py       # Zenodo 5914554 (v0.2.2): annotations.zip + evaluation.zip, MD5-verified (~3.85 GB)
python scripts/prepare_neon.py     # 193 image-annotated NEON images (SJER_016_2018 excluded)
python scripts/fetch_ventura.py    # urban-tree-detection-data @ 78e81bdbb484048472e77cbedd3afb49a6b621c6 (~450 MB)
python scripts/prepare_ventura.py  # 307 Ventura 2020 images, one per location (seed 20261121)
python scripts/build_benchmark.py  # offline; freezes the 500-image benchmark_v1
```

Each script stops with an error rather than overwriting existing data. To
rebuild a prepared dataset, delete its folder deliberately. `benchmark_v1` is
never overwritten; build a new version instead.

## Layout

```
data/
├── raw/
│   ├── neon/        Original Zenodo archives, unmodified
│   └── ventura/     Shallow Git checkout at the pinned revision, unmodified
├── prepared/
│   ├── neon/        images/*.png (RGB), annotations/*.xml (original boxes), manifest.csv
│   └── ventura/     images/*.png (bands 1-3), annotations/*.csv (original points), manifest.csv
└── benchmark_v1/    images/, annotations/, manifest.csv (with SHA-256 per file)
```

Benchmark identifiers are source-prefixed, e.g. `neon__SJER_052_2018` and
`ventura__bishop_2020_0`. NEON references are crown boxes (XML) and Ventura
references are tree points (CSV); they are never converted into each other.

Selection rules, exclusions and known limitations are recorded in
`docs/decision_log.md` (D-002). The expected list of source IDs and versions is
version-controlled in `docs/benchmark_v1_selection.csv`, and
`build_benchmark.py` refuses to freeze a benchmark that does not match it.
