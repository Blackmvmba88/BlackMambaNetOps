from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


@dataclass(frozen=True)
class ArtifactIdentity:
    path: str
    sha256: str
    size: int


def identify(path: Path, *, max_bytes: int = 128 * 1024 * 1024) -> ArtifactIdentity:
    """Hash a selected regular file without executing it."""
    stat = path.stat()
    if not path.is_file():
        raise ValueError("artifact must be a regular file")
    if stat.st_size > max_bytes:
        raise ValueError("artifact exceeds bounded hashing limit")
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return ArtifactIdentity(str(path), digest.hexdigest(), stat.st_size)
