import unittest
from datetime import datetime, timezone

from automation_platform.core.event import Event
from automation_platform.core.identity import EntityId


class EventTests(unittest.TestCase):

    def test_create_generates_event_id(self):
        correlation_id = EntityId.new()

        event = Event.create(
            event_type="task.created",
            source="core",
            correlation_id=correlation_id,
            payload={"name": "test"},
        )

        self.assertIsInstance(event.event_id, EntityId)

    def test_event_is_timestamped_in_utc(self):
        event = Event.create(
            event_type="task.created",
            source="core",
            correlation_id=EntityId.new(),
            payload={},
        )

        self.assertIsInstance(event.occurred_at, datetime)
        self.assertEqual(event.occurred_at.tzinfo, timezone.utc)

    def test_correlation_and_causation(self):
        correlation_id = EntityId.new()
        causation_id = EntityId.new()

        event = Event.create(
            event_type="execution.started",
            source="runtime",
            correlation_id=correlation_id,
            causation_id=causation_id,
            payload={},
        )

        self.assertEqual(event.correlation_id, correlation_id)
        self.assertEqual(event.causation_id, causation_id)

    def test_event_is_immutable(self):
        event = Event.create(
            event_type="task.created",
            source="core",
            correlation_id=EntityId.new(),
            payload={},
        )

        with self.assertRaises(AttributeError):
            event.event_type = "something.else"

    def test_invalid_event_type_is_rejected(self):
        with self.assertRaises(ValueError):
            Event.create(
                event_type="",
                source="core",
                correlation_id=EntityId.new(),
                payload={},
            )

    def test_invalid_version_is_rejected(self):
        with self.assertRaises(ValueError):
            Event.create(
                event_type="task.created",
                source="core",
                correlation_id=EntityId.new(),
                payload={},
                event_version=0,
            )


if __name__ == "__main__":
    unittest.main()
