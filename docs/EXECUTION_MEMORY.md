# CrossExtend-KG Execution Memory

**Updated**: 2026-04-18  
**Purpose**: Resume-oriented working memory for future sessions  
**Scope**: Current O&M-only architecture, validated runs, and next action priorities

## 1. Current Project Position

CrossExtend-KG is now centered on a single paper-facing path:

- O&M manuals only
- fixed backbone
- concept-layer graph construction
- auditable attachment and relation validation
- manual-gold evaluation plan

The active domains in the repository are:

- `battery`
- `cnc`
- `nev`

The active source type is:

- `om_manual`

Legacy `product_intro` and `fault_case` routing has been removed from the active preprocessing/config path.

## 2. Architecture Decisions That Are Still Binding

These should be treated as design law unless the user explicitly changes them.

### Backbone

- the backbone is predefined and frozen at runtime
- candidates may reuse the backbone, specialize under it, or be rejected
- there is no active dynamic backbone growth

### Active Routes

Only these routes are active:

- `reuse_backbone`
- `vertical_specialize`
- `reject`

### No-Fallback Principle

- required stages must run correctly or fail explicitly
- do not silently bypass the designed semantic chain
- deterministic normalization inside the chain is acceptable
- silent degraded alternatives are not acceptable

### Node Admission Policy

- person-role nodes stay in provenance, not in the graph
- document titles stay in provenance, not in the graph
- O&M step nodes (`T1`, `T2`, ...) should stay under `Task`
- observation-like concepts may enter as `Signal` or `State` when grounded
- low-value micro-components with zero relation participation may be rejected

## 3. Important Fixes Completed On 2026-04-18

### Preprocessing and Parsing

- O&M filename-based type inference added for `BATOM_*`, `CNCOM_*`, and `EVMAN_*`
- O&M documents get a much larger preprocessing content window
- UTF-8 BOM markers are stripped during markdown reading and normalization
- O&M extraction prompt was rewritten to:
  - keep step rows as `Task`
  - discourage document-title extraction
  - discourage generic person-role extraction
  - ground diagnostic observations as `Signal`
  - ground standing conditions as `State`

### Attachment and Filtering

- `T<number>` step labels containing `report` or `document` are no longer treated as document titles by the rule filter
- reject-route rescue was added for valid O&M step nodes
- observation-like rejects can now be rescued as `Signal` or `State` when grounded
- person-role detection was strengthened for labels such as `Reviewer`

### Memory and Validation

- MemoryBank retrieval now deduplicates entries by `memory_id` before embedding retrieval
- relation constraints were rewritten in clean English
- `communication` now allows `State` heads for diagnostic-condition edges

### Reliability

- transient DeepSeek SSL/provider failures are retried
- preprocessing and pipeline both completed successfully on repeated real runs

## 4. Validated Real Runs

### Best Dense Run

Run root:

- `artifacts/deepseek-20260418T095937Z`

This is the strongest single run to cite when showing the adapted architecture on the current three-domain O&M data.

Summary:

- relation validation: `114 / 117` valid
- invalid family bucket: `communication = 2`
- `battery`: `37` nodes, `44` accepted triples
- `cnc`: `33` nodes, `31` accepted triples
- `nev`: `38` nodes, `39` accepted triples

Why it matters:

- O&M steps are preserved as `Task`
- observation nodes such as `pressure result`, `fresh wetting`, and `wet after shutdown` survive correctly
- duplicate historical context hits were verified to be zero
- BOM pollution is gone from `raw_text`

### Latest Confirmation Run

Run root:

- `artifacts/deepseek-20260418T105526Z`

Summary:

- relation validation: `110 / 113` valid
- invalid family bucket: `communication = 2`
- `battery`: `42` nodes, `52` accepted triples
- `cnc`: `28` nodes, `26` accepted triples
- `nev`: `31` nodes, `32` accepted triples

Interpretation:

- the architecture still runs end-to-end after the O&M-only cleanup and no-fallback tightening
- however, repeated runs still show LLM extraction variance in candidate count and relation wording

## 5. Current Technical Interpretation

The main architecture problem is no longer "can the pipeline adapt to O&M manuals?".

That question is now answered:

- yes, the pipeline adapts to three O&M domains and produces usable graphs

The main remaining engineering/paper problem is now:

- extraction variance across repeated LLM runs

That means the next credibility bottleneck is evaluation design, not backbone design.

## 6. Evaluation Position

Current evaluation stance should be:

- auto-generated references are silver
- human-adjudicated labels are gold
- main paper metrics should use the manual gold subset

See:

- `docs/MANUAL_ANNOTATION_PROTOCOL.md`

## 7. Recommended Next Priorities

1. Build a manually annotated gold subset from the current three O&M forms.
2. When reporting experiments, distinguish:
   - best-quality verified run
   - latest confirmation run
3. If more runs are executed, track run-to-run variance rather than reporting a single random run without qualification.
4. Expand relation normalization for rare verbs if they recur, for example:
   - `reflects`
   - `transitionsFrom`
   - other low-frequency diagnostic phrasing
5. Extend the current focused regression suite beyond:
   - O&M contract enforcement
   - O&M step preservation
   - memory dedupe
   - BOM stripping

## 8. Resume Procedure

When resuming in a future terminal:

1. Read this file first.
2. Then read:
   - `docs/SYSTEM_DESIGN.md`
   - `docs/PIPELINE_INTEGRATION.md`
   - `docs/REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md`
3. If checking code, start from:
   - `preprocessing/parser.py`
   - `preprocessing/processor.py`
   - `rules/filtering.py`
   - `pipeline/memory.py`
   - `pipeline/graph.py`
4. If checking latest runtime behavior, compare:
   - `artifacts/deepseek-20260418T095937Z`
   - `artifacts/deepseek-20260418T105526Z`
