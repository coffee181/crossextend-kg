# CrossExtend-KG Project Architecture

**Updated**: 2026-04-18  
**Status**: Current O&M-form runtime layout

## Repository Layout

```text
crossextend_kg/
  backends/
    embeddings.py
    llm.py
  config/
    persistent/
    prompts/
    templates/
    README.md
  data/
    battery/
    cnc/
    nev/
    evidence_records_llm.json
  docs/
    README.md
    SYSTEM_DESIGN.md
    PIPELINE_INTEGRATION.md
    PROJECT_ARCHITECTURE.md
    EXECUTION_MEMORY.md
    MANUAL_ANNOTATION_PROTOCOL.md
    REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md
    REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418_CN.md
  pipeline/
    artifacts.py
    attachment.py
    backbone.py
    evidence.py
    graph.py
    memory.py
    relation_validation.py
    router.py
    runner.py
    utils.py
  preprocessing/
    extractor.py
    models.py
    parser.py
    processor.py
    README.md
  rules/
    filtering.py
  scripts/
    visualize_propagation.py
  tests/
    conftest.py
    test_filtering_rules.py
    test_memory_bank.py
    test_preprocessing_om_contract.py
  artifacts/
  README.md
  cli.py
  config.py
  exceptions.py
  io.py
  logging_config.py
  models.py
  validation.py
```

## Module Responsibilities

### `preprocessing/`

Converts raw O&M markdown into `EvidenceRecord`.

Important files:

- `parser.py`
  File reading, filename-based doc-type inference, BOM stripping, content normalization
- `extractor.py`
  LLM extraction wrapper
- `processor.py`
  Multi-domain preprocessing orchestration and relation-label normalization

### `pipeline/`

Runs the main construction chain.

Important files:

- `evidence.py`
  Load and aggregate `SchemaCandidate`
- `backbone.py`
  Build the fixed backbone
- `router.py`
  Embedding-based backbone anchor retrieval
- `memory.py`
  Temporal memory-bank retrieval and persistence
- `attachment.py`
  LLM or deterministic attachment decisions
- `graph.py`
  Graph assembly, relation validation, and snapshots
- `artifacts.py`
  Disk export and summaries
- `runner.py`
  End-to-end orchestration

### `rules/`

- `filtering.py`
  Final node-admission policy, person/document rejection, O&M task rescue, and observation grounding

### `config/`

- `persistent/`
  Daily-use presets
- `prompts/`
  Attachment and preprocessing prompts
- `templates/`
  Reference configuration template

### `docs/`

Paper-facing architecture, run notes, and annotation guidance.

## Active Data Shape

The current paper pipeline assumes:

- raw input: markdown O&M forms
- preprocessing output: `EvidenceRecord`
- graph scope: concept layer plus temporal snapshot exports

It does not currently assume:

- downstream product analysis
- standalone fault-case corpus processing
- dynamic backbone construction

## Current Notable Absences

- No downstream evaluation package is active in the current paper path.
- No dynamic backbone-growth package is active in the current paper path.
