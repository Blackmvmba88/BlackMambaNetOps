from __future__ import annotations

from dataclasses import dataclass

from .intent import Intent, Risk
from .management_link import ManagementLink


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


class PolicyEngine:
    """Context-aware policy; mechanism remains inside adapters."""

    def evaluate(self, intent: Intent, link: ManagementLink | None = None) -> Decision:
        if intent.risk is Risk.PROTECTED:
            return Decision(False, "protected provisioning boundary")
        if intent.action == "wifi.radio.write":
            if link is None or not link.safe_for_radio_mutation:
                return Decision(False, "radio mutation requires a verified wired management link")
        return Decision(True, "policy satisfied")
