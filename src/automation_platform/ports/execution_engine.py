from __future__ import annotations

from datetime import datetime
from typing import Protocol

from automation_platform.core.capability import Capability
from automation_platform.core.execution import Execution
from automation_platform.core.outcome import ExecutionOutcome
from automation_platform.core.node import Node


class ExecutionEnginePort(Protocol):
    """
    Structural contract for the Execution Engine.

    The Engine owns Execution lifecycle semantics.
    Executors perform domain work and report observations.
    """

    def admit(
        self,
        execution: Execution,
        *,
        occurred_at: datetime,
    ) -> Execution:
        """
        Admit an execution into the Engine lifecycle.
        """
        ...

    def select(
        self,
        execution: Execution,
        *,
        required_capabilities: frozenset[Capability],
    ) -> Node:
        """
        Select an execution resource capable of satisfying
        the required capabilities.
        """
        ...

    def start(
        self,
        execution: Execution,
        *,
        occurred_at: datetime,
    ) -> Execution:
        """
        Start an admitted execution.
        """
        ...

    def observe(
        self,
        execution: Execution,
        *,
        success: bool,
        occurred_at: datetime,
    ) -> Execution:
        """
        Apply an external execution observation.

        The observation is evidence from the Executor or
        execution environment. It does not directly mutate
        Execution state.
        """
        ...

    def cancel(
        self,
        execution: Execution,
        *,
        occurred_at: datetime,
    ) -> Execution:
        """
        Cancel an execution.
        """
        ...

    def retry(
        self,
        execution: Execution,
        *,
        created_at: datetime,
    ) -> Execution:
        """
        Create a new execution attempt.

        Retry never rewinds or mutates the original execution.
        """
        ...

    def run(
        self,
        execution: Execution,
        *,
        required_capabilities: frozenset[Capability],
        occurred_at: datetime,
    ) -> ExecutionOutcome:
        """
        Run one complete execution lifecycle.
        """
        ...
