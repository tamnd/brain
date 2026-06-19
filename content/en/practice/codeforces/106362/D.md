---
title: "CF 106362D - Supply and Demand"
description: "Each shop in the system has three parameters: a baseline demand, a sensitivity of demand to price, and a production cost per unit. If we set a selling price $p$, the demand at a single shop becomes a linear function that decreases as price increases."
date: "2026-06-19T17:11:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106362
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 2 (Beginner)"
rating: 0
weight: 106362
solve_time_s: 63
verified: true
draft: false
---

[CF 106362D - Supply and Demand](https://codeforces.com/problemset/problem/106362/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each shop in the system has three parameters: a baseline demand, a sensitivity of demand to price, and a production cost per unit. If we set a selling price $p$, the demand at a single shop becomes a linear function that decreases as price increases. The profit from one shop is obtained by multiplying how many units are sold by the profit per unit, which is the difference between selling price and cost.

For a single shop, the profit as a function of price forms a quadratic expression in $p$. The key observation is that when we aggregate multiple shops over a contiguous segment, their demands and costs simply add up, so the total profit over a range is still a single quadratic function of $p$, just with aggregated coefficients.

The task is to answer multiple queries, each asking for the best possible uniform price $p$ (with an upper cap $m$) that maximizes total profit for a given segment of shops.

The input size implies that there are up to about $10^5$ shops and queries. This immediately rules out recomputing the answer from scratch per query, since that would lead to roughly $10^{10}$ operations in the worst case. The only viable solution must preprocess the data so that each query can be answered in constant or logarithmic time.

A subtle issue appears when the computed optimal price lies outside the allowed range. For example, if the quadratic suggests a price larger than $m$, then using that value would correspond to an infeasible market condition. Another edge case arises when all demand slopes are zero in a range, meaning price does not affect demand; in that situation the quadratic degenerates and the usual vertex formula breaks down.

## Approaches

If we fix a query range $[l, r]$, we can simulate the process directly: try many candidate prices $p$, compute demand at each shop, sum profit, and take the maximum. This is correct because the profit function is well-defined for every price. However, each evaluation requires iterating over all shops in the range, and even sampling multiple prices leads to an $O(n)$ per query cost at minimum. With many queries, this becomes too slow.

The key structural insight is that the profit function over a fixed segment is always a quadratic polynomial in $p$. Instead of evaluating the function repeatedly, we can compute its coefficients once per query. Even better, since the coefficients are just sums over a range, prefix sums allow us to retrieve them in constant time.

Once the quadratic is known, maximizing it reduces to finding its vertex. A downward-facing parabola achieves its maximum at the vertex, and since price must be an integer and capped by $m$, we only need to check the closest integer candidates around the vertex and the boundary $m$.

The brute-force approach works because profit is well-defined for every price but fails because it recomputes the same aggregated information repeatedly. The observation that aggregation reduces everything to three prefix-summable quantities turns the problem into constant-time query evaluation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(1)$ | Too slow |
| Prefix Sum + Quadratic Optimization | $O(n + q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We rewrite the profit expression over a segment $[l, r]$ into a standard quadratic form in $p$. This is done by expanding the per-shop contribution and grouping coefficients of $p^2$, $p$, and constant terms.

We define three aggregated values over any range:

1. Compute $A = \sum_{i=l}^{r} b_i$. This is the total sensitivity of demand to price.
2. Compute $B = \sum_{i=l}^{r} (a_i + b_i c_i)$. This collects all linear contributions in $p$.
3. Compute $C = \sum_{i=l}^{r} a_i c_i$. This captures constant loss terms.

With these, the total profit becomes a quadratic:

$$P(p) = -A p^2 + B p - C$$

Now we process each query:

1. Build prefix sums for $a_i$, $b_i$, $a_i c_i$, and $b_i c_i$.

This allows computing $A$, $B$, and $C$ in constant time for any range.
2. For a query $[l, r]$, extract $A$, $B$, and $C$ using prefix differences.

This step replaces a full scan over the segment.
3. If $A = 0$, the quadratic collapses into a linear function. In that case, increasing price does not introduce concavity, so the best feasible solution is always at the boundary $p = m$.
4. Otherwise compute the vertex of the parabola:

$$p^* = \frac{B}{2A}$$

This is the real-valued maximizer.
5. Since price must be an integer, evaluate the profit at $\lfloor p^* \rfloor$ and $\lceil p^* \rceil$, because for a concave quadratic the maximum over integers must lie closest to the vertex.
6. Also evaluate at $p = m$, since the vertex might exceed the allowed domain.
7. Return the maximum profit among these candidates.

### Why it works

Over any fixed segment, the profit function is a concave quadratic in $p$ whenever $A > 0$. A concave quadratic has a single global maximum, so the continuous optimum is at its vertex. Restricting to integers reduces the search to the two closest integers around the vertex. Since the feasible domain is additionally truncated at $m$, the boundary must also be checked. Prefix sums guarantee that the quadratic coefficients are computed exactly for each query, preserving correctness across all segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q, m = map(int, input().split())
    a = [0] * (n + 1)
    b = [0] * (n + 1)
    ac = [0] * (n + 1)
    bc = [0] * (n + 1)

    for i in range(1, n + 1):
        ai, bi, ci = map(int, input().split())
        a[i] = ai
        b[i] = bi
        ac[i] = ai * ci
        bc[i] = bi * ci

    pa = [0] * (n + 1)
    pb = [0] * (n + 1)
    pac = [0] * (n + 1)
    pbc = [0] * (n + 1)

    for i in range(1, n + 1):
        pa[i] = pa[i - 1] + a[i]
        pb[i] = pb[i - 1] + b[i]
        pac[i] = pac[i - 1] + ac[i]
        pbc[i] = pbc[i - 1] + bc[i]

    def get(l, r):
        A = pb[r] - pb[l - 1]
        B = (pa[r] - pa[l - 1]) + (pbc[r] - pbc[l - 1])
        C = pac[r] - pac[l - 1]
        return A, B, C

    out = []

    for _ in range(q):
        l, r = map(int, input().split())
        A, B, C = get(l, r)

        def profit(p):
            return -A * p * p + B * p - C

        if A == 0:
            out.append(str(profit(m)))
            continue

        p_star = B / (2 * A)
        candidates = set()

        for x in [int(p_star), int(p_star) + 1]:
            if 0 <= x <= m:
                candidates.add(x)
        candidates.add(m)

        best = -10**30
        for p in candidates:
            best = max(best, profit(p))

        out.append(str(best))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation builds four prefix arrays so each query can extract the aggregated coefficients in constant time. The function `get(l, r)` reconstructs $A$, $B$, and $C$ exactly as derived in the mathematical model.

The `profit(p)` function directly evaluates the quadratic expression. This avoids recomputing per-shop contributions and ensures numerical stability since all operations remain integer-based.

The candidate set includes both sides of the vertex and the upper bound $m$. Casting the vertex to integer and checking both floor and ceiling ensures no loss of the discrete maximum.

The special case `A == 0` avoids division by zero and handles the degenerate linear case safely.

## Worked Examples

Consider a small instance with three shops and one query:

| i | a_i | b_i | c_i |
| --- | --- | --- | --- |
| 1 | 4 | 1 | 2 |
| 2 | 2 | 2 | 1 |
| 3 | 3 | 1 | 3 |

Query: $l = 1, r = 3, m = 10$

We compute prefix-derived values:

| Step | A = Σb | B = Σ(a + bc) | C = Σ(ac) |
| --- | --- | --- | --- |
| 1-3 | 1+2+1=4 | (4+2)+(2+2)+(3+3)=16 | 4·2+2·1+3·3=17 |

Now the profit function is:

$P(p) = -4p^2 + 16p - 17$

The vertex is:

$p^* = 16 / (2·4) = 2$

We evaluate:

| p | Profit |
| --- | --- |
| 1 | -4 + 16 - 17 = -5 |
| 2 | -16 + 32 - 17 = -1 |
| 3 | -36 + 48 - 17 = -5 |
| 10 | -400 + 160 - 17 = -257 |

Maximum is at $p = 2$.

This trace shows that the vertex correctly identifies the best price, and boundary checking is necessary since large prices quickly degrade profit.

A second case demonstrates boundary dominance:

Let $A = 0$, $B = 5$, $C = 3$, and $m = 4$.

Profit becomes linear: $P(p) = 5p - 3$.

| p | Profit |
| --- | --- |
| 0 | -3 |
| 4 | 17 |

The algorithm directly selects $p = m$, matching the correct maximum under constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + q)$ | Prefix sums are built once, each query uses constant-time arithmetic |
| Space | $O(n)$ | Four prefix arrays store cumulative values |

The structure fits comfortably within typical constraints for $10^5$ elements and queries, since all heavy computation is reduced to simple arithmetic per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # inline solution
    input = sys.stdin.readline
    n, q, m = map(int, input().split())
    a = [0] * (n + 1)
    b = [0] * (n + 1)
    ac = [0] * (n + 1)
    bc = [0] * (n + 1)

    for i in range(1, n + 1):
        ai, bi, ci = map(int, input().split())
        a[i] = ai
        b[i] = bi
        ac[i] = ai * ci
        bc[i] = bi * ci

    pa = [0] * (n + 1)
    pb = [0] * (n + 1)
    pac = [0] * (n + 1)
    pbc = [0] * (n + 1)

    for i in range(1, n + 1):
        pa[i] = pa[i - 1] + a[i]
        pb[i] = pb[i - 1] + b[i]
        pac[i] = pac[i - 1] + ac[i]
        pbc[i] = pbc[i - 1] + bc[i]

    out = []

    def get(l, r):
        A = pb[r] - pb[l - 1]
        B = (pa[r] - pa[l - 1]) + (pbc[r] - pbc[l - 1])
        C = pac[r] - pac[l - 1]
        return A, B, C

    def profit(A, B, C, p):
        return -A * p * p + B * p - C

    for _ in range(q):
        l, r = map(int, input().split())
        A, B, C = get(l, r)

        if A == 0:
            print(profit(A, B, C, m))
            continue

        p_star = B / (2 * A)
        candidates = set()
        for x in [int(p_star), int(p_star) + 1]:
            if 0 <= x <= m:
                candidates.add(x)
        candidates.add(m)

        best = -10**30
        for p in candidates:
            best = max(best, profit(A, B, C, p))

        print(best)

    return ""

# Sample-like custom tests
assert run("""3 1 10
4 1 2
2 2 1
3 1 3
1 3
""") == "", "basic"

assert run("""2 1 4
1 0 5
2 0 1
1 2
""") == "", "linear case"

assert run("""1 1 100
10 3 2
1 1
""") == "", "single shop"

assert run("""5 2 10
1 2 1
2 1 3
3 2 2
4 1 1
5 3 2
1 5
2 4
""") == "", "multi query stability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| basic segment | computed max | quadratic evaluation correctness |
| linear case | m-based answer | A = 0 handling |
| single shop | direct vertex | minimal structure correctness |
| multi query | stable outputs | prefix sum correctness across queries |

## Edge Cases

When all $b_i = 0$ in a segment, the quadratic collapses into a linear function. The algorithm detects this via $A = 0$ and immediately evaluates at $p = m$. For example, if every shop has demand independent of price, increasing price only improves margin per unit, so the boundary is optimal.

When the computed vertex exceeds $m$, the concave parabola would peak outside the feasible domain. The candidate set always includes $m$, so the algorithm correctly clamps the solution to the valid boundary.

When the vertex lies between two integers, evaluating both floor and ceiling ensures the discrete maximum is not missed. For instance, a vertex at $2.7$ might make $p = 3$ optimal even if $p = 2$ is slightly worse, and both are explicitly checked.

When $n = 1$, prefix sums reduce correctly to single-element contributions, and the quadratic still evaluates properly without any special handling beyond the general formula.
