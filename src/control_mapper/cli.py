from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from control_mapper.batch import export_results, map_batch, map_collector_findings
from control_mapper.collector_pack import load_evidence_pack_observations
from control_mapper.coverage import calculate_coverage
from control_mapper.engine import list_finding_types, map_finding
from control_mapper.models import TechnicalObservation
from control_mapper.report_export import export_summary, render_markdown
from control_mapper.reporting import summarize_coverage

app = typer.Typer(help="Map technical security findings to supporting control references.")

FindingTypeArg = Annotated[str, typer.Argument(help="Normalized finding type.")]
InputFileArg = Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)]
InputDirArg = Annotated[Path, typer.Argument(exists=True, file_okay=False, readable=True)]
OutputOption = Annotated[Path | None, typer.Option("--output", "-o")]
JsonOption = Annotated[bool, typer.Option("--json", help="Emit machine-readable JSON.")]


@app.command("list-findings")
def list_findings() -> None:
    for finding_type in list_finding_types():
        typer.echo(finding_type)


@app.command("map")
def map_command(
    finding_type: FindingTypeArg,
    json_output: JsonOption = False,
) -> None:
    try:
        result = map_finding(finding_type)
    except KeyError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    if json_output:
        typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))
        return
    typer.echo(f"{result.finding_type}: {result.title}")
    typer.echo(f"Mapping version: {result.mapping_version}")
    typer.echo("Evidence needed:")
    for item in result.evidence_needed:
        typer.echo(f"- {item}")
    typer.echo("References:")
    for reference in result.references:
        typer.echo(
            f"- {reference.framework} {reference.reference}: {reference.title} "
            f"[{reference.confidence.value}] — {reference.relevance}"
        )
    typer.echo(result.disclaimer)


@app.command("map-file")
def map_file(
    input_path: InputFileArg,
    output: OutputOption = None,
) -> None:
    try:
        results = map_batch(input_path)
        if output is not None:
            export_results(results, output)
    except (KeyError, ValueError) as exc:
        typer.echo(f"Mapping failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    for result in results:
        typer.echo(f"{result.finding_type}: {len(result.references)} references")
    if output is not None:
        typer.echo(f"Exported: {output}")


@app.command("map-collector")
def map_collector(
    findings_path: InputFileArg,
    output: OutputOption = None,
) -> None:
    try:
        results = map_collector_findings(findings_path)
        if output is not None:
            export_results(results, output)
    except ValueError as exc:
        typer.echo(f"Collector mapping failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(f"Mapped {len(results)} collector findings")
    for result in results:
        typer.echo(
            f"{result.source_finding_id or '-'} | {result.source_check_id or '-'} | "
            f"{result.finding_type} | {len(result.references)} references"
        )
    if output is not None:
        typer.echo(f"Exported: {output}")


def _render_coverage(results, json_output: bool) -> None:
    if json_output:
        typer.echo(json.dumps([item.model_dump(mode="json") for item in results], indent=2))
        return
    typer.echo("Status    | Confidence | Framework | Reference | Evidence gaps")
    for item in results:
        typer.echo(
            f"{item.status.value:<9} | {item.confidence.value:<10} | {item.framework} | "
            f"{item.reference} | {len(item.evidence_needed)}"
        )


@app.command("coverage")
def coverage_command(
    observations_path: InputFileArg,
    json_output: JsonOption = False,
) -> None:
    try:
        payload = json.loads(observations_path.read_text(encoding="utf-8"))
        raw = payload.get("observations", payload) if isinstance(payload, dict) else payload
        if not isinstance(raw, list):
            raise TypeError("Expected a JSON list or an object with an observations list")
        observations = [TechnicalObservation.model_validate(item) for item in raw]
        results = calculate_coverage(observations)
    except Exception as exc:
        typer.echo(f"Coverage analysis failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    _render_coverage(results, json_output)


@app.command("coverage-pack")
def coverage_pack(
    evidence_pack: InputDirArg,
    json_output: JsonOption = False,
) -> None:
    try:
        observations = load_evidence_pack_observations(evidence_pack)
        results = calculate_coverage(observations)
    except Exception as exc:
        typer.echo(f"Evidence Pack coverage failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    _render_coverage(results, json_output)


@app.command("assurance-report")
def assurance_report(
    evidence_pack: InputDirArg,
    output: OutputOption = None,
    json_output: JsonOption = False,
) -> None:
    """Generate management-level assurance reporting from an Evidence Pack."""
    try:
        observations = load_evidence_pack_observations(evidence_pack)
        coverage = calculate_coverage(observations)
        summary = summarize_coverage(coverage)
        if output is not None:
            export_summary(summary, output)
    except Exception as exc:
        typer.echo(f"Assurance reporting failed: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    if json_output:
        typer.echo(json.dumps(summary.to_dict(), indent=2))
    else:
        typer.echo(render_markdown(summary))
    if output is not None:
        typer.echo(f"Exported: {output}")


if __name__ == "__main__":
    app()
