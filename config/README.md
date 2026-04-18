# Config Guide

**Updated**: 2026-04-18

`config/` stores the active runtime configuration assets for the current O&M-form pipeline.

## Main References

- `templates/pipeline.config.reference.json`
- `../docs/SYSTEM_DESIGN.md`
- `../docs/PIPELINE_INTEGRATION.md`

## Current Presets

Recommended presets:

- `persistent/preprocessing.deepseek.json`
  O&M preprocessing with DeepSeek
- `persistent/pipeline.deepseek.json`
  Recommended main run
- `persistent/pipeline.deepseek_full.json`
  Optional multi-variant ablation/stress run on the same architecture

Current active domains in the repository:

- `battery`
- `cnc`
- `nev`

Current active source type:

- `om_manual`

## What Matters Most

### Preprocessing Config

Key fields:

- `data_root`
- `domain_ids`
- `output_path`
- `prompt_template_path`
- `llm`

Current recommended preprocessing prompt:

- `prompts/preprocessing_extraction_om.txt`

### Pipeline Config

Key fields:

- `backbone`
- `relations`
- `runtime`
- `variants`
- `domains`

Current recommended pipeline prompt files:

- `prompts/attachment_judge.txt`

Current recommended relation constraints:

- `persistent/relation_constraints.json`

## Runtime Notes

- The backbone is fixed.
- The recommended paper variant is `full_llm`.
- `domains[].source_types` should currently be `["om_manual"]` for the active real-data path.
- MemoryBank retrieval is enabled and deduplicated by `memory_id` before scoring.
- Config loading follows a no-fallback rule for the active schema; deleted legacy synthetic fields should not be reintroduced.

## Commands

Preprocess:

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

Main run:

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```
