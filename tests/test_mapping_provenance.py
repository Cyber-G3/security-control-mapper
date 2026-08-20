from control_mapper.engine import map_check_id, map_finding


def test_mapping_result_exposes_dataset_provenance() -> None:
    result = map_finding("branch-protection-disabled")
    assert result.mapping_version == "0.3"
    assert result.mapping_effective_date == "2026-08-20"
    assert result.mapping_metadata_version == "1.0"
    assert result.mapping_sources
    assert any(source.framework == "NIS2" for source in result.mapping_sources)


def test_check_mapping_preserves_source_context_and_provenance() -> None:
    result = map_check_id(
        "github.branch.protection",
        finding_id="finding-1",
        severity="HIGH",
    )
    assert result.source_check_id == "github.branch.protection"
    assert result.source_finding_id == "finding-1"
    assert result.source_severity == "HIGH"
    assert result.mapping_effective_date is not None


def test_known_mapping_regression_reference_is_stable() -> None:
    result = map_finding("secret-scanning-disabled")
    references = {(item.framework, item.reference) for item in result.references}
    assert ("ISO/IEC 27001:2022", "A.5.17") in references
