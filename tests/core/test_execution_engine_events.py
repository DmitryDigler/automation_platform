import unittest
from datetime import datetime, timezone

from automation_platform.core.execution import (
    Execution,
)
from automation_platform.core.execution_engine import ExecutionEngine
from automation_platform.core.execution_event import (
    ExecutionAdmitted,
    ExecutionStarted,
    ExecutionSucceeded,
)
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


class ExecutionEngineEventTests(unittest.TestCase):

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

    def test_run_returns_lifecycle_events(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        self.assertEqual(len(outcome.events), 3)

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

    def test_events_reference_same_execution(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        for event in outcome.events:
            self.assertEqual(
                event.execution_id,
                execution.execution_id,
            )

    def test_event_timestamps_are_preserved(self):
        engine = self.create_engine(
            ExecutionResult.success("hello")
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset(),
            occurred_at=self.NOW,
        )

        for event in outcome.events:
            self.assertEqual(
                event.occurred_at,
                self.NOW,
            )


if __name__ == "__main__":
    unittest.main()
