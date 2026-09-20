from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .base import DeviceAdapter


@dataclass(frozen=True)
class Probe:
    vendor: str
    model: str | None = None
    firmware: str | None = None


Factory = Callable[[], DeviceAdapter]


class AdapterRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, Factory] = {}

    def register(self, vendor: str, factory: Factory) -> None:
        self._factories[vendor.casefold()] = factory

    def resolve(self, probe: Probe) -> DeviceAdapter:
        try:
            return self._factories[probe.vendor.casefold()]()
        except KeyError as exc:
            raise LookupError(f"No adapter for vendor {probe.vendor!r}") from exc
