from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ManagementLink:
    gateway: str
    interface: str
    local_address: str
    medium: str
    verified: bool

    @property
    def safe_for_radio_mutation(self) -> bool:
        return self.verified and self.medium.lower() in {"ethernet", "wired"}


class ManagementLinkResolver:
    """Platform adapters implement route/interface discovery.

    The control plane consumes this abstraction and never assumes en0.
    """

    def resolve(self, gateway: str) -> ManagementLink:
        raise NotImplementedError
