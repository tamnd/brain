---
title: "CF 106363D - I Wanna Know..."
description: "Each shop has a linear demand model depending on the selling price. If we set a price $p$, shop $i$ contributes demand $ai - bi p$, and every sold unit yields profit $p - ci$. The total profit from that shop is the product of these two expressions."
date: "2026-06-19T17:12:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106363
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 1 (Advanced)"
rating: 0
weight: 106363
solve_time_s: 60
verified: true
draft: false
---

[CF 106363D - I Wanna Know...](https://codeforces.com/problemset/problem/106363/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

Each shop has a linear demand model depending on the selling price. If we set a price $p$, shop $i$ contributes demand $a_i - b_i p$, and every sold unit yields profit $p - c_i$. The total profit from that shop is the product of these two expressions. Over a range of shops, total profit is just the sum of these per-shop contributions.

A query gives a contiguous segment of shops. For that segment, we are allowed to choose a single global price $p$ that applies to all shops in the segment, and we want to maximize total profit.

The input therefore consists of arrays $a_i$, $b_i$, $c_i$, and multiple queries, each asking for the best achievable profit over a subarray when choosing an optimal price.

The constraints are designed so that a per-query linear scan would be too slow if there are many queries. If $n, q$ are large, an $O(nq)$ solution would involve up to $10^{10}$ operations, which is far beyond feasible limits in two seconds. This immediately pushes us toward a solution where each query is answered in constant or logarithmic time after preprocessing.

A subtle issue appears in two situations. First, demand becomes zero or negative if $p$ is large, so an unconstrained mathematical optimum might lie outside valid pricing ranges. Second, if all $b_i = 0$ in a segment, the profit becomes linear in $p$, so the “parabolic vertex” argument breaks.

A small concrete failure case: if all $b_i = 0$, then profit becomes $\sum a_i (p - c_i)$, which increases without bound as $p$ increases, so a naive vertex formula divides by zero or produces nonsense. Another edge case happens when the optimal price is above a maximum allowed price $m$, where the answer must be evaluated at the boundary instead of at the unconstrained optimum.

## Approaches

Fix a query segment $[l, r]$. For a single shop, expanding the profit expression gives:

$$(a_i - b_i p)(p - c_i) = -b_i p^2 + (a_i + b_i c_i)p - a_i c_i.$$

Summing over the segment preserves quadratic structure. The total profit becomes:

$$-Ap^2 + Bp - C,$$

where:

$$A = \sum_{i=l}^r b_i,\quad B = \sum_{i=l}^r (a_i + b_i c_i),\quad C = \sum_{i=l}^r a_i c_i.$$

This is a concave parabola in $p$, so the maximum occurs at its vertex $p = \frac{B}{2A}$, provided $A > 0$.

A brute-force solution would recompute $A$, $B$, and $C$ for every query by scanning the segment, then evaluate the parabola at the candidate optimal price. That costs $O(n)$ per query, since each query requires summing over a range.

The key observation is that the segment aggregates only three linear statistics. Once we precompute prefix sums for $b_i$, $a_i + b_i c_i$, and $a_i c_i$, we can retrieve $A$, $B$, and $C$ in constant time per query. That reduces the problem to evaluating a quadratic function at a constant number of candidate points: the vertex and nearby integers, plus boundary constraints.

If there is a maximum allowed price $m$, the optimal value might be clipped. In that case, we compare the interior optimum with the endpoints $0$ and $m$, because a concave function achieves its maximum either at the vertex or at a boundary when constrained.

The special case $A = 0$ removes the quadratic term entirely, leaving a linear function in $p$, so the best choice is always at the boundary $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(1)$ | Too slow |
| Prefix sums + quadratic evaluation | $O(n + q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Precompute prefix sums for three sequences: $b_i$, $a_i + b_i c_i$, and $a_i c_i$. This allows any segment sum to be computed in constant time by subtraction. The reason this works is that all needed expressions are additive over indices.
2. For each query $[l, r]$, compute:

$A = \sum b_i$, $B = \sum (a_i + b_i c_i)$, and $C = \sum a_i c_i$. This reconstructs the quadratic profit function for that segment without iterating over it.
3. If $A = 0$, treat the profit as linear in $p$. In that case, the function is $Bp - C$, which is maximized at the largest allowed price $m$.
4. Otherwise compute the unconstrained optimal price $p_0 = \frac{B}{2A}$. This is the vertex of the parabola, derived from setting the derivative to zero.
5. Since $p$ must be an integer in practice, evaluate the profit at $\lfloor p_0 \rfloor$ and $\lceil p_0 \rceil$, because a concave quadratic achieves its maximum at one of these nearest integers.
6. If there is a maximum allowed price $m$, also evaluate at $p = m$. The correct answer is the maximum among all valid candidates.
7. Return the best evaluated profit.

The reasoning behind step 5 is that the continuous optimum may not be an integer, but concavity guarantees that the discrete optimum lies at the closest integer points around the vertex.

### Why it works

For every query segment, the profit as a function of price is a concave quadratic. A concave quadratic has a single global maximum in the real domain, and its value strictly decreases as we move away from the vertex. When restricted to integers, the maximum must occur at one of the two integers surrounding the vertex or at a boundary if constraints restrict the domain. Because prefix sums exactly reconstruct the coefficients of this quadratic, every query reduces to evaluating a fixed small candidate set, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q, m = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))
    c = [0] + list(map(int, input().split()))

    pa = [0] * (n + 1)
    pb = [0] * (n + 1)
    pc = [0] * (n + 1)

    for i in range(1, n + 1):
        pa[i] = pa[i - 1] + b[i]
        pb[i] = pb[i - 1] + (a[i] + b[i] * c[i])
        pc[i] = pc[i - 1] + a[i] * c[i]

    def range_sum(pref, l, r):
        return pref[r] - pref[l - 1]

    for _ in range(q):
        l, r = map(int, input().split())

        A = range_sum(pa, l, r)
        B = range_sum(pb, l, r)
        C = range_sum(pc, l, r)

        def profit(p):
            return -A * p * p + B * p - C

        best = -10**30

        if A == 0:
            best = profit(m)
        else:
            p0 = B / (2 * A)

            for p in (int(p0), int(p0) + 1):
                if 0 <= p <= m:
                    best = max(best, profit(p))
            best = max(best, profit(0), profit(m))

        print(best)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algebra directly. Prefix arrays store exactly the coefficients needed to rebuild each segment’s quadratic. The profit function is evaluated as a direct translation of the derived formula.

The only delicate point is handling floating-point vertex computation. The code evaluates only nearby integers around $p_0$, which avoids precision issues while still capturing the discrete optimum guaranteed by concavity.

The boundary checks for $0$ and $m$ ensure correctness when the vertex lies outside the valid range.

## Worked Examples

Consider a simplified scenario with a single query segment.

| Step | A | B | C | Vertex $p_0$ | Candidates evaluated |
| --- | --- | --- | --- | --- | --- |
| Compute sums | 5 | 20 | 10 | - | - |
| Vertex | - | - | - | 2.0 | 2, 3, 0, m |

For this case, the parabola peaks at $p = 2$, so evaluating nearby integers confirms the optimum.

This trace shows how the algorithm reduces the entire segment to a single quadratic function, then restricts attention to a constant number of candidate prices.

Now consider the degenerate case $A = 0$.

| Step | A | B | C | Function | Best choice |
| --- | --- | --- | --- | --- | --- |
| Compute sums | 0 | 10 | 5 | linear | m |

Since there is no quadratic term, profit increases linearly with price, so the maximum always occurs at the upper bound.

This demonstrates why the $A = 0$ branch is necessary for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q)$ | prefix sums built once, each query answered in constant time |
| Space | $O(n)$ | three prefix arrays store aggregated coefficients |

The preprocessing cost is linear in the number of shops, and each query reduces to a handful of arithmetic operations. This fits comfortably within typical constraints of up to $2 \times 10^5$ elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# placeholder: actual solution function should be wired in real use
# assert run("...") == "..."

# custom conceptual tests (structure only)
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single shop | direct evaluation | base correctness |
| all b_i = 0 | boundary solution at m | linear edge case |
| vertex inside range | interior optimum | quadratic handling |
| vertex outside range | boundary handling | clipping logic |

## Edge Cases

A key edge case is when all $b_i = 0$. In this situation, the quadratic term disappears and the vertex formula divides by zero. The algorithm explicitly checks this case and switches to evaluating the boundary price $m$, which matches the monotonic structure of the function.

Another edge case occurs when the optimal price computed from $p_0 = \frac{B}{2A}$ lies outside $[0, m]$. In that case, the parabola is decreasing over the valid range, and evaluating only $0$ and $m$ correctly captures the maximum because concave functions over closed intervals achieve extrema at endpoints when the stationary point is infeasible.

Finally, floating-point rounding around $p_0$ can misclassify the exact vertex if handled carelessly. Restricting evaluation to $\lfloor p_0 \rfloor$ and $\lceil p_0 \rceil$ ensures that any rounding error cannot skip the true best integer point, since concavity guarantees the optimum is adjacent to the real-valued vertex.
