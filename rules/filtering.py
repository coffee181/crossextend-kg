#!/usr/bin/env python3
"""Filtering and validation rules for attachment decisions."""

from __future__ import annotations

import re

from ..models import AttachmentDecision, SchemaCandidate


_PERSON_TITLE_PATTERN = re.compile(r"^(dr|mr|mrs|ms|prof)\.?\s+", re.IGNORECASE)
_PERSON_NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){1,3}$")
_PERSON_ROLE_PATTERN = re.compile(
    r"\b(engineer|technician|operator|inspector|analyst|doctor|specialist|reviewer|approver)\b",
    re.IGNORECASE,
)
_DOCUMENT_LABEL_PATTERN = re.compile(r"\b(document|report|manual|ticket|work order|sop)\b", re.IGNORECASE)
_DOCUMENT_DESCRIPTION_PATTERN = re.compile(r"\b(case document|service report|inspection report|maintenance report|document)\b", re.IGNORECASE)
_TASK_STEP_PATTERN = re.compile(r"^T\d+\b", re.IGNORECASE)
_ASSET_PATTERN = re.compile(r"\b(pack|vehicle|machine|line|cabinet|station|platform|equipment|asset)\b", re.IGNORECASE)
_COMPONENT_PATTERN = re.compile(
    r"\b(bms|management system|controller|sensor|cell|anode|cathode|separator|vent|bearing|motor|valve|module|connector|board|pump|fan)\b",
    re.IGNORECASE,
)
_SIGNAL_PATTERN = re.compile(
    r"\b(signal|curve|history|reading|telemetry|odor|count|alarm|warning|runtime reduction|result|response|level|wetness|wetting|seepage)\b",
    re.IGNORECASE,
)
_OBSERVATION_SIGNAL_PATTERN = re.compile(
    r"\b(pressure result|pressure test result|residue path|drip path|leak path|wet boundary|fresh wetting|insertion depth|latch height|clocking|preload|side load|coolant level|residue color|witness pattern)\b",
    re.IGNORECASE,
)
_STATE_PATTERN = re.compile(r"\b(state|status|condition|mode)\b", re.IGNORECASE)
_STATE_CONTEXT_PATTERN = re.compile(
    r"\b(as-found|as found|as-received|as received|under circulation|after shutdown|remains wet|stays dry|operating condition|safe state|opened state|closed state)\b",
    re.IGNORECASE,
)
_STATE_DESCRIPTION_PATTERN = re.compile(r"^(?:state|condition|status)\b.*\b(where|when)\b", re.IGNORECASE)
_FAULT_PATTERN = re.compile(
    r"\b(fault|failure|degradation|crack|cracking|plating|anomaly|defect|growth|leak|leakage|distortion)\b",
    re.IGNORECASE,
)
_TASK_PATTERN = re.compile(r"\b(task|test|inspection|analysis|diagnosis|dump|verification|correlation|repair|replacement)\b", re.IGNORECASE)
_SIGNAL_CONTEXT_PATTERN = re.compile(
    r"\b(reported|detected|telemetry|sensor reading|reading|warning|alarm|measured|observed|visible|photographed)\b",
    re.IGNORECASE,
)
_PERSON_KEYWORDS = {
    "engineer",
    "technician",
    "operator",
    "inspector",
    "analyst",
    "doctor",
    "specialist",
    "reviewer",
    "approver",
}


def _reject(decision: AttachmentDecision, justification: str, reject_reason: str) -> AttachmentDecision:
    return decision.model_copy(
        update={
            "route": "reject",
            "accept": False,
            "admit_as_node": False,
            "parent_anchor": None,
            "reject_reason": reject_reason,
            "justification": justification,
        }
    )


def _compact(text: str) -> str:
    return " ".join(text.lower().split())


def _looks_like_document(candidate: SchemaCandidate) -> bool:
    if _TASK_STEP_PATTERN.match(candidate.label.strip()):
        return False
    return bool(
        _DOCUMENT_LABEL_PATTERN.search(candidate.label)
        or _DOCUMENT_DESCRIPTION_PATTERN.search(candidate.description)
    )


def _looks_like_person(candidate: SchemaCandidate) -> bool:
    label = candidate.label.strip()
    label_compact = _compact(label)
    description = _compact(candidate.description)
    if _PERSON_TITLE_PATTERN.match(label):
        return True
    if _PERSON_ROLE_PATTERN.search(label_compact):
        return True
    if _PERSON_NAME_PATTERN.match(label) and any(keyword in description for keyword in _PERSON_KEYWORDS):
        return True
    return False


def _relation_support_count(candidate: SchemaCandidate) -> int:
    return int(candidate.routing_features.get("relation_participation_count", 0))


def _preferred_parent_anchor(candidate: SchemaCandidate) -> str | None:
    label = candidate.label
    description = candidate.description
    text = f"{label} {description}"
    # O&M form steps should remain execution tasks at the concept layer.
    if _TASK_STEP_PATTERN.match(label):
        return "Task"
    if _OBSERVATION_SIGNAL_PATTERN.search(label):
        return "Signal"
    if _SIGNAL_PATTERN.search(label):
        return "Signal"
    if _STATE_CONTEXT_PATTERN.search(label):
        return "State"
    if _STATE_PATTERN.search(label):
        return "State"
    if _FAULT_PATTERN.search(label):
        return "Fault"
    if _TASK_PATTERN.search(label):
        return "Task"
    if _OBSERVATION_SIGNAL_PATTERN.search(text):
        return "Signal"
    if _SIGNAL_CONTEXT_PATTERN.search(description):
        return "Signal"
    if _SIGNAL_PATTERN.search(text):
        return "Signal"
    if _STATE_DESCRIPTION_PATTERN.search(description):
        return "State"
    if _STATE_CONTEXT_PATTERN.search(text):
        return "State"
    if _STATE_PATTERN.search(text):
        return "State"
    if _FAULT_PATTERN.search(text):
        return "Fault"
    if _COMPONENT_PATTERN.search(text):
        return "Component"
    if _ASSET_PATTERN.search(text):
        return "Asset"
    if _TASK_PATTERN.search(text):
        return "Task"
    return None


def _rescue_rejected_candidate(
    candidate: SchemaCandidate,
    decision: AttachmentDecision,
    backbone_concepts: set[str],
) -> AttachmentDecision | None:
    support_count = _relation_support_count(candidate)
    if support_count <= 0:
        return None

    if _TASK_STEP_PATTERN.match(candidate.label) and "Task" in backbone_concepts:
        return decision.model_copy(
            update={
                "route": "vertical_specialize",
                "parent_anchor": "Task",
                "accept": True,
                "admit_as_node": True,
                "reject_reason": None,
                "justification": "rescued O&M step candidate as Task despite reject route",
            }
        )

    preferred_anchor = _preferred_parent_anchor(candidate)
    if (
        decision.reject_reason == "observation_like_not_grounded"
        and preferred_anchor in {"Signal", "State"}
        and preferred_anchor in backbone_concepts
    ):
        return decision.model_copy(
            update={
                "route": "vertical_specialize",
                "parent_anchor": preferred_anchor,
                "accept": True,
                "admit_as_node": True,
                "reject_reason": None,
                "justification": f"rescued grounded O&M observation as {preferred_anchor}",
            }
        )

    return None


def filter_attachment_decision(
    candidate: SchemaCandidate,
    decision: AttachmentDecision,
    backbone_concepts: set[str],
    allowed_routes: set[str],
    allow_free_form_growth: bool,
) -> AttachmentDecision:
    if candidate.label in backbone_concepts:
        return AttachmentDecision(
            candidate_id=candidate.candidate_id,
            label=candidate.label,
            route="reuse_backbone",
            parent_anchor=None,
            accept=True,
            admit_as_node=True,
            reject_reason=None,
            confidence=1.0,
            justification=decision.justification or "seed or promoted backbone concept",
            evidence_ids=list(candidate.evidence_ids),
        )

    if decision.route not in allowed_routes:
        return _reject(decision, "route is not allowed by config", "route_not_allowed")

    if decision.route == "vertical_specialize":
        if _looks_like_person(candidate):
            return _reject(decision, "person names are not eligible as graph nodes", "person_name")
        if _looks_like_document(candidate):
            return _reject(decision, "document titles are kept in provenance instead of graph nodes", "document_title")
        if decision.parent_anchor and decision.parent_anchor in backbone_concepts:
            preferred_anchor = _preferred_parent_anchor(candidate)
            if preferred_anchor and preferred_anchor in backbone_concepts and preferred_anchor != decision.parent_anchor:
                decision = decision.model_copy(
                    update={
                        "parent_anchor": preferred_anchor,
                        "justification": f"{decision.justification}; normalized parent anchor to {preferred_anchor}",
                    }
                )
            if _relation_support_count(candidate) <= 0:
                return _reject(
                    decision,
                    "candidate does not participate in any relation chain",
                    "weak_relation_support",
                )
            return decision.model_copy(update={"accept": True, "admit_as_node": True, "reject_reason": None})
        if allow_free_form_growth:
            return decision.model_copy(update={"accept": True, "admit_as_node": True, "reject_reason": None})
        return _reject(
            decision,
            "vertical specialization requires a backbone parent when free-form growth is disabled",
            "invalid_backbone_parent",
        )

    if decision.route == "reuse_backbone":
        if candidate.label in backbone_concepts:
            return decision.model_copy(update={"accept": True, "admit_as_node": True, "reject_reason": None})
        return _reject(
            decision,
            "candidate label does not exactly match a backbone concept",
            "backbone_label_mismatch",
        )

    if decision.route == "reject":
        if _looks_like_person(candidate):
            return _reject(decision, "person names are not eligible as graph nodes", "person_name")
        rescued_decision = _rescue_rejected_candidate(candidate, decision, backbone_concepts)
        if rescued_decision is not None:
            return rescued_decision
        reject_reason = decision.reject_reason or "low_graph_value"
        return decision.model_copy(update={"accept": False, "admit_as_node": False, "reject_reason": reject_reason})

    return _reject(decision, "unsupported route", "route_not_allowed")
