from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .sensors import ReadOnlySensor, SensorObservation


class MacOSPersistenceSensor(ReadOnlySensor):
    """Inventory common macOS persistence locations without executing their contents."""

    SYSTEM_PATHS = (Path("/Library/LaunchAgents"), Path("/Library/LaunchDaemons"))

    def __init__(self, home: Path | None = None) -> None:
        self.home = home or Path.home()

    def _locations(self) -> Iterable[Path]:
        yield self.home / "Library/LaunchAgents"
        yield from self.SYSTEM_PATHS

    def observe(self) -> list[SensorObservation]:
        out: list[SensorObservation] = []
        for directory in self._locations():
            try:
                entries = sorted(p for p in directory.iterdir() if p.is_file())
            except (FileNotFoundError, PermissionError):
                continue
            for path in entries:
                stat = path.stat()
                out.append(SensorObservation(
                    source="macos.persistence", kind="launch_item", subject=f"file:{path}",
                    payload={"path": str(path), "size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "mode": oct(stat.st_mode & 0o777)},
                ))
        return out
