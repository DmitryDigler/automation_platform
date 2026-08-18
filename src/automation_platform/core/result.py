from __future__ import annotations

from dataclasses import dataclass


class _SuccessFactory:
    def __get__(self, instance, owner):
        if instance is None:
            return lambda value=None: owner(
                _success=True,
                value=value,
                error=None,
            )

        return instance._success


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """
    Immutable observation produced by an Executor.

    A result represents what happened during one execution attempt.
    It does not change Execution lifecycle directly.
    """

    _success: bool
    value: object | None = None
    error: str | None = None

    success = _SuccessFactory()

    @classmethod
    def failure(cls, error: str) -> ExecutionResult:
        if not error:
            raise ValueError("execution error must not be empty")

        return cls(
            _success=False,
            value=None,
            error=error,
        )
