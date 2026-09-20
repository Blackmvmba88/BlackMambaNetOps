from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Drift:
    key: str
    before: Any
    after: Any


def diff(before: Mapping[str, Any], after: Mapping[str, Any]) -> list[Drift]:
    """Describe change without pretending that change is malicious."""
    keys = before.keys() | after.keys()
    return [
        Drift(k, before.get(k), after.get(k))
        for k in sorted(keys)
        if before.get(k) != after.get(k)
    ]
