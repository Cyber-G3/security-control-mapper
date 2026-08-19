from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from control_mapper.contextual_assessment import ContextualAssessment, assess_finding


@dataclass(frozen=True)
class FindingInput:
    finding_type: str
    sector: str = "general"
    asset_criticality: str = "MEDIUM"
    internet_exposed: bool = False
    active_exploitation: bool = False
    data_sensitivity: str = "INTERNAL"
    service_criticality: str = "MEDIUM"
    compensating_controls: bool = False


@dataclass(frozen=True)
class PortfolioSummary:
    total: int
    critical: int
    high: int
    medium: int
    low: int
    assessments: tuple[ContextualAssessment, ...]


def prioritize_findings(items: list[FindingInput]) -> PortfolioSummary:
    assessments = [
        assess_finding(
            item.finding_type,
            sector=item.sector,
            asset_criticality=item.asset_criticality,
            internet_exposed=item.internet_exposed,
            active_exploitation=item.active_exploitation,
            data_sensitivity=item.data_sensitivity,
            service_criticality=item.service_criticality,
            compensating_controls=item.compensating_controls,
        )
        for item in items
    ]
    assessments.sort(
        key=lambda item: (-item.risk.score, item.finding.finding_id)
    )
    counts = Counter(item.risk.priority.value for item in assessments)
    return PortfolioSummary(
        total=len(assessments),
        critical=counts["CRITICAL"],
        high=counts["HIGH"],
        medium=counts["MEDIUM"],
        low=counts["LOW"],
        assessments=tuple(assessments),
    )
