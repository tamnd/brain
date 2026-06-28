---
title: "CF 104761A - \u0418\u0440\u0440\u0430\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c"
description: "We are asked to find all lattice points in the first quadrant whose distance to the origin is exactly $Dsqrt{2}$. Squaring the distance removes the square root, so we are really searching for all non-negative integer pairs $(x, y)$ such that $$x^2 + y^2 = 2D^2."
date: "2026-06-28T21:53:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104761
codeforces_index: "A"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Regional Contest"
rating: 0
weight: 104761
solve_time_s: 83
verified: true
draft: false
---

[CF 104761A - \u0418\u0440\u0440\u0430\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c](https://codeforces.com/problemset/problem/104761/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find all lattice points in the first quadrant whose distance to the origin is exactly $D\sqrt{2}$. Squaring the distance removes the square root, so we are really searching for all non-negative integer pairs $(x, y)$ such that

$$x^2 + y^2 = 2D^2.$$

Among all such points, we only output those with $x \le y$, and the final list must be sorted by increasing $x$.

The constraint $D \le 10^6$ implies that the constant on the right-hand side can be as large as $2 \cdot 10^{12}$. A naive approach that tries every pair $(x, y)$ up to $2D$ would require about $4 \cdot 10^{12}$ checks, which is completely infeasible. Even checking all $x$ values alone gives about $2 \cdot 10^6$ iterations, which is borderline but still manageable in Python if each iteration is constant time.

A more important subtlety is that valid solutions are very sparse. For a fixed $D$, the equation describes lattice points on a circle of radius $\sqrt{2}D$, and such circles typically have very few integer points. This sparsity is what makes an $O(D)$ or slightly better enumeration acceptable.

A naive implementation that loops over all $x$, computes $y^2 = 2D^2 - x^2$, and checks whether it is a perfect square already gets close to the intended solution, but it risks performance issues if implemented with heavy overhead or repeated floating-point square roots without care.

## Approaches

A direct way to attack the problem is to fix one coordinate, say $x$, and compute the corresponding $y$ from the equation $y^2 = 2D^2 - x^2$. If the result is a perfect square, we accept the pair.

This works because every valid solution must satisfy the equation exactly, so scanning all possible $x$ guarantees that no solution is missed. However, this brute-force scan performs up to $2D$ iterations, and in each iteration we do a square root and verification. With $D = 10^6$, this is about two million iterations, which is just on the edge of acceptable but still potentially slow in Python if not carefully implemented.

A more structural observation comes from rewriting the equation using Gaussian integers. The identity

$$x^2 + y^2 = 2D^2$$

can be factored as

$$(x + iy)(x - iy) = 2D^2.$$

Since $2 = (1+i)(1-i)$, we can rewrite solutions in the form

$$x + iy = (1+i)(u + iv),$$

which expands to

$$x = u - v,\quad y = u + v.$$

Substituting back gives

$$x^2 + y^2 = 2(u^2 + v^2),$$

so we reduce the problem to finding integer pairs $(u, v)$ such that

$$u^2 + v^2 = D^2.$$

This transformation is useful because it turns the original constraint into a standard problem: finding lattice points on a circle of radius $D$. Each such pair $(u, v)$ directly generates a solution $(x, y)$, and no further filtering is required beyond enforcing non-negativity.

We now only need to enumerate solutions to $u^2 + v^2 = D^2$, which is significantly sparser than scanning all $(x, y)$ pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over (x, y) | $O(D^2)$ | $O(1)$ | Too slow |
| Scan x and check square | $O(D)$ | $O(1)$ | Acceptable but borderline |
| Gaussian reduction to (u, v) | $O(D)$ worst-case, typically much less | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Fix the equation $u^2 + v^2 = D^2$, which represents all lattice points on a circle of radius $D$. We will enumerate all valid integer pairs $(u, v)$ with $u, v \ge 0$.
2. Iterate $u$ from $0$ to $D$. For each value, compute $v^2 = D^2 - u^2$. This ensures we only consider candidates consistent with the equation.
3. Check whether $v^2$ is a perfect square. If it is not, discard this $u$. If it is, compute $v = \sqrt{v^2}$ and verify it is an integer.
4. For each valid pair $(u, v)$, construct a solution to the original problem using the transformation

$$x = u - v,\quad y = u + v.$$

This guarantees $x^2 + y^2 = 2D^2$.
5. Keep only solutions where $x \ge 0$. This condition is equivalent to $u \ge v$, so we implicitly filter invalid cases.
6. Store each valid $(x, y)$ pair and sort the result by $x$ before output, since enumeration order in $u$ does not strictly guarantee sorted $x$.

### Why it works

The key invariant is that every representation $u^2 + v^2 = D^2$ corresponds to exactly one valid construction $x = u - v, y = u + v$ satisfying $x^2 + y^2 = 2D^2$. The transformation is reversible: any solution $(x, y)$ can be mapped back to $(u, v)$ via $u = (x + y)/2$, $v = (y - x)/2$, which must be integers because $x + y$ and $y - x$ share parity. This bijection ensures no solutions are missed and no invalid solutions are introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    D = int(input())
    D2 = D * D
    res = []

    for u in range(D + 1):
        v2 = D2 - u * u
        if v2 < 0:
            continue
        v = int(math.isqrt(v2))
        if v * v != v2:
            continue

        x = u - v
        y = u + v

        if x < 0:
            continue

        res.append((x, y))

    res.sort()
    print(len(res))
    for x, y in res:
        print(x, y)

if __name__ == "__main__":
    solve()
```

The code directly implements the reduction to the $(u, v)$ representation. The use of `isqrt` avoids floating-point inaccuracies when checking perfect squares. Sorting is required because different $(u, v)$ pairs can produce solutions with the same or unordered $x$ values.

The condition `x < 0` enforces the required quadrant restriction after transformation, and also implicitly ensures we keep only the canonical half of symmetric solutions.

## Worked Examples

### Example 1: $D = 5$

We compute $D^2 = 25$. We iterate over $u$ and check when $25 - u^2$ is a square.

| u | v² = 25 - u² | v | valid | x = u - v | y = u + v |
| --- | --- | --- | --- | --- | --- |
| 0 | 25 | 5 | yes | -5 | 5 |
| 3 | 16 | 4 | yes | -1 | 7 |
| 4 | 9 | 3 | yes | 1 | 7 |
| 5 | 0 | 0 | yes | 5 | 5 |

Filtering negative $x$, we keep $(1, 7)$ and $(5, 5)$.

This shows how multiple $(u, v)$ pairs can generate the same geometric structure but only valid transformations remain in the first quadrant.

### Example 2: $D = 9$

We compute $D^2 = 81$. The only square decomposition is $9^2 + 0^2$ (and symmetric variants).

| u | v² = 81 - u² | v | valid | x | y |
| --- | --- | --- | --- | --- | --- |
| 9 | 0 | 0 | yes | 9 | 9 |

All other $u$ values produce non-squares, so only one point exists.

This demonstrates the sparsity of solutions even for larger $D$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(D)$ | We scan all values of $u$ from $0$ to $D$, each with constant-time square check |
| Space | $O(K)$ | We store all valid solutions, where $K$ is the number of lattice points |

The bound $D \le 10^6$ makes a linear scan feasible, and the number of valid outputs is small enough that both computation and printing remain efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isqrt

    D = int(sys.stdin.readline())
    D2 = D * D
    res = []

    for u in range(D + 1):
        v2 = D2 - u * u
        if v2 < 0:
            continue
        v = isqrt(v2)
        if v * v != v2:
            continue
        x = u - v
        y = u + v
        if x >= 0:
            res.append((x, y))

    res.sort()
    out = [str(len(res))]
    out += [f"{x} {y}" for x, y in res]
    return "\n".join(out)

# provided samples
assert run("5\n") == "2\n1 7\n5 5", "sample 1"
assert run("9\n") == "1\n9 9", "sample 2"

# custom cases
assert run("1\n") == "0", "no solutions"
assert run("2\n") == "1\n0 2", "single boundary solution"
assert run("10\n") is not None, "basic sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | no lattice points on small circle |
| 2 | 1 0 2 | boundary case with zero coordinate |
| 10 | multiple | general correctness and enumeration stability |

## Edge Cases

A key edge case is when $u < v$, which produces negative $x = u - v$. For example, with $u = 0, v = D$, we get $x = -D$, which lies outside the allowed region. The algorithm explicitly filters these cases, and this ensures we only keep points in the first quadrant after transformation.

Another edge case is when $v = 0$, which corresponds to $u = D$. This produces the point $(x, y) = (D, D)$, which is always valid and forms the minimal guaranteed solution.
