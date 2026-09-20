from __future__ import annotations

import json
import subprocess
from typing import Callable

from .sensors import ReadOnlySensor, SensorObservation

Runner = Callable[[list[str]], subprocess.CompletedProcess[str]]


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, capture_output=True, text=True, timeout=8, check=False)


class MacOSHostSensor(ReadOnlySensor):
    """Read-only macOS witness. Uses bounded argv calls; never invokes a shell."""

    def __init__(self, runner: Runner = _run) -> None:
        self.runner = runner

    def _capture(self, kind: str, argv: list[str]) -> SensorObservation:
        result = self.runner(argv)
        return SensorObservation(
            source="macos",
            kind=kind,
            subject="host:local",
            payload={"argv": argv, "returncode": result.returncode, "stdout": result.stdout[:200_000], "stderr": result.stderr[:20_000]},
        )

    def observe(self) -> list[SensorObservation]:
        # No sudo, no shell, no mutation. These snapshots are evidence inputs.
        commands = [
            ("interfaces", ["ifconfig", "-a"]),
            ("routes", ["netstat", "-rn"]),
            ("neighbors", ["arp", "-an"]),
            ("sockets", ["lsof", "-nP", "-i"]),
            ("processes", ["ps", "-axo", "pid,ppid,user,lstart,command"]),
            ("dns", ["scutil", "--dns"]),
            ("proxy", ["scutil", "--proxy"]),
        ]
        return [self._capture(kind, argv) for kind, argv in commands]
