import unittest

from automation_platform.adapters.registry_node_selector import (
    RegistryNodeSelector,
)
from automation_platform.core.capability import Capability
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node, NodeStatus
from automation_platform.core.node_registry import NodeRegistry


class RegistryNodeSelectorTests(unittest.TestCase):

    def create_node(
        self,
        *capabilities: Capability,
        status: str = NodeStatus.AVAILABLE,
    ) -> Node:
        node = Node.create(
            runtime_id=EntityId.new(),
            capabilities=frozenset(capabilities),
        )

        return node.with_status(status)

    def test_select_returns_capable_available_node(self):
        python = Capability("python")
        gpu = Capability("gpu")

        node = self.create_node(
            python,
            gpu,
        )

        registry = NodeRegistry.empty().register(node)
        selector = RegistryNodeSelector(registry)

        selected = selector.select(
            frozenset({python, gpu})
        )

        self.assertEqual(selected, node)

    def test_select_ignores_nodes_without_required_capabilities(self):
        python = Capability("python")
        gpu = Capability("gpu")

        python_only = self.create_node(python)
        python_gpu = self.create_node(python, gpu)

        registry = (
            NodeRegistry.empty()
            .register(python_only)
            .register(python_gpu)
        )

        selector = RegistryNodeSelector(registry)

        selected = selector.select(
            frozenset({python, gpu})
        )

        self.assertEqual(selected, python_gpu)

    def test_select_ignores_unavailable_nodes(self):
        python = Capability("python")

        unavailable = self.create_node(
            python,
            status=NodeStatus.UNAVAILABLE,
        )

        registry = NodeRegistry.empty().register(unavailable)
        selector = RegistryNodeSelector(registry)

        with self.assertRaisesRegex(
            RuntimeError,
            "no capable node available",
        ):
            selector.select(
                frozenset({python})
            )

    def test_select_fails_when_no_capable_node_exists(self):
        python = Capability("python")
        gpu = Capability("gpu")

        node = self.create_node(python)

        registry = NodeRegistry.empty().register(node)
        selector = RegistryNodeSelector(registry)

        with self.assertRaisesRegex(
            RuntimeError,
            "no capable node available",
        ):
            selector.select(
                frozenset({python, gpu})
            )

    def test_select_with_no_requirements_returns_available_node(self):
        node = self.create_node(
            Capability("python"),
        )

        registry = NodeRegistry.empty().register(node)
        selector = RegistryNodeSelector(registry)

        selected = selector.select(frozenset())

        self.assertEqual(selected, node)

    def test_selector_does_not_mutate_registry(self):
        node = self.create_node(
            Capability("python"),
        )

        registry = NodeRegistry.empty().register(node)
        selector = RegistryNodeSelector(registry)

        selector.select(
            frozenset({Capability("python")})
        )

        self.assertEqual(
            registry.nodes,
            frozenset({node}),
        )


if __name__ == "__main__":
    unittest.main()
