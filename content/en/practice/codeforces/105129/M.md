---
title: "CF 105129M - Problem Validator"
description: "The system we are validating is extremely simple: for each test case, we are told how many tests a program was supposed to run and how many of them it actually passed. From this, we decide whether the program fully succeeded or not."
date: "2026-06-27T19:23:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "M"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 43
verified: true
draft: false
---

[CF 105129M - Problem Validator](https://codeforces.com/problemset/problem/105129/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The system we are validating is extremely simple: for each test case, we are told how many tests a program was supposed to run and how many of them it actually passed. From this, we decide whether the program fully succeeded or not.

Each input test case describes a single submission. The first number is the total number of test cases that exist for that submission. The second number is how many of those test cases the submission passed successfully. The required decision is binary. If every single test case was passed, we declare the submission fully correct and output AC. If even one test case was not passed, we output WA.

The constraints are small, with the number of test cases per query bounded by at most 100. This means even the most straightforward per-test-case processing is trivial in terms of computational cost. There is no need for precomputation, data structures, or optimization tricks because the input size per check is constant-bounded and the operation per check is constant-time comparison.

Edge cases are mainly about boundary equality. The most important situation is when the number of passed tests equals the total number of tests, including the smallest possible case where both are 1. For example, an input like `1 1` must output AC. A slightly different input like `1 0` must output WA because at least one test failed. A common mistake in naive implementations is accidentally checking whether `m > 0` instead of `m == n`, which would incorrectly accept cases like `3 2`.

Another subtle issue is forgetting that passing all tests means exact equality, not “close to full coverage.” Inputs like `100 99` should still produce WA even though the success rate is high.

## Approaches

The brute-force interpretation of the problem would simulate checking each test case individually. One could imagine iterating over all n tests and verifying whether each one was marked as passed. However, this is unnecessary because the input already provides aggregated information: the number of successful tests m.

In a direct simulation, we would conceptually reconstruct an array of size n and mark m of them as passed, then verify whether any failure exists. That would cost O(n) per test case. While n is at most 100, this approach is logically redundant because we never need to inspect individual test results.

The key observation is that the entire problem reduces to a single equality check. If the number of successful tests equals the total number of tests, there are no failures. Otherwise, at least one failure exists. This collapses the problem from iteration over a structure to a single comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T · n) | O(1) | Accepted but unnecessary |
| Optimal | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

We process each submission independently and decide its verdict using a direct comparison.

1. Read the number of test cases T. This determines how many submissions we will evaluate.
2. For each submission, read two integers n and m. The first is the total number of tests, and the second is the number of tests that passed. These two values fully determine correctness, so no additional data is needed.
3. Compare m with n. If they are equal, it means every test was successful. Otherwise, at least one test failed.
4. Output "AC" if m equals n, otherwise output "WA".

The logic is intentionally minimal because the input already encodes the full evaluation result.

### Why it works

For each submission, the set of failed tests has size n − m. The submission is accepted only when this quantity is zero. Since n − m = 0 is equivalent to m = n, equality fully characterizes correctness. There is no hidden structure or dependency between test cases, so this condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        if n == m:
            out.append("AC")
        else:
            out.append("WA")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases once and stores results in a list to avoid repeated I/O overhead. The core decision is the equality check `n == m`, which directly encodes whether any test case failed. There are no edge conditions beyond ensuring correct parsing of input lines.

## Worked Examples

### Example 1

Input:

```
3
3 3
3 2
1 1
```

| Step | n | m | Condition (n == m) | Output |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | True | AC |
| 2 | 3 | 2 | False | WA |
| 3 | 1 | 1 | True | AC |

The first and third submissions pass all tests exactly, while the second has one missing test, immediately triggering a WA.

### Example 2

Input:

```
4
2 1
5 5
10 9
1 0
```

| Step | n | m | Condition (n == m) | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | False | WA |
| 2 | 5 | 5 | True | AC |
| 3 | 10 | 9 | False | WA |
| 4 | 1 | 0 | False | WA |

This example highlights that even a single missing test among many is sufficient to reject the submission, and that the smallest non-zero failure case behaves identically to larger ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case is handled with a single integer comparison |
| Space | O(1) | Only constant storage aside from output buffer |

The constraints guarantee that T is small enough that a single linear pass is instantaneous. Each operation is constant-time arithmetic and comparison, so the solution is well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        out.append("AC" if n == m else "WA")
    return "\n".join(out)

# provided sample
assert run("3\n3 3\n3 2\n1 1\n") == "AC\nWA\nAC"

# minimum size, failure
assert run("1\n1 0\n") == "WA"

# minimum size, success
assert run("1\n1 1\n") == "AC"

# partial success
assert run("1\n100 99\n") == "WA"

# all equal large
assert run("1\n100 100\n") == "AC"

# mixed cases
assert run("3\n2 2\n2 1\n3 0\n") == "AC\nWA\nWA"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | WA | minimum failing case |
| 1 1 | AC | minimum passing case |
| 100 99 | WA | near-complete failure |
| 100 100 | AC | full success at upper bound |
| mixed small set | AC/WA/WA | consistency across multiple cases |

## Edge Cases

The smallest meaningful case is `n = 1`. For input `1 1`, the algorithm compares equality and outputs AC immediately, since m equals n. For `1 0`, the condition fails and WA is produced. This confirms correct handling of boundary values without any special casing.

For near-boundary cases such as `100 99`, the comparison still correctly identifies that at least one test failed. The computation does not depend on magnitude, only equality, so large values behave identically to small ones.
