import unittest

from automation_platform.core.capability import Capability


class CapabilityTests(unittest.TestCase):

    def test_capability_can_be_created(self):
        capability = Capability(
            name="filesystem.read",
        )

        self.assertEqual(
            capability.name,
            "filesystem.read",
        )

        self.assertEqual(
            capability.version,
            "1",
        )

    def test_capability_is_immutable(self):
        capability = Capability(
            name="browser",
        )

        with self.assertRaises(AttributeError):
            capability.name = "gpu"

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Capability(name="")

    def test_empty_version_is_rejected(self):
        with self.assertRaises(ValueError):
            Capability(
                name="browser",
                version="",
            )

    def test_capabilities_are_value_objects(self):
        first = Capability(
            name="python",
            version="3",
        )

        second = Capability(
            name="python",
            version="3",
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
