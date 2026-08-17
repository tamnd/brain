---
title: "CF 102212A - Adding Two Integers"
description: "The task is deliberately simple: one line contains two integers, a and b, and the program must print the integer obtained by adding them."
date: "2026-08-18T00:22:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102212
codeforces_index: "A"
codeforces_contest_name: "Amazalgo Uni 2019 Practice Contest"
rating: 0
weight: 102212
solve_time_s: 149
verified: false
draft: false
---

[CF 102212A - Adding Two Integers](https://codeforces.com/problemset/problem/102212/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

The task is deliberately simple: one line contains two integers, `a` and `b`, and the program must print the integer obtained by adding them. The values may be positive, zero, or negative, so the operation is ordinary signed integer addition rather than any special handling of nonnegative values.

The bounds are small enough that the arithmetic itself is trivial. Each input value lies between `-1,000,000,000` and `1,000,000,000`, so their sum lies between `-2,000,000,000` and `2,000,000,000`. There is no need for an algorithm that depends on the magnitude of either number. A constant amount of work is enough, and Python's integer type can represent every value in the stated range without overflow.

The main edge cases come from signs and boundary values. For example, with input `50 -26`, the correct output is `24`. A careless solution that assumes both values are positive could mishandle the negative operand. With input `-1000000000 -1000000000`, the correct output is `-2000000000`, so the implementation must preserve both the sign and the full magnitude. Similarly, `1000000000 1000000000` must produce `2000000000`, which catches implementations using an unnecessarily narrow integer type in languages where overflow is possible.

Zero is another simple boundary case. For input `0 7`, the answer is `7`, and for `-5 0`, the answer is `-5`. There is no special algorithmic branch needed for zero, which is one of the useful observations in this problem.

## Approaches

A literal brute-force approach could treat addition as repeated incrementing. Starting from `a`, it could perform one increment for every unit represented by a positive `b`, or one decrement for every unit represented by a negative `b`. This is correct because each operation changes the current value by exactly one, so after the required number of operations the result is `a + b`. The problem is the number of operations. For example, adding `1,000,000,000` would require one billion iterations, and in the worst case the magnitude of the second operand is `1,000,000,000`. That gives up to `1,000,000,000` iterations, far beyond what a one-second Codeforces limit can accommodate.

The structure of the problem gives us a much simpler observation. The operation being requested is already directly supported by the programming language: integer addition computes the desired result in constant time. There is no hidden search space, no array to process, and no relationship between multiple test cases that needs to be exploited.

The brute-force method works because it reconstructs addition one unit at a time, but fails because the number of units can be as large as one billion. The observation that the required operation is itself a primitive integer operation lets us reduce the entire task to one addition after parsing the two input values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | b | ) | O(1) | Too slow in the worst case |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers from the single input line. They are separated by whitespace, so splitting the line gives the two values directly.
2. Compute `a + b`. This is exactly the mathematical quantity requested, and Python handles signed integer arithmetic directly.
3. Print the resulting integer. Printing the value as an integer preserves its sign when the result is negative.

### Why it works

The only maintained value is the exact mathematical sum of the two parsed operands. The addition operation replaces the two input values with their arithmetic sum, so the resulting value is precisely the quantity required by the problem. Since no approximation, iteration, or transformation is involved, there is no intermediate state that can introduce an error.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    print(a + b)

if __name__ == "__main__":
    solve()
```

The first line imports `sys`, allowing the solution to use the required `sys.stdin.readline` input method. The `input` alias reads the complete input line efficiently and matches the standard competitive-programming template.

Inside `solve`, `map(int, input().split())` converts the two textual values into Python integers. Negative numbers are handled automatically by `int`, so no separate sign parsing is necessary.

The expression `a + b` performs the only computation required. Python integers have arbitrary precision, so even the largest possible result, `2,000,000,000`, is represented exactly. There are no loops, array indices, or boundary conditions where an off-by-one error could occur.

The problem contains exactly one pair of integers, so there is no test-case count to read and no loop over multiple cases. The `if __name__ == "__main__"` guard simply makes `solve()` run when the file is executed normally.

## Worked Examples

For Sample 1, the input contains two positive integers.

| Step | `a` | `b` | `a + b` |
| --- | --- | --- | --- |
| Read input | 5 | 9 | 14 |
| Add values | 5 | 9 | 14 |
| Print result | 5 | 9 | 14 |

The computed value is `5 + 9 = 14`, so the program prints `14`. This demonstrates the ordinary positive-integer case.

For Sample 2, the second operand is negative.

| Step | `a` | `b` | `a + b` |
| --- | --- | --- | --- |
| Read input | 50 | -26 | 24 |
| Add values | 50 | -26 | 24 |
| Print result | 50 | -26 | 24 |

The negative sign is preserved when Python parses `-26`, and ordinary signed addition gives `50 + (-26) = 24`. This confirms that the algorithm does not need a special case for mixed signs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The solution parses two integers and performs one addition. |
| Space | O(1) | Only the two input integers and the resulting integer are stored. |

The input contains only two bounded integers, so the constant-time solution is vastly below the one-second time limit. Its memory usage is also negligible compared with the 64 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    a, b = map(int, input().split())
    print(a + b)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    finally:
        sys.stdin = old_stdin
        input = old_input

# A version of run that captures stdout correctly.
def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided samples
assert run("5 9\n") == "14\n", "sample 1"
assert run("50 -26\n") == "24\n", "sample 2"

# Custom cases
assert run("0 0\n") == "0\n", "both operands are zero"
assert run("-1000000000 -1000000000\n") == "-2000000000\n", "minimum possible sum"
assert run("1000000000 1000000000\n") == "2000000000\n", "maximum possible sum"
assert run("-1 1\n") == "0\n", "opposite values cancel exactly"
assert run("-1000000000 1000000000\n") == "0\n", "maximum magnitudes cancel"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0` | Smallest magnitude values and the zero result |
| `-1000000000 -1000000000` | `-2000000000` | Lower boundary of the possible sum |
| `1000000000 1000000000` | `2000000000` | Upper boundary of the possible sum |
| `-1 1` | `0` | Exact cancellation between opposite signs |
| `-1000000000 1000000000` | `0` | Cancellation at the largest allowed magnitudes |

The test helper temporarily replaces standard input and output so that `solve()` can be exercised exactly as it would be on Codeforces. The tests restore the original streams afterward, preventing one test from affecting another.

## Edge Cases

The mixed-sign case `50 -26` is handled by parsing both tokens as signed integers and evaluating `50 + (-26)`, which produces `24`. No branch is required to distinguish addition from subtraction because the negative sign is already part of the integer value.

For the smallest possible operands, the input `-1000000000 -1000000000` is parsed as two negative integers. The addition produces `-2000000000`, which is exactly the minimum allowed sum. Python's integer representation does not overflow at this boundary.

For the largest possible operands, `1000000000 1000000000` produces `2000000000`. The algorithm performs the same single addition as it does for small values, so there is no special upper-bound branch or off-by-one condition.

For exact cancellation, consider `-1000000000 1000000000`. The two operands have equal magnitude and opposite signs, so the addition gives `0`. This checks that the implementation preserves both signs correctly rather than treating the input values as absolute magnitudes.

Finally, `0 7` gives `7`, while `-5 0` gives `-5`. Zero does not require special handling because adding zero leaves the other operand unchanged, which is exactly what the direct integer addition operation computes.
