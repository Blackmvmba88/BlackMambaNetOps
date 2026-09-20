from __future__ import annotations

from dataclasses import dataclass

from blackmamba_netops.adapters.base import DeviceAdapter
from blackmamba_netops.core.model import Capability


@dataclass
class HuaweiFirmwareProfile:
    wifi_path: str = "/html/bbsp/wlan/wlan.asp"
    login_path: str = "/login.cgi"
    set_path: str = "/set.cgi"
    token_path: str = "/asp/GetRandCount.asp"

    def referer_for(self, path: str) -> str:
        # Field-observed quirk: this firmware rejects set.cgi with a self-referer.
        return self.wifi_path if path.startswith(self.set_path) else "/"


class HuaweiAdapter(DeviceAdapter):
    """Contract shell for the field-tested Huawei implementation.

    Network I/O stays out of this initial canonical scaffold until the live
    prototype is imported verbatim and covered by fixtures.
    """

    def __init__(self, profile: HuaweiFirmwareProfile | None = None):
        self.profile = profile or HuaweiFirmwareProfile()

    def capabilities(self) -> list[Capability]:
        return [
            Capability("inventory.read"),
            Capability("wifi.radio.read"),
            Capability("wifi.radio.write", writable=True),
            Capability("provisioning.gpon", writable=False, protected=True),
            Capability("provisioning.wan", writable=False, protected=True),
        ]

    def observe(self) -> dict[str, object]:
        raise NotImplementedError("Import live field adapter before enabling network I/O")
