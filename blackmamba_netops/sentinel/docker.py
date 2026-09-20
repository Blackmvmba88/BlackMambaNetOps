from __future__ import annotations

import json
import subprocess
from typing import Callable

from .sensors import ReadOnlySensor, SensorObservation

Runner = Callable[[list[str]], subprocess.CompletedProcess[str]]


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, capture_output=True, text=True, timeout=10, check=False)


class DockerSensor(ReadOnlySensor):
    """Read-only Docker witness using inspect/list APIs exposed by the CLI."""

    def __init__(self, runner: Runner = _run) -> None:
        self.runner = runner

    def observe(self) -> list[SensorObservation]:
        ps = self.runner(["docker", "ps", "-aq"])
        ids = [line.strip() for line in ps.stdout.splitlines() if line.strip()]
        observations = [SensorObservation("docker", "inventory", "docker:daemon", {"container_ids": ids, "returncode": ps.returncode})]
        if not ids:
            return observations

        inspected = self.runner(["docker", "inspect", *ids])
        try:
            containers = json.loads(inspected.stdout) if inspected.returncode == 0 else []
        except json.JSONDecodeError:
            containers = []
        for c in containers:
            cid = c.get("Id", "unknown")
            host = c.get("HostConfig") or {}
            mounts = c.get("Mounts") or []
            observations.append(SensorObservation(
                "docker", "container", f"container:{cid[:12]}",
                {
                    "name": c.get("Name", "").lstrip("/"),
                    "image": (c.get("Config") or {}).get("Image"),
                    "privileged": bool(host.get("Privileged")),
                    "network_mode": host.get("NetworkMode"),
                    "port_bindings": host.get("PortBindings") or {},
                    "mounts": [{"type": m.get("Type"), "source": m.get("Source"), "destination": m.get("Destination"), "rw": m.get("RW")} for m in mounts],
                    "docker_socket_mounted": any(m.get("Destination") == "/var/run/docker.sock" for m in mounts),
                },
            ))
        return observations
