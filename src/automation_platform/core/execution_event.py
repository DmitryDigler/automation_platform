from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation_platform.core.execution import Execution
from automation_platform.core.identity import EntityId


@dataclass(frozen=True, slots=True)
class ExecutionAdmitted:
    event_id: EntityId
    execution_id: EntityId
    correlation_id: EntityId
    causation_id: EntityId | None
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        occurred_at: datetime,
        causation_id: EntityId | None = None,
    ) -> ExecutionAdmitted:
        return cls(
            event_id=EntityId.new(),
            execution_id=execution.execution_id,
            correlation_id=execution.correlation_id,
            causation_id=causation_id,
            occurred_at=occurred_at,
        )


@dataclass(frozen=True, slots=True)
class ExecutionStarted:
    event_id: EntityId
    execution_id: EntityId
    correlation_id: EntityId
    causation_id: EntityId | None
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        occurred_at: datetime,
        causation_id: EntityId | None = None,
    ) -> ExecutionStarted:
        return cls(
            event_id=EntityId.new(),
            execution_id=execution.execution_id,
            correlation_id=execution.correlation_id,
            causation_id=causation_id,
            occurred_at=occurred_at,
        )


@dataclass(frozen=True, slots=True)
class ExecutionSucceeded:
    event_id: EntityId
    execution_id: EntityId
    correlation_id: EntityId
    causation_id: EntityId | None
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        occurred_at: datetime,
        causation_id: EntityId | None = None,
    ) -> ExecutionSucceeded:
        return cls(
            event_id=EntityId.new(),
            execution_id=execution.execution_id,
            correlation_id=execution.correlation_id,
            causation_id=causation_id,
            occurred_at=occurred_at,
        )


@dataclass(frozen=True, slots=True)
class ExecutionFailed:
    event_id: EntityId
    execution_id: EntityId
    correlation_id: EntityId
    causation_id: EntityId | None
    error: str
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        error: str,
        occurred_at: datetime,
        causation_id: EntityId | None = None,
    ) -> ExecutionFailed:
        if not error:
            raise ValueError("execution error must not be empty")

        return cls(
            event_id=EntityId.new(),
            execution_id=execution.execution_id,
            correlation_id=execution.correlation_id,
            causation_id=causation_id,
            error=error,
            occurred_at=occurred_at,
        )
