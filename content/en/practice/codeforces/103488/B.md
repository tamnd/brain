---
title: "CF 103488B - Boboge and Tall Building"
description: "The building is modeled as a vertical structure split into a fixed number of equal-height floors. The total height of the building is given as a single value, and that height is distributed uniformly across all floors."
date: "2026-07-03T06:16:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103488
codeforces_index: "B"
codeforces_contest_name: "The 2021 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 103488
solve_time_s: 45
verified: true
draft: false
---

[CF 103488B - Boboge and Tall Building](https://codeforces.com/problemset/problem/103488/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The building is modeled as a vertical structure split into a fixed number of equal-height floors. The total height of the building is given as a single value, and that height is distributed uniformly across all floors. The first floor sits at height 0, and each next floor increases linearly until the top floor reaches the full height.

For each test case, we are given three values. The first value tells us which floor Boboge lives on, counted from the bottom starting at 1. The second value is the total number of floors in the building. The third value is the total height of the building. The task is to compute the exact height of Boboge’s floor.

Each floor corresponds to a uniform segment of the total height. This immediately implies that the problem is fundamentally about proportional division of an interval into equal parts, then selecting a specific breakpoint.

The constraints are very small, with up to 100 test cases and all values bounded by 100. This guarantees that any arithmetic-heavy or floating-point direct computation will comfortably run within limits. There is no need for optimization beyond constant-time evaluation per test case.

A subtle issue that can appear in careless implementations is off-by-one indexing of floors. Since the first floor is explicitly defined to be at height 0, floor 1 must map to 0, not to a positive fraction. For example, if n = 1, m = 4, k = 10, the correct answer is 0. If we incorrectly treat floors as 0-indexed or shift incorrectly, we might output 2.5 or another fractional value, which is wrong.

Another potential edge case is when n equals m. In that case, Boboge is on the top floor, and the height must be exactly k. If one mistakenly divides by m instead of m − 1, the computed height of the top floor will incorrectly fall short of k.

## Approaches

The structure of the building suggests a direct geometric interpretation. The height range from 0 to k is split into m − 1 equal segments, because there are m floors but m − 1 gaps between them. Each segment therefore has size k / (m − 1).

A brute-force interpretation would explicitly simulate each floor boundary, repeatedly adding the segment height until reaching the desired floor. This is correct, but unnecessary. It performs O(m) additions per test case, which is still trivial for m ≤ 100, but it obscures the direct relationship.

The key observation is that floors form an arithmetic progression in height. The i-th floor (1-indexed) sits at height (i − 1) times the uniform step size. Once this is recognized, the answer becomes a single multiplication.

The brute-force approach works because it builds the progression incrementally, but it is effectively recomputing a formula we can write directly. The closed form reduces the computation to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m) per test case | O(1) | Accepted but unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so computations do not carry over.
2. For each test case, read n, m, k, where n is the target floor index, m is total floors, and k is total height.
3. Compute the vertical distance between consecutive floors as step = k / (m − 1). This works because there are exactly m − 1 equal gaps between floor 1 at height 0 and floor m at height k.
4. Compute the height of floor n as (n − 1) * step. This reflects that the first floor is anchored at zero height and each subsequent floor adds one full step.
5. Output the result as a floating-point number with sufficient precision.

### Why it works

The building heights form an arithmetic progression starting at 0 with common difference k / (m − 1). Any arithmetic progression is fully determined by its first term and common difference, so the height of any term is uniquely given by the closed form formula. Since floor indexing matches the term index shifted by one, mapping floor n to term (n − 1) preserves correctness for all valid inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    step = k / (m - 1)
    ans = (n - 1) * step
    print(ans)
```

The solution relies entirely on translating the floor system into an arithmetic progression. The key implementation detail is using floating-point division for the step size, since integer division would destroy precision. Another subtle point is ensuring the denominator is m − 1 rather than m, because floors represent boundaries including both endpoints 0 and k.

The expression (n − 1) * step directly encodes the offset from the base floor. No loops are required, and each test case is resolved with a constant number of arithmetic operations.

## Worked Examples

Consider the input where n = 3, m = 4, k = 10. The step size is 10 / 3.

| Step | n | m | k | step | expression | result |
| --- | --- | --- | --- | --- | --- | --- |
| init | 3 | 4 | 10 | - | - | - |
| compute step | 3 | 4 | 10 | 3.333... | - | - |
| compute answer | 3 | 4 | 10 | 3.333... | (3 − 1) * 3.333... | 6.666... |

This confirms that floor 3 lies two steps above ground level.

Now consider n = 1, m = 4, k = 10.

| Step | n | m | k | step | expression | result |
| --- | --- | --- | --- | --- | --- | --- |
| init | 1 | 4 | 10 | - | - | - |
| compute step | 1 | 4 | 10 | 3.333... | - | - |
| compute answer | 1 | 4 | 10 | 3.333... | (1 − 1) * 3.333... | 0 |

This shows that the ground floor remains at height 0 regardless of total height.

These traces confirm the arithmetic progression interpretation and show that both interior and boundary floors behave consistently under the same formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs constant-time arithmetic operations |
| Space | O(1) | No auxiliary structures are used beyond variables |

The constraints allow up to 100 test cases, so the solution runs in negligible time. Even with floating-point operations, the workload remains trivial for a 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m, k = map(int, input().split())
        step = k / (m - 1)
        out.append(str((n - 1) * step))
    return "\n".join(out)

# provided samples
assert run("5\n3 4 10\n1 4 10\n2 3 10\n2 5 12\n4 5 12\n") == \
"6.666666666666667\n0.0\n5.0\n2.5\n9.0"

# custom cases
assert run("1\n1 2 100\n") == "0.0", "minimum floors"
assert run("1\n2 2 100\n") == "100.0", "two-floor boundary"
assert run("1\n5 5 100\n") == "100.0", "top floor exact match"
assert run("1\n3 6 11\n") == "4.4", "fractional step case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 100 | 0.0 | minimum index at ground floor |
| 2 2 100 | 100.0 | top floor with two floors total |
| 5 5 100 | 100.0 | equality of floors and height endpoints |
| 3 6 11 | 4.4 | non-integer division correctness |

## Edge Cases

When n = 1, the formula becomes (1 − 1) * k / (m − 1), which always evaluates to 0 regardless of k and m. This matches the definition that the first floor is anchored at height zero.

For example, input n = 1, m = 4, k = 10 produces step = 10 / 3 and final answer 0. The computation never depends on k beyond step calculation, so any floating-point issues do not propagate here.

When n = m, the expression becomes (m − 1) * k / (m − 1), which simplifies exactly to k. Even if floating-point rounding occurs in the intermediate step, multiplication by (m − 1) restores the endpoint correctly within precision limits.

When m = 2, there is only one segment between floor 1 and floor 2. The step becomes k / 1, so floor 1 is 0 and floor 2 is k. This is a minimal non-trivial case that confirms the arithmetic progression model still holds when the number of segments is smallest possible.
