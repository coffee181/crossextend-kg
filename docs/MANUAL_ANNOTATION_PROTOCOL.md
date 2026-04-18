# Manual Annotation Protocol for O&M Gold Evaluation

**Updated**: 2026-04-18  
**Scope**: Human annotation protocol for publication-grade evaluation on O&M form data  
**Applies to**: `battery`, `cnc`, `nev` domains with `source_type="om_manual"`

Current note:

- the strongest current annotation packet source is the three-domain O&M run family from 2026-04-18
- when choosing a packet for initial human annotation, prefer the best dense run artifacts under `artifacts/deepseek-20260418T095937Z/full_llm/working/<domain>/`

## 1. Purpose

This document defines how to build a small but credible human-annotated gold set for CrossExtend-KG.

Current project status:

- automatic labels are useful for development
- automatic labels should be treated as **silver**, not true gold
- the paper's main quantitative claims should rely on a **human-validated gold set**

The goal of the gold set is not to re-annotate the entire corpus. The goal is to create an independent evaluation set that can support:

- node admission quality
- backbone attachment quality
- relation family and direction quality
- final triple acceptance quality

## 2. What Should Be Called Gold

Use these terms consistently in the paper:

- **silver set**: automatically generated or automatically normalized references
- **gold set**: labels independently produced and adjudicated by human annotators

A set should be called gold only if:

1. At least two human annotators label the same subset independently.
2. Disagreements are resolved through adjudication.
3. The final released label is the adjudicated human decision.

If a subset is only checked by one person after automatic generation, call it:

- `human-checked silver`
- or `expert-reviewed silver`

Do not call it gold.

## 3. Annotation Targets

For the current paper, human annotation should focus on the parts that directly support the method claims.

### Target A: Node Admission

For each candidate concept in an O&M form, decide:

- should this concept become a graph node
- if yes, should it attach under the fixed backbone
- if no, why it should be rejected

### Target B: Attachment / Parent Anchor

For each admitted concept, decide:

- which route is correct:
  - `reuse_backbone`
  - `vertical_specialize`
  - `reject`
- if admitted, what the correct `parent_anchor` is

### Target C: Relation Validity

For each candidate relation / triple, decide:

- whether the head and tail are correct
- whether the relation direction is correct
- whether the relation family is correct
- whether the triple should be accepted into the final graph

## 4. Annotation Unit Definition

The annotation unit should match the current runtime structure.

### Concept-Level Unit

A concept-level unit is one candidate label within one `EvidenceRecord`.

Recommended primary key:

- `evidence_id`
- `domain_id`
- `candidate_label`

Optional but helpful:

- source sentence or table row
- short note with the human rationale

### Relation-Level Unit

A relation-level unit is one candidate triple within one `EvidenceRecord`.

Recommended primary key:

- `evidence_id`
- `domain_id`
- `head_label`
- `relation_label`
- `tail_label`

Optional but helpful:

- source row or sentence
- whether this relation was directly stated or inferred from step sequence

## 5. Recommended Gold Fields

### 5.1 Concept Annotation Schema

Each concept annotation record should contain:

```json
{
  "evidence_id": "EVMAN_001",
  "domain_id": "nev",
  "candidate_label": "T2 Power Down & Gain Access",
  "candidate_description": "optional copied context",
  "node_decision": "admit",
  "route": "vertical_specialize",
  "parent_anchor": "Task",
  "reject_reason": null,
  "annotator_id": "ann_a",
  "notes": "O&M step node; should remain a task concept"
}
```

Allowed values:

- `node_decision`: `admit` or `reject`
- `route`: `reuse_backbone`, `vertical_specialize`, `reject`
- `parent_anchor`:
  - `Asset`
  - `Component`
  - `Process`
  - `Task`
  - `Signal`
  - `State`
  - `Fault`
  - `MaintenanceAction`
  - `Incident`
  - `Actor`
  - `Document`
  - `null` when rejected

Recommended reject reasons:

- `person_name`
- `document_title`
- `observation_like_not_grounded`
- `cannot_anchor_backbone`
- `weak_relation_support`
- `low_graph_value`
- `unsupported_semantic_type`
- `invalid_backbone_parent`
- `other_manual`

### 5.2 Relation Annotation Schema

Each relation annotation record should contain:

```json
{
  "evidence_id": "BATOM_001",
  "domain_id": "battery",
  "head_label": "T3 Trace Coolant Source",
  "relation_label": "triggers",
  "tail_label": "T4 Pressure Test Suspect Section",
  "relation_family": "task_dependency",
  "direction_correct": true,
  "triple_decision": "accept",
  "reject_reason": null,
  "annotator_id": "ann_b",
  "notes": "Sequential O&M step relation"
}
```

Allowed values:

- `relation_family`:
  - `task_dependency`
  - `communication`
  - `propagation`
  - `lifecycle`
  - `structural`
- `direction_correct`: `true` or `false`
- `triple_decision`: `accept` or `reject`

Recommended reject reasons:

- `wrong_head`
- `wrong_tail`
- `wrong_direction`
- `wrong_family`
- `not_grounded_in_text`
- `endpoint_not_graphworthy`
- `other_manual`

## 6. O&M-Specific Labeling Rules

These rules should be treated as active annotation law for the current O&M data.

### 6.1 Step Nodes

Labels such as `T1 ...`, `T2 ...`, `T3 ...` are usually:

- `node_decision = admit`
- `route = vertical_specialize`
- `parent_anchor = Task`

They should not be attached as:

- `Asset`
- `Component`
- `State`

unless the text is truly not an operation step and the label is badly formed.

### 6.2 Equipment / Platform Names

Examples:

- `Aurex BatteryHub-612 LR`
- `Kestrel VMC-850`
- `Novaris Trax-712 EV`

These are usually:

- admitted
- attached under `Asset`

### 6.3 Physical Parts and Assemblies

Examples:

- `outlet quick connector`
- `hose support bracket`
- `ground strap`
- `resolver connector`

These are usually:

- admitted
- attached under `Component`

### 6.4 Measurements and Observations

Examples:

- `pressure result`
- `comparison-branch response`
- `coolant level`
- `undertray wetness`

These should usually be:

- `Signal` if they are measured, observed, reported, or used diagnostically
- `State` only if they describe a standing condition rather than a measurement or observation

### 6.5 Fault-Like Concepts

Examples:

- `connector shell crack`
- `coolant leak`
- `hose-end distortion`

These are usually:

- admitted
- attached under `Fault`

### 6.6 Concepts That Should Normally Be Rejected

These should usually not become graph nodes in the current concept-layer evaluation:

- person names
- raw report titles
- work-order ids
- document filenames
- bare timestamps
- form-only bookkeeping fields

## 7. Annotation Workflow

### Step 1: Build Candidate Packets

For each selected O&M document, prepare a packet containing:

- raw markdown form
- `adapter_candidates.json`
- `attachment_decisions.json`
- `relation_edges.candidates.json`
- optional `final_graph.json`

This packet gives annotators the source text and the system proposals without requiring them to inspect code.

### Step 2: Independent Concept Annotation

Two annotators independently label all concept-level units in the packet.

Recommended order:

1. decide `admit` or `reject`
2. if admitted, assign `route`
3. if admitted, assign `parent_anchor`
4. if rejected, assign `reject_reason`

### Step 3: Independent Relation Annotation

Two annotators independently label all relation-level units in the packet.

Recommended order:

1. check whether head and tail are valid concept nodes
2. check whether the relation is grounded in the text
3. check relation family
4. check direction
5. assign final `accept` or `reject`

### Step 4: Adjudication

A senior annotator or project lead resolves disagreements.

Adjudication should produce one final released label per unit.

Recommended adjudication priority:

1. concept admission
2. parent anchor
3. relation family
4. relation direction
5. final triple decision

## 8. Minimum Recommended Annotation Size

If data is still limited, annotate every available O&M form.

### Immediate Pilot Set

For the current repository status, annotate:

- all currently available O&M forms in `battery`
- all currently available O&M forms in `cnc`
- all currently available O&M forms in `nev`

This gives a small but valid pilot gold set for method debugging and paper preparation.

### Submission-Grade Target

If more O&M forms become available, target at least:

- `4-8` forms per domain when possible
- or at minimum:
  - `250+` concept-level decisions
  - `150+` relation-level decisions

Balanced coverage matters more than raw document count.

Try to include:

- leak diagnosis steps
- safety / shutdown access steps
- inspection / comparison steps
- repair / closure / release steps

## 9. Agreement and Quality Control

Report inter-annotator agreement before adjudication.

Recommended metrics:

- concept admission: Cohen's kappa or binary F1 agreement
- parent anchor: macro F1 or multi-class kappa
- relation family: macro F1 or multi-class kappa
- final triple acceptance: binary F1 agreement

Also report:

- number of adjudicated disagreements
- most common disagreement categories
- a few representative examples

## 10. How to Use the Gold Set in the Paper

Recommended reporting structure:

### Main Quantitative Table

Use the human gold set for:

- node admission precision / recall / F1
- parent-anchor accuracy or macro F1
- relation family accuracy or macro F1
- final triple precision / recall / F1

### Auxiliary Development Table

Use the silver set only for:

- large-scale ablation trends
- engineering diagnostics
- early development comparisons

Label it clearly as silver.

### Case Study Section

Show a few O&M forms and explain:

- which step nodes were admitted
- how they were anchored
- which relations were accepted
- what the remaining error types are

## 11. Practical Recommendation for This Repository

For the current CrossExtend-KG O&M pipeline, the most defensible paper setup is:

1. Keep the automatically generated references as `silver`.
2. Build a manually annotated O&M gold test subset.
3. Report main metrics on the human gold subset.
4. Report ablations on silver only as supplementary or diagnostic results.

This keeps the evaluation independent from:

- LLM extraction
- LLM attachment
- rule-based normalization

and gives the paper much stronger credibility.

## 12. Suggested First Execution

Do this first before scaling annotation:

1. Select one O&M form from each of `battery`, `cnc`, and `nev`.
2. Export candidate and relation packets from the current artifacts.
3. Ask two annotators to independently label all concept and relation units.
4. Adjudicate the disagreements.
5. Measure agreement and error types.
6. Use that pilot to refine the guidelines before labeling more data.

That pilot is small enough to finish quickly and strong enough to tell whether the current evaluation protocol is ready for a paper.
