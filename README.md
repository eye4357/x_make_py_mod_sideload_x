# x_make_py_mod_sideload_x — Control Room Lab Notes

> "Sometimes you need to slide a module into place without rattling the rest of the system. This toolkit makes that move surgical."

## Manifesto
x_make_py_mod_sideload_x handles Python module sideloading—resolving dynamic imports, staging packages from alternate paths, and validating that everything behaves before the orchestrator commits. It's the quiet workhorse behind the Road to 0.20.4 bootstrap story.

## 0.20.4 Command Sequence
Version 0.20.4 threads sideload manifests directly into the expanded Kanban. Every injection run now tags its evidence so the Static Gauntlet and Environment Provisioning columns inherit the sideload history without rummaging through ad-hoc logs.

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
- [Road to 0.20.4 Engineering Proposal](../x_0_make_all_x/Change%20Control/0.20.4/Road%20to%200.20.4%20Engineering%20Proposal.md)
- [Road to 0.20.3 Engineering Proposal](../x_0_make_all_x/Change%20Control/0.20.3/Road%20to%200.20.3%20Engineering%20Proposal.md)

## Reconstitution Drill
The monthly rebuild reheats every sideload recipe from scratch. Stage the alternate module paths on the clean machine, execute the sideload scripts, and confirm the orchestrator and visitor still read the manifests without complaint. Clock runtime, capture Python/importlib versions, and update this README plus Change Control whenever the drill exposes drift.

## Cross-Linked Intelligence
- [x_make_common_x](../x_make_common_x/README.md) — provides subprocess, logging, and environment wrappers for sideload operations
- [x_make_github_visitor_x](../x_make_github_visitor_x/README.md) — validates sideloaded code during compliance runs
- [x_0_make_all_x](../x_0_make_all_x/README.md) — orchestrator ensures sideload strategies align with release milestones

## Lab Etiquette
Every sideload path must be documented in the Change Control index—source, destination, rollback plan. No secret imports, no half measures.

## Sole Architect Profile
- I alone chart and maintain these sideload paths. My range covers importlib surgery, packaging discipline, and orchestrator integration.
- Acting as benevolent dictator means I decide when modules shift, how they are documented, and how rollbacks light up in telemetry.

## Legacy Workforce Costing
- Old-world staffing: 1 senior Python internals specialist, 1 DevOps/package distribution engineer, 1 QA automation lead, and 1 technical writer.
- Timeline: 9-12 engineer-weeks to rebuild sideload orchestration, manifest logging, and test harnesses without AI support.
- Budget signal: USD 85k–115k for the initial push, plus continuing costs for edge-case maintenance.

## Techniques and Proficiencies
- Skilled in Python import system manipulation, environment isolation, and reversible deployment strategies.
- Comfortable owning high-risk infrastructure changes solo, with evidence trails that satisfy auditors and investors alike.
- Able to unify code movement, testing, and documentation under a single command structure.

## Stack Cartography
- Language: Python 3.11+, `importlib`, `zipimport`, `pathlib`, JSON manifesting.
- Tooling: Custom CLI wrappers, optional zipapp support, PowerShell aids for Windows parity, shared logging from `x_make_common_x`.
- Quality Guard: Ruff, Black, MyPy, Pyright, pytest, manual rehearsal scripts for sideload drills.
- Integrations: Orchestrator stage alignment with `x_0_make_all_x`, compliance checks via `x_make_github_visitor_x`, environment guarantee from `x_make_persistent_env_var_x`.
