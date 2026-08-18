from __future__ import annotations

from dataclasses import dataclass

from automation_platform.core.execution import Execution
from automation_platform.core.result import ExecutionResult


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    """
    Immutable outcome of one execution attempt.

    Contains:
    - the final execution lifecycle state;
    - the observation produced by the Executor;
    - lifecycle events produced during the execution.
    """

    execution: Execution
    result: ExecutionResult
    events: tuple[object, ...] = ()
