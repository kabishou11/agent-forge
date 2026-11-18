import json

import tags

CASES = (
    ("alpha, beta", ["alpha", "beta"]),
    ("alpha,beta", ["alpha", "beta"]),
    ("  ", []),
    ("one, two, one", ["one", "two", "one"]),
)

failures = []
for raw, expected in CASES:
    actual = tags.split_tags(raw)
    if actual != expected:
        failures.append({"input": raw, "expected": expected, "actual": actual})

status = "pass" if not failures else "fail"
print(json.dumps({"checks": len(CASES), "failures": failures, "status": status}, indent=2))
raise SystemExit(0 if status == "pass" else 1)
