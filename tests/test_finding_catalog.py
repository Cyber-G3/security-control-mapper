import pytest

from control_mapper.finding_catalog import FindingDomain, get_finding, list_findings


def test_catalog_contains_cross_domain_findings() -> None:
    findings = list_findings()
    assert any(item.finding_type == "branch-protection-disabled" for item in findings)
    assert any(item.finding_type == "mfa-not-enforced" for item in findings)
    assert any(item.finding_type == "critical-supplier-not-assessed" for item in findings)


def test_catalog_can_filter_by_domain() -> None:
    findings = list_findings(domain=FindingDomain.IDENTITY_ACCESS)
    assert findings
    assert all(item.domain is FindingDomain.IDENTITY_ACCESS for item in findings)


def test_catalog_lookup_is_normalized() -> None:
    finding = get_finding("  MFA-NOT-ENFORCED  ")
    assert finding.finding_id == "SCM-IAM-001"


def test_unknown_catalog_finding_raises() -> None:
    with pytest.raises(KeyError):
        get_finding("unknown-finding")
