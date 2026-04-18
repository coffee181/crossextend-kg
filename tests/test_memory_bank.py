from __future__ import annotations

from crossextend_kg.models import MemoryEntry
from crossextend_kg.pipeline.memory import _dedupe_memory_entries


def test_memory_dedupe_keeps_newest_copy() -> None:
    old_entry = MemoryEntry(
        memory_id="evidence::BATOM_001",
        entry_type="evidence",
        domain_id="battery",
        timestamp="2026-04-18T09:00:00Z",
        summary="old copy",
    )
    new_entry = MemoryEntry(
        memory_id="evidence::BATOM_001",
        entry_type="evidence",
        domain_id="battery",
        timestamp="2026-04-18T10:00:00Z",
        summary="new copy",
    )
    other_entry = MemoryEntry(
        memory_id="evidence::CNCOM_001",
        entry_type="evidence",
        domain_id="cnc",
        timestamp="2026-04-18T09:30:00Z",
        summary="other entry",
    )

    deduped = _dedupe_memory_entries([old_entry, new_entry, other_entry])

    assert len(deduped) == 2
    assert deduped[0].memory_id == "evidence::BATOM_001"
    assert deduped[0].summary == "new copy"
