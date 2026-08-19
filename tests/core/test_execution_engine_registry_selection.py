import unittest
from datetime import datetime, timezone

from automation_platform.adapters.registry_node_selector import (
    RegistryNodeSelector,
)
from automation_platform.core.capability import Capability
from automation_platform.core.execution import (
    Execution,
    ExecutionStatus,
)
from automation_platform.core.execution_engine import ExecutionEngine
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node, NodeStatus
from automation_platform.core.node_registry import NodeRegistry
from automation_platform.core.result import ExecutionResult


class TrackingExecutor:
    def __init__(self, result):
        self.result = result
        self.called = False

    @property
    def name(self):
        return "tracking"

    def execute(self, execution):
        self.called = True
        return self.result


class ExecutionEngineRegistrySelectionTests(unittest.TestCase):

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
            executor="tracking",
            created_at=self.NOW,
        )

    def create_node(self, *capabilities, status=NodeStatus.AVAILABLE):
        return Node.create(
            runtime_id=EntityId.new(),
            capabilities=frozenset(capabilities),
        ).with_status(status)

    def test_run_uses_registry_backed_selector(self):
        python = Capability("python")

        node = self.create_node(python)

        registry = (
            NodeRegistry.empty()
            .register(node)
        )

        selector = RegistryNodeSelector(registry)

        executor = TrackingExecutor(
            ExecutionResult.success("hello")
        )

        engine = ExecutionEngine(
            selector=selector,
            executor=executor,
        )

        execution = self.create_execution()

        outcome = engine.run(
            execution,
            required_capabilities=frozenset({python}),
            occurred_at=self.NOW,
        )

        self.assertTrue(executor.called)

        self.assertEqual(
            outcome.execution.status,
            ExecutionStatus.SUCCEEDED,
        )

        self.assertEqual(
            outcome.result,
            ExecutionResult.success("hello"),
        )

    def test_run_does_not_execute_when_registry_has_no_capable_node(self):
        python = Capability("python")

        registry = NodeRegistry.empty()
        selector = RegistryNodeSelector(registry)

        executor = TrackingExecutor(
            ExecutionResult.success("should not run")
        )

        engine = ExecutionEngine(
            selector=selector,
            executor=executor,
        )

        execution = self.create_execution()

        with self.assertRaisesRegex(
            RuntimeError,
            "no capable node available",
        ):
            engine.run(
                execution,
                required_capabilities=frozenset({python}),
                occurred_at=self.NOW,
            )

        self.assertFalse(executor.called)


if __name__ == "__main__":
    unittest.main()
