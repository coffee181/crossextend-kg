#!/usr/bin/env python3
"""Preprocessing module for converting O&M markdown to EvidenceRecords.

This module provides tools to:
- parse markdown O&M manuals
- extract concepts and relations using LLM
- generate EvidenceRecords compatible with CrossExtend-KG

Supported directory structure:
    data_root/
    ├── battery/
    │   └── BATOM_001.md
    ├── cnc/
    │   └── CNCOM_001.md
    └── nev/
        └── EVMAN_001.md

Public API:
- run_preprocessing: Full preprocessing pipeline from config
- preprocess_single_document: Convenience function for single files
- load_preprocessing_config: Load config from JSON file
"""

from __future__ import annotations

from .extractor import LLMExtractor, build_extractor
from .models import DocumentInput, ExtractionResult, PreprocessingConfig, PreprocessingResult
from .parser import (
    classify_doc_type,
    infer_doc_type_from_filename,
    normalize_content,
    parse_markdown_directory,
    parse_markdown_file,
    parse_multi_domain_directory,
)
from .processor import load_preprocessing_config, preprocess_single_document, run_preprocessing

__all__ = [
    "DocumentInput",
    "ExtractionResult",
    "PreprocessingConfig",
    "PreprocessingResult",
    "parse_markdown_file",
    "parse_markdown_directory",
    "parse_multi_domain_directory",
    "classify_doc_type",
    "infer_doc_type_from_filename",
    "normalize_content",
    "run_preprocessing",
    "preprocess_single_document",
    "load_preprocessing_config",
    "LLMExtractor",
    "build_extractor",
]
