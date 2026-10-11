import unittest

from run_tests import pass_rate, run_solution


GOOD = """
def add(a, b):
    return a + b
"""

BUGGY = """
def add(a, b):
    return a - b
"""

TESTS = [("add(2, 3)", 5), ("add(-1, 1)", 0), ("add(10, 10)", 20)]


class RunTestsTests(unittest.TestCase):
    def test_correct_solution_passes_everything(self):
        outcome = run_solution(GOOD, TESTS)
        self.assertEqual(pass_rate(outcome), 1.0)

    def test_buggy_solution_is_caught(self):
        outcome = run_solution(BUGGY, TESTS)
        self.assertEqual(pass_rate(outcome), 0.0)
        self.assertFalse(outcome["results"][0]["pass"])

    def test_syntax_error_is_reported_not_raised(self):
        outcome = run_solution("def add(a, b) return a + b", TESTS)
        self.assertIn("error", outcome)
        self.assertEqual(pass_rate(outcome), 0.0)

    def test_infinite_loop_times_out(self):
        outcome = run_solution("def f():\n    while True:\n        pass", [("f()", 1)], timeout=1.0)
        self.assertIn("timed out", outcome["error"])

    def test_runtime_exception_is_recorded_as_failure(self):
        outcome = run_solution(GOOD, [("add(1, 'x')", 1)])
        self.assertFalse(outcome["results"][0]["pass"])
        self.assertIn("TypeError", outcome["results"][0]["got"])


if __name__ == "__main__":
    unittest.main()
