from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class EntityId:
    """
    Globally unique identity of a platform entity.

    The value is immutable and can safely cross process boundaries.
    """

    value: UUID

    @classmethod
    def new(cls) -> EntityId:
        return cls(uuid4())

    @classmethod
    def from_string(cls, value: str) -> EntityId:
        return cls(UUID(value))

    def __str__(self) -> str:
        return str(self.value)
