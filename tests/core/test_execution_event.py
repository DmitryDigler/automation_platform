import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import Execution, ExecutionStatus
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionStarted,
    ExecutionSucceeded,
    ExecutionFailed,
)
from automation_platform.core.identity import EntityId


class ExecutionEventTests(unittest.TestCase):

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

    def test_admitted_event_contains_execution_identity(self):
        execution = self.create_execution()

        event = ExecutionAdmitted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        self.assertEqual(
            event.execution_id,
            execution.execution_id,
        )

        self.assertEqual(
            event.occurred_at,
            self.NOW,
        )

    def test_started_event_contains_execution_identity(self):
        execution = self.create_execution()

        event = ExecutionStarted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        self.assertEqual(
            event.execution_id,
            execution.execution_id,
        )

    def test_succeeded_event_contains_execution_identity(self):
        execution = self.create_execution()

        event = ExecutionSucceeded.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        self.assertEqual(
            event.execution_id,
            execution.execution_id,
        )

    def test_failed_event_contains_error(self):
        execution = self.create_execution()

        event = ExecutionFailed.create(
            execution=execution,
            error="boom",
            occurred_at=self.NOW,
        )

        self.assertEqual(
            event.execution_id,
            execution.execution_id,
        )

        self.assertEqual(
            event.error,
            "boom",
        )

    def test_events_are_immutable(self):
        execution = self.create_execution()

        event = ExecutionStarted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        with self.assertRaises(AttributeError):
            event.execution_id = EntityId.new()

    def test_failed_event_preserves_identity_and_causation(self):
        execution = self.create_execution()

        causation_id = EntityId.new()

        event = ExecutionFailed.create(
            execution=execution,
            error="boom",
            occurred_at=self.NOW,
            causation_id=causation_id,
        )

        self.assertIsInstance(
            event.event_id,
            EntityId,
        )

        self.assertEqual(
            event.execution_id,
            execution.execution_id,
        )

        self.assertEqual(
            event.correlation_id,
            execution.correlation_id,
        )

        self.assertEqual(
            event.causation_id,
            causation_id,
        )

        self.assertEqual(
            event.occurred_at,
            self.NOW,
        )

if __name__ == "__main__":
    unittest.main()
