# Preprocessing Module

**Updated**: 2026-04-18

`preprocessing/` converts raw O&M markdown into `EvidenceRecord` for the main CrossExtend-KG pipeline.

## Current Scope

The active preprocessing path is designed for:

- O&M manuals
- markdown table steps such as `T1`, `T2`, `T3`
- three current domains: `battery`, `cnc`, `nev`

It is no longer optimized around the old `product_intro` / `fault_case` paper path.
The active parser now enforces an O&M-only contract and fails explicitly on unsupported markdown instead of falling back to legacy doc types.

## Current Behavior

- infer `om_manual` from filenames like `BATOM_*`, `CNCOM_*`, `EVMAN_*`
- reject markdown that does not satisfy the active O&M filename/content contract
- strip UTF-8 BOM if present
- preserve markdown tables for step extraction
- use an O&M-specific prompt
- output one unified `EvidenceRecord` file for downstream loading

## Recommended Command

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

## Output Shape

```json
{
  "evidence_id": "BATOM_001",
  "domain_id": "battery",
  "role": "target",
  "source_type": "om_manual",
  "timestamp": "2026-04-18T00:00:00Z",
  "raw_text": "...",
  "concept_mentions": [
    {
      "label": "T1 Record Coolant Condition",
      "description": "Initial O&M inspection step",
      "node_worthy": true
    }
  ],
  "relation_mentions": [
    {
      "label": "triggers",
      "family": "task_dependency",
      "head": "T1 Record Coolant Condition",
      "tail": "T2 Isolate and Expose Outlet Area"
    }
  ]
}
```

## Current Prompt

- `config/prompts/preprocessing_extraction_om.txt`

This prompt now explicitly:

- keeps step rows under `Task`
- discourages document-title extraction
- discourages generic human-role extraction
- grounds measurements and visual outcomes as `Signal`
- grounds standing conditions as `State`
