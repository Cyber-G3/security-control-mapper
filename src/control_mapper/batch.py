from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from control_mapper.engine import map_check_id, map_finding
from control_mapper.models import MappingResult


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def map_collector_findings(path: Path) -> list[MappingResult]:
    payload = _load_json(path)
    findings = payload.get("findings", []) if isinstance(payload, dict) else []
    results: list[MappingResult] = []
    for finding in findings:
        check_id = str(finding.get("check_id", "")).strip()
        if not check_id:
            continue
        try:
            results.append(
                map_check_id(
                    check_id,
                    finding_id=str(finding.get("finding_id") or "") or None,
                    severity=str(finding.get("severity") or "") or None,
                )
            )
        except KeyError:
            continue
    return results


def map_batch(path: Path) -> list[MappingResult]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = _load_json(path)
        if isinstance(payload, dict) and "findings" in payload:
            return map_collector_findings(path)
        items = payload if isinstance(payload, list) else []
        results: list[MappingResult] = []
        for item in items:
            if isinstance(item, str):
                results.append(map_finding(item))
            elif isinstance(item, dict) and item.get("finding_type"):
                results.append(map_finding(str(item["finding_type"])))
        return results

    if suffix == ".csv":
        results = []
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                finding_type = str(row.get("finding_type") or "").strip()
                check_id = str(row.get("check_id") or "").strip()
                if finding_type:
                    results.append(map_finding(finding_type))
                elif check_id:
                    results.append(map_check_id(check_id))
        return results

    raise ValueError("Input must be .json or .csv")


def export_results(results: list[MappingResult], output: Path) -> None:
    if output.suffix.lower() == ".json":
        output.write_text(
            json.dumps([item.model_dump(mode="json") for item in results], indent=2),
            encoding="utf-8",
        )
        return

    if output.suffix.lower() == ".csv":
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "finding_type",
                    "source_check_id",
                    "source_finding_id",
                    "source_severity",
                    "mapping_version",
                    "framework",
                    "reference",
                    "title",
                    "relevance",
                    "evidence_needed",
                ],
            )
            writer.writeheader()
            for result in results:
                for reference in result.references:
                    writer.writerow(
                        {
                            "finding_type": result.finding_type,
                            "source_check_id": result.source_check_id or "",
                            "source_finding_id": result.source_finding_id or "",
                            "source_severity": result.source_severity or "",
                            "mapping_version": result.mapping_version,
                            "framework": reference.framework,
                            "reference": reference.reference,
                            "title": reference.title,
                            "relevance": reference.relevance,
                            "evidence_needed": " | ".join(result.evidence_needed),
                        }
                    )
        return

    raise ValueError("Output must be .json or .csv")
