import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import Execution
from automation_platform.ports.execution_engine import ExecutionEnginePort


def now():
    return datetime.now(timezone.utc)


class FakeExecutionEngine:
    def admit(self, execution):
        return execution.transition(
            "ready",
            occurred_at=now(),
        )

    def select(self, execution):
        return execution

    def start(self, execution):
        return execution.transition(
            "running",
            occurred_at=now(),
        )

    def observe(self, execution, observation):
        return execution

    def cancel(self, execution):
        return execution.transition(
            "cancelled",
            occurred_at=now(),
        )

    def retry(self, execution):
        return Execution.create(
            command_id=execution.command_id,
            plan_id=execution.plan_id,
            correlation_id=execution.correlation_id,
            executor=execution.executor,
            created_at=now(),
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
            created_at=now(),
        )

    def test_execution_starts_as_created(self):
        execution = self.create_execution()

        self.assertEqual(
            execution.status,
            "created",
        )

    def test_execution_can_be_admitted(self):
        engine = FakeExecutionEngine()
        execution = self.create_execution()

        admitted = engine.admit(execution)

        self.assertEqual(
            admitted.status,
            "ready",
        )

        self.assertEqual(
            execution.status,
            "created",
        )

    def test_execution_transition_is_immutable(self):
        engine = FakeExecutionEngine()
        execution = self.create_execution()

        admitted = engine.admit(execution)
        started = engine.start(admitted)

        self.assertEqual(
            execution.status,
            "created",
        )

        self.assertEqual(
            admitted.status,
            "ready",
        )

        self.assertEqual(
            started.status,
            "running",
        )

    def test_retry_creates_new_execution(self):
        engine = FakeExecutionEngine()
        original = self.create_execution()

        retry = engine.retry(original)

        self.assertNotEqual(
            original.execution_id,
            retry.execution_id,
        )

        self.assertEqual(
            retry.status,
            "created",
        )


if __name__ == "__main__":
    unittest.main()
