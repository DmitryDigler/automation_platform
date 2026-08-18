from __future__ import annotations

from typing import Protocol

from automation_platform.core.execution import Execution


class ExecutionEnginePort(Protocol):
    """
    Structural contract for the Execution Engine.

    The Engine owns Execution lifecycle semantics.
    Executors perform domain work and report observations.
    """

    def admit(self, execution: Execution) -> Execution:
        """
        Admit an execution into the Engine lifecycle.
        """
        ...

    def select(self, execution: Execution) -> Execution:
        """
        Select execution resources / executor for the attempt.
        """
        ...

    def start(self, execution: Execution) -> Execution:
        """
        Start an admitted execution.
        """
        ...

    def observe(
        self,
        execution: Execution,
        observation,
    ) -> Execution:
        """
        Apply an external execution observation.

        The observation is evidence from the Executor or
        execution environment. It does not directly mutate
        Execution state.
        """
        ...

    def cancel(self, execution: Execution) -> Execution:
        """
        Request cancellation of an execution.
        """
        ...

    def retry(self, execution: Execution) -> Execution:
        """
        Create a new execution attempt.

        Retry never rewinds or mutates the original execution.
        """
        ...
