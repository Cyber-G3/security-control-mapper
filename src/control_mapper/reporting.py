from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass

from control_mapper.models import CoverageResult, CoverageStatus


@dataclass(frozen=True)
class FrameworkSummary:
    framework: str
    total: int
    supported: int
    partial: int
    gap: int
    unknown: int


@dataclass(frozen=True)
class AssuranceSummary:
    total_controls: int
    supported: int
    partial: int
    gap: int
    unknown: int
    frameworks: list[FrameworkSummary]
    priority_actions: list[dict[str, object]]

    def to_dict(self) -> dict[str, object]:
        return {
            "total_controls": self.total_controls,
            "supported": self.supported,
            "partial": self.partial,
            "gap": self.gap,
            "unknown": self.unknown,
            "frameworks": [asdict(item) for item in self.frameworks],
            "priority_actions": self.priority_actions,
        }


def summarize_coverage(results: list[CoverageResult]) -> AssuranceSummary:
    counts = Counter(item.status for item in results)
    grouped: dict[str, list[CoverageResult]] = defaultdict(list)
    for item in results:
        grouped[item.framework].append(item)

    frameworks: list[FrameworkSummary] = []
    for framework, items in sorted(grouped.items()):
        local = Counter(item.status for item in items)
        frameworks.append(
            FrameworkSummary(
                framework=framework,
                total=len(items),
                supported=local[CoverageStatus.SUPPORTED],
                partial=local[CoverageStatus.PARTIAL],
                gap=local[CoverageStatus.GAP],
                unknown=local[CoverageStatus.UNKNOWN],
            )
        )

    rank = {
        CoverageStatus.GAP: 0,
        CoverageStatus.PARTIAL: 1,
        CoverageStatus.UNKNOWN: 2,
        CoverageStatus.SUPPORTED: 3,
    }
    actions: list[dict[str, object]] = []
    for item in sorted(results, key=lambda x: (rank[x.status], x.framework, x.reference)):
        if item.status is CoverageStatus.SUPPORTED:
            continue
        actions.append(
            {
                "framework": item.framework,
                "reference": item.reference,
                "title": item.title,
                "status": item.status.value,
                "confidence": item.confidence.value,
                "failing_checks": item.failing_checks,
                "unknown_checks": item.unknown_checks,
                "evidence_needed": item.evidence_needed,
            }
        )

    return AssuranceSummary(
        total_controls=len(results),
        supported=counts[CoverageStatus.SUPPORTED],
        partial=counts[CoverageStatus.PARTIAL],
        gap=counts[CoverageStatus.GAP],
        unknown=counts[CoverageStatus.UNKNOWN],
        frameworks=frameworks,
        priority_actions=actions,
    )
