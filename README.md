# x_make_py_mod_sideload_x — Control Room Lab Notes

> "Sometimes you need to slide a module into place without rattling the rest of the system. This toolkit makes that move surgical."

## Manifesto
x_make_py_mod_sideload_x handles Python module sideloading—resolving dynamic imports, staging packages from alternate paths, and validating that everything behaves before the orchestrator commits. It's the quiet workhorse behind the Road to 0.20.2 bootstrap story.

## 0.20.2 Command Sequence
Version 0.20.2 documents the sideload procedures I trust right now. Use this checklist to mirror the Road to 0.20.2 baseline and you won't blindside the orchestrator with untracked imports.

## Ingredients
- Python 3.11+
- Ruff, Black, MyPy, and Pyright
- Optional: zipapp, importlib resources, and platform-specific hooks you may enable when extending sideload strategies

## Cook Instructions
1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `python -m pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. `python -m x_make_py_mod_sideload_x` or execute the CLI helpers to rehearse your sideload scenario before touching production

## Quality Assurance
| Check | Command |
| --- | --- |
| Formatting sweep | `python -m black .`
| Lint interrogation | `python -m ruff check .`
| Type audit | `python -m mypy .`
| Static contract scan | `python -m pyright`
| Functional verification | `pytest`

## Distribution Chain
- [Changelog](./CHANGELOG.md)
- [Road to 0.20.2 Control Room Ledger](../x_0_make_all_x/Change%20Control/0.20.2/Road%20to%200.20.2%20Engineering%20Proposal.md)
- [Road to 0.20.2 Engineering Proposal](../x_0_make_all_x/Change%20Control/0.20.2/Road%20to%200.20.2%20Engineering%20Proposal.md)

## Cross-Linked Intelligence
- [x_make_common_x](../x_make_common_x/README.md) — provides subprocess, logging, and environment wrappers for sideload operations
- [x_make_github_visitor_x](../x_make_github_visitor_x/README.md) — validates sideloaded code during compliance runs
- [x_0_make_all_x](../x_0_make_all_x/README.md) — orchestrator ensures sideload strategies align with release milestones

## Lab Etiquette
Every sideload path must be documented in the Change Control index—source, destination, rollback plan. No secret imports, no half measures.
