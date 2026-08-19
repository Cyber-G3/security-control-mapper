from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RiskPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


_SEVERITY = {"LOW": 10, "MEDIUM": 30, "HIGH": 55, "CRITICAL": 75}
_ASSET = {"LOW": 0, "MEDIUM": 8, "HIGH": 15, "CRITICAL": 22}
_DATA = {"PUBLIC": 0, "INTERNAL": 4, "CONFIDENTIAL": 9, "RESTRICTED": 14}
_SERVICE = {"LOW": 0, "MEDIUM": 5, "HIGH": 10, "CRITICAL": 15}


@dataclass(frozen=True)
class RiskContext:
    severity: str = "MEDIUM"
    asset_criticality: str = "MEDIUM"
    internet_exposed: bool = False
    active_exploitation: bool = False
    data_sensitivity: str = "INTERNAL"
    service_criticality: str = "MEDIUM"
    compensating_controls: bool = False


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    priority: RiskPriority
    reason_codes: tuple[str, ...]
    remediation_urgency: str


def _normalise(value: str) -> str:
    return value.strip().upper()


def assess_risk(context: RiskContext) -> RiskAssessment:
    severity = _normalise(context.severity)
    asset = _normalise(context.asset_criticality)
    data = _normalise(context.data_sensitivity)
    service = _normalise(context.service_criticality)

    try:
        score = _SEVERITY[severity] + _ASSET[asset] + _DATA[data] + _SERVICE[service]
    except KeyError as exc:
        raise ValueError(f"Unsupported risk context value: {exc.args[0]}") from exc

    reasons: list[str] = [f"severity:{severity.lower()}"]

    if asset in {"HIGH", "CRITICAL"}:
        reasons.append(f"asset:{asset.lower()}")
    if context.internet_exposed:
        score += 12
        reasons.append("internet_exposed")
    if context.active_exploitation:
        score += 20
        reasons.append("active_exploitation")
    if data in {"CONFIDENTIAL", "RESTRICTED"}:
        reasons.append(f"data:{data.lower()}")
    if service in {"HIGH", "CRITICAL"}:
        reasons.append(f"service:{service.lower()}")
    if context.compensating_controls:
        score -= 12
        reasons.append("compensating_controls")

    score = max(0, min(100, score))

    if score >= 85:
        priority = RiskPriority.CRITICAL
        urgency = "Immediate / emergency remediation review"
    elif score >= 65:
        priority = RiskPriority.HIGH
        urgency = "Prioritize for rapid remediation"
    elif score >= 40:
        priority = RiskPriority.MEDIUM
        urgency = "Plan remediation in the normal security backlog"
    else:
        priority = RiskPriority.LOW
        urgency = "Track and remediate according to standard maintenance"

    return RiskAssessment(
        score=score,
        priority=priority,
        reason_codes=tuple(reasons),
        remediation_urgency=urgency,
    )
