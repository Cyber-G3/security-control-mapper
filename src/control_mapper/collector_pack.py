from __future__ import annotations

import json
from pathlib import Path

from control_mapper.models import ObservationStatus, TechnicalObservation


def load_evidence_pack_observations(pack_path: Path) -> list[TechnicalObservation]:
    normalized = pack_path / "normalized" / "github"
    if not normalized.is_dir():
        raise ValueError("Evidence Pack must contain normalized/github")

    observations: list[TechnicalObservation] = []
    for path in sorted(normalized.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        check_id = str(payload.get("check_id") or "").strip()
        status_raw = str(payload.get("status") or "").strip().upper()
        if not check_id or not status_raw:
            continue
        try:
            status = ObservationStatus(status_raw)
        except ValueError:
            status = ObservationStatus.UNKNOWN
        observations.append(
            TechnicalObservation(
                check_id=check_id,
                status=status,
                reason=str(payload.get("reason") or "") or None,
            )
        )
    if not observations:
        raise ValueError("No normalized GitHub observations found in Evidence Pack")
    return observations
