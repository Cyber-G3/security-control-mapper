from datetime import UTC, datetime, timedelta

from control_mapper.evidence_quality import (
    EvidenceContext,
    EvidenceQuality,
    assess_evidence_quality,
)


def test_missing_evidence() -> None:
    result = assess_evidence_quality(EvidenceContext(present=False))
    assert result.quality == EvidenceQuality.MISSING


def test_stale_evidence() -> None:
    now = datetime(2026, 8, 19, tzinfo=UTC)
    result = assess_evidence_quality(
        EvidenceContext(
            present=True,
            collected_at=now - timedelta(days=91),
            max_age_days=90,
            integrity_verified=True,
        ),
        now=now,
    )
    assert result.quality == EvidenceQuality.STALE
    assert result.age_days == 91


def test_unverified_evidence() -> None:
    result = assess_evidence_quality(
        EvidenceContext(present=True, integrity_verified=False)
    )
    assert result.quality == EvidenceQuality.UNVERIFIED


def test_incomplete_evidence_has_priority_over_unverified() -> None:
    result = assess_evidence_quality(
        EvidenceContext(
            present=True,
            integrity_verified=False,
            complete=False,
        )
    )
    assert result.quality == EvidenceQuality.INCOMPLETE


def test_current_verified_evidence() -> None:
    result = assess_evidence_quality(
        EvidenceContext(present=True, integrity_verified=True)
    )
    assert result.quality == EvidenceQuality.PRESENT
