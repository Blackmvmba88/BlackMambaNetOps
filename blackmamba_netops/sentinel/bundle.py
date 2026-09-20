from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


def write_bundle(bundle: dict[str, Any], destination: Path) -> tuple[Path, str]:
    """Write a canonical evidence bundle plus a sidecar digest for off-host storage."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(bundle, sort_keys=True, indent=2, default=str).encode("utf-8")
    destination.write_bytes(raw)
    digest = sha256(raw).hexdigest()
    sidecar = destination.with_suffix(destination.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {destination.name}\n", encoding="utf-8")
    return sidecar, digest
