from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation_platform.core.identity import EntityId


class ExecutionStatus:
    """
    Stable execution lifecycle states.

    Execution history is immutable.
    A retry creates a new Execution rather than rewinding
    an existing one.
    """

    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INTERRUPTED = "interrupted"


_TERMINAL_STATES = frozenset(
    {
        ExecutionStatus.SUCCEEDED,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
        ExecutionStatus.INTERRUPTED,
    }
)

_ALLOWED_TRANSITIONS = {
    ExecutionStatus.CREATED: frozenset(
        {
            ExecutionStatus.READY,
            ExecutionStatus.CANCELLED,
        }
    ),
    ExecutionStatus.READY: frozenset(
        {
            ExecutionStatus.RUNNING,
            ExecutionStatus.CANCELLED,
        }
    ),
    ExecutionStatus.RUNNING: frozenset(
        {
            ExecutionStatus.SUCCEEDED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
            ExecutionStatus.INTERRUPTED,
        }
    ),
    ExecutionStatus.SUCCEEDED: frozenset(),
    ExecutionStatus.FAILED: frozenset(),
    ExecutionStatus.CANCELLED: frozenset(),
    ExecutionStatus.INTERRUPTED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class Execution:
    """
    Immutable description of one concrete execution attempt.

    An Execution is not a Command and not a Plan.

    It represents one attempt to fulfill a previously established Plan.
    """

    execution_id: EntityId
    command_id: EntityId
    plan_id: EntityId
    correlation_id: EntityId

    attempt: int
    status: str

    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    executor: str

    @classmethod
    def create(
        cls,
        *,
        command_id: EntityId,
        plan_id: EntityId,
        correlation_id: EntityId,
        executor: str,
        attempt: int = 1,
        created_at: datetime,
    ) -> Execution:
        if attempt < 1:
            raise ValueError("attempt must be >= 1")

        if not executor:
            raise ValueError("executor must not be empty")

        return cls(
            execution_id=EntityId.new(),
            command_id=command_id,
            plan_id=plan_id,
            correlation_id=correlation_id,
            attempt=attempt,
            status=ExecutionStatus.CREATED,
            created_at=created_at,
            started_at=None,
            finished_at=None,
            executor=executor,
        )

    def can_transition_to(self, target: str) -> bool:
        return target in _ALLOWED_TRANSITIONS[self.status]

    def transition(
        self,
        target: str,
        *,
        occurred_at: datetime,
    ) -> Execution:
        if not self.can_transition_to(target):
            raise ValueError(
                f"Invalid execution transition: "
                f"{self.status!r} -> {target!r}"
            )

        started_at = self.started_at
        finished_at = self.finished_at

        if target == ExecutionStatus.RUNNING:
            started_at = occurred_at

        if target in _TERMINAL_STATES:
            finished_at = occurred_at

        return Execution(
            execution_id=self.execution_id,
            command_id=self.command_id,
            plan_id=self.plan_id,
            correlation_id=self.correlation_id,
            attempt=self.attempt,
            status=target,
            created_at=self.created_at,
            started_at=started_at,
            finished_at=finished_at,
            executor=self.executor,
        )
