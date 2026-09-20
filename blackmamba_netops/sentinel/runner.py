from __future__ import annotations

from .ledger import EvidenceLedger
from .sensors import ReadOnlySensor


def collect(ledger: EvidenceLedger, sensors: list[ReadOnlySensor]) -> EvidenceLedger:
    """Collect witnesses into one epoch ledger while preserving source provenance."""
    for sensor in sensors:
        for observation in sensor.observe():
            ledger.append(source=observation.source, kind=observation.kind, subject=observation.subject, payload=observation.payload)
    return ledger
