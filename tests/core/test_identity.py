import unittest
from uuid import UUID

from automation_platform.core.identity import EntityId


class EntityIdTests(unittest.TestCase):

    def test_new_creates_valid_uuid(self):
        entity_id = EntityId.new()

        self.assertIsInstance(entity_id.value, UUID)

    def test_new_creates_unique_ids(self):
        first = EntityId.new()
        second = EntityId.new()

        self.assertNotEqual(first, second)

    def test_string_round_trip(self):
        original = EntityId.new()

        restored = EntityId.from_string(str(original))

        self.assertEqual(original, restored)

    def test_entity_id_is_immutable(self):
        entity_id = EntityId.new()

        with self.assertRaises(AttributeError):
            entity_id.value = UUID(int=0)


if __name__ == "__main__":
    unittest.main()
