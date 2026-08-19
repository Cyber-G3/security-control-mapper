from __future__ import annotations

import json

import typer

from control_mapper.engine import list_finding_types, map_finding

app = typer.Typer(help="Map technical security findings to supporting control references.")


@app.command("list-findings")
def list_findings() -> None:
    for finding_type in list_finding_types():
        typer.echo(finding_type)


@app.command("map")
def map_command(
    finding_type: str = typer.Argument(..., help="Normalized finding type."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON."),
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
            f"- {reference.framework} {reference.reference}: {reference.title} — {reference.relevance}"
        )
    typer.echo(result.disclaimer)


if __name__ == "__main__":
    app()
