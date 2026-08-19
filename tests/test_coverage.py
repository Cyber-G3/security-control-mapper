from control_mapper.coverage import calculate_coverage
from control_mapper.models import CoverageStatus, ObservationStatus, TechnicalObservation


def test_gap_when_mapped_check_fails():
    results = calculate_coverage([
        TechnicalObservation(check_id="github.branch.protection", status=ObservationStatus.FAIL)
    ])
    assert results
    assert any(item.status is CoverageStatus.GAP for item in results)
    assert any(item.evidence_needed for item in results)


def test_partial_when_shared_control_has_pass_and_fail():
    results = calculate_coverage([
        TechnicalObservation(check_id="github.branch.protection", status=ObservationStatus.PASS),
        TechnicalObservation(check_id="github.branch.required_reviews", status=ObservationStatus.FAIL),
    ])
    iso = [
        item for item in results
        if item.framework == "ISO/IEC 27001:2022" and item.reference == "A.8.32"
    ]
    assert iso and iso[0].status is CoverageStatus.PARTIAL
    assert "github.branch.protection" in iso[0].supporting_checks
    assert "github.branch.required_reviews" in iso[0].failing_checks


def test_unknown_is_not_treated_as_gap():
    results = calculate_coverage([
        TechnicalObservation(check_id="github.security.secret_scanning", status=ObservationStatus.UNKNOWN)
    ])
    assert results
    assert all(item.status is CoverageStatus.UNKNOWN for item in results)
