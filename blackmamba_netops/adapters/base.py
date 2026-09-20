from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from blackmamba_netops.core.model import Capability


class DeviceAdapter(ABC):
    @abstractmethod
    def observe(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> list[Capability]:
        raise NotImplementedError
