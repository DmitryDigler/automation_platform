from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation_platform.core.execution import (
    Execution,
    ExecutionStatus,
)
from automation_platform.core.node import Node
from automation_platform.core.capability import Capability
from automation_platform.ports.executor import Executor
from automation_platform.ports.node_selector import NodeSelector


@dataclass(frozen=True, slots=True)
class ExecutionEngine:
    """
    Orchestrates execution without owning execution semantics.

    The engine coordinates:
        Execution -> NodeSelector -> Node -> Executor

    Execution itself remains immutable.
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
