import unittest

from automation_platform.core.capability import Capability
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node, NodeStatus
from automation_platform.core.node_registry import NodeRegistry


class NodeRegistryTests(unittest.TestCase):

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

    def test_empty_registry_contains_no_nodes(self):
        registry = NodeRegistry.empty()

        self.assertEqual(registry.nodes, frozenset())

    def test_register_adds_node(self):
        registry = NodeRegistry.empty()
        node = self.create_node(
            Capability("python"),
        )

        updated = registry.register(node)

        self.assertEqual(registry.nodes, frozenset())
        self.assertIn(node, updated.nodes)

    def test_register_replaces_same_logical_node(self):
        registry = NodeRegistry.empty()

        node = self.create_node(
            Capability("python"),
        )

        updated = registry.register(node)

        replacement = node.with_capabilities(
            frozenset(
                {
                    Capability("python"),
                    Capability("gpu"),
                }
            )
        )

        final = updated.register(replacement)

        self.assertEqual(len(final.nodes), 1)
        self.assertEqual(
            final.get(node.node_id),
            replacement,
        )

    def test_remove_node(self):
        node = self.create_node(
            Capability("python"),
        )

        registry = NodeRegistry.empty().register(node)
        updated = registry.remove(node.node_id)

        self.assertIsNone(updated.get(node.node_id))
        self.assertIn(node, registry.nodes)

    def test_available_nodes_excludes_unavailable_nodes(self):
        available = self.create_node(
            Capability("python"),
            status=NodeStatus.AVAILABLE,
        )

        unavailable = self.create_node(
            Capability("python"),
            status=NodeStatus.UNAVAILABLE,
        )

        registry = (
            NodeRegistry.empty()
            .register(available)
            .register(unavailable)
        )

        candidates = registry.available_nodes()

        self.assertIn(available, candidates)
        self.assertNotIn(unavailable, candidates)

    def test_find_capable_requires_all_capabilities(self):
        python = Capability("python")
        gpu = Capability("gpu")

        python_only = self.create_node(python)
        python_gpu = self.create_node(python, gpu)

        registry = (
            NodeRegistry.empty()
            .register(python_only)
            .register(python_gpu)
        )

        candidates = registry.find_capable(
            frozenset({python, gpu})
        )

        self.assertNotIn(python_only, candidates)
        self.assertIn(python_gpu, candidates)

    def test_find_capable_ignores_unavailable_nodes(self):
        python = Capability("python")

        node = self.create_node(
            python,
            status=NodeStatus.UNAVAILABLE,
        )

        registry = NodeRegistry.empty().register(node)

        candidates = registry.find_capable(
            frozenset({python})
        )

        self.assertEqual(candidates, frozenset())

    def test_find_capable_with_no_requirements_returns_available_nodes(self):
        first = self.create_node(Capability("python"))
        second = self.create_node(Capability("gpu"))

        registry = (
            NodeRegistry.empty()
            .register(first)
            .register(second)
        )

        candidates = registry.find_capable(frozenset())

        self.assertEqual(
            candidates,
            frozenset({first, second}),
        )

    def test_registry_is_immutable(self):
        registry = NodeRegistry.empty()
        node = self.create_node(Capability("python"))

        updated = registry.register(node)

        self.assertEqual(registry.nodes, frozenset())
        self.assertNotEqual(registry, updated)

        with self.assertRaises(AttributeError):
            registry.nodes = frozenset({node})


if __name__ == "__main__":
    unittest.main()
