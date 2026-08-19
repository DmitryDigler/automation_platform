from __future__ import annotations

from automation_platform.core.capability import Capability
from automation_platform.core.node import Node
from automation_platform.core.node_registry import NodeRegistry
from automation_platform.ports.node_selector import NodeSelector


class RegistryNodeSelector(NodeSelector):
    """
    Node selector backed by an immutable NodeRegistry.

    Selection is limited to currently available nodes that satisfy
    all required capabilities.

    The selector does not execute work and does not mutate the registry.
    """

    def __init__(self, registry: NodeRegistry):
        self._registry = registry

    def select(
        self,
        required: frozenset[Capability],
    ) -> Node:
        candidates = self._registry.find_capable(required)

        if not candidates:
            raise RuntimeError(
                "no capable node available"
            )

        return min(
            candidates,
            key=lambda node: str(node.node_id),
        )
