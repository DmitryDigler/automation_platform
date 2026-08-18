import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import Execution
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionStarted,
)
from automation_platform.core.identity import EntityId
from automation_platform.core.outcome import ExecutionOutcome
from automation_platform.core.result import ExecutionResult


class ExecutionOutcomeEventTests(unittest.TestCase):

    NOW = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    def create_execution(self):
        return Execution.create(
            command_id=EntityId.new(),
            plan_id=EntityId.new(),
            correlation_id=EntityId.new(),
            executor="fake",
            created_at=self.NOW,
        )

    def test_events_are_immutable(self):
        execution = self.create_execution()

        events = (
            ExecutionAdmitted.create(
                execution=execution,
                occurred_at=self.NOW,
            ),
            ExecutionStarted.create(
                execution=execution,
                occurred_at=self.NOW,
            ),
        )

        outcome = ExecutionOutcome(
            execution=execution,
            result=ExecutionResult.success("hello"),
            events=events,
        )

        with self.assertRaises(AttributeError):
            outcome.events = ()

    def test_events_are_stored_as_tuple(self):
        execution = self.create_execution()

        events = [
            ExecutionAdmitted.create(
                execution=execution,
                occurred_at=self.NOW,
            ),
            ExecutionStarted.create(
                execution=execution,
                occurred_at=self.NOW,
            ),
        ]

        outcome = ExecutionOutcome(
            execution=execution,
            result=ExecutionResult.success("hello"),
            events=events,
        )

        self.assertIsInstance(
            outcome.events,
            tuple,
        )

        self.assertEqual(
            len(outcome.events),
            2,
        )


if __name__ == "__main__":
    unittest.main()
