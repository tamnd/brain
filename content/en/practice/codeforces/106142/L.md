---
title: "CF 106142L - \u0422\u0440\u0435\u0442\u044c\u044f \u0441\u0442\u043e\u0440\u043e\u043d\u0430"
description: "We are given two fixed side lengths of a triangle, $a$ and $b$, and we want to understand what integer values a third side $c$ can take so that the three segments form a valid triangle with positive area."
date: "2026-06-19T19:32:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106142
codeforces_index: "L"
codeforces_contest_name: "2025-2026 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 25, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 106142
solve_time_s: 47
verified: true
draft: false
---

[CF 106142L - \u0422\u0440\u0435\u0442\u044c\u044f \u0441\u0442\u043e\u0440\u043e\u043d\u0430](https://codeforces.com/problemset/problem/106142/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two fixed side lengths of a triangle, $a$ and $b$, and we want to understand what integer values a third side $c$ can take so that the three segments form a valid triangle with positive area.

A triangle has positive area exactly when it is non-degenerate, meaning all triangle inequalities are strict. So the third side must satisfy two conditions simultaneously: it must be short enough to fit with the other two sides, and it must also be long enough so that the triangle does not collapse into a straight line.

Concretely, for sides $a$, $b$, and $c$, validity requires:

$a + b > c$, $a + c > b$, and $b + c > a$.

The task is to find the smallest and largest integer $c$ that satisfy these conditions.

The constraints go up to $10^6$, which means any solution must run in constant time per test case. A solution that iterates over all possible values of $c$ up to the sum of sides would be far too slow in the worst case. The structure of the constraints suggests a direct algebraic characterization rather than enumeration.

A common subtle failure case is when one side is very large compared to the other. For example, if $a = 1$ and $b = 10$, then many naive implementations incorrectly assume any $c$ between $1$ and $11$ works, but they forget the strictness of inequalities and the lower bound imposed by the triangle condition $c > |a - b|$.

## Approaches

A brute-force approach would try every integer $c$ from 1 up to $a + b - 1$, checking whether $a, b, c$ form a valid triangle. Each check is constant time, so the complexity becomes $O(a + b)$, which in the worst case is about $2 \cdot 10^6$. While this might pass in some environments, it is unnecessary and fragile, especially since the logic inside the loop is just verifying inequalities that can be simplified.

The key observation is that triangle validity constraints collapse into a tight interval for $c$. From the triangle inequalities:

$c < a + b$,

$c > a - b$,

$c > b - a$.

The last two combine into $c > |a - b|$. Since $c$ is an integer, this becomes $c \ge |a - b| + 1$. Similarly, the strict upper bound becomes $c \le a + b - 1$.

So the valid range is a continuous integer segment:

$$|a - b| + 1 \le c \le a + b - 1$$

This turns the problem into simply computing endpoints of an interval rather than searching.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(a + b)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compute the valid range of the third side directly from triangle inequalities.

1. Compute the lower bound of $c$ as $|a - b| + 1$. This ensures the triangle is not degenerate and satisfies both $a + c > b$ and $b + c > a$. The absolute difference captures the stronger of the two lower constraints.
2. Compute the upper bound of $c$ as $a + b - 1$. This enforces strict positivity of area by ensuring $c < a + b$.
3. Output the two values as the answer.

### Why it works

The triangle inequality system defines a convex set of feasible values for $c$. Because all constraints are linear in $c$, their intersection is a single continuous interval. The lower bound comes from ensuring $c$ is larger than both differences $a - b$ and $b - a$, while the upper bound comes from the sum constraint. Since integer values are required, the continuous interval translates into an integer segment with endpoints adjusted by ±1 due to strict inequalities. No gaps or disjoint regions exist, so the endpoints fully describe the solution set.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
b = int(input())

low = abs(a - b) + 1
high = a + b - 1

print(low, high)
```

The solution reads two integers and directly computes the valid interval. The only subtle point is respecting strict inequalities: the upper bound is reduced by one, and the lower bound is increased beyond the absolute difference. Both adjustments are necessary because equality would produce a degenerate triangle.

No loops are needed, and no additional data structures are required.

## Worked Examples

### Example 1

Input:

```
6
14
```

We compute:

| Step | a | b | low = |a-b|+1 | high = a+b-1 |

|------|---|---|------------------|----------------|

| Init | 6 | 14 | 9 | 19 |

| Result | - | - | 9 | 19 |

So valid $c$ values are from 9 to 19.

This confirms that when one side is significantly larger, the lower bound dominates, preventing degenerate skinny configurations.

### Example 2

Input:

```
1000000
1000000
```

| Step | a | b | low | high |
| --- | --- | --- | --- | --- |
| Init | 1e6 | 1e6 | 1 | 1999999 |

So $c \in [1, 1999999]$.

This shows that when sides are equal, the lower bound becomes minimal, and the constraint is almost entirely governed by the sum condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations are performed regardless of input size |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution is optimal for the constraints since any iteration over possible third sides would be unnecessary work, while the final answer depends only on simple algebraic transformations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    a = int(input())
    b = int(input())

    low = abs(a - b) + 1
    high = a + b - 1

    return f"{low} {high}"

# provided sample
assert run("6\n14\n") == "9 19"

# equal sides
assert run("5\n5\n") == "1 9"

# minimal case
assert run("1\n1\n") == "1 1"

# highly unbalanced
assert run("1\n10\n") == "10 10"

# large values
assert run("1000000\n999999\n") == "2 1999998"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 | 1 9 | symmetric case |
| 1 1 | 1 1 | smallest bounds |
| 1 10 | 10 10 | tight lower bound case |
| 1000000 999999 | 2 1999998 | large boundary correctness |

## Edge Cases

One important edge case is when the two given sides are equal. For example, $a = b = 5$. The algorithm computes $low = |5 - 5| + 1 = 1$ and $high = 9$. This correctly allows all valid triangle third sides from 1 to 9. The key point is that the lower bound does not collapse to zero; the strict inequality forces at least 1.

Another edge case is when one side is much larger than the other, such as $a = 1$, $b = 10$. The computation yields $low = 10$, $high = 10$, meaning only one valid triangle exists. Tracing inequalities confirms this: $c$ must be greater than $9$ and less than $11$, leaving only $10$.

Finally, when both values are large and close, the interval becomes wide. For $a = 10^6$, $b = 10^6$, we get a near full range from 1 to almost $2 \cdot 10^6$, showing that the constraint is dominated by the sum condition rather than the difference.
