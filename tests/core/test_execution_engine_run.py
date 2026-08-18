import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import (
    Execution,
    ExecutionStatus,
)
from automation_platform.core.execution_engine import ExecutionEngine
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node
from automation_platform.core.result import ExecutionResult


class FakeSelector:
    def __init__(self, node):
        self.node = node

    def select(self, required):
        return self.node


class FakeExecutor:
    def __init__(self, result):
        self.result = result

    @property
    def name(self):
        return "fake"

    def execute(self, execution):
        return self.result


class ExecutionEngineRunTests(unittest.TestCase):

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

    def create_node(self):
        return Node.create(
            runtime_id=EntityId.new(),
        )

    def test_run_completes_successful_execution(self):
        engine = ExecutionEngine(
            selector=FakeSelector(self.create_node()),
            executor=FakeExecutor(
                ExecutionResult.success("hello")
            ),
        )

        execution = self.create_execution()

        result = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(
            result.execution.status,
            ExecutionStatus.SUCCEEDED,
        )

    def test_run_fails_when_executor_reports_failure(self):
        engine = ExecutionEngine(
            selector=FakeSelector(self.create_node()),
            executor=FakeExecutor(
                ExecutionResult.failure("boom")
            ),
        )

        execution = self.create_execution()

        result = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(
            result.execution.status,
            ExecutionStatus.FAILED,
        )

    def test_run_does_not_mutate_original_execution(self):
        engine = ExecutionEngine(
            selector=FakeSelector(self.create_node()),
            executor=FakeExecutor(
                ExecutionResult.success()
            ),
        )

        execution = self.create_execution()

        result = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.CREATED,
        )

        self.assertEqual(
            result.execution.status,
            ExecutionStatus.SUCCEEDED,
        )

        self.assertEqual(
            execution.execution_id,
            result.execution.execution_id,
        )

    def test_run_rejects_invalid_executor_observation(self):
        class InvalidExecutor:
            @property
            def name(self):
                return "invalid"

            def execute(self, execution):
                return "not-an-execution-result"

        engine = ExecutionEngine(
            selector=FakeSelector(self.create_node()),
            executor=InvalidExecutor(),
        )

        execution = self.create_execution()

        with self.assertRaisesRegex(
            TypeError,
            "executor must return ExecutionResult",
        ):
            engine.run(
                execution,
                required_capabilities=frozenset(),
                occurred_at=self.NOW,
            )


if __name__ == "__main__":
    unittest.main()
