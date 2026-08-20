from __future__ import annotations

import json
from pathlib import Path

from control_mapper.reporting import AssuranceSummary


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, str)]


def render_markdown(summary: AssuranceSummary) -> str:
    lines = [
        "# Security Assurance Coverage Report",
        "",
        "> Evidence-support analysis only. This report does not establish compliance, certification, legal applicability, or full control implementation.",
        "",
        "## Executive summary",
        "",
        f"- Total mapped controls/references: {summary.total_controls}",
        f"- Supported: {summary.supported}",
        f"- Partial: {summary.partial}",
        f"- Gap: {summary.gap}",
        f"- Unknown: {summary.unknown}",
        "",
        "## Coverage by framework",
        "",
        "| Framework | Total | Supported | Partial | Gap | Unknown |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for framework_summary in summary.frameworks:
        lines.append(
            f"| {framework_summary.framework} | {framework_summary.total} | "
            f"{framework_summary.supported} | {framework_summary.partial} | "
            f"{framework_summary.gap} | {framework_summary.unknown} |"
        )

    lines.extend(["", "## Prioritized evidence actions", ""])
    if not summary.priority_actions:
        lines.append("No mapped evidence gaps were identified from the supplied observations.")
    else:
        for index, action in enumerate(summary.priority_actions, start=1):
            lines.append(
                f"### {index}. {action['framework']} {action['reference']} — {action['status']}"
            )
            lines.append("")
            lines.append(str(action["title"]))
            lines.append("")
            lines.append(f"Mapping confidence: **{action['confidence']}**")
            failing = _string_list(action["failing_checks"])
            unknown = _string_list(action["unknown_checks"])
            evidence = _string_list(action["evidence_needed"])
            if failing:
                lines.append(f"\nFailing checks: {', '.join(failing)}")
            if unknown:
                lines.append(f"\nUnknown checks: {', '.join(unknown)}")
            if evidence:
                lines.append("\nEvidence/actions needed:")
                for evidence_item in evidence:
                    lines.append(f"- {evidence_item}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def export_summary(summary: AssuranceSummary, output: Path) -> None:
    suffix = output.suffix.lower()
    if suffix == ".json":
        output.write_text(json.dumps(summary.to_dict(), indent=2) + "\n", encoding="utf-8")
        return
    if suffix in {".md", ".markdown"}:
        output.write_text(render_markdown(summary), encoding="utf-8")
        return
    raise ValueError("Report output must be .json or .md")
