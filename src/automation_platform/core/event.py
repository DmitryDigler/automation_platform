from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from automation_platform.core.identity import EntityId


@dataclass(frozen=True, slots=True)
class Event:
    """
    Immutable record describing something that happened.

    Events are the foundation for observation, tracing, auditing,
    replay, recovery, and future distributed execution.
    """

    event_id: EntityId
    event_type: str
    event_version: int
    occurred_at: datetime
    source: str
    correlation_id: EntityId
    causation_id: EntityId | None
    payload: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        event_type: str,
        source: str,
        correlation_id: EntityId,
        payload: Mapping[str, Any],
        causation_id: EntityId | None = None,
        event_version: int = 1,
    ) -> Event:
        if not event_type:
            raise ValueError("event_type must not be empty")

        if not source:
            raise ValueError("source must not be empty")

        if event_version < 1:
            raise ValueError("event_version must be >= 1")

        return cls(
            event_id=EntityId.new(),
            event_type=event_type,
            event_version=event_version,
            occurred_at=datetime.now(timezone.utc),
            source=source,
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload=dict(payload),
        )
