import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import Execution
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionStarted,
    ExecutionSucceeded,
)
from automation_platform.core.identity import EntityId


class ExecutionEventCausationChainTests(unittest.TestCase):
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

    def test_lifecycle_events_form_causation_chain(self):
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

        succeeded = ExecutionSucceeded.create(
            execution=execution,
            occurred_at=self.NOW,
            causation_id=started.event_id,
        )

        self.assertIsNone(admitted.causation_id)

        self.assertEqual(
            started.causation_id,
            admitted.event_id,
        )

        self.assertEqual(
            succeeded.causation_id,
            started.event_id,
        )

        self.assertEqual(
            admitted.correlation_id,
            started.correlation_id,
        )

        self.assertEqual(
            started.correlation_id,
            succeeded.correlation_id,
        )


if __name__ == "__main__":
    unittest.main()
