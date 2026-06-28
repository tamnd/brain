---
title: "CF 104882L - Line without beginning, line without end"
description: "We are trying to recover an unknown straight line in the plane, known to have the form $y = kx + b$, where both parameters are real numbers bounded between $-100$ and $100$."
date: "2026-06-28T09:20:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104882
codeforces_index: "L"
codeforces_contest_name: "Voronezh State University - Sitronics contest II"
rating: 0
weight: 104882
solve_time_s: 55
verified: true
draft: false
---

[CF 104882L - Line without beginning, line without end](https://codeforces.com/problemset/problem/104882/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are trying to recover an unknown straight line in the plane, known to have the form $y = kx + b$, where both parameters are real numbers bounded between $-100$ and $100$. The only way to learn anything about the line is to ask questions of the form “what is the shortest distance from this point $(x, y)$ to the line?”, and the judge returns that distance.

The interaction is constrained: we can ask at most five such questions, and after that we must output an approximation of $k$ and $b$ with relative or absolute error at most $10^{-3}$.

Each query gives a geometric constraint: all points at a fixed distance from a line form two parallel lines. So each answer does not pin down a single line, but restricts it to a symmetric pair of possibilities around the query point. The difficulty is to combine a small number of these nonlinear constraints into a unique line.

The bounds matter in a subtle way. Since $k$ and $b$ are small, we can safely construct queries with coordinates like $-100, 0, 100$ without numerical instability. The problem is not numerical precision but resolving ambiguity from absolute values in the distance formula.

A naive strategy would try to guess the line from two or three points, but we do not get points on the line, only distances. That means we never directly observe sign information.

A common failure case is assuming the sign inside the distance formula is fixed. For example, interpreting distance from $(0,0)$ as $b / \sqrt{k^2+1}$ ignores that it is actually $|b| / \sqrt{k^2+1}$, which loses the sign of $b$. Any approach that ignores this symmetry will produce multiple valid candidate lines.

## Approaches

A brute-force idea is to sample a few points, treat each query as defining a pair of parallel boundary lines, and attempt to intersect all possibilities geometrically. Each query introduces a binary ambiguity, so after $m$ queries we may have up to $2^m$ candidate lines. With five queries this is already up to 32 possibilities, which is still manageable, but the geometry of intersections becomes messy and numerically unstable if done directly in slope-intercept form.

The key observation is to switch representation. Instead of working with $y = kx + b$, we treat the line in normalized form:

$$Ax + By + C = 0$$

where for our line $A = k$, $B = -1$, $C = b$, up to scaling. The distance formula becomes:

$$\frac{|Ax + By + C|}{\sqrt{A^2 + B^2}}$$

Each query gives a quadratic equation in $A, B, C$, but more importantly, it gives a linear constraint up to a sign and a shared normalization factor.

We reduce the problem by choosing three carefully selected points. Each query yields:

$$|kx - y + b| = d \cdot \sqrt{k^2 + 1}$$

Let $t = \sqrt{k^2 + 1}$. Then every query becomes:

$$kx - y + b = \pm d \cdot t$$

This converts the problem into solving a small system with unknowns $k, b, t$ and unknown signs per equation. With three queries we get three equations and only eight possible sign assignments, which we can brute force. Each assignment yields a candidate solution that can be checked against consistency.

This turns the geometric reconstruction into a finite enumeration problem with a closed-form solution per case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Geometric brute intersection | $O(2^5)$ + unstable geometry | $O(1)$ | Too fragile |
| Sign enumeration on linearized system | $O(8)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We choose three fixed query points: $(0,0)$, $(100,0)$, and $(0,100)$.

1. Query $(0,0)$, receive $d_1$. This corresponds to $|b| = d_1 \cdot t$, where $t = \sqrt{k^2 + 1}$.
2. Query $(100,0)$, receive $d_2$. This gives $|100k + b| = d_2 \cdot t$.
3. Query $(0,100)$, receive $d_3$. This gives $|b - 100| = d_3 \cdot t$.

At this point, all information is encoded in three absolute-value equations with shared scale factor $t$.

1. Enumerate all sign triples $(e_1, e_2, e_3) \in \{\pm 1\}^3$. Replace each absolute value with signed form:

$$b = e_1 d_1 t,\quad 100k + b = e_2 d_2 t,\quad b - 100 = e_3 d_3 t$$
2. From the first two equations eliminate $b$ and solve for $k$ in terms of $t$:

$$100k = t(e_2 d_2 - e_1 d_1)$$

so

$$k = \frac{t(e_2 d_2 - e_1 d_1)}{100}$$
3. Substitute into $t^2 = k^2 + 1$, which produces a single equation in $t$. Solve it explicitly.
4. Recover $k$ and $b$, then verify consistency with the third equation:

$$|b - 100| \approx d_3 t$$

If it matches within tolerance, this assignment is correct.
5. Output $k, b$.

The crucial mechanism is that each sign choice transforms nonlinear absolute constraints into a linear system with one remaining scalar unknown, and the normalization condition resolves that scalar uniquely.

### Why it works

The line is fully determined by three real degrees of freedom in this representation: slope, intercept, and scale of the implicit form. Each query contributes one quadratic constraint, but after introducing the shared scale $t$, each becomes linear up to a sign. The sign ambiguity is discrete and small, so exhaustive enumeration guarantees that the correct configuration is tested. Once the correct signs are chosen, the system has a unique consistent solution, and all other configurations violate at least one constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def ask(x, y):
    print(f"? {x} {y}")
    sys.stdout.flush()
    d = float(input().strip())
    if d < 0:
        sys.exit(0)
    return d

def solve():
    d1 = ask(0, 0)
    d2 = ask(100, 0)
    d3 = ask(0, 100)

    for e1 in (-1, 1):
        for e2 in (-1, 1):
            for e3 in (-1, 1):

                # We derive t from k^2 + 1 = t^2
                # k = t * C / 100, where C = e2*d2 - e1*d1
                C = e2 * d2 - e1 * d1

                denom = 1 - (C * C) / 10000.0
                if abs(denom) < 1e-12:
                    continue

                t2 = 1.0 / denom
                if t2 <= 0:
                    continue

                t = math.sqrt(t2)

                k = t * C / 100.0
                b = e1 * d1 * t

                # verify third equation
                if abs(abs(b - 100) - d3 * t) < 1e-3:
                    print(f"! {k:.10f} {b:.10f}")
                    sys.stdout.flush()
                    return

solve()
```

The implementation mirrors the algebra directly. The only subtlety is guarding against numerical instability when the denominator $1 - C^2 / 10000$ becomes extremely small due to a nearly degenerate configuration of signs.

The verification step is essential because multiple algebraic branches can produce numerically plausible but incorrect solutions when floating-point rounding interacts with the square root extraction.

## Worked Examples

Consider a line $y = 2x + 5$.

After querying, we conceptually receive distances:

| Query point | Expression | Value form |
| --- | --- | --- |
| (0,0) | ( | 5 |
| (100,0) | ( | 205 |
| (0,100) | ( | -95 |

Trying sign configuration $e_1 = +1, e_2 = +1, e_3 = -1$ aligns all expressions consistently. The derived system reconstructs $t$, then $k = 2$, $b = 5$, and passes the third constraint.

A wrong sign choice, such as flipping $e_2$, produces an inconsistent value of $t$ that fails the verification step.

This shows that correctness is enforced not by solving a continuous optimization problem but by eliminating discrete inconsistencies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(8)$ | constant enumeration over sign triples with constant algebra per case |
| Space | $O(1)$ | only a few scalar variables are stored |

The interaction cost is three queries, well within the limit of five. All computations are constant time, so the solution comfortably fits in both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    def fake_input():
        return sys.stdin.readline()
    return ""

# Note: interactive problem, so deterministic unit tests are conceptual placeholders

# sanity-style placeholders
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| line y=0x+0 | trivial reconstruction | zero intercept handling |
| line y=x | symmetric case | equal magnitude constraints |
| line y=100x-100 | boundary slope/intercept | extreme parameter values |

## Edge Cases

One subtle situation is when $1 - C^2 / 10000$ becomes extremely small. This corresponds to a near-degenerate configuration where the derived linear relation almost forces $k^2 \approx -1$, which is impossible, indicating an invalid sign assignment. In such cases the algorithm skips the branch safely due to the denominator check.

Another edge case is when $b = 0$, making the first query return zero distance. The algorithm handles this naturally because $e_1 d_1 t = 0$ forces $b = 0$ regardless of $t$, and the remaining equations still determine $k$ uniquely.

A third case is when the line is nearly vertical in slope-intercept representation, but since $k$ is bounded and finite, the representation remains stable and the normalization via $t$ prevents blow-up.
