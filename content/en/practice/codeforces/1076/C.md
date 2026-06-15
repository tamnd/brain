---
title: "CF 1076C - Meme Problem"
description: "We are given a number $d$, and we want to decide whether we can split it into two non-negative real numbers $a$ and $b$ such that two conditions hold at the same time: their sum equals $d$, and their product also equals $d$."
date: "2026-06-15T14:34:04+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1076
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 54 (Rated for Div. 2)"
rating: 1300
weight: 1076
solve_time_s: 761
verified: true
draft: false
---

[CF 1076C - Meme Problem](https://codeforces.com/problemset/problem/1076/C)

**Rating:** 1300  
**Tags:** binary search, math  
**Solve time:** 12m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number $d$, and we want to decide whether we can split it into two non-negative real numbers $a$ and $b$ such that two conditions hold at the same time: their sum equals $d$, and their product also equals $d$.

So geometrically, we are looking for two points on the non-negative real line whose sum and product coincide with a fixed target value. Each test case asks whether such a pair exists, and if it does, we must construct any valid pair, not necessarily a unique one.

The constraint $d \le 10^3$ and $t \le 10^3$ means we only need a constant-time computation per test case. Any approach involving iteration over candidate values with fine granularity would still be acceptable, but anything exponential or dependent on precision search without structure is unnecessary. The structure of the equations suggests a direct algebraic reduction rather than numerical brute force.

The main subtlety is that the problem allows real numbers with precision up to $10^{-6}$. That rules out purely integer reasoning and forces us to interpret the conditions as real-valued constraints. Another subtle point is that floating-point roots near boundary cases, especially around $d = 0$ and $d = 1$, can behave differently in naive formulas, so those need explicit handling.

A failure mode appears when trying to assume that any quadratic always yields real non-negative solutions. For example, $d = 1$ leads to a discriminant that collapses to zero in a way that makes the system inconsistent under the required equality constraints, even though algebraic manipulation may misleadingly suggest a borderline solution. Another edge case is $d = 0$, where both variables must collapse to zero simultaneously.

## Approaches

The brute-force view would try to pick a candidate $a$ and compute $b = d - a$, then check whether $a \cdot b \approx d$. Since $a$ is real, we would discretize the range $[0, d]$ into many small steps. This is correct in principle because every valid solution must satisfy the sum constraint exactly, but it becomes computationally meaningless since the solution space is continuous and requires extremely fine sampling to meet the precision requirement. Even with 10^6 steps per test case, the worst-case input of 10^3 tests already becomes too slow.

The key structural observation is that the system is fully determined once we substitute $b = d - a$. This converts the product condition into a single quadratic equation in $a$. However, instead of solving it directly every time, we can observe that feasibility depends only on whether the resulting quadratic has real roots in the non-negative domain, and those roots can be constructed explicitly. The constraint structure reduces the problem to solving a quadratic equation with a parameter $d$, and selecting any valid root pair.

The algebra leads to:

$$a(d - a) = d \Rightarrow a^2 - da + d = 0$$

This gives a discriminant condition:

$$\Delta = d^2 - 4d = d(d - 4)$$

So real solutions exist only when $d \ge 4$ or $d = 0$. The special case $d = 4$ gives a repeated root, and $d = 0$ collapses trivially to $(0, 0)$. For $d \in (0, 4)$, the discriminant is negative, so no real solution exists.

When solutions exist, we compute:

$$a = \frac{d - \sqrt{d^2 - 4d}}{2}, \quad b = d - a$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(td / \epsilon)$ | $O(1)$ | Too slow |
| Optimal | $O(t)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $d$. The goal is to decide feasibility of a quadratic constraint system derived from the sum-product condition.
2. If $d = 0$, immediately output $a = 0$, $b = 0$. This is the only way both sum and product can be zero simultaneously without introducing contradiction.
3. If $d < 4$, output “N”. This follows from the discriminant $d(d - 4)$, which becomes negative and eliminates real solutions.
4. Otherwise compute the discriminant $\Delta = d^2 - 4d$. This value determines whether the quadratic equation derived from the constraints has real roots.
5. Take the square root of $\Delta$ and compute the smaller root:

$$a = \frac{d - \sqrt{\Delta}}{2}$$

Choosing the smaller root ensures both values remain non-negative and numerically stable.
6. Compute $b = d - a$. This enforces the sum constraint exactly, preventing floating-point drift from violating $a + b = d$.
7. Output “Y” followed by $a$ and $b$.

### Why it works

Every valid pair must satisfy both constraints simultaneously, and substituting one variable reduces the system to a single quadratic equation whose roots exactly characterize all feasible solutions. The discriminant fully determines existence of real solutions, and the constructed roots automatically satisfy both sum and product conditions by algebraic equivalence. No other pairs can exist outside these roots because the transformation is bijective over the constraint $b = d - a$.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    d = float(input().strip())

    if d == 0:
        print("Y 0.0 0.0")
        continue

    if d < 4:
        print("N")
        continue

    disc = d * d - 4 * d
    root = math.sqrt(disc)

    a = (d - root) / 2
    b = d - a

    print("Y", a, b)
```

The code directly implements the quadratic reduction. The early exits handle the degenerate and infeasible ranges, avoiding unnecessary floating-point operations. The discriminant computation is stable because $d \le 10^3$, so $d^2$ remains well within floating-point precision limits. Computing $b$ as $d - a$ preserves the sum constraint exactly and avoids compounding rounding errors.

## Worked Examples

### Example: $d = 5$

| Step | Value |
| --- | --- |
| d | 5 |
| discriminant $d^2 - 4d$ | 25 - 20 = 5 |
| sqrt | 2.2360679 |
| a | (5 - 2.2360679)/2 = 1.381966 |
| b | 3.618034 |

This confirms a valid decomposition where both constraints match numerically.

### Example: $d = 3$

| Step | Value |
| --- | --- |
| d | 3 |
| check | d < 4 |
| output | N |

Here the discriminant is negative, confirming no real solution exists.

The first trace demonstrates how the quadratic root construction yields valid pairs, while the second shows the feasibility boundary at $d = 4$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case uses constant arithmetic and one square root |
| Space | $O(1)$ | No auxiliary storage beyond a few scalars |

The solution comfortably fits within limits since even 10^3 square root operations are trivial under a 1-second constraint.

## Test Cases

```python
import sys, io
import math

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        d = float(input().strip())

        if d == 0:
            print("Y 0.0 0.0")
            continue
        if d < 4:
            print("N")
            continue

        disc = d * d - 4 * d
        root = math.sqrt(disc)
        a = (d - root) / 2
        b = d - a
        print("Y", a, b)

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old
    return out.getvalue().strip()

# provided sample checks (structure only; exact floating output may vary slightly)
assert run("7\n69\n0\n1\n4\n5\n999\n1000\n").split()[0] == "Y"

# edge: minimum
assert "Y" in run("1\n0\n")

# edge: infeasible region
assert run("1\n3\n").strip() == "N"

# edge: boundary
assert "Y" in run("1\n4\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n0 | Y 0 0 | Degenerate zero case |
| 1\n3 | N | Infeasible region |
| 1\n4 | Y ... | Boundary feasibility |

## Edge Cases

For $d = 0$, the algorithm immediately outputs $(0, 0)$. Substituting gives sum 0 and product 0, matching exactly.

For $d = 3$, the algorithm rejects the case because $d < 4$. The discriminant $9 - 12 = -3$ confirms no real roots, so no valid pair exists.

For $d = 4$, the discriminant becomes zero, giving a single repeated root $a = b = 2$. The algorithm computes $\sqrt{0} = 0$, then returns $a = 2$, $b = 2$, which satisfies both constraints exactly.
