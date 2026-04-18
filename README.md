# CrossExtend-KG

CrossExtend-KG currently constructs industrial knowledge graphs from O&M manuals with a fixed shared backbone and an auditable attachment pipeline.

The active paper-facing setup is:

- O&M manuals only
- three current domains: `battery`, `cnc`, `nev`
- fixed backbone
- `full_llm` as the recommended runtime variant
- manual gold planned for final paper metrics

## Documentation

- `docs/SYSTEM_DESIGN.md`
  Current architecture rules and runtime phases
- `docs/PIPELINE_INTEGRATION.md`
  Commands, verification checkpoints, and validation notes
- `docs/PROJECT_ARCHITECTURE.md`
  Repository layout and module ownership
- `docs/EXECUTION_MEMORY.md`
  Latest fixes, validated runs, and next priorities
- `docs/MANUAL_ANNOTATION_PROTOCOL.md`
  Human gold protocol for publication-grade evaluation
- `docs/REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md`
  Main real-run document for the current three-domain O&M setup

## Pipeline Flow

```text
markdown O&M -> EvidenceRecord -> fixed backbone -> retrieval -> attachment -> filtering -> graph assembly -> validation -> snapshots -> export
```

## Recommended Commands

Preprocess raw O&M markdown:

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

Run the main pipeline:

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```

## Current Status

Verified on 2026-04-18:

- preprocessing succeeded on all three current O&M documents
- BOM-contaminated markdown input was cleaned correctly
- MemoryBank retrieval no longer duplicates historical hits
- the adapted three-domain O&M pipeline completed repeated real runs successfully

Best dense verified run:

- `artifacts/deepseek-20260418T095937Z`

Latest confirmation run:

- `artifacts/deepseek-20260418T105526Z`

## Current Evaluation Position

- auto-generated references should be treated as silver
- main paper metrics should come from a human-adjudicated gold subset

See:

- `docs/MANUAL_ANNOTATION_PROTOCOL.md`
