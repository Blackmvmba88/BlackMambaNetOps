from __future__ import annotations

from dataclasses import dataclass
from .ledger import ObservationEvent


@dataclass(frozen=True)
class Finding:
    subject: str
    sources: tuple[str, ...]
    kinds: tuple[str, ...]
    evidence_count: int
    status: str


def correlate(events: tuple[ObservationEvent, ...]) -> list[Finding]:
    """Correlate evidence without claiming compromise or attacker identity."""
    grouped: dict[str, list[ObservationEvent]] = {}
    for event in events:
        grouped.setdefault(event.subject, []).append(event)

    findings: list[Finding] = []
    for subject, observed in sorted(grouped.items()):
        sources = tuple(sorted({e.source for e in observed}))
        kinds = tuple(sorted({e.kind for e in observed}))
        findings.append(Finding(
            subject=subject,
            sources=sources,
            kinds=kinds,
            evidence_count=len(observed),
            status="corroborated" if len(sources) >= 2 else "single-source",
        ))
    return findings
