from __future__ import annotations

from typing import FrozenSet, Protocol

from automation_platform.core.capability import Capability
from automation_platform.core.node import Node


class NodeSelector(Protocol):
    """
    Port describing how an execution environment is selected.

    The Execution Engine asks for a Node satisfying required
    capabilities. The selector decides which eligible Node
    should be returned.

    Selection policy remains outside the semantic Core.
    """

    def select(
        self,
        required: FrozenSet[Capability],
    ) -> Node:
        """
        Select one Node capable of satisfying the requirements.

        Implementations may apply policies involving:

        - capabilities
        - locality
        - availability
        - trust
        - resources
        - cost
        - affinity

        The selector does not execute work.
        """
        ...
