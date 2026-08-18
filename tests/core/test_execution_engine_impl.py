import unittest
from datetime import datetime, timezone

from automation_platform.core.capability import Capability
from automation_platform.core.execution import (
    Execution,
    ExecutionStatus,
)
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node
from automation_platform.core.execution_engine import ExecutionEngine


class FakeSelector:
    def __init__(self, node):
        self.node = node
        self.requested = None

    def select(self, required):
        self.requested = required
        return self.node


class FakeExecutor:
    pass


class ExecutionEngineTests(unittest.TestCase):

    def create_execution(self):
        now = datetime.now(timezone.utc)

        return Execution.create(
            command_id=EntityId.new(),
            plan_id=EntityId.new(),
            correlation_id=EntityId.new(),
            executor="default",
            created_at=now,
        )

    def create_node(self):
        return Node.create(
            runtime_id=EntityId.new(),
            capabilities=frozenset(
                {
                    Capability("python"),
                }
            ),
        )

    def create_engine(self):
        return ExecutionEngine(
            selector=FakeSelector(self.create_node()),
            executor=FakeExecutor(),
        )

    def test_admit_moves_created_to_ready(self):
        engine = self.create_engine()
        execution = self.create_execution()
        now = datetime.now(timezone.utc)

        admitted = engine.admit(
            execution,
            occurred_at=now,
        )

        self.assertEqual(
            admitted.status,
            ExecutionStatus.READY,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )

    def test_select_uses_node_selector(self):
        node = self.create_node()
        selector = FakeSelector(node)

        engine = ExecutionEngine(
            selector=selector,
            executor=FakeExecutor(),
        )

        execution = self.create_execution()
        execution = engine.admit(
            execution,
            occurred_at=datetime.now(timezone.utc),
        )

        required = frozenset(
            {
                Capability("python"),
            }
        )

        selected = engine.select(
            execution,
            required_capabilities=required,
        )

        self.assertEqual(selected, node)
        self.assertEqual(selector.requested, required)

    def test_start_moves_ready_to_running(self):
        engine = self.create_engine()
        execution = self.create_execution()

        now = datetime.now(timezone.utc)

        execution = engine.admit(
            execution,
            occurred_at=now,
        )

        started = engine.start(
            execution,
            occurred_at=now,
        )

        self.assertEqual(
            started.status,
            ExecutionStatus.RUNNING,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.READY,
        )

    def test_observation_success_completes_execution(self):
        engine = self.create_engine()
        execution = self.create_execution()

        now = datetime.now(timezone.utc)

        execution = engine.admit(
            execution,
            occurred_at=now,
        )

        execution = engine.start(
            execution,
            occurred_at=now,
        )

        completed = engine.observe(
            execution,
            success=True,
            occurred_at=now,
        )

        self.assertEqual(
            completed.status,
            ExecutionStatus.SUCCEEDED,
        )

        self.assertEqual(
            completed.finished_at,
            now,
        )

    def test_observation_failure_fails_execution(self):
        engine = self.create_engine()
        execution = self.create_execution()

        now = datetime.now(timezone.utc)

        execution = engine.admit(
            execution,
            occurred_at=now,
        )

        execution = engine.start(
            execution,
            occurred_at=now,
        )

        failed = engine.observe(
            execution,
            success=False,
            occurred_at=now,
        )

        self.assertEqual(
            failed.status,
            ExecutionStatus.FAILED,
        )

    def test_retry_creates_new_attempt(self):
        engine = self.create_engine()
        execution = self.create_execution()

        now = datetime.now(timezone.utc)

        retry = engine.retry(
            execution,
            created_at=now,
        )

        self.assertNotEqual(
            execution.execution_id,
            retry.execution_id,
        )

        self.assertEqual(
            retry.attempt,
            execution.attempt + 1,
        )

        self.assertEqual(
            retry.status,
            ExecutionStatus.CREATED,
        )


if __name__ == "__main__":
    unittest.main()
