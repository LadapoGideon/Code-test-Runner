"""Run a candidate Python function against test cases in a separate process.

The candidate code runs in its own interpreter with a timeout, so an infinite
loop or a crash cannot take down the evaluator.
"""
import json
import os
import subprocess
import sys
import tempfile

HARNESS = """
import json as _json
_results = []
def _run(expr, expected):
    try:
        got = eval(expr)
        _results.append({"expr": expr, "pass": got == expected, "got": repr(got)})
    except Exception as err:
        _results.append({"expr": expr, "pass": False, "got": type(err).__name__ + ": " + str(err)})
"""


def run_solution(source, tests, timeout=5.0):
    """
    source: Python code that defines the solution.
    tests: list of (expression, expected_value) pairs, e.g. ("add(2, 3)", 5).
    Returns {"results": [...]} or {"error": "..."} if the code crashed or timed out.
    """
    lines = [source, HARNESS]
    for expr, expected in tests:
        lines.append(f"_run({expr!r}, {expected!r})")
    lines.append("print(_json.dumps(_results))")
    script = "\n".join(lines)

    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "candidate.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
        try:
            proc = subprocess.run(
                [sys.executable, "-I", path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return {"error": f"timed out after {timeout} seconds"}

    if proc.returncode != 0:
        last_line = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "exited with an error"
        return {"error": last_line}

    return {"results": json.loads(proc.stdout.strip().splitlines()[-1])}


def pass_rate(outcome):
    if "error" in outcome:
        return 0.0
    results = outcome["results"]
    return sum(r["pass"] for r in results) / len(results)
