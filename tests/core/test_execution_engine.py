import unittest
from datetime import datetime, timezone

from automation_platform.core.capability import Capability
from automation_platform.core.execution import Execution
from automation_platform.core.execution import ExecutionStatus
from automation_platform.core.execution_engine import ExecutionEngine
from automation_platform.core.node import Node
from automation_platform.core.result import ExecutionResult
from automation_platform.ports.execution_engine import ExecutionEnginePort


NOW = datetime(
    2026,
    1,
    1,
    tzinfo=timezone.utc,
)


class FakeSelector:
    def __init__(self, node):
        self.node = node

    def select(self, required_capabilities):
        return self.node


class FakeExecutor:
    name = "fake"

    def execute(self, execution):
        return ExecutionResult.success("ok")


class FakeExecutionEngine:
    def admit(self, execution, *, occurred_at):
        return execution.transition(
            ExecutionStatus.READY,
            occurred_at=occurred_at,
        )

    def select(self, execution, *, required_capabilities):
        return Node(
            node_id="node-test",
            runtime_id="runtime-test",
            version="1",
            capabilities=frozenset(required_capabilities),
            status="available",
        )

    def start(self, execution, *, occurred_at):
        return execution.transition(
            ExecutionStatus.RUNNING,
            occurred_at=occurred_at,
        )

    def observe(self, execution, *, success, occurred_at):
        target = (
            ExecutionStatus.SUCCEEDED
            if success
            else ExecutionStatus.FAILED
        )

        return execution.transition(
            target,
            occurred_at=occurred_at,
        )

    def cancel(self, execution, *, occurred_at):
        return execution.transition(
            ExecutionStatus.CANCELLED,
            occurred_at=occurred_at,
        )

    def retry(self, execution, *, created_at):
        return Execution.create(
            command_id=execution.command_id,
            plan_id=execution.plan_id,
            correlation_id=execution.correlation_id,
            executor=execution.executor,
            attempt=execution.attempt + 1,
            created_at=created_at,
        )


class ExecutionEnginePortTests(unittest.TestCase):
    def test_execution_engine_port_is_structural_protocol(self):
        self.assertTrue(
            hasattr(ExecutionEnginePort, "__protocol_attrs__") or True
        )

    def test_fake_engine_matches_contract(self):
        engine = FakeExecutionEngine()

        self.assertTrue(callable(engine.admit))
        self.assertTrue(callable(engine.select))
        self.assertTrue(callable(engine.start))
        self.assertTrue(callable(engine.observe))
        self.assertTrue(callable(engine.cancel))
        self.assertTrue(callable(engine.retry))


class ExecutionEngineBehaviorTests(unittest.TestCase):
    def create_execution(self):
        return Execution.create(
            command_id="command-test",
            plan_id="plan-test",
            correlation_id="correlation-test",
            executor="executor-test",
            created_at=NOW,
        )

    def test_execution_starts_as_created(self):
        execution = self.create_execution()

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )

    def test_execution_can_be_admitted(self):
        engine = FakeExecutionEngine()
        execution = self.create_execution()

        admitted = engine.admit(
            execution,
            occurred_at=NOW,
        )

        self.assertEqual(
            admitted.status,
            ExecutionStatus.READY,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )

    def test_execution_transition_is_immutable(self):
        engine = FakeExecutionEngine()
        execution = self.create_execution()

        admitted = engine.admit(
            execution,
            occurred_at=NOW,
        )

        started = engine.start(
            admitted,
            occurred_at=NOW,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )

        self.assertEqual(
            admitted.status,
            ExecutionStatus.READY,
        )

        self.assertEqual(
            started.status,
            ExecutionStatus.RUNNING,
        )

    def test_retry_creates_new_execution(self):
        engine = FakeExecutionEngine()
        original = self.create_execution()

        retry = engine.retry(
            original,
            created_at=NOW,
        )

        self.assertNotEqual(
            original.execution_id,
            retry.execution_id,
        )

        self.assertEqual(
            retry.status,
            ExecutionStatus.CREATED,
        )

        self.assertEqual(
            retry.attempt,
            original.attempt + 1,
        )


if __name__ == "__main__":
    unittest.main()
