from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class EvidenceQuality(StrEnum):
    PRESENT = "PRESENT"
    MISSING = "MISSING"
    STALE = "STALE"
    INCOMPLETE = "INCOMPLETE"
    UNVERIFIED = "UNVERIFIED"


@dataclass(frozen=True)
class EvidenceContext:
    present: bool
    collected_at: datetime | None = None
    max_age_days: int | None = None
    integrity_verified: bool = False
    complete: bool = True
    provenance_present: bool = True
    owner_present: bool = True


@dataclass(frozen=True)
class EvidenceAssessment:
    quality: EvidenceQuality
    reason_codes: tuple[str, ...]
    age_days: int | None


def assess_evidence_quality(
    context: EvidenceContext,
    *,
    now: datetime | None = None,
) -> EvidenceAssessment:
    """Assess evidence quality without making a compliance determination."""
    if not context.present:
        return EvidenceAssessment(
            quality=EvidenceQuality.MISSING,
            reason_codes=("evidence_missing",),
            age_days=None,
        )

    reasons: list[str] = []
    age_days: int | None = None

    if not context.complete:
        reasons.append("evidence_incomplete")
    if not context.provenance_present:
        reasons.append("provenance_missing")
    if not context.owner_present:
        reasons.append("owner_missing")

    if context.collected_at is not None:
        reference = now or datetime.now(UTC)
        collected = context.collected_at
        if collected.tzinfo is None:
            collected = collected.replace(tzinfo=UTC)
        age_days = max(0, (reference - collected).days)
        if context.max_age_days is not None and age_days > context.max_age_days:
            reasons.append("evidence_stale")

    if "evidence_stale" in reasons:
        quality = EvidenceQuality.STALE
    elif "evidence_incomplete" in reasons or "provenance_missing" in reasons or "owner_missing" in reasons:
        quality = EvidenceQuality.INCOMPLETE
    elif not context.integrity_verified:
        reasons.append("integrity_unverified")
        quality = EvidenceQuality.UNVERIFIED
    else:
        quality = EvidenceQuality.PRESENT
        reasons.append("evidence_current_and_verified")

    return EvidenceAssessment(
        quality=quality,
        reason_codes=tuple(reasons),
        age_days=age_days,
    )
