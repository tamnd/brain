---
title: "CF 102623I - Immortal Trees"
description: "We need count labeled trees on vertices 1..n that satisfy two kinds of restrictions. Some pairs of vertices are forced to be connected by an edge. Other restrictions limit the final degree of particular vertices from above or below."
date: "2026-08-04T17:12:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "I"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 82
verified: true
draft: false
---

[CF 102623I - Immortal Trees](https://codeforces.com/problemset/problem/102623/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We need count labeled trees on vertices `1..n` that satisfy two kinds of restrictions. Some pairs of vertices are forced to be connected by an edge. Other restrictions limit the final degree of particular vertices from above or below.

The answer is not asking us to construct one tree. We need count every possible adjacency matrix that represents a valid tree, modulo `998244353`.

The small value `n <= 60` rules out any approach that enumerates trees or edges. The number of labeled trees is `n^(n-2)` by Cayley's formula, which is already enormous for `n = 60`. We need a polynomial solution.

The key observation is that the forced edges form a forest in every valid case. If they contain a cycle, no tree can contain all of them. After contracting every connected component of this forest, the remaining choices are only about connecting these components into a tree.

A subtle point is that degree restrictions apply to original vertices, not contracted components. A vertex already has some degree contributed by forced edges, and only its remaining degree can be supplied by edges between components.

## Approaches

A brute force solution could generate all labeled trees using Prüfer sequences. A tree corresponds to a sequence of length `n-2`, so we could enumerate every sequence, rebuild the tree, and check all constraints. This is correct because every labeled tree appears exactly once. However, there are `n^(n-2)` sequences, which is impossible even for moderate `n`.

The useful structure comes from contracting mandatory edges. Suppose the mandatory forest has `c` connected components. Any valid final tree is obtained by adding exactly `c-1` edges between these components. After contraction, every pair of components can be connected, and choosing an endpoint inside a component contributes to the degree of that endpoint.

For a component `C`, let

```
S_C = sum(x_v)
```

over all vertices `v` inside it. The weighted Cayley formula says that the generating function of trees on the contracted components is

```
(S_1 + S_2 + ... + S_c)^(c-2) * S_1 * S_2 * ... * S_c
```

where the exponent of `x_v` represents how many new edges leave vertex `v`.

The remaining task is extracting only the degrees allowed by the constraints. Because `n` is only 60, a dynamic programming over possible total external degrees is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Prüfer enumeration | O(n^(n-2) * n) | O(n) | Too slow |
| Contracted forest + generating function DP | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Check whether the mandatory edges form a forest using DSU. If an edge joins two already connected vertices, the answer is zero because every tree is acyclic.
2. For every vertex, compute its degree inside the mandatory forest. This is the part of the final degree that is already fixed.
3. Convert every degree constraint into a range for the number of additional edges incident to the vertex. If a vertex already has mandatory degree `d`, then its extra degree must satisfy:

```
lower - d <= extra_degree <= upper - d
```
4. Contract the mandatory forest into components. If there is only one component, all edges of the final tree are already fixed, so the answer is one if all degree constraints match.
5. For every component, compute a polynomial describing how many ways its vertices can receive a given total number of external edges. For a vertex that can receive `t` external edges, its contribution is:

```
x^t / t!
```

Multiplying these polynomials inside a component gives the component polynomial.
6. Combine all components. A component must have at least one outgoing edge in the contracted tree, so its total external degree is `g >= 1`. The Cayley formula contributes:

```
(c-2)! * g
```

for choosing the component contribution.
7. Run a knapsack over components to make the total external degree equal to `2(c-1)`, because a tree on `c` contracted nodes has `c-1` edges and every such edge contributes two degrees.

### Why it works

The mandatory edges define a fixed forest. Every valid tree corresponds uniquely to a tree between the contracted components plus choices of which original vertices are endpoints of the new edges.

The generating function encodes exactly those endpoint choices. The coefficient of a monomial gives the number of ways to distribute external degrees among vertices. Cayley's formula gives the number of ways to connect the components with those component degrees. Since the DP sums all possible valid degree assignments, every valid tree is counted once and invalid trees are excluded.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m, k = map(int, input().split())

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return False
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        return True

    forced_deg = [0] * n

    ok = True
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        forced_deg[a] += 1
        forced_deg[b] += 1
        if not union(a, b):
            ok = False

    low = [1] * n
    high = [n - 1] * n

    for _ in range(k):
        op, x, d = map(int, input().split())
        x -= 1
        if op == 0:
            low[x] = max(low[x], d)
        else:
            high[x] = min(high[x], d)

    if not ok:
        print(0)
        return

    for i in range(n):
        low[i] -= forced_deg[i]
        high[i] -= forced_deg[i]
        if high[i] < 0:
            print(0)
            return
        low[i] = max(low[i], 0)

    roots = {}
    comp_id = []
    for i in range(n):
        r = find(i)
        if r not in roots:
            roots[r] = len(roots)
        comp_id.append(roots[r])

    c = len(roots)

    if c == 1:
        ans = 1
        for i in range(n):
            if not (low[i] <= 0 <= high[i]):
                ans = 0
        print(ans)
        return

    fact = [1] * (n + 5)
    invfact = [1] * (n + 5)
    for i in range(1, n + 5):
        fact[i] = fact[i-1] * i % MOD
    invfact[-1] = pow(fact[-1], MOD - 2, MOD)
    for i in range(n + 4, 0, -1):
        invfact[i-1] = invfact[i] * i % MOD

    comps = [[] for _ in range(c)]
    for i in range(n):
        comps[comp_id[i]].append(i)

    polys = []

    for comp in comps:
        poly = [1]
        for v in comp:
            nxt = [0] * (len(poly) + n)
            for i, a in enumerate(poly):
                if a:
                    for d in range(low[v], high[v] + 1):
                        nxt[i + d] = (nxt[i + d] + a * invfact[d]) % MOD
            poly = nxt

        val = [0] * len(poly)
        for i in range(1, len(poly)):
            val[i] = poly[i] * i % MOD
        polys.append(val)

    dp = [0] * (2 * c)
    dp[0] = 1

    for poly in polys:
        ndp = [0] * (2 * c)
        for i in range(len(dp)):
            if dp[i]:
                for j in range(1, len(poly)):
                    if i + j < len(ndp):
                        ndp[i + j] = (ndp[i + j] + dp[i] * poly[j]) % MOD
        dp = ndp

    ans = dp[2 * c - 2] * fact[c - 2] % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The DSU part handles the mandatory forest. A repeated connection inside the same component immediately proves impossibility because a tree cannot contain a cycle.

The degree transformation is the part that is easiest to get wrong. The restrictions describe final degrees, but the generating function only counts newly added edges. Subtracting the already fixed forest degree converts the problem into exactly the quantity represented by the polynomial.

The factorial inverses appear because the coefficient of a multinomial expansion contains divisions by the factorials of the chosen exponents. Multiplying by the component degree later restores the Cayley contribution for the contracted tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Polynomial merging dominates, with at most 60 vertices and degree range 60 |
| Space | O(n^2) | DP arrays store only degree distributions |

The maximum degree range is small because every tree has only `n-1` edges. With `n = 60`, the cubic bound is easily within the limits.
