import pytest

from control_mapper.risk import RiskContext, RiskPriority, assess_risk


def test_critical_context_is_prioritized():
    result = assess_risk(
        RiskContext(
            severity="CRITICAL",
            asset_criticality="CRITICAL",
            internet_exposed=True,
            active_exploitation=True,
            data_sensitivity="RESTRICTED",
            service_criticality="CRITICAL",
        )
    )
    assert result.priority is RiskPriority.CRITICAL
    assert result.score == 100
    assert "active_exploitation" in result.reason_codes


def test_compensating_controls_reduce_but_do_not_hide_risk():
    untreated = assess_risk(
        RiskContext(severity="HIGH", asset_criticality="HIGH", internet_exposed=True)
    )
    treated = assess_risk(
        RiskContext(
            severity="HIGH",
            asset_criticality="HIGH",
            internet_exposed=True,
            compensating_controls=True,
        )
    )
    assert treated.score < untreated.score
    assert "compensating_controls" in treated.reason_codes


def test_invalid_context_is_rejected():
    with pytest.raises(ValueError):
        assess_risk(RiskContext(severity="EXTREME"))
