import json
from pathlib import Path

from control_mapper.collector_pack import load_evidence_pack_observations
from control_mapper.coverage import calculate_coverage
from control_mapper.models import CoverageStatus


def _write_check(root: Path, name: str, check_id: str, status: str) -> None:
    path = root / "normalized" / "github" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"check_id": check_id, "status": status, "reason": "test"}),
        encoding="utf-8",
    )


def test_loads_full_evidence_pack_and_calculates_mixed_coverage(tmp_path: Path):
    _write_check(tmp_path, "branch.json", "github.branch.protection", "PASS")
    _write_check(tmp_path, "reviews.json", "github.branch.required_reviews", "FAIL")
    observations = load_evidence_pack_observations(tmp_path)
    results = calculate_coverage(observations)
    a832 = next(
        item for item in results
        if item.framework == "ISO/IEC 27001:2022" and item.reference == "A.8.32"
    )
    assert a832.status is CoverageStatus.PARTIAL
    assert "github.branch.protection" in a832.supporting_checks
    assert "github.branch.required_reviews" in a832.failing_checks


def test_new_taxonomy_maps_dependabot_and_workflow_permissions(tmp_path: Path):
    _write_check(tmp_path, "dep.json", "github.dependencies.dependabot_config", "FAIL")
    _write_check(
        tmp_path,
        "permissions.json",
        "github.actions.default_workflow_permissions",
        "UNKNOWN",
    )
    results = calculate_coverage(load_evidence_pack_observations(tmp_path))
    references = {(item.framework, item.reference, item.status.value) for item in results}
    assert ("ISO/IEC 27001:2022", "A.8.8", "GAP") in references
    assert ("ISO/IEC 27001:2022", "A.8.2", "UNKNOWN") in references
