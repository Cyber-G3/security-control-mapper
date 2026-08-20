from control_mapper.expected_evidence import (
    expected_evidence_for_references,
    load_expected_evidence_catalog,
    required_evidence,
)


def test_catalog_loads_versioned_records() -> None:
    records = load_expected_evidence_catalog()
    assert records
    assert all(record.catalog_version == "1.0" for record in records)
    assert all(record.effective_date == "2026-08-20" for record in records)


def test_required_evidence_resolves_nis2_reference() -> None:
    record = required_evidence("NIS2", "Article 21(2)(d)")
    assert record is not None
    assert record.title == "Supply chain security"
    assert any(item.required for item in record.expected_evidence)


def test_required_evidence_is_case_insensitive() -> None:
    record = required_evidence("nis2", "article 21(2)(e)")
    assert record is not None
    assert record.reference == "Article 21(2)(e)"


def test_unknown_reference_returns_none() -> None:
    assert required_evidence("NIS2", "Article 999") is None


def test_multi_reference_lookup_deduplicates() -> None:
    records = expected_evidence_for_references(
        [
            ("NIS2", "Article 21(2)(b)"),
            ("nis2", "article 21(2)(b)"),
            ("ISO/IEC 27001:2022", "A.8.32"),
        ]
    )
    assert len(records) == 2
