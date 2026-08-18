from __future__ import annotations

from typing import Protocol

from automation_platform.core.execution import Execution


class Executor(Protocol):
    """
    Port describing a mechanism capable of performing one Execution.

    The Execution Engine owns lifecycle orchestration.
    The Executor performs the actual work and reports its outcome.

    Concrete execution mechanisms belong to adapters.
    """

    @property
    def name(self) -> str:
        """Stable logical executor identifier."""
        ...

    def execute(self, execution: Execution) -> object:
        """
        Perform one execution attempt.

        The supplied Execution is immutable and must not be mutated.

        The Executor performs work and reports an observed outcome.
        Execution lifecycle transitions remain the responsibility
        of the Execution Engine.

        The concrete outcome type will be formalized by the Result model.
        """
        ...
