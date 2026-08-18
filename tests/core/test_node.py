import unittest

from automation_platform.core.capability import Capability
from automation_platform.core.identity import EntityId
from automation_platform.core.node import Node, NodeStatus


class NodeTests(unittest.TestCase):

    def create_node(self) -> Node:
        return Node.create(
            runtime_id=EntityId.new(),
            capabilities=frozenset(
                {
                    Capability("filesystem.read"),
                    Capability("python", "3"),
                }
            ),
        )

    def test_node_can_be_created(self):
        node = self.create_node()

        self.assertTrue(node.node_id)
        self.assertTrue(node.runtime_id)
        self.assertEqual(node.status, NodeStatus.DISCOVERED)
        self.assertEqual(node.version, "1")

    def test_node_has_capability(self):
        node = self.create_node()

        self.assertTrue(
            node.has_capability(
                Capability("filesystem.read")
            )
        )

        self.assertFalse(
            node.has_capability(
                Capability("gpu")
            )
        )

    def test_node_capabilities_are_immutable(self):
        node = self.create_node()

        with self.assertRaises(AttributeError):
            node.capabilities = frozenset()

    def test_node_is_immutable(self):
        node = self.create_node()

        with self.assertRaises(AttributeError):
            node.status = NodeStatus.AVAILABLE

    def test_status_change_creates_new_node(self):
        node = self.create_node()

        updated = node.with_status(NodeStatus.AVAILABLE)

        self.assertEqual(node.status, NodeStatus.DISCOVERED)
        self.assertEqual(updated.status, NodeStatus.AVAILABLE)

        self.assertEqual(
            node.node_id,
            updated.node_id,
        )

    def test_capability_change_creates_new_node(self):
        node = self.create_node()

        updated = node.with_capabilities(
            frozenset(
                {
                    Capability("gpu"),
                }
            )
        )

        self.assertTrue(
            node.has_capability(
                Capability("filesystem.read")
            )
        )

        self.assertFalse(
            node.has_capability(
                Capability("gpu")
            )
        )

        self.assertTrue(
            updated.has_capability(
                Capability("gpu")
            )
        )

    def test_runtime_identity_is_separate_from_node_identity(self):
        runtime_id = EntityId.new()

        node = Node.create(
            runtime_id=runtime_id,
        )

        self.assertEqual(node.runtime_id, runtime_id)
        self.assertNotEqual(node.node_id, node.runtime_id)

    def test_empty_version_is_rejected(self):
        with self.assertRaises(ValueError):
            Node.create(
                runtime_id=EntityId.new(),
                version="",
            )


if __name__ == "__main__":
    unittest.main()
