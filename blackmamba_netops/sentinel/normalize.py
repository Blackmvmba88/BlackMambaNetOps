from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .sensors import SensorObservation


@dataclass(frozen=True)
class SocketEdge:
    process: str
    pid: int
    protocol: str
    local: str
    remote: str | None
    state: str | None


_LSOF = re.compile(r"^(?P<cmd>\S+)\s+(?P<pid>\d+)\s+\S+.*?\s(?P<proto>TCP|UDP)\s+(?P<endpoint>\S+)(?:\s+\((?P<state>[^)]+)\))?$")


def parse_lsof_sockets(text: str) -> list[SocketEdge]:
    edges: list[SocketEdge] = []
    for raw in text.splitlines():
        match = _LSOF.match(raw.strip())
        if not match:
            continue
        endpoint = match.group("endpoint")
        if "->" in endpoint:
            local, remote = endpoint.split("->", 1)
        else:
            local, remote = endpoint, None
        edges.append(SocketEdge(match.group("cmd"), int(match.group("pid")), match.group("proto"), local, remote, match.group("state")))
    return edges


def normalize_host(observations: Iterable[SensorObservation]) -> list[SensorObservation]:
    normalized: list[SensorObservation] = []
    for obs in observations:
        if obs.source == "macos" and obs.kind == "sockets":
            for edge in parse_lsof_sockets(str(obs.payload.get("stdout", ""))):
                normalized.append(SensorObservation(
                    source="macos.socket", kind="process_socket", subject=f"pid:{edge.pid}",
                    payload={"process": edge.process, "pid": edge.pid, "protocol": edge.protocol, "local": edge.local, "remote": edge.remote, "state": edge.state},
                ))
    return normalized
