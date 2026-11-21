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
