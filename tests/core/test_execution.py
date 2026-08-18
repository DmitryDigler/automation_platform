import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import (
    Execution,
    ExecutionStatus,
)
from automation_platform.core.identity import EntityId


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)

        self.command_id = EntityId.new()
        self.plan_id = EntityId.new()
        self.correlation_id = EntityId.new()

    def create_execution(self):
        return Execution.create(
            command_id=self.command_id,
            plan_id=self.plan_id,
            correlation_id=self.correlation_id,
            executor="local",
            created_at=self.now,
        )

    def test_new_execution_starts_created(self):
        execution = self.create_execution()

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )
        self.assertEqual(execution.attempt, 1)

    def test_created_can_become_ready(self):
        execution = self.create_execution()

        ready = execution.transition(
            ExecutionStatus.READY,
            occurred_at=self.now,
        )

        self.assertEqual(ready.status, ExecutionStatus.READY)
        self.assertEqual(ready.execution_id, execution.execution_id)

    def test_ready_can_become_running(self):
        execution = self.create_execution()
        execution = execution.transition(
            ExecutionStatus.READY,
            occurred_at=self.now,
        )

        started_at = datetime(
            2026,
            8,
            18,
            10,
            0,
            tzinfo=timezone.utc,
        )

        running = execution.transition(
            ExecutionStatus.RUNNING,
            occurred_at=started_at,
        )

        self.assertEqual(running.status, ExecutionStatus.RUNNING)
        self.assertEqual(running.started_at, started_at)

    def test_running_can_succeed(self):
        execution = self.create_execution()

        execution = execution.transition(
            ExecutionStatus.READY,
            occurred_at=self.now,
        )

        execution = execution.transition(
            ExecutionStatus.RUNNING,
            occurred_at=self.now,
        )

        finished_at = datetime(
            2026,
            8,
            18,
            10,
            1,
            tzinfo=timezone.utc,
        )

        completed = execution.transition(
            ExecutionStatus.SUCCEEDED,
            occurred_at=finished_at,
        )

        self.assertEqual(
            completed.status,
            ExecutionStatus.SUCCEEDED,
        )
        self.assertEqual(completed.finished_at, finished_at)

    def test_invalid_transition_is_rejected(self):
        execution = self.create_execution()

        with self.assertRaises(ValueError):
            execution.transition(
                ExecutionStatus.SUCCEEDED,
                occurred_at=self.now,
            )

    def test_terminal_execution_cannot_restart(self):
        execution = self.create_execution()

        execution = execution.transition(
            ExecutionStatus.READY,
            occurred_at=self.now,
        )

        execution = execution.transition(
            ExecutionStatus.RUNNING,
            occurred_at=self.now,
        )

        execution = execution.transition(
            ExecutionStatus.FAILED,
            occurred_at=self.now,
        )

        with self.assertRaises(ValueError):
            execution.transition(
                ExecutionStatus.RUNNING,
                occurred_at=self.now,
            )

    def test_transition_does_not_mutate_original(self):
        execution = self.create_execution()

        ready = execution.transition(
            ExecutionStatus.READY,
            occurred_at=self.now,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )

        self.assertEqual(
            ready.status,
            ExecutionStatus.READY,
        )

    def test_retry_is_a_new_execution(self):
        first = self.create_execution()

        failed = first.transition(
            ExecutionStatus.READY,
            occurred_at=self.now,
        )
        failed = failed.transition(
            ExecutionStatus.RUNNING,
            occurred_at=self.now,
        )
        failed = failed.transition(
            ExecutionStatus.FAILED,
            occurred_at=self.now,
        )

        retry = Execution.create(
            command_id=failed.command_id,
            plan_id=failed.plan_id,
            correlation_id=failed.correlation_id,
            executor=failed.executor,
            attempt=2,
            created_at=self.now,
        )

        self.assertNotEqual(
            retry.execution_id,
            failed.execution_id,
        )
        self.assertEqual(retry.command_id, failed.command_id)
        self.assertEqual(retry.attempt, 2)
        self.assertEqual(
            failed.status,
            ExecutionStatus.FAILED,
        )


if __name__ == "__main__":
    unittest.main()
