from __future__ import annotations

from crossextend_kg.models import AttachmentDecision, SchemaCandidate
from crossextend_kg.rules.filtering import filter_attachment_decision


BACKBONE_CONCEPTS = {
    "Asset",
    "Component",
    "Process",
    "Task",
    "Signal",
    "State",
    "Fault",
    "MaintenanceAction",
    "Incident",
    "Actor",
    "Document",
}
ALLOWED_ROUTES = {"reuse_backbone", "vertical_specialize", "reject"}


def test_om_step_candidate_is_preserved_as_task() -> None:
    candidate = SchemaCandidate(
        candidate_id="battery::T1 Report Coolant Condition",
        domain_id="battery",
        label="T1 Report Coolant Condition",
        description="Initial O&M inspection step",
        evidence_ids=["BATOM_001"],
        evidence_texts=["..."],
        support_count=1,
        routing_features={"relation_participation_count": 1},
    )
    decision = AttachmentDecision(
        candidate_id=candidate.candidate_id,
        label=candidate.label,
        route="vertical_specialize",
        parent_anchor="Document",
        accept=False,
        admit_as_node=False,
        confidence=0.8,
        justification="llm proposed document-like anchor",
        evidence_ids=["BATOM_001"],
    )

    filtered = filter_attachment_decision(
        candidate=candidate,
        decision=decision,
        backbone_concepts=BACKBONE_CONCEPTS,
        allowed_routes=ALLOWED_ROUTES,
        allow_free_form_growth=False,
    )

    assert filtered.accept is True
    assert filtered.admit_as_node is True
    assert filtered.parent_anchor == "Task"
    assert filtered.route == "vertical_specialize"
    assert filtered.reject_reason is None


def test_document_title_is_rejected() -> None:
    candidate = SchemaCandidate(
        candidate_id="battery::Battery Service Report",
        domain_id="battery",
        label="Battery Service Report",
        description="inspection report for service team",
        evidence_ids=["BATOM_001"],
        evidence_texts=["..."],
        support_count=1,
        routing_features={"relation_participation_count": 2},
    )
    decision = AttachmentDecision(
        candidate_id=candidate.candidate_id,
        label=candidate.label,
        route="vertical_specialize",
        parent_anchor="Document",
        accept=True,
        admit_as_node=True,
        confidence=0.7,
        justification="llm proposed document anchor",
        evidence_ids=["BATOM_001"],
    )

    filtered = filter_attachment_decision(
        candidate=candidate,
        decision=decision,
        backbone_concepts=BACKBONE_CONCEPTS,
        allowed_routes=ALLOWED_ROUTES,
        allow_free_form_growth=False,
    )

    assert filtered.accept is False
    assert filtered.admit_as_node is False
    assert filtered.parent_anchor is None
    assert filtered.reject_reason == "document_title"
