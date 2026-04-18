# Pipeline Integration Verification

**Updated**: 2026-04-18  
**Status**: Active O&M-form runtime

## Active Entry Points

- Preprocessing:
  `config/persistent/preprocessing.deepseek.json`
- Main run:
  `config/persistent/pipeline.deepseek.json`

Both configs now target only:

- `battery`
- `cnc`
- `nev`

with:

- `source_types = ["om_manual"]`

## End-to-End Flow

### Phase 1: Parse and Preprocess O&M Markdown

Command:

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

Verification points:

- all configured domains are present under `data/`
- filenames like `BATOM_*`, `CNCOM_*`, and `EVMAN_*` resolve to `om_manual`
- markdown that does not match the active O&M contract fails explicitly instead of falling back to a legacy type
- BOM markers are stripped before LLM extraction
- raw markdown tables remain intact for step extraction
- LLM extraction errors fail the preprocessing run instead of producing partial output
- output file is `data/evidence_records_llm.json`

Verified on 2026-04-18:

- `total_docs = 3`
- `successful_docs = 3`
- `failed_docs = 0`
- all output records have `source_type = "om_manual"`

### Phase 2: Evidence Loading and Candidate Aggregation

Verification points:

- all domains load from the same `EvidenceRecord` file
- candidates are aggregated per domain and label
- zero-length domains fail explicitly instead of silently continuing

### Phase 3: Backbone Retrieval and Memory Retrieval

Verification points:

- embedding routing returns backbone anchor suggestions
- temporal memory retrieval excludes self-evidence and future evidence
- memory entries are deduplicated by `memory_id` before retrieval scoring

Verified on run `artifacts/deepseek-20260418T095937Z`:

- duplicate `memory_id` hits in `historical_context.json` were checked and found to be zero for `battery`, `cnc`, and `nev`

### Phase 4: Attachment and Filtering

Verification points:

- `T<number>` step candidates stay under `Task`
- document-like wording inside step labels no longer causes false `document_title` rejection
- O&M observations such as `pressure result`, `fresh wetting`, and `wet after shutdown` can survive as `Signal` or `State`
- generic person-role nodes remain rejected

### Phase 5: Graph Assembly and Relation Validation

Verification points:

- accepted adapter concepts materialize into graph nodes
- relation validation rejects type-incompatible triples
- snapshots are exported per domain

Two real verification runs were executed after the O&M adaptation:

1. Best dense run:
   `artifacts/deepseek-20260418T095937Z`
   - relation validation: `114 / 117` valid
   - remaining invalid triples: `2`
   - invalid family bucket: `communication`

2. Latest confirmation run:
   `artifacts/deepseek-20260418T105526Z`
   - relation validation: `110 / 113` valid
   - remaining invalid triples: `3`
   - invalid family bucket: `communication`

Interpretation:

- the architecture is now stable for O&M manuals, including after the O&M-only cleanup
- remaining issues are mostly extraction-label variance, not structural pipeline failure

## Key Commands

Preprocess:

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

Main run:

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```

Syntax sanity:

```bash
python -m py_compile preprocessing\parser.py preprocessing\processor.py rules\filtering.py pipeline\memory.py pipeline\attachment.py
```

## Current Testing Reality

There is now a small focused `tests/` directory for core O&M regressions.

Current validation relies on:

- `pytest -q tests`
- targeted `py_compile`
- artifact inspection
- repeated real O&M runs
- manual spot checks on `data_flow_trace.json`, `adapter_candidates.rejected_by_reason.json`, and `relation_edges.rejected_type.json`

For paper preparation, this is acceptable as engineering validation, but broader regression coverage would still be worthwhile.
