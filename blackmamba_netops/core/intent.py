from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Risk(str, Enum):
    READ = "read"
    MUTATE = "mutate"
    PROTECTED = "protected"


@dataclass(frozen=True)
class Intent:
    action: str
    risk: Risk
    target: str
    desired: object | None = None


class IntentDenied(RuntimeError):
    pass


class IntentGate:
    """One choke point for every state-changing operation."""

    def authorize(self, intent: Intent) -> None:
        if intent.risk is Risk.PROTECTED:
            raise IntentDenied(
                f"{intent.action} targets protected provisioning state: {intent.target}"
            )
