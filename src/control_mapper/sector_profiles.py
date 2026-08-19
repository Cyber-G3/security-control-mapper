from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Sector(StrEnum):
    GENERAL = "general"
    SAAS_TECHNOLOGY = "saas-technology"
    CLOUD_PROVIDER = "cloud-provider"
    FINANCIAL_SERVICES = "financial-services"
    HEALTHCARE_LIFE_SCIENCES = "healthcare-life-sciences"
    PUBLIC_SECTOR = "public-sector"
    CRITICAL_INFRASTRUCTURE = "critical-infrastructure"
    MANUFACTURING_INDUSTRIAL = "manufacturing-industrial"
    PROFESSIONAL_SERVICES = "professional-services"


@dataclass(frozen=True)
class SectorProfile:
    sector: Sector
    label: str
    risk_adjustment: int
    evidence_focus: tuple[str, ...]
    priority_domains: tuple[str, ...]
    disclaimer: str = (
        "Sector profiles tune contextual risk and evidence expectations only. "
        "They do not determine legal or regulatory applicability."
    )


_PROFILES: dict[Sector, SectorProfile] = {
    Sector.GENERAL: SectorProfile(
        Sector.GENERAL, "General", 0,
        ("governance", "identity", "vulnerability management", "incident response"),
        ("identity-access", "vulnerability-management", "governance"),
    ),
    Sector.SAAS_TECHNOLOGY: SectorProfile(
        Sector.SAAS_TECHNOLOGY, "SaaS / Technology", 5,
        ("secure development", "cloud security", "software supply chain", "availability"),
        ("repository-security", "cicd-security", "software-supply-chain", "cloud-security"),
    ),
    Sector.CLOUD_PROVIDER: SectorProfile(
        Sector.CLOUD_PROVIDER, "Cloud Provider", 10,
        ("tenant isolation", "privileged access", "logging", "resilience", "supplier dependencies"),
        ("cloud-security", "privileged-access", "logging-monitoring", "business-continuity"),
    ),
    Sector.FINANCIAL_SERVICES: SectorProfile(
        Sector.FINANCIAL_SERVICES, "Financial Services", 10,
        ("resilience", "access control", "third-party risk", "incident evidence"),
        ("privileged-access", "third-party-risk", "business-continuity", "incident-response"),
    ),
    Sector.HEALTHCARE_LIFE_SCIENCES: SectorProfile(
        Sector.HEALTHCARE_LIFE_SCIENCES, "Healthcare / Life Sciences", 10,
        ("sensitive data", "availability", "access control", "supplier risk"),
        ("data-protection", "identity-access", "backup-recovery", "third-party-risk"),
    ),
    Sector.PUBLIC_SECTOR: SectorProfile(
        Sector.PUBLIC_SECTOR, "Public Sector", 8,
        ("governance", "access control", "auditability", "resilience"),
        ("governance", "identity-access", "logging-monitoring", "business-continuity"),
    ),
    Sector.CRITICAL_INFRASTRUCTURE: SectorProfile(
        Sector.CRITICAL_INFRASTRUCTURE, "Critical Infrastructure", 15,
        ("service continuity", "incident response", "segmentation", "supply chain"),
        ("business-continuity", "incident-response", "network-security", "third-party-risk"),
    ),
    Sector.MANUFACTURING_INDUSTRIAL: SectorProfile(
        Sector.MANUFACTURING_INDUSTRIAL, "Manufacturing / Industrial", 8,
        ("availability", "network segmentation", "legacy systems", "supplier dependencies"),
        ("network-security", "patch-management", "business-continuity", "third-party-risk"),
    ),
    Sector.PROFESSIONAL_SERVICES: SectorProfile(
        Sector.PROFESSIONAL_SERVICES, "Professional Services", 3,
        ("client data", "identity", "endpoint security", "third parties"),
        ("data-protection", "identity-access", "endpoint-security", "third-party-risk"),
    ),
}


def get_sector_profile(sector: Sector | str) -> SectorProfile:
    normalized = sector if isinstance(sector, Sector) else Sector(sector.strip().lower())
    return _PROFILES[normalized]


def list_sector_profiles() -> list[SectorProfile]:
    return [_PROFILES[sector] for sector in Sector]
