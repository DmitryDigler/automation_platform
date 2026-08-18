from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from automation_platform.core.capability import Capability
from automation_platform.core.node import Node, NodeStatus
from automation_platform.core.identity import EntityId


@dataclass(frozen=True, slots=True)
class NodeRegistry:
    """
    Immutable registry of logical execution Nodes.

    The registry knows which Nodes exist and which capabilities
    they currently advertise.

    It does not perform execution and does not own Execution lifecycle.
    """

    nodes: FrozenSet[Node]

    @classmethod
    def empty(cls) -> NodeRegistry:
        return cls(nodes=frozenset())

    def register(self, node: Node) -> NodeRegistry:
        return NodeRegistry(
            nodes=frozenset(
                existing
                for existing in self.nodes
                if existing.node_id != node.node_id
            )
            | {node}
        )

    def remove(self, node_id: EntityId) -> NodeRegistry:
        return NodeRegistry(
            nodes=frozenset(
                node
                for node in self.nodes
                if node.node_id != node_id
            )
        )

    def get(self, node_id: EntityId) -> Node | None:
        for node in self.nodes:
            if node.node_id == node_id:
                return node

        return None

    def available_nodes(self) -> FrozenSet[Node]:
        return frozenset(
            node
            for node in self.nodes
            if node.status == NodeStatus.AVAILABLE
        )

    def find_capable(
        self,
        required: FrozenSet[Capability],
    ) -> FrozenSet[Node]:
        """
        Return available Nodes providing every required capability.
        """

        return frozenset(
            node
            for node in self.available_nodes()
            if required.issubset(node.capabilities)
        )
