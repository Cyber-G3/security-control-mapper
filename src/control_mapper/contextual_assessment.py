from __future__ import annotations

from dataclasses import dataclass

from control_mapper.finding_catalog import FindingDefinition, get_finding
from control_mapper.risk import RiskAssessment, RiskContext, assess_risk
from control_mapper.sector_profiles import Sector, SectorProfile, get_sector_profile


@dataclass(frozen=True)
class ContextualAssessment:
    finding: FindingDefinition
    sector: SectorProfile
    risk: RiskAssessment
    expected_evidence: tuple[str, ...]
    remediation: str
    disclaimer: str = (
        "This contextual assessment prioritizes technical risk and evidence expectations. "
        "It does not establish legal applicability, certification status, or compliance."
    )


def assess_finding(
    finding_type: str,
    *,
    sector: Sector | str = Sector.GENERAL,
    asset_criticality: str = "MEDIUM",
    internet_exposed: bool = False,
    active_exploitation: bool = False,
    data_sensitivity: str = "INTERNAL",
    service_criticality: str = "MEDIUM",
    compensating_controls: bool = False,
) -> ContextualAssessment:
    finding = get_finding(finding_type)
    profile = get_sector_profile(sector)

    base_context = RiskContext(
        severity=finding.default_severity,
        asset_criticality=asset_criticality,
        internet_exposed=internet_exposed,
        active_exploitation=active_exploitation,
        data_sensitivity=data_sensitivity,
        service_criticality=service_criticality,
        compensating_controls=compensating_controls,
    )
    base = assess_risk(base_context)

    adjusted_score = max(0, min(100, base.score + profile.risk_adjustment))
    if finding.domain.value in profile.priority_domains:
        adjusted_score = min(100, adjusted_score + 5)

    if adjusted_score >= 85:
        priority = type(base.priority).CRITICAL
        urgency = "Immediate / emergency remediation review"
    elif adjusted_score >= 65:
        priority = type(base.priority).HIGH
        urgency = "Prioritize for rapid remediation"
    elif adjusted_score >= 40:
        priority = type(base.priority).MEDIUM
        urgency = "Plan remediation in the normal security backlog"
    else:
        priority = type(base.priority).LOW
        urgency = "Track and remediate according to standard maintenance"

    reasons = list(base.reason_codes)
    if profile.risk_adjustment:
        reasons.append(f"sector:{profile.sector.value}")
    if finding.domain.value in profile.priority_domains:
        reasons.append(f"sector_priority_domain:{finding.domain.value}")

    risk = RiskAssessment(
        score=adjusted_score,
        priority=priority,
        reason_codes=tuple(reasons),
        remediation_urgency=urgency,
    )

    return ContextualAssessment(
        finding=finding,
        sector=profile,
        risk=risk,
        expected_evidence=finding.evidence_expected,
        remediation=finding.remediation,
    )
