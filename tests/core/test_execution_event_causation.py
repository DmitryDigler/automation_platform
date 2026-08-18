import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import Execution
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionStarted,
)
from automation_platform.core.identity import EntityId


class ExecutionEventCausationTests(unittest.TestCase):
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

    def test_event_has_own_identity(self):
        execution = self.create_execution()

        event = ExecutionAdmitted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        self.assertIsInstance(
            event.event_id,
            EntityId,
        )

    def test_event_preserves_execution_correlation_id(self):
        execution = self.create_execution()

        event = ExecutionAdmitted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        self.assertEqual(
            event.correlation_id,
            execution.correlation_id,
        )

    def test_first_event_has_no_causation(self):
        execution = self.create_execution()

        event = ExecutionAdmitted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        self.assertIsNone(
            event.causation_id,
        )

    def test_next_event_can_reference_previous_event(self):
        execution = self.create_execution()

        admitted = ExecutionAdmitted.create(
            execution=execution,
            occurred_at=self.NOW,
        )

        started = ExecutionStarted.create(
            execution=execution,
            occurred_at=self.NOW,
            causation_id=admitted.event_id,
        )

        self.assertEqual(
            started.causation_id,
            admitted.event_id,
        )


if __name__ == "__main__":
    unittest.main()
