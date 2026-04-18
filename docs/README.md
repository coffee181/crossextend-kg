# CrossExtend-KG Documentation

**Updated**: 2026-04-18  
**Scope**: Current O&M-form-first runtime and paper-facing evaluation workflow

## Reading Order

1. `SYSTEM_DESIGN.md`
   Current architecture rules, runtime phases, and active assumptions.
2. `CHANGE_SUMMARY_20260418_OM_ONLY_CLEANUP.md`
   Repository cleanup summary for the O&M-only paper path and no-fallback tightening.
3. `PIPELINE_INTEGRATION.md`
   End-to-end execution checkpoints, commands, and verification notes.
4. `PROJECT_ARCHITECTURE.md`
   Repository layout and responsibility of each module.
5. `EXECUTION_MEMORY.md`
   Resume-oriented working memory: latest fixes, validated runs, and next priorities.
6. `MANUAL_ANNOTATION_PROTOCOL.md`
   Human gold annotation protocol for publication-grade evaluation.
7. `REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md`
   Detailed real-run narrative for the current three-domain O&M setup.
8. `REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418_CN.md`
   Chinese version of the same real-run narrative.

## Current Truth

- The active input type is `om_manual` only.
- The current repository data covers three domains: `battery`, `cnc`, and `nev`.
- Legacy `product_intro` and `fault_case` paths have been removed from the active preprocessing and config path.
- The backbone is fixed at runtime.
- The main paper-facing pipeline is `full_llm`.
- Evaluation credibility should come from a manually annotated gold subset, not auto-generated references alone.
- The runtime follows a no-fallback rule: unsupported markdown, missing required config, or failed LLM extraction should fail explicitly.

## Real-Run Docs

- `REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md` is the main run document for the current architecture.

## Related Directories

- `../config/`
  Runtime configs, prompts, and reference templates.
- `../preprocessing/`
  O&M markdown to `EvidenceRecord` conversion.
- `../pipeline/`
  Backbone retrieval, memory, attachment, graph assembly, and export.
- `../rules/`
  Final attachment filtering and node-admission logic.
- `../tests/`
  Focused regression checks for O&M parsing, filtering, and memory deduplication.
