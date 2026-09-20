from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .model import DeviceRecord


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str
    evidence: str


@dataclass
class Topology:
    nodes: dict[str, DeviceRecord] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def ingest(self, records: Iterable[DeviceRecord]) -> None:
        for record in records:
            self.nodes[record.stable_id] = record

    def relate(self, source: str, target: str, relation: str, evidence: str) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("Topology edges require known nodes")
        self.edges.append(Edge(source, target, relation, evidence))
