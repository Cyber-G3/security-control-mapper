from control_mapper.contextual_assessment import assess_finding


def test_financial_sector_increases_priority_context() -> None:
    general = assess_finding("mfa-not-enforced", sector="general")
    financial = assess_finding("mfa-not-enforced", sector="financial-services")
    assert financial.risk.score >= general.risk.score
    assert "sector:financial-services" in financial.risk.reason_codes


def test_critical_infrastructure_priority_domain_bonus() -> None:
    result = assess_finding(
        "incident-plan-not-tested",
        sector="critical-infrastructure",
        service_criticality="HIGH",
    )
    assert "sector_priority_domain:incident-response" in result.risk.reason_codes


def test_contextual_assessment_preserves_remediation_and_evidence() -> None:
    result = assess_finding("critical-supplier-not-assessed", sector="healthcare-life-sciences")
    assert result.remediation
    assert result.expected_evidence
    assert "compliance" in result.disclaimer.lower()
