import unittest

from automation_platform.core.capability import Capability
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node, NodeStatus
from automation_platform.ports.node_selector import NodeSelector


class NodeSelectorPortTests(unittest.TestCase):

    def test_node_selector_is_importable(self):
        self.assertTrue(NodeSelector)

    def test_node_selector_is_structural_protocol(self):
        self.assertTrue(hasattr(NodeSelector, "select"))

    def test_fake_selector_matches_contract(self):
        class FakeSelector:

            def select(self, required):
                return Node.create(
                    runtime_id=EntityId.new(),
                    capabilities=frozenset(required),
                ).with_status(NodeStatus.AVAILABLE)

        selector: NodeSelector = FakeSelector()

        required = frozenset(
            {
                Capability("python"),
            }
        )

        node = selector.select(required)

        self.assertTrue(
            node.has_capability(
                Capability("python")
            )
        )

        self.assertEqual(
            node.status,
            NodeStatus.AVAILABLE,
        )


if __name__ == "__main__":
    unittest.main()
