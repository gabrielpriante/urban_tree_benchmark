# CLAUDE.md

Instructions for Claude Code and any other automated assistant working in
this repository. These rules override default assistant behavior.

## 1. Repository boundaries

- Work only inside the `urban_tree_benchmark` repository.
- Do **not** read from, modify, or write to `tree_boxes` or any other
  repository unless the maintainer explicitly asks for a specific read-only
  lookup.
- `tree_boxes` is frozen (research freeze: November 9, 2026). Never copy its
  experimental outputs, figures, or result tables into this repository.
  Reference them by path or commit instead.
- Do not download datasets, model weights, or imagery, and do not create or
  change Python environments, unless explicitly asked.
- Review existing configuration files before editing them. Never overwrite
  them blindly.

## 2. Research organization

- This is ongoing research. Questions, criteria, and methods in `docs/` are
  provisional until a recorded decision makes them final.
- `docs/dataset_registry.md`: never invent dataset characteristics. Any field
  not confirmed against a primary source (paper, official repository, data
  portal, license file) stays marked **Requires verification**. Cite the
  source for each verified field.
- Record significant research decisions in `docs/decision_log.md` using its
  template. Do not edit or delete past entries; add a new entry that
  supersedes the old one.
- Keep the structure minimal. Do not add folders, packages, or frameworks
  without the maintainer's approval.

## 3. Reproducibility requirements

- Every reported number must be traceable to: code version (commit), dataset
  name and version, model name and version or weights checksum, configuration,
  and random seed where relevant.
- Pin dependency versions once an environment is created.
- Do not commit raw or processed imagery, archives, or large outputs (see
  `.gitignore`). Record where data came from and how to get it.
- Keep evaluation scripts deterministic where possible, and document any
  non-determinism (e.g., GPU kernels, VLM sampling).

## 4. Git authorship

- The sole commit author is **Gabriel Penedo**, using the email already
  configured in this repository's Git settings.
- Never change Git author, committer, or user configuration.
- Never add AI tools (Claude, Anthropic, Copilot, ChatGPT, or others) to
  commit authors, `Co-Authored-By` trailers, contributor lists, or repository
  credits.

## 5. Commit and push policy

- Automated assistants must **never** commit, push, tag, create branches,
  merge, rebase, or open pull requests without explicit permission from the
  maintainer for that specific action.
- The maintainer reviews and makes all commits manually (via GitHub Desktop).
- Read-only Git commands (`git status`, `git diff`, `git log`) are allowed for
  reporting changes.
