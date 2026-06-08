---
title: "CF 2009A - Minimize!"
description: "We are given multiple independent queries. Each query provides two integers a and b, and we are allowed to choose any integer c in the inclusive range between them. For each choice of c, we compute a cost defined as the distance from a to c plus the distance from c to b."
date: "2026-06-08T13:16:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 2009
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 971 (Div. 4)"
rating: 800
weight: 2009
solve_time_s: 65
verified: true
draft: false
---

[CF 2009A - Minimize!](https://codeforces.com/problemset/problem/2009/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent queries. Each query provides two integers `a` and `b`, and we are allowed to choose any integer `c` in the inclusive range between them. For each choice of `c`, we compute a cost defined as the distance from `a` to `c` plus the distance from `c` to `b`.

Geometrically, this is like placing a point `c` somewhere on a number line between `a` and `b`, and measuring how far we travel from `a` to `b` via `c`. The task is to choose `c` so that this total travel cost is minimized, and output that minimum value.

The constraints are extremely small: both `a` and `b` are at most 10, so even a brute force check of all possible `c` values would be trivial. However, recognizing structure matters more than computation here.

A subtle pitfall in naive reasoning is to assume the best `c` depends on its position or requires searching. Another is to try to “optimize” by testing midpoints or special values. Because the expression hides cancellation, such heuristics can overcomplicate something that is actually constant.

## Approaches

A brute-force solution would iterate over every possible `c` between `a` and `b`, compute `(c - a) + (b - c)`, and take the minimum. This works because the range is tiny, but it obscures the key observation.

Expanding the expression reveals its structure:

`(c - a) + (b - c) = c - a + b - c = b - a`

The variable `c` disappears completely. This means every valid choice of `c` produces exactly the same value. There is no optimization to perform, because the cost does not depend on the decision.

The brute-force works because it evaluates redundant cases, but it fails to reveal that all cases are identical. The observation that the middle term cancels allows us to reduce the problem to a direct subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(b - a + 1) | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

The optimal solution follows directly from simplifying the formula.

1. Read integers `a` and `b` for each test case. These define the endpoints of the segment.
2. Compute the difference `b - a`. This represents the total distance between endpoints.
3. Output this value immediately. No dependence on `c` remains after simplification.

The key idea is that every possible choice of `c` induces the same algebraic cancellation, so there is no decision-making step beyond reading input.

### Why it works

The expression `(c - a) + (b - c)` always simplifies to `b - a` because the `+c` and `-c` terms cancel exactly. Since this identity holds for all integers `c`, the minimum over all valid `c` is also `b - a`, and no alternative configuration can improve or worsen the result.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(b - a)
```

The implementation mirrors the derivation directly. Each test case is independent, so we process them in a loop. The subtraction `b - a` is the fully simplified form of the objective function, so no search or branching is needed. There are no edge cases beyond the trivial case where `a == b`, which correctly produces zero.

## Worked Examples

### Example 1

Input:

```
a = 1, b = 2
```

| c | (c - a) | (b - c) | total |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 1 |

The table shows that every valid choice produces the same value, confirming that the answer is fixed at 1, which matches `b - a`.

### Example 2

Input:

```
a = 3, b = 10
```

| c | (c - a) | (b - c) | total |
| --- | --- | --- | --- |
| 3 | 0 | 7 | 7 |
| 6 | 3 | 4 | 7 |
| 10 | 7 | 0 | 7 |

Again, every possible `c` yields the same result, confirming the direct formula `10 - 3 = 7`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One constant-time computation per test case |
| Space | O(1) | No auxiliary storage beyond input variables |

The solution easily fits within limits since it performs only a single subtraction per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        a, b = map(int, input().split())
        out.append(str(b - a))
    return "\n".join(out)

# provided samples
assert run("""3
1 2
3 10
5 5
""") == """1
7
0"""

# custom cases
assert run("""1
1 1
""") == "0", "single point"

assert run("""2
2 3
4 4
""") == """1
0""", "mixed small ranges"

assert run("""2
1 10
10 10
""") == """9
0""", "boundary ranges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | zero-length interval |
| 2 3, 4 4 | 1, 0 | mixed small and degenerate cases |
| 1 10, 10 10 | 9, 0 | typical and boundary behavior |

## Edge Cases

The only non-obvious edge case is when `a == b`. In that case, the range of `c` collapses to a single value, and the expression evaluates to zero. The formula `b - a` naturally handles this because it becomes `0`, matching the correct result without any special branching.
