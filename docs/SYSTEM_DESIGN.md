# CrossExtend-KG System Design

**Updated**: 2026-04-18  
**Scope**: Active architecture for O&M-form knowledge graph construction

## Core Rules

1. The backbone is fixed at runtime.
2. All domains are treated uniformly as application cases with `role="target"`.
3. The active input source type is `om_manual`.
4. The main pipeline must fail explicitly when required stages break; no silent fallback path is allowed.
5. Runtime outputs are auditable graph-construction artifacts, not downstream product-analysis or fault-case reports.
6. Preprocessing accepts only O&M-contract markdown; unsupported files must fail instead of being re-routed into legacy types.

## Problem Framing

CrossExtend-KG currently treats industrial KG construction as constrained schema adaptation over O&M forms:

- preprocessing converts raw markdown manuals into `EvidenceRecord`
- a fixed backbone provides shared upper-level anchors
- candidate concepts are attached under the backbone or rejected
- accepted concepts and relations are assembled into per-domain graphs with provenance and snapshots

The current paper-facing objective is:

- robustly adapt the pipeline to stepwise O&M manuals
- preserve task sequence and diagnostic evidence
- keep node admission auditable
- evaluate with human gold rather than auto-generated pseudo-gold

## Active Input Contract

The repository currently uses one markdown O&M form per domain:

- `data/battery/BATOM_001.md`
- `data/cnc/CNCOM_001.md`
- `data/nev/EVMAN_001.md`

The parser now supports filename-based type inference for these O&M naming conventions and strips optional UTF-8 BOM markers before downstream extraction.
If a markdown file does not match the active O&M filename or content contract, preprocessing should stop with an explicit error.

## Runtime Phases

### Phase 0: Preprocessing

`preprocessing/` converts raw markdown manuals into `EvidenceRecord`.

Current O&M preprocessing behavior:

- infer `doc_type="om_manual"` from O&M-style filenames
- reject markdown files that do not satisfy the active O&M contract
- keep markdown tables intact for `T1`, `T2`, ... step recognition
- use the O&M-specific extraction prompt
- treat step rows as `Task` concepts
- prefer measurement/observation outcomes as `Signal`
- prefer standing conditions as `State`
- discourage document-title and generic-person-role extraction
- allow much longer content windows for O&M manuals than generic docs
- fail the preprocessing run if required prompt/config resources are missing or the LLM extraction step fails

### Phase 1: Evidence Loading

`pipeline/evidence.py`:

- loads `EvidenceRecord` JSON
- filters by configured `domain_id` and `source_types`
- aggregates concept-level `SchemaCandidate` objects per domain

### Phase 2: Frozen Backbone Build

`pipeline/backbone.py` builds the shared backbone from:

- `backbone.seed_concepts`
- `backbone.seed_descriptions`
- optional curated supplements from `domains[].ontology_seed_path`

No dynamic backbone growth is active in the current runtime.

### Phase 3: Retrieval and Historical Context

Two retrieval layers guide attachment:

- `pipeline/router.py`: embedding retrieval over backbone descriptions
- `pipeline/memory.py`: temporal memory-bank retrieval over prior evidence, attachments, and snapshots

Important 2026-04-18 fix:

- memory entries are deduplicated by `memory_id` before embedding retrieval, so historical evidence is no longer double-counted in prompts and ranking

### Phase 4: Attachment and Filtering

`pipeline/attachment.py` decides one of three routes:

- `reuse_backbone`
- `vertical_specialize`
- `reject`

`rules/filtering.py` then enforces final legality and admission.

Important current filtering behavior:

- reject document titles and person-role nodes
- keep `T<number>` O&M steps under `Task`
- re-ground observation-like candidates as `Signal` or `State` when the evidence and relation support are strong enough
- require relation support for component-like low-value nodes

### Phase 5: Graph Assembly and Relation Validation

`pipeline/graph.py`:

- materializes adapter concepts
- converts accepted relation mentions into graph edges
- creates temporal assertions and snapshots
- validates edges against `config/persistent/relation_constraints.json`

Current constraint intent:

- `task_dependency` captures step sequence and task-to-output edges
- `communication` captures diagnostic evidence such as `Signal indicates Fault`
- `communication` also allows `State` heads when a standing condition is diagnostic evidence

### Phase 6: Export

`pipeline/artifacts.py` exports:

- run-level summaries
- per-domain working artifacts
- accepted/rejected candidates
- accepted/rejected relations
- snapshot files
- `latest_summary.json`
- `data_flow_trace.json`

## Recommended Variant

The recommended paper-facing runtime is:

- config: `config/persistent/pipeline.deepseek.json`
- variant: `full_llm`

This variant keeps:

- LLM attachment
- embedding routing
- rule filtering
- temporal memory bank
- snapshots

## Known Quality Characteristics

The current architecture is now compatible with three-domain O&M manuals, but one important risk remains:

- extraction variance across repeated LLM runs still changes the exact candidate set and relation labels

That variance is now a larger concern than architectural incompatibility. Because of that, the paper should:

- report main metrics on a human gold subset
- describe auto-generated references as silver
- optionally report repeated-run variance or majority-vote extraction diagnostics

## Current Gaps Worth Future Work

1. Expand relation-label normalization for rare verbs such as `reflects`, `transitionsFrom`, and other low-frequency diagnostic phrasing.
2. Reduce over-generation of zero-relation micro-components without harming useful diagnostic observations.
3. Add a small automated regression suite for the O&M-specific filtering and preprocessing rules.
4. Continue tightening timestamp semantics if document-native time metadata is added later.
