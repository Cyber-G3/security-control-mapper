from control_mapper.models import (
    CoverageResult,
    CoverageStatus,
    MappingConfidence,
)
from control_mapper.reporting import summarize_coverage


def _item(framework: str, reference: str, status: CoverageStatus) -> CoverageResult:
    return CoverageResult(
        framework=framework,
        reference=reference,
        title="Example",
        status=status,
        confidence=MappingConfidence.SUPPORTING,
        supporting_checks=["check.pass"] if status is CoverageStatus.SUPPORTED else [],
        failing_checks=["check.fail"] if status is CoverageStatus.GAP else [],
        unknown_checks=["check.unknown"] if status is CoverageStatus.UNKNOWN else [],
        evidence_needed=[] if status is CoverageStatus.SUPPORTED else ["Evidence item"],
        mapping_version="0.3",
    )


def test_summarize_coverage_counts_and_prioritizes_gaps():
    summary = summarize_coverage(
        [
            _item("ISO/IEC 27001:2022", "A.8.8", CoverageStatus.GAP),
            _item("ISO/IEC 27001:2022", "A.8.32", CoverageStatus.PARTIAL),
            _item("ENS", "org.3", CoverageStatus.SUPPORTED),
            _item("NIS2", "Article 21(2)(e)", CoverageStatus.UNKNOWN),
        ]
    )
    assert summary.total_controls == 4
    assert summary.gap == 1
    assert summary.partial == 1
    assert summary.supported == 1
    assert summary.unknown == 1
    assert summary.priority_actions[0]["status"] == "GAP"
    assert len(summary.frameworks) == 3
