import unittest
from datetime import datetime, timezone

from automation_platform.core.event import Event
from automation_platform.core.execution import Execution
from automation_platform.core.identity import EntityId
from automation_platform.ports.executor import Executor


class ExecutorPortTests(unittest.TestCase):

    def create_execution(self) -> Execution:
        now = datetime.now(timezone.utc)

        return Execution.create(
            command_id=EntityId.new(),
            plan_id=EntityId.new(),
            correlation_id=EntityId.new(),
            executor="fake",
            created_at=now,
        )

    def test_executor_port_is_importable(self):
        self.assertTrue(Executor)

    def test_executor_is_structural_protocol(self):
        self.assertTrue(hasattr(Executor, "execute"))
        self.assertTrue(hasattr(Executor, "name"))

    def test_fake_executor_matches_contract(self):
        class FakeExecutor:

            @property
            def name(self) -> str:
                return "fake"

            def execute(self, execution: Execution) -> list[Event]:
                return []

        executor: Executor = FakeExecutor()
        execution = self.create_execution()

        self.assertEqual(executor.name, "fake")
        self.assertEqual(executor.execute(execution), [])

    def test_executor_can_report_observation(self):
        class RecordingExecutor:

            @property
            def name(self) -> str:
                return "recording"

            def execute(self, execution: Execution) -> list[Event]:
                return [
                    Event.create(
                        event_type="execution.observed",
                        source=self.name,
                        correlation_id=execution.correlation_id,
                        causation_id=execution.execution_id,
                        payload={
                            "execution_id": str(execution.execution_id),
                        },
                    )
                ]

        executor: Executor = RecordingExecutor()
        execution = self.create_execution()

        events = executor.execute(execution)

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0].event_type,
            "execution.observed",
        )
        self.assertEqual(
            events[0].causation_id,
            execution.execution_id,
        )

    def test_executor_does_not_mutate_execution(self):
        class FakeExecutor:

            @property
            def name(self) -> str:
                return "fake"

            def execute(self, execution: Execution) -> list[Event]:
                return []

        executor: Executor = FakeExecutor()
        execution = self.create_execution()

        original_status = execution.status

        executor.execute(execution)

        self.assertEqual(
            execution.status,
            original_status,
        )


if __name__ == "__main__":
    unittest.main()
