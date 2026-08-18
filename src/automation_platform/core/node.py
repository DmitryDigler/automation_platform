from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from automation_platform.core.capability import Capability
from automation_platform.core.identity import EntityId


class NodeStatus:
    DISCOVERED = "discovered"
    REGISTERED = "registered"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DRAINING = "draining"
    RETIRED = "retired"


@dataclass(frozen=True, slots=True)
class Node:
    """
    Immutable logical execution environment.

    Node identity is semantic and independent from the physical
    machine, operating system, process, container, or location.
    """

    node_id: EntityId
    runtime_id: EntityId
    status: str
    capabilities: FrozenSet[Capability]
    version: str

    @classmethod
    def create(
        cls,
        *,
        runtime_id: EntityId,
        capabilities: FrozenSet[Capability] | None = None,
        version: str = "1",
    ) -> Node:
        if not version:
            raise ValueError("node version must not be empty")

        return cls(
            node_id=EntityId.new(),
            runtime_id=runtime_id,
            status=NodeStatus.DISCOVERED,
            capabilities=frozenset(capabilities or ()),
            version=version,
        )

    def has_capability(self, capability: Capability) -> bool:
        return capability in self.capabilities

    def with_status(self, status: str) -> Node:
        return Node(
            node_id=self.node_id,
            runtime_id=self.runtime_id,
            status=status,
            capabilities=self.capabilities,
            version=self.version,
        )

    def with_capabilities(
        self,
        capabilities: FrozenSet[Capability],
    ) -> Node:
        return Node(
            node_id=self.node_id,
            runtime_id=self.runtime_id,
            status=self.status,
            capabilities=frozenset(capabilities),
            version=self.version,
        )
