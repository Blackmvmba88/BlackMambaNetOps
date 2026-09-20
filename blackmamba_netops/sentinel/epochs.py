from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EpochChange:
    subject: str
    status: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None


def compare_epochs(before: dict[str, Any], after: dict[str, Any]) -> list[EpochChange]:
    """Compare exported ledgers by stable source/kind/subject identity."""
    def index(bundle: dict[str, Any]) -> dict[tuple[str, str, str], dict[str, Any]]:
        return {(e["source"], e["kind"], e["subject"]): e for e in bundle.get("events", [])}

    old, new = index(before), index(after)
    changes: list[EpochChange] = []
    for key in sorted(old.keys() | new.keys()):
        a, b = old.get(key), new.get(key)
        subject = key[2]
        if a is None:
            changes.append(EpochChange(subject, "appeared", None, b))
        elif b is None:
            changes.append(EpochChange(subject, "disappeared", a, None))
        elif a.get("payload") != b.get("payload"):
            changes.append(EpochChange(subject, "changed", a, b))
        else:
            changes.append(EpochChange(subject, "reappeared", a, b))
    return changes
