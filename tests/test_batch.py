import json
from pathlib import Path

from control_mapper.batch import export_results, map_batch, map_collector_findings


def test_map_collector_findings_preserves_source_metadata(tmp_path: Path):
    source = tmp_path / "findings.json"
    source.write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "finding_id": "GH-001",
                        "check_id": "github.governance.security_policy",
                        "severity": "MEDIUM",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    results = map_collector_findings(source)
    assert len(results) == 1
    assert results[0].finding_type == "security-policy-missing"
    assert results[0].source_finding_id == "GH-001"
    assert results[0].source_check_id == "github.governance.security_policy"
    assert results[0].source_severity == "MEDIUM"
    assert any(ref.framework == "ENS" for ref in results[0].references)


def test_map_batch_csv_supports_finding_type(tmp_path: Path):
    source = tmp_path / "input.csv"
    source.write_text("finding_type\nbranch-protection-disabled\n", encoding="utf-8")
    results = map_batch(source)
    assert len(results) == 1
    assert results[0].finding_type == "branch-protection-disabled"


def test_export_results_json(tmp_path: Path):
    source = tmp_path / "input.csv"
    source.write_text("finding_type\nrequired-pr-reviews-disabled\n", encoding="utf-8")
    results = map_batch(source)
    output = tmp_path / "output.json"
    export_results(results, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload[0]["finding_type"] == "required-pr-reviews-disabled"
    assert payload[0]["mapping_version"] == "0.2"
