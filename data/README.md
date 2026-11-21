# data/

Local working directory for datasets. **Contents are not tracked by Git**;
only this README is committed (see `.gitignore`).

## Policy

- Do not commit raw imagery, processed rasters, annotations downloaded from
  third parties, or archives.
- Record each dataset's source, version, license, and access date in
  `docs/dataset_registry.md`.
- Keep downloaded data unchanged. Write derived or processed data to a
  separate subfolder.

## Suggested local layout (not yet in use)

```
data/
├── raw/         Original downloads, unmodified
└── processed/   Derived tiles, converted annotations, etc.
```

No data has been downloaded yet.
