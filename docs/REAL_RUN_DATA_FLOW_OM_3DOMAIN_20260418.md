# Real Run Data Flow: O&M 3-Domain Pipeline (2026-04-18)

**Updated**: 2026-04-18  
**Scope**: Current real-data chain for `battery`, `cnc`, and `nev` O&M manuals

## 1. Data Used

Raw markdown inputs:

- `data/battery/BATOM_001.md`
- `data/cnc/CNCOM_001.md`
- `data/nev/EVMAN_001.md`

All three are treated as:

- `source_type = "om_manual"`

## 2. Commands Used

Preprocessing:

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

Main run:

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```

## 3. What Changed Before This Run

The current O&M pipeline includes the following key adaptations:

- O&M filename inference for `BATOM_*`, `CNCOM_*`, `EVMAN_*`
- BOM stripping during markdown reading
- O&M-specific preprocessing prompt
- step-task preservation in filtering
- observation grounding rescue for `Signal` and `State`
- MemoryBank dedupe before retrieval
- relation constraints aligned to O&M diagnostic semantics

## 4. Best Dense Verified Run

Run directory:

- `artifacts/deepseek-20260418T095937Z`

This run is the strongest current illustration of the adapted architecture.

### 4.1 Validation Summary

- relation validation: `114 / 117` valid
- invalid family bucket:
  - `communication = 2`

### 4.2 Per-Domain Summary

- `battery`
  - `37` admitted adapter candidates
  - `44` accepted triples
  - `0` rejected triples
- `cnc`
  - `33` admitted adapter candidates
  - `31` accepted triples
  - `1` rejected triple
- `nev`
  - `38` admitted adapter candidates
  - `39` accepted triples
  - `2` rejected triples

### 4.3 What Worked

- O&M steps were preserved as `Task` nodes.
- Former false rejects such as step labels containing `report` or `document` were recovered.
- Diagnostic observations such as `pressure result`, `fresh wetting`, and `wet after shutdown` were grounded as graph-worthy nodes.
- `historical_context.json` no longer contained duplicate `memory_id` hits.
- `CNCOM_001` no longer carried BOM-polluted raw text.

### 4.4 Remaining Errors In This Run

The remaining invalid triples came from rare task wording that still entered the wrong family:

- `T6 Inspect Components -> separates -> connector leakage`
- `T6 Inspect Components -> separates -> plate-side crack`

This was a localized label-normalization issue, not a broad architectural failure.

## 5. Latest Confirmation Run

Run directory:

- `artifacts/deepseek-20260418T101615Z`

This run was executed after an extra normalization tweak for the `separates` wording.

### 5.1 Validation Summary

- relation validation: `106 / 108` valid
- invalid family bucket:
  - `lifecycle = 1`

### 5.2 Interpretation

This run confirms that:

- the pipeline still works end-to-end after the final normalization change
- the remaining issue count is very low

But it also shows an important reality:

- repeated LLM-based preprocessing runs still change the exact candidate inventory and relation wording

So the current bottleneck is now extraction variance, not pipeline incompatibility.

## 6. Stage-by-Stage Data Flow

### Stage A: Markdown -> `DocumentInput`

`preprocessing/parser.py`:

- reads markdown with `utf-8-sig`
- strips BOM
- infers `om_manual`
- preserves table structure

### Stage B: `DocumentInput` -> `EvidenceRecord`

`preprocessing/processor.py` + O&M prompt:

- extracts step tasks
- extracts grounded components, signals, states, faults
- normalizes relation labels/families
- writes `data/evidence_records_llm.json`

### Stage C: `EvidenceRecord` -> `SchemaCandidate`

`pipeline/evidence.py`:

- loads records per domain
- aggregates concept candidates
- records relation-support counts

### Stage D: Retrieval + Memory

`pipeline/router.py` and `pipeline/memory.py`:

- retrieve anchor candidates from the fixed backbone
- retrieve historical context without duplicate `memory_id` inflation

### Stage E: Attachment + Filtering

`pipeline/attachment.py` + `rules/filtering.py`:

- produce route decisions
- reject person/document nodes
- rescue valid O&M step nodes
- re-ground valid O&M observations as `Signal` or `State`

### Stage F: Graph Assembly + Validation

`pipeline/graph.py`:

- materializes accepted nodes
- validates triples by relation family constraints
- exports accepted/rejected relation files

## 7. Main Review Findings

### Strong Outcomes

1. The O&M-only adaptation is successful across all three current domains.
2. Preprocessing is now robust to O&M filenames and BOM-polluted markdown.
3. The filtering layer is much better aligned with stepwise maintenance data.
4. Memory retrieval no longer duplicates historical hints.

### Remaining Risks

1. LLM extraction still has run-to-run variance.
2. Rare low-frequency relation verbs still benefit from extra normalization rules.
3. Candidate generation can still over-propose granular zero-relation components, though these are mostly rejected cleanly.

## 8. Paper Recommendation

For the paper, the most defensible framing is:

- use the 2026-04-18 three-domain O&M pipeline as the active system
- cite the best dense run for illustrative artifact quality
- mention repeated-run variance honestly
- report main metrics on a manually annotated gold subset
- treat auto-generated references only as silver
