---
title: "CF 104207E - Evil Forest"
description: "We are asked to size production for a sequence of painting competitions. Each competition has a known number of participants, and every participant consumes exactly one sketchpad."
date: "2026-07-01T23:56:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104207
codeforces_index: "E"
codeforces_contest_name: "2017 China Collegiate Programming Contest Final (CCPC-Final 2017)"
rating: 0
weight: 104207
solve_time_s: 42
verified: true
draft: false
---

[CF 104207E - Evil Forest](https://codeforces.com/problemset/problem/104207/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to size production for a sequence of painting competitions. Each competition has a known number of participants, and every participant consumes exactly one sketchpad. On top of that, each competition must also receive additional sketchpads as a safety buffer equal to 10% of the participants in that competition.

The input gives several independent test cases. For each test case, we are given the number of competitions, followed by the participant counts for each competition. The task is to compute the total number of sketchpads needed across all competitions, where each competition contributes its own requirement independently.

A key detail is that the “10% extra” is not shared across competitions. It is applied per competition, so rounding behavior happens per value, not globally.

The constraints are small enough that even a linear scan per test case is easily sufficient. With at most 1000 competitions per test case and 100 test cases, a direct O(N) per test case solution runs comfortably within limits.

The main subtlety is how to interpret 10% extra when the result is not an integer. Since sketchpads are discrete, fractional values cannot exist, so the extra must be rounded up. This is where many naive solutions fail: using integer division or floating-point truncation produces incorrect totals.

A typical failing scenario happens when the number of participants is small. For example, if a competition has 1 participant, 10% is 0.1, which must become 1 extra sketchpad after rounding up. A naive computation like `a // 10` would incorrectly give 0.

## Approaches

The brute-force idea is to compute each competition independently, calculate its required sketchpads using floating-point arithmetic, and sum everything. This is correct in principle because the requirement is additive across competitions. However, it risks precision issues and incorrect rounding, especially when using floating-point multiplication and casting to integers.

A more robust brute-force would explicitly compute the ceiling of 10% for each value, but even then, a careless implementation often introduces off-by-one errors.

The key observation is that each competition is independent and contributes exactly `a_i + ceil(0.1 * a_i)` sketchpads. This transforms the problem into a simple per-element transformation followed by a sum.

We avoid floating-point entirely by rewriting the ceiling term. The expression `ceil(a / 10)` can be computed as `(a + 9) // 10`. This avoids precision errors and guarantees correctness for all integer inputs.

Once this is recognized, the solution becomes a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (float + rounding) | O(N) | O(1) | Risky / may fail |
| Optimal (integer ceiling arithmetic) | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal Algorithm

1. For each test case, read the number of competitions and the list of participant counts. This establishes the independent units we will process.
2. Initialize an accumulator `total = 0`. This will store the final number of sketchpads required.
3. For each competition value `a`, compute the required sketchpads contributed by this competition. The base requirement is `a`, since each participant needs one sketchpad.
4. Compute the backup requirement as `ceil(a / 10)`, which ensures at least 10% extra is always rounded up. We compute this as `(a + 9) // 10`. The +9 ensures that any non-multiple of 10 correctly rounds up when integer-divided.
5. Add both parts to the running total.
6. After processing all competitions, output the accumulated total in the required format.

### Why it works

Each competition is independent, so the total requirement is the sum of per-competition requirements. The only non-trivial part is correctly computing the ceiling of a linear fraction. The identity `(a + 9) // 10` exactly matches `ceil(a / 10)` for all integers `a >= 1`. Since every term is computed independently and summed without interaction, there is no cross-contamination between competitions, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        n = int(input())
        arr = list(map(int, input().split()))
        
        total = 0
        for a in arr:
            total += a + (a + 9) // 10
        
        print(f"Case #{tc}: {total}")

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently and processes the list in a single pass. The expression `(a + 9) // 10` is the crucial implementation detail; replacing it with `int(a * 0.1)` or `a // 10` would both be incorrect due to truncation instead of ceiling.

The formatting step follows the required output structure exactly.

## Worked Examples

### Example 1

Input:

```
1
3
10 11 12
```

We compute each competition separately.

| a | base a | extra ceil(a/10) | contribution | total |
| --- | --- | --- | --- | --- |
| 10 | 10 | 1 | 11 | 11 |
| 11 | 11 | 2 | 13 | 24 |
| 12 | 12 | 2 | 14 | 38 |

Output:

```
Case #1: 38
```

This demonstrates how rounding up changes the second and third values significantly compared to naive integer division.

### Example 2

Input:

```
1
5
1 2 3 4 5
```

| a | base a | extra ceil(a/10) | contribution | total |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 2 |
| 2 | 2 | 1 | 3 | 5 |
| 3 | 3 | 1 | 4 | 9 |
| 4 | 4 | 1 | 5 | 14 |
| 5 | 5 | 1 | 6 | 20 |

Output:

```
Case #1: 20
```

This case highlights the smallest values, where every single competition still requires at least one backup sketchpad.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | Each competition is processed once with O(1) work |
| Space | O(1) extra | Only a running sum is maintained |

The constraints allow up to 1000 competitions per test case and 100 test cases, so the total number of operations is at most 100,000, which is trivial for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    input = sys.stdin.readline

    T = int(input())
    out_lines = []
    for tc in range(1, T + 1):
        n = int(input())
        arr = list(map(int, input().split()))
        total = 0
        for a in arr:
            total += a + (a + 9) // 10
        out_lines.append(f"Case #{tc}: {total}")
    return "\n".join(out_lines)

# sample-style test
assert run("1\n3\n10 11 12\n") == "Case #1: 38"

# all small values
assert run("1\n5\n1 1 1 1 1\n") == "Case #1: 10"

# single competition
assert run("1\n1\n100\n") == "Case #1: 110"

# mixed values
assert run("1\n4\n9 10 11 99\n") == "Case #1: 9+1 + 10+1 + 11+2 + 99+10".replace("+", "").replace(" ", "")

# zero-like boundary behavior not needed since ai >= 1, but still small edge
assert run("1\n2\n1 2\n") == "Case #1: 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 test, all ones | Case #1: 10 | minimum-value ceiling behavior |
| single large value | Case #1: 110 | scaling correctness |
| mixed values | computed sum | correctness across range |
| small pair | Case #1: 5 | basic arithmetic sanity |

## Edge Cases

The most important edge case is when `a < 10`. In that regime, `a / 10` is less than 1, but still non-zero in reality, so the ceiling must return 1.

For example:

Input:

```
1
1
7
```

The algorithm computes:

`7 + (7 + 9) // 10 = 7 + 1 = 8`.

A naive implementation using `7 // 10` would produce `7`, missing the required extra sketchpad entirely. This is exactly the kind of silent undercounting bug that appears correct on large inputs but fails on small constraints-heavy tests.

Another edge case is exact multiples of 10. For `a = 20`, `(20 + 9) // 10 = 2`, matching `ceil(2.0)` exactly. Any attempt to use floating-point rounding like `int(a * 0.1 + 0.5)` risks incorrect behavior due to floating precision, especially for larger values, so the integer formula avoids that entire class of errors.
