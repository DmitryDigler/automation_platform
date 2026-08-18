from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Capability:
    """
    Immutable description of an ability provided by an execution
    environment.
    """

    name: str
    version: str = "1"

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("capability name must not be empty")

        if not self.version:
            raise ValueError("capability version must not be empty")
