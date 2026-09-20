from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any


@dataclass(frozen=True)
class ObservationEvent:
    epoch: str
    source: str
    kind: str
    subject: str
    payload: dict[str, Any]
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def canonical(self) -> bytes:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), default=str).encode()

    @property
    def digest(self) -> str:
        return sha256(self.canonical()).hexdigest()


class EvidenceLedger:
    """Append-only in-memory ledger; storage backends can persist/export it later."""

    def __init__(self, epoch: str) -> None:
        self.epoch = epoch
        self._events: list[ObservationEvent] = []

    def append(self, *, source: str, kind: str, subject: str, payload: dict[str, Any]) -> ObservationEvent:
        event = ObservationEvent(self.epoch, source, kind, subject, dict(payload))
        self._events.append(event)
        return event

    def events(self) -> tuple[ObservationEvent, ...]:
        return tuple(self._events)

    def export(self) -> dict[str, Any]:
        return {
            "epoch": self.epoch,
            "events": [{**asdict(e), "sha256": e.digest} for e in self._events],
        }
