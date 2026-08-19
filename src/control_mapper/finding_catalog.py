from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from importlib.resources import files


class FindingDomain(StrEnum):
    REPOSITORY_SECURITY = "repository-security"
    IDENTITY_ACCESS = "identity-access"
    PRIVILEGED_ACCESS = "privileged-access"
    SECRETS = "secrets"
    VULNERABILITY_MANAGEMENT = "vulnerability-management"
    PATCH_MANAGEMENT = "patch-management"
    ENDPOINT_SECURITY = "endpoint-security"
    NETWORK_SECURITY = "network-security"
    CLOUD_SECURITY = "cloud-security"
    CICD_SECURITY = "cicd-security"
    SOFTWARE_SUPPLY_CHAIN = "software-supply-chain"
    LOGGING_MONITORING = "logging-monitoring"
    CRYPTOGRAPHY = "cryptography"
    BACKUP_RECOVERY = "backup-recovery"
    INCIDENT_RESPONSE = "incident-response"
    BUSINESS_CONTINUITY = "business-continuity"
    THIRD_PARTY_RISK = "third-party-risk"
    GOVERNANCE = "governance"
    DATA_PROTECTION = "data-protection"
    AI_SECURITY = "ai-security"


@dataclass(frozen=True)
class FindingDefinition:
    finding_id: str
    finding_type: str
    title: str
    domain: FindingDomain
    default_severity: str
    source_type: str
    remediation: str
    evidence_expected: tuple[str, ...]


def _load_catalog() -> tuple[str, tuple[FindingDefinition, ...]]:
    path = files("control_mapper").joinpath("data/findings-v0.2.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    version = str(payload["catalog_version"])
    findings = tuple(
        FindingDefinition(
            finding_id=str(item["finding_id"]),
            finding_type=str(item["finding_type"]),
            title=str(item["title"]),
            domain=FindingDomain(str(item["domain"])),
            default_severity=str(item["default_severity"]),
            source_type=str(item["source_type"]),
            remediation=str(item["remediation"]),
            evidence_expected=tuple(str(value) for value in item.get("evidence_expected", [])),
        )
        for item in payload["findings"]
    )
    return version, findings


def catalog_version() -> str:
    version, _ = _load_catalog()
    return version


def list_findings(*, domain: FindingDomain | None = None) -> list[FindingDefinition]:
    _, findings = _load_catalog()
    result = list(findings)
    if domain is not None:
        result = [item for item in result if item.domain is domain]
    return sorted(result, key=lambda item: item.finding_id)


def get_finding(finding_type: str) -> FindingDefinition:
    normalized = finding_type.strip().lower()
    _, findings = _load_catalog()
    for item in findings:
        if item.finding_type == normalized:
            return item
    raise KeyError(f"Unknown catalog finding type: {finding_type}")
