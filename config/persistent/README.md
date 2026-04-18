# Persistent Configs

**Updated**: 2026-04-18

`config/persistent/` contains the presets intended for real execution and daily editing.

## Recommended Presets

- `pipeline.deepseek.json`
  Recommended paper-facing run
- `pipeline.deepseek_full.json`
  Optional multi-variant ablation/stress run
- `preprocessing.deepseek.json`
  Recommended O&M preprocessing preset

## Current Active Assumptions

- domains: `battery`, `cnc`, `nev`
- source type: `om_manual`
- main variant: `full_llm`
- relation constraints: `relation_constraints.json`
- no fallback: unsupported markdown or failed extraction should stop the run

## Usually Edited Fields

1. `llm.base_url`, `llm.api_key`, `llm.model`
2. `embedding.base_url`, `embedding.api_key`, `embedding.model`
3. `runtime.artifact_root`
4. `runtime.run_prefix`
5. `domains[].data_path`
6. `domains[].source_types`

## Quick Run

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```
