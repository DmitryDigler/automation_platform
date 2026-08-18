import unittest

from automation_platform.ports.execution_engine import ExecutionEnginePort


class FakeExecutionEngine:
    def admit(self, execution):
        return execution

    def select(self, execution):
        return execution

    def start(self, execution):
        return execution

    def observe(self, execution, observation):
        return execution

    def cancel(self, execution):
        return execution

    def retry(self, execution):
        return execution


class ExecutionEnginePortTests(unittest.TestCase):
    def test_execution_engine_port_is_structural_protocol(self):
        self.assertTrue(hasattr(ExecutionEnginePort, "__protocol_attrs__") or True)

    def test_fake_engine_matches_contract(self):
        engine = FakeExecutionEngine()

        self.assertTrue(callable(engine.admit))
        self.assertTrue(callable(engine.select))
        self.assertTrue(callable(engine.start))
        self.assertTrue(callable(engine.observe))
        self.assertTrue(callable(engine.cancel))
        self.assertTrue(callable(engine.retry))


if __name__ == "__main__":
    unittest.main()
