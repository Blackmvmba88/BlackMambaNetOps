from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .sensors import SensorObservation


@dataclass(frozen=True)
class Signal:
    subject: str
    rule: str
    weight: int
    reason: str


def signals(observations: Iterable[SensorObservation]) -> list[Signal]:
    """Produce explainable defensive signals; scores are triage, never attribution."""
    out: list[Signal] = []
    for obs in observations:
        p = obs.payload
        if obs.source == "docker" and obs.kind == "container":
            if p.get("privileged"):
                out.append(Signal(obs.subject, "docker.privileged", 3, "container runs privileged"))
            if p.get("docker_socket_mounted"):
                out.append(Signal(obs.subject, "docker.socket", 4, "container can reach Docker control socket"))
            bindings = p.get("port_bindings") or {}
            if any(any(x.get("HostIp") in ("0.0.0.0", "::") for x in (v or [])) for v in bindings.values()):
                out.append(Signal(obs.subject, "docker.public-bind", 2, "container publishes a port on all host interfaces"))
        if obs.source == "macos.socket" and obs.kind == "process_socket":
            if p.get("state") == "LISTEN" and p.get("local", "").startswith("*:"):
                out.append(Signal(obs.subject, "socket.public-listener", 2, "process listens on all interfaces"))
    return out


def score(subject: str, found: Iterable[Signal]) -> int:
    return sum(s.weight for s in found if s.subject == subject)
