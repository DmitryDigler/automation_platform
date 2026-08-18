from __future__ import annotations

from dataclasses import dataclass

from automation_platform.core.execution import Execution
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionFailed,
    ExecutionStarted,
    ExecutionSucceeded,
)
from automation_platform.core.result import ExecutionResult


ExecutionEvent = (
    ExecutionAdmitted
    | ExecutionStarted
    | ExecutionSucceeded
    | ExecutionFailed
)


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    """
    Immutable outcome of one execution attempt.

    Contains:
    - the final execution lifecycle state;
    - the observation produced by the Executor;
    - lifecycle events produced by the Engine.
    """

    execution: Execution
    result: ExecutionResult
    events: tuple[ExecutionEvent, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "events",
            tuple(self.events),
        )
