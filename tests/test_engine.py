import pytest

from control_mapper.engine import list_finding_types, map_finding


def test_lists_initial_findings():
    findings = list_finding_types()
    assert "branch-protection-disabled" in findings
    assert "secret-scanning-disabled" in findings


def test_maps_branch_protection_to_versioned_references():
    result = map_finding("branch-protection-disabled")
    assert result.mapping_version == "0.2"
    assert result.references
    assert any(ref.framework == "ISO/IEC 27001:2022" for ref in result.references)
    assert result.evidence_needed


def test_mapping_is_case_and_space_normalized():
    result = map_finding("  SECRET-SCANNING-DISABLED  ")
    assert result.finding_type == "secret-scanning-disabled"


def test_unknown_finding_raises_key_error():
    with pytest.raises(KeyError):
        map_finding("not-a-real-finding")
