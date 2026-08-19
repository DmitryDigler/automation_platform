import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import Execution, ExecutionStatus
from automation_platform.core.execution_engine import ExecutionEngine
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionFailed,
    ExecutionStarted,
    ExecutionSucceeded,
)
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node
from automation_platform.core.outcome import ExecutionOutcome
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


class ExecutionEngineOutcomeTests(unittest.TestCase):

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

    def create_engine(self, result):
        return ExecutionEngine(
            selector=FakeSelector(
                Node.create(
                    runtime_id=EntityId.new(),
                )
            ),
            executor=FakeExecutor(result),
        )

    def test_run_preserves_success_result(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        outcome = engine.run(
            self.create_execution(),
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(
            outcome.execution.status,
            ExecutionStatus.SUCCEEDED,
        )

        self.assertTrue(outcome.result.success)

        self.assertEqual(
            outcome.result.value,
            "hello",
        )

    def test_run_preserves_failure_result(self):
        engine = self.create_engine(
            ExecutionResult.failure("boom")
        )

        outcome = engine.run(
            self.create_execution(),
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(
            outcome.execution.status,
            ExecutionStatus.FAILED,
        )

        self.assertFalse(outcome.result.success)

        self.assertEqual(
            outcome.result.error,
            "boom",
        )

    def test_outcome_keeps_same_execution_identity(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(
            execution.execution_id,
            outcome.execution.execution_id,
        )

    def test_run_returns_complete_execution_outcome(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertIsInstance(
            outcome,
            ExecutionOutcome,
        )

        self.assertIs(
            outcome.result,
            engine.executor.result,
        )

        self.assertEqual(
            len(outcome.events),
            3,
        )

        self.assertIsInstance(
            outcome.events[0],
            ExecutionAdmitted,
        )

        self.assertIsInstance(
            outcome.events[1],
            ExecutionStarted,
        )

        self.assertIsInstance(
            outcome.events[2],
            ExecutionSucceeded,
        )

    def test_run_returns_complete_failed_execution_outcome(self):
        engine = self.create_engine(
            ExecutionResult.failure("boom")
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertIsInstance(
            outcome,
            ExecutionOutcome,
        )

        self.assertIs(
            outcome.result,
            engine.executor.result,
        )

        self.assertEqual(
            outcome.execution.status,
            ExecutionStatus.FAILED,
        )

        self.assertEqual(
            len(outcome.events),
            3,
        )

        self.assertIsInstance(
            outcome.events[0],
            ExecutionAdmitted,
        )

        self.assertIsInstance(
            outcome.events[1],
            ExecutionStarted,
        )

        self.assertIsInstance(
            outcome.events[2],
            ExecutionFailed,
        )

    def test_outcome_is_immutable(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        outcome = engine.run(
            self.create_execution(),
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        with self.assertRaises(AttributeError):
            outcome.result = ExecutionResult.success("changed")

    def test_run_returns_events_with_causation_chain(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        outcome = engine.run(
            self.create_execution(),
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertIsNone(
            outcome.events[0].causation_id,
        )

        self.assertEqual(
            outcome.events[1].causation_id,
            outcome.events[0].event_id,
        )

        self.assertEqual(
            outcome.events[2].causation_id,
            outcome.events[1].event_id,
        )


if __name__ == "__main__":
    unittest.main()