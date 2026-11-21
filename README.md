# urban_tree_benchmark

Urban tree detection dataset research and model benchmarking.

> **Status: ongoing research.** This repository is not a finished benchmark.
> Research questions, dataset choices, and methods are provisional and will
> change as the investigation goes on. Results should not be cited until a
> tagged release says they are final.

## Purpose

This repository supports a planned paper for **IGARSS 2027** that evaluates
existing tree-counting and tree-detection models on aerial imagery. The focus
is on **urban forestry**.

The repository is meant to support:

- a systematic investigation of candidate benchmark datasets,
- reproducible evaluation of existing models (not training new ones), and
- clear records of research decisions and how they were made.

## Relationship to prior work (`tree_boxes`)

Pilot experiments using DeepForest and vision-language models were done in a
separate repository, `tree_boxes`. That repository is **frozen** as of
**November 9, 2026**.

- `tree_boxes` is the record of the pilot phase. It stays unchanged.
- This repository does **not** contain copies of pilot outputs. Where pilot
  findings shape decisions here, they are cited by reference (repository,
  freeze date, and file path or commit) in `docs/decision_log.md`.

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
4. **Environment setup**: pin dependencies and model versions (not done yet).
5. **Evaluation**: run the benchmark with documented configurations.
6. **Reporting**: summarize results for the paper.

## Repository layout

```
urban_tree_benchmark/
├── README.md            Project overview (this file)
├── CLAUDE.md            Rules for automated assistants working in this repo
├── docs/
│   ├── research_questions.md
│   ├── dataset_registry.md
│   ├── selection_criteria.md
│   ├── methodology.md
│   └── decision_log.md
├── data/                Local data (contents not tracked by Git)
├── src/                 Evaluation code (none yet)
└── results/             Experiment outputs (large outputs not tracked)
```

## Data policy

Raw imagery, processed rasters, archives, and large outputs are **not**
committed. See [data/README.md](data/README.md) and
[results/README.md](results/README.md).

## Authorship

Gabriel Penedo, Frontline Labs.
