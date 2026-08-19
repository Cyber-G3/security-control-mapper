from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


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


_FINDINGS: tuple[FindingDefinition, ...] = (
    FindingDefinition(
        "SCM-REP-001", "branch-protection-disabled", "Branch protection disabled",
        FindingDomain.REPOSITORY_SECURITY, "HIGH", "github",
        "Enable protected-branch rules appropriate to the repository's change-control model.",
        ("Branch protection configuration", "Change approval workflow"),
    ),
    FindingDefinition(
        "SCM-REP-002", "required-pr-reviews-disabled", "Required PR reviews disabled",
        FindingDomain.REPOSITORY_SECURITY, "HIGH", "github",
        "Require independent review before changes can be merged.",
        ("Pull-request approval rules", "Reviewer assignment evidence"),
    ),
    FindingDefinition(
        "SCM-SEC-001", "secret-scanning-disabled", "Secret scanning disabled",
        FindingDomain.SECRETS, "HIGH", "github",
        "Enable secret scanning or an equivalent detective control and define credential rotation handling.",
        ("Secret scanning configuration", "Credential management procedure"),
    ),
    FindingDefinition(
        "SCM-VUL-001", "critical-vulnerability-overdue", "Critical vulnerability remediation overdue",
        FindingDomain.VULNERABILITY_MANAGEMENT, "CRITICAL", "vulnerability-scanner",
        "Prioritize remediation or documented risk treatment for overdue critical vulnerabilities.",
        ("Vulnerability record", "Remediation evidence", "Risk acceptance if applicable"),
    ),
    FindingDefinition(
        "SCM-IAM-001", "mfa-not-enforced", "Multi-factor authentication not enforced",
        FindingDomain.IDENTITY_ACCESS, "HIGH", "identity-provider",
        "Enforce MFA for applicable identities, with stronger requirements for privileged access.",
        ("MFA enforcement policy", "Identity-provider configuration"),
    ),
    FindingDefinition(
        "SCM-PAM-001", "privileged-access-not-reviewed", "Privileged access not periodically reviewed",
        FindingDomain.PRIVILEGED_ACCESS, "HIGH", "identity-provider",
        "Establish periodic privileged-access review and evidence reviewer decisions.",
        ("Privileged access inventory", "Access review record"),
    ),
    FindingDefinition(
        "SCM-LOG-001", "security-logging-disabled", "Security logging disabled or insufficient",
        FindingDomain.LOGGING_MONITORING, "HIGH", "siem",
        "Enable security-relevant logging and define retention, monitoring and alerting requirements.",
        ("Logging configuration", "Retention configuration", "Alerting evidence"),
    ),
    FindingDefinition(
        "SCM-BCK-001", "backup-restore-not-tested", "Backup restoration not tested",
        FindingDomain.BACKUP_RECOVERY, "HIGH", "backup-platform",
        "Perform and evidence restoration testing at a frequency aligned to service criticality.",
        ("Backup configuration", "Restore test record", "Recovery result"),
    ),
    FindingDefinition(
        "SCM-IR-001", "incident-plan-not-tested", "Incident response plan not tested",
        FindingDomain.INCIDENT_RESPONSE, "MEDIUM", "governance",
        "Run an incident-response exercise and capture lessons, actions and ownership.",
        ("Incident response plan", "Exercise record", "Improvement actions"),
    ),
    FindingDefinition(
        "SCM-TPR-001", "critical-supplier-not-assessed", "Critical supplier security risk not assessed",
        FindingDomain.THIRD_PARTY_RISK, "HIGH", "tprm",
        "Perform a risk-based supplier security assessment and document treatment decisions.",
        ("Supplier inventory", "Risk assessment", "Due-diligence evidence"),
    ),
)


def list_findings(*, domain: FindingDomain | None = None) -> list[FindingDefinition]:
    findings = list(_FINDINGS)
    if domain is not None:
        findings = [item for item in findings if item.domain is domain]
    return sorted(findings, key=lambda item: item.finding_id)


def get_finding(finding_type: str) -> FindingDefinition:
    normalized = finding_type.strip().lower()
    for item in _FINDINGS:
        if item.finding_type == normalized:
            return item
    raise KeyError(f"Unknown catalog finding type: {finding_type}")
