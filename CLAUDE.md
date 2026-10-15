# dbt Learning Project — Tutor Notes

Mike is learning dbt by building this project from scratch, with Claude as tutor.
Read this file first when resuming a session.

## How to teach (agreed working style)
- One step at a time. Before each step: 2–4 sentences on what and why it matters in real projects.
- Run setup commands myself, but show the command and explain it.
- After each step, STOP and wait for "next" or questions.
- At key moments (✍️), Mike writes the model/test first; review it like a senior analytics engineer.
- Every few steps (❓), ask 1–2 quick questions to check understanding.
- When something fails, explain the error before fixing it — reading dbt errors is a skill to build.

## Environment
- WSL2 Ubuntu 24.04, VS Code, Python 3.12.3, git 2.43.0
- venv at `.venv/` — activate with `source .venv/bin/activate`
- dbt Core 1.12.6 + dbt-duckdb 1.11.0 (pinned in `requirements.txt`).
  Deliberately staying on dbt Core v1 despite the CLI's "dbt v2 available" notice.
- `profiles.yml` lives in the project folder (not `~/.dbt`).

## Learning plan
**Phase A — Foundation**
- [x] 1. Project skeleton: venv, dbt-core + dbt-duckdb, git init, .gitignore, CLAUDE.md
- [ ] 2. dbt project + profile: dbt_project.yml, in-project profiles.yml, `dbt debug`
- [ ] 3. Seeds: generate CSVs with planted data-quality issues, `dbt seed`, explore ❓

**Phase B — Staging layer**
- [ ] 4. Sources: `_sources.yml`, `source()` vs `ref()`, folder/naming conventions
- [ ] 5. Staging models `stg_<source>__<entity>` (rename/cast/clean only) ✍️
- [ ] 6. Generic tests + schema.yml docs; read failures, fix data issues ❓

**Phase C — Business logic**
- [ ] 7. Packages: dbt_utils (`generate_surrogate_key`, `unique_combination_of_columns`)
- [ ] 8. Intermediate models `int_` (joins, aggregation)
- [ ] 9. Marts `dim_customers`, `fct_orders`; view vs table materializations ✍️ ❓
- [ ] 10. Incremental model (`is_incremental()`, `unique_key`, `--full-refresh`)

**Phase D — Advanced**
- [ ] 11. A simple macro; inspect compiled SQL
- [ ] 12. Singular (custom SQL) test ✍️
- [ ] 13. Snapshot (SCD2 on customers) ❓
- [ ] 14. `dbt build`, node selection, `dbt docs generate/serve`, lineage graph
- [ ] 15. Review + final knowledge check

**Phase E — Only when Mike asks**
- [ ] Explain migrating to Microsoft Fabric (dbt-fabric adapter, profile, auth, DuckDB vs T-SQL)

## Conventions agreed
- Python deps pinned in `requirements.txt`.
- Ignored by git: `.venv/`, `target/`, `dbt_packages/`, `logs/`, `*.duckdb`.

## Concepts Mike struggled with
_(none yet)_

## Session log
- 2026-10-15: Environment checked (installed python3.12-venv). Completed step 1.
