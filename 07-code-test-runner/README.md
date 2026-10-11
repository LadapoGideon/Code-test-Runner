# Code Test Runner

Use this to grade code that an AI wrote. You give it the code and a list of test cases, and it runs each case and reports pass or fail. Each run happens in a separate Python process with a timeout, so broken or endless code cannot crash the evaluator.

**Skills shown:** programming, debugging, writing test harnesses, handling untrusted code safely.

## Run the tests

```
python3 -m unittest -v
```

## Example

```python
from run_tests import run_solution, pass_rate

code = "def add(a, b):\n    return a + b"
tests = [("add(2, 3)", 5), ("add(-1, 1)", 0)]
outcome = run_solution(code, tests)
print(pass_rate(outcome))  # 1.0
```

## Security note

This isolates the code in a subprocess with a timeout. It is not a full security sandbox. Do not run code from untrusted sources on a machine with sensitive data without a container or VM around it.
