from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation_platform.core.capability import Capability
from automation_platform.core.execution import (
    Execution,
    ExecutionStatus,
)
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionFailed,
    ExecutionStarted,
    ExecutionSucceeded,
)
from automation_platform.core.node import Node
from automation_platform.core.outcome import ExecutionOutcome
from automation_platform.core.result import ExecutionResult
from automation_platform.ports.executor import Executor
from automation_platform.ports.node_selector import NodeSelector


@dataclass(frozen=True, slots=True)
class ExecutionEngine:
    """
    Orchestrates execution without owning execution semantics.

    The engine coordinates:

        Execution
            -> NodeSelector
            -> Node
            -> Executor
            -> ExecutionResult
            -> ExecutionOutcome
    """

    selector: NodeSelector
    executor: Executor

    def admit(
        self,
        execution: Execution,
        *,
        occurred_at: datetime,
    ) -> Execution:
        return execution.transition(
            ExecutionStatus.READY,
            occurred_at=occurred_at,
        )

    def select(
        self,
        execution: Execution,
        *,
        required_capabilities: frozenset[Capability],
    ) -> Node:
        if execution.status != ExecutionStatus.READY:
            raise ValueError(
                "execution must be ready before node selection"
            )

        return self.selector.select(required_capabilities)

    def start(
        self,
        execution: Execution,
        *,
        occurred_at: datetime,
    ) -> Execution:
        return execution.transition(
            ExecutionStatus.RUNNING,
            occurred_at=occurred_at,
        )

    def observe(
        self,
        execution: Execution,
        *,
        success: bool,
        occurred_at: datetime,
    ) -> Execution:
        if execution.status != ExecutionStatus.RUNNING:
            raise ValueError(
                "execution must be running before observation"
            )

        target = (
            ExecutionStatus.SUCCEEDED
            if success
            else ExecutionStatus.FAILED
        )

        return execution.transition(
            target,
            occurred_at=occurred_at,
        )

    def cancel(
        self,
        execution: Execution,
        *,
        occurred_at: datetime,
    ) -> Execution:
        return execution.transition(
            ExecutionStatus.CANCELLED,
            occurred_at=occurred_at,
        )

    def retry(
        self,
        execution: Execution,
        *,
        created_at: datetime,
    ) -> Execution:
        return Execution.create(
            command_id=execution.command_id,
            plan_id=execution.plan_id,
            correlation_id=execution.correlation_id,
            executor=execution.executor,
            attempt=execution.attempt + 1,
            created_at=created_at,
        )

    def run(
        self,
        execution: Execution,
        *,
        required_capabilities: frozenset[Capability],
        occurred_at: datetime,
    ) -> ExecutionOutcome:
        """
        Run one complete execution lifecycle and preserve
        the Executor observation and lifecycle events.

        CREATED
            -> ExecutionAdmitted
            -> READY
            -> Node selected
            -> ExecutionStarted
            -> RUNNING
            -> Executor observation
            -> ExecutionSucceeded / ExecutionFailed
            -> SUCCEEDED / FAILED
        """

        events: list[object] = []

        current = self.admit(
            execution,
            occurred_at=occurred_at,
        )

        events.append(
            ExecutionAdmitted.create(
                execution=current,
                occurred_at=occurred_at,
            )
        )

        self.select(
            current,
            required_capabilities=required_capabilities,
        )

        current = self.start(
            current,
            occurred_at=occurred_at,
        )

        events.append(
            ExecutionStarted.create(
                execution=current,
                occurred_at=occurred_at,
            )
        )

        observation = self.executor.execute(current)

        if not isinstance(observation, ExecutionResult):
            raise TypeError(
                "executor must return ExecutionResult"
            )

        current = self.observe(
            current,
            success=observation.success,
            occurred_at=occurred_at,
        )

        if observation.success:
            events.append(
                ExecutionSucceeded.create(
                    execution=current,
                    occurred_at=occurred_at,
                )
            )
        else:
            events.append(
                ExecutionFailed.create(
                    execution=current,
                    error=observation.error or "execution failed",
                    occurred_at=occurred_at,
                )
            )

        return ExecutionOutcome(
            execution=current,
            result=observation,
            events=tuple(events),
        )
