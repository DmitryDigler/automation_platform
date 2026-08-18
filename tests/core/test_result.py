import unittest

from automation_platform.core.result import ExecutionResult


class ExecutionResultTests(unittest.TestCase):

    def test_success_result(self):
        result = ExecutionResult.success(
            value="hello",
        )

        self.assertTrue(result.success)
        self.assertEqual(result.value, "hello")
        self.assertIsNone(result.error)

    def test_failure_result(self):
        result = ExecutionResult.failure(
            error="boom",
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error, "boom")
        self.assertIsNone(result.value)

    def test_result_is_immutable(self):
        result = ExecutionResult.success(
            value="hello",
        )

        with self.assertRaises(AttributeError):
            result.success = False

    def test_empty_error_is_rejected(self):
        with self.assertRaises(ValueError):
            ExecutionResult.failure(
                error="",
            )


if __name__ == "__main__":
    unittest.main()
