from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Confidence(str, Enum):
    OBSERVED = "observed"
    VERIFIED = "verified"
    OPERATOR = "operator"


@dataclass(frozen=True)
class Evidence:
    source: str
    key: str
    value: Any
    confidence: Confidence = Confidence.OBSERVED


@dataclass
class Capability:
    name: str
    readable: bool = True
    writable: bool = False
    protected: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DeviceRecord:
    stable_id: str
    observed: dict[str, Any] = field(default_factory=dict)
    annotations: dict[str, Any] = field(default_factory=dict)
    evidence: list[Evidence] = field(default_factory=list)

    def annotate(self, key: str, value: Any) -> None:
        """Human meaning never overwrites observed router evidence."""
        self.annotations[key] = value
