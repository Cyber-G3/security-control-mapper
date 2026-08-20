import json
from pathlib import Path

from control_mapper.cli import app
from control_mapper.portfolio import FindingInput, prioritize_findings
from control_mapper.report_export import export_summary, render_markdown
from control_mapper.reporting import AssuranceSummary, FrameworkSummary
from typer.testing import CliRunner


runner = CliRunner()


def test_cli_lists_findings_and_maps_json() -> None:
    listed = runner.invoke(app, ["list-findings"])
    assert listed.exit_code == 0
    assert "branch-protection-disabled" in listed.stdout

    mapped = runner.invoke(app, ["map", "branch-protection-disabled", "--json"])
    assert mapped.exit_code == 0
    payload = json.loads(mapped.stdout)
    assert payload["finding_type"] == "branch-protection-disabled"
    assert payload["mapping_version"] == "0.3"
    assert payload["references"]


def test_cli_map_file_exports_results(tmp_path: Path) -> None:
    source = tmp_path / "findings.csv"
    output = tmp_path / "mapped.json"
    source.write_text("finding_type\nsecret-scanning-disabled\n", encoding="utf-8")

    result = runner.invoke(app, ["map-file", str(source), "--output", str(output)])
    assert result.exit_code == 0
    assert "Exported:" in result.stdout
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload[0]["finding_type"] == "secret-scanning-disabled"


def test_portfolio_prioritizes_contextual_findings() -> None:
    summary = prioritize_findings(
        [
            FindingInput(
                finding_type="branch-protection-disabled",
                asset_criticality="CRITICAL",
                internet_exposed=True,
                active_exploitation=True,
                service_criticality="CRITICAL",
            ),
            FindingInput(finding_type="secret-scanning-disabled"),
        ]
    )
    assert summary.total == 2
    assert len(summary.assessments) == 2
    assert summary.assessments[0].risk.score >= summary.assessments[1].risk.score
    assert summary.critical + summary.high + summary.medium + summary.low == 2


def _summary() -> AssuranceSummary:
    return AssuranceSummary(
        total_controls=2,
        supported=1,
        partial=0,
        gap=1,
        unknown=0,
        frameworks=[
            FrameworkSummary(
                framework="NIS2",
                total=2,
                supported=1,
                partial=0,
                gap=1,
                unknown=0,
            )
        ],
        priority_actions=[
            {
                "framework": "NIS2",
                "reference": "Article 21(2)(e)",
                "title": "Technical vulnerability management",
                "status": "GAP",
                "confidence": "SUPPORTING",
                "failing_checks": ["github.branch.protection"],
                "unknown_checks": [],
                "evidence_needed": ["Approved remediation record"],
            }
        ],
    )


def test_report_export_renders_markdown_and_json(tmp_path: Path) -> None:
    summary = _summary()
    markdown = render_markdown(summary)
    assert "Security Assurance Coverage Report" in markdown
    assert "Article 21(2)(e)" in markdown
    assert "Approved remediation record" in markdown

    json_path = tmp_path / "report.json"
    md_path = tmp_path / "report.md"
    export_summary(summary, json_path)
    export_summary(summary, md_path)
    assert json.loads(json_path.read_text(encoding="utf-8"))["gap"] == 1
    assert "Evidence-support analysis only" in md_path.read_text(encoding="utf-8")
