# Change Summary: O&M-Only Cleanup and No-Fallback Tightening

**Updated**: 2026-04-18  
**Scope**: Repository-wide cleanup and stabilization for the current paper-facing three-domain O&M pipeline

## Goal

This update consolidates CrossExtend-KG around the active paper path only:

- input type: `om_manual`
- domains: `battery`, `cnc`, `nev`
- runtime variant: `full_llm`
- evaluation direction: human-annotated gold subset
- engineering principle: **no fallback**

The repository is no longer maintained as a mixed experimental workspace for product analysis, fault-case preprocessing, or synthetic data generation.

## Main Changes

### 1. Preprocessing was narrowed to O&M-only

- `preprocessing/parser.py` now recognizes only the active O&M contract.
- Unsupported markdown no longer falls back to legacy `fault_case` or `product_intro`.
- O&M filenames such as `BATOM_*`, `CNCOM_*`, and `EVMAN_*` remain first-class inputs.
- UTF-8 BOM stripping and markdown-table preservation remain in place.
- `preprocessing/extractor.py` now uses the active O&M prompt path directly instead of doc-type prompt fallback behavior.
- `preprocessing/processor.py` now fails explicitly when extraction fails.

### 2. Runtime/config schema was simplified

- `config.py` removed synthetic-generation schema remnants from the active runtime config model.
- Active presets were simplified to the current O&M path.
- Reference config templates now describe the real three-domain O&M setup rather than mixed legacy/synthetic scenarios.

### 3. Legacy files were removed

Removed or retired from the active repository path:

- legacy pipeline presets:
  - `config/persistent/pipeline.default.json`
  - `config/persistent/pipeline.local_ollama.json`
  - `config/persistent/pipeline.openai.json`
  - `config/persistent/pipeline.real_data.json`
- legacy preprocessing presets:
  - `config/persistent/preprocessing.deepseek_full.json`
  - `config/persistent/preprocessing.nev_om.json`
- legacy prompts:
  - `config/prompts/preprocessing_extraction.txt`
  - `config/prompts/synthetic_generator.txt`
  - `config/prompts/synthetic_generator_english.txt`
- archived battery-only real-run docs:
  - `docs/REAL_RUN_DATA_FLOW_BATTERY_20260417.md`
  - `docs/REAL_RUN_DATA_FLOW_BATTERY_20260417_CN.md`
- old raw source files for product/fault paths under `data/`

### 4. Documentation was rewritten to match the current architecture

Updated core docs:

- `README.md`
- `README_CN.md`
- `docs/README.md`
- `docs/SYSTEM_DESIGN.md`
- `docs/PIPELINE_INTEGRATION.md`
- `docs/PROJECT_ARCHITECTURE.md`
- `docs/EXECUTION_MEMORY.md`
- `preprocessing/README.md`
- `config/README.md`
- `config/persistent/README.md`

Added current paper-facing docs:

- `docs/MANUAL_ANNOTATION_PROTOCOL.md`
- `docs/REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md`
- `docs/REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418_CN.md`

### 5. Regression protection was added

Added a small focused test suite:

- `tests/test_preprocessing_om_contract.py`
- `tests/test_filtering_rules.py`
- `tests/test_memory_bank.py`

These tests lock in key behaviors:

- O&M-only preprocessing contract
- BOM stripping
- rejection of unsupported markdown
- O&M step preservation under `Task`
- MemoryBank deduplication by `memory_id`

### 6. Repository hygiene was improved

- Added `.gitignore` for `__pycache__/`, compiled Python artifacts, `.pytest_cache/`, `.claude/`, and generated `artifacts/`.
- Removed tracked cache artifacts from the repository path.

## Validation

The cleaned repository was validated on the active real-data path.

### Static / Regression Checks

- `python -m py_compile ...` passed on the updated Python entry points.
- `python -m pytest -q D:\crossextend_kg\tests` passed with `7 passed`.

### Real End-to-End Runs

Preprocessing:

- `python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json`
- result: `3 / 3` documents succeeded
- output file: `data/evidence_records_llm.json`
- `domain_stats` now contains only `om_manual`

Main pipeline:

- `python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json`
- a first attempt failed explicitly because of transient DeepSeek SSL/provider instability
- a second full rerun completed successfully under the no-fallback rule

Latest successful run:

- `artifacts/deepseek-20260418T105526Z`

Latest summary highlights:

- relation validation: `110 / 113` valid
- invalid family bucket: `communication = 2`
- duplicate `memory_id` historical hits: `0` for `battery`, `cnc`, and `nev`

## Current Interpretation

After this cleanup, the main risk is no longer repository ambiguity or legacy-path contamination.

The remaining major issue is:

- extraction variance and occasional external LLM-provider instability

That means the codebase is now much closer to a stable paper artifact for the current design, and the next important credibility step is to build the manual gold subset on top of this cleaned baseline.
