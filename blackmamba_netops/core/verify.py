from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Verification(Generic[T]):
    expected: T
    observed: T
    verified: bool


def act_and_verify(
    action: Callable[[], object],
    readback: Callable[[], T],
    expected: T,
) -> Verification[T]:
    """Transport success is not state success."""
    action()
    observed = readback()
    return Verification(expected=expected, observed=observed, verified=observed == expected)
