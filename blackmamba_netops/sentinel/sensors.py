from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SensorObservation:
    source: str
    kind: str
    subject: str
    payload: dict[str, Any]


class ReadOnlySensor(ABC):
    """Sensor contract deliberately exposes no mutation primitive."""

    @abstractmethod
    def observe(self) -> list[SensorObservation]:
        raise NotImplementedError


class HostSensor(ReadOnlySensor):
    """Contract for platform collectors: processes, sockets, routes, neighbors, persistence."""

    def observe(self) -> list[SensorObservation]:
        raise NotImplementedError("platform host collector not wired yet")


class ContainerSensor(ReadOnlySensor):
    """Contract for Docker/container metadata: ports, mounts, networks and privileges."""

    def observe(self) -> list[SensorObservation]:
        raise NotImplementedError("container collector not wired yet")
