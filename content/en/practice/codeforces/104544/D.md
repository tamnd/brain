---
title: "CF 104544D - For A Few Dollars More"
description: "We are asked to decide how cheaply Yazan can order two dishes, one for each friend, under two constraints. The first dish has cost a and must be at least x. The second dish has cost b and is tied to the total bill: it must be at least y% of the combined cost a + b."
date: "2026-06-30T09:02:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104544
codeforces_index: "D"
codeforces_contest_name: "Aleppo Collegiate Programming Contest 2023 V.2"
rating: 0
weight: 104544
solve_time_s: 91
verified: false
draft: false
---

[CF 104544D - For A Few Dollars More](https://codeforces.com/problemset/problem/104544/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to decide how cheaply Yazan can order two dishes, one for each friend, under two constraints.

The first dish has cost `a` and must be at least `x`. The second dish has cost `b` and is tied to the total bill: it must be at least `y%` of the combined cost `a + b`.

So the structure is circular. The value of `b` depends on the total, but the total depends on `b`. The goal is to choose integers `a` and `b` satisfying both conditions while minimizing `a + b`.

The input gives multiple independent test cases, each with bounds `x` and `y`. For each test case, we must output the minimum possible total cost or `-1` if no valid pair exists.

The key difficulty is the self-referential constraint on `b`. A naive attempt would try all pairs `(a, b)` up to some bound, but there is no obvious finite upper limit on either variable. However, since both constraints only increase costs as values grow, any optimal solution will live at the smallest feasible values, which strongly suggests we should not be exploring large ranges.

A subtle edge case appears when `y = 100`. In that case, the second constraint becomes `b ≥ a + b`, which forces `0 ≥ a`, impossible because `a ≥ x ≥ 1`. So every test case with `y = 100` is immediately infeasible.

Another potential pitfall is treating the percentage constraint incorrectly as `b ≥ (y/100) * a`, which ignores that the percentage is of the total, not just the first dish.

## Approaches

A brute-force approach would try all integer pairs `(a, b)` up to some maximum bound, checking whether both constraints hold and tracking the minimum sum. While correct, this is not well-defined computationally because there is no natural upper bound on `a` and `b`, and even if we impose one like 10^5, it would be far too slow at O(N^2).

The key observation is that the second constraint can be rewritten to eliminate the circular dependency. Starting from:

`b ≥ y/100 * (a + b)`

we rearrange:

`100b ≥ y(a + b)`

`100b ≥ ya + yb`

`(100 - y)b ≥ ya`

If `y < 100`, this becomes:

`b ≥ (y * a) / (100 - y)`

So for a fixed `a`, the smallest valid `b` is determined directly. This removes the dependency cycle completely.

Now the problem becomes minimizing:

`a + b(a) = a + ceil(y * a / (100 - y))`

Since both terms grow linearly with `a`, the sum is monotonically increasing as `a` increases. Therefore, the optimal solution always uses the smallest possible `a`, which is `a = x`.

This reduces the entire problem to a direct computation, except for the special case `y = 100`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (a, b) | O(N²) or unbounded | O(1) | Too slow / Undefined |
| Formula reduction | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal method

1. Check if `y == 100`. If so, immediately output `-1`. This is because the constraint forces `b ≥ a + b`, which is impossible for any positive `a`.
2. Otherwise compute the minimal valid `a`, which is always `a = x`. Increasing `a` only increases both total cost and required `b`, so no larger choice can improve the answer.
3. Rewrite the constraint into a direct lower bound for `b`:

`b ≥ (y * a) / (100 - y)`
4. Compute the smallest integer `b` satisfying this bound using ceiling division.
5. Output `a + b`.

### Why it works

The transformation removes the dependency loop between `a`, `b`, and the total sum. For any fixed `a`, the constraint uniquely determines the smallest feasible `b`. Since both `a` and `b(a)` are non-decreasing functions of `a`, the objective function `a + b(a)` is also non-decreasing, so its minimum must occur at the smallest feasible `a`. This guarantees that restricting attention to `a = x` does not exclude any optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    
    if y == 100:
        print(-1)
        continue
    
    a = x
    numerator = y * a
    denominator = 100 - y
    
    b = (numerator + denominator - 1) // denominator
    print(a + b)
```

The code directly follows the derived formula. The only branching is the `y == 100` case, which handles the impossibility condition.

The ceiling division `(numerator + denominator - 1) // denominator` is critical; using floating-point arithmetic would risk precision errors, especially since constraints are tight and exact integer correctness is required.

## Worked Examples

### Example 1

Input:

```
x = 2, y = 40
```

We compute `a = 2`.

| Step | a | numerator = y·a | denominator | b = ceil(n/d) | total |
| --- | --- | --- | --- | --- | --- |
| init | 2 | - | - | - | - |
| compute | 2 | 80 | 60 | 2 | 4 |

Here `b = ceil(80/60) = 2`, so total cost is `4`.

This demonstrates that the second constraint binds tightly and forces `b` to be proportional to `a`.

### Example 2

Input:

```
x = 1, y = 10
```

| Step | a | numerator | denominator | b | total |
| --- | --- | --- | --- | --- | --- |
| init | 1 | - | - | - | - |
| compute | 1 | 10 | 90 | 1 | 2 |

We get `b = ceil(10/90) = 1`, total `2`.

This shows that when `y` is small, the percentage constraint is weak and both dishes can stay minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is solved with a constant number of arithmetic operations |
| Space | O(1) | Only a few integers are used |

The solution easily fits within constraints since `t ≤ 100` and each case is constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        x, y = map(int, input().split())
        if y == 100:
            out.append("-1")
            continue
        a = x
        b = (y * a + (100 - y) - 1) // (100 - y)
        out.append(str(a + b))
    return "\n".join(out)

# provided samples
assert run("5\n2 40\n4 60\n2 100\n3 50\n1 10\n") == "4\n10\n-1\n6\n2"

# custom cases
assert run("1\n1 99\n") == "100", "high percentage edge"
assert run("1\n100 1\n") == "101", "large x small y"
assert run("1\n5 100\n") == "-1", "impossible case"
assert run("1\n10 50\n") == "20", "balanced ratio"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 99` | `100` | near-impossible percentage forces large b |
| `100 1` | `101` | large base cost dominates |
| `5 100` | `-1` | infeasible constraint case |
| `10 50` | `20` | symmetric midpoint ratio |

## Edge Cases

### Case `y = 100`

Input:

```
x = 5, y = 100
```

The constraint becomes:

`b ≥ a + b`

Subtracting `b` gives `0 ≥ a`, which contradicts `a ≥ 5`. The algorithm immediately returns `-1` before any computation.

### Small `y` values

Input:

```
x = 1, y = 1
```

Here the percentage constraint is extremely weak. The algorithm computes:

`b = ceil(1 / 99) = 1`, so total is `2`. The minimal `a` choice remains optimal because increasing `a` only worsens both numerator and total.

### Large `x`

Input:

```
x = 100, y = 50
```

The algorithm fixes `a = 100`, then computes `b = ceil(5000/50) = 100`, giving total `200`. Any larger `a` would only increase both values proportionally, confirming that the boundary choice is always optimal.
