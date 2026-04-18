from __future__ import annotations

from pathlib import Path

import pytest

from crossextend_kg.preprocessing.parser import (
    classify_doc_type,
    infer_doc_type_from_filename,
    parse_markdown_file,
    parse_multi_domain_directory,
)


def test_infer_doc_type_from_filename_for_active_om_files() -> None:
    assert infer_doc_type_from_filename(Path("BATOM_001.md")) == "om_manual"
    assert infer_doc_type_from_filename(Path("CNCOM_001.md")) == "om_manual"
    assert infer_doc_type_from_filename(Path("EVMAN_001.md")) == "om_manual"


def test_parse_markdown_file_strips_utf8_bom(tmp_path: Path) -> None:
    file_path = tmp_path / "BATOM_001.md"
    file_path.write_text(
        "\ufeff| Time step | O&M sample text |\n|---|---|\n| T1 | Inspect coolant level. |\n",
        encoding="utf-8",
    )

    document = parse_markdown_file(
        file_path=file_path,
        domain_id="battery",
        role="target",
        doc_type="om_manual",
    )

    assert not document.content.startswith("\ufeff")


def test_classify_doc_type_rejects_non_om_content() -> None:
    with pytest.raises(ValueError, match="active om_manual content contract"):
        classify_doc_type("# Product Specification\n\nRated voltage and brochure details.")


def test_parse_multi_domain_directory_rejects_unrecognized_markdown(tmp_path: Path) -> None:
    battery_dir = tmp_path / "battery"
    battery_dir.mkdir()
    (battery_dir / "misc_notes.md").write_text("This file has no time-step O&M structure.", encoding="utf-8")

    with pytest.raises(ValueError, match="unsupported markdown input"):
        parse_multi_domain_directory(tmp_path, ["battery"], "target")
