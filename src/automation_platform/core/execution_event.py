from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation_platform.core.execution import Execution
from automation_platform.core.identity import EntityId


@dataclass(frozen=True, slots=True)
class ExecutionAdmitted:
    execution_id: EntityId
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        occurred_at: datetime,
    ) -> ExecutionAdmitted:
        return cls(
            execution_id=execution.execution_id,
            occurred_at=occurred_at,
        )


@dataclass(frozen=True, slots=True)
class ExecutionStarted:
    execution_id: EntityId
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        occurred_at: datetime,
    ) -> ExecutionStarted:
        return cls(
            execution_id=execution.execution_id,
            occurred_at=occurred_at,
        )


@dataclass(frozen=True, slots=True)
class ExecutionSucceeded:
    execution_id: EntityId
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        occurred_at: datetime,
    ) -> ExecutionSucceeded:
        return cls(
            execution_id=execution.execution_id,
            occurred_at=occurred_at,
        )


@dataclass(frozen=True, slots=True)
class ExecutionFailed:
    execution_id: EntityId
    error: str
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        *,
        execution: Execution,
        error: str,
        occurred_at: datetime,
    ) -> ExecutionFailed:
        if not error:
            raise ValueError("execution error must not be empty")

        return cls(
            execution_id=execution.execution_id,
            error=error,
            occurred_at=occurred_at,
        )
