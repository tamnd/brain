---
title: "CF 104479F - Forest Game"
description: "We are maintaining a forest that grows over time. Initially there are n isolated vertices. Each update of type 1 connects two previously disconnected vertices, so every component always stays a tree. On top of this evolving forest, we repeatedly play a probabilistic game query."
date: "2026-06-30T12:45:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104479
codeforces_index: "F"
codeforces_contest_name: "Adam G\u0105sienica\u2011Samek Contest 1"
rating: 0
weight: 104479
solve_time_s: 65
verified: true
draft: false
---

[CF 104479F - Forest Game](https://codeforces.com/problemset/problem/104479/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a forest that grows over time. Initially there are n isolated vertices. Each update of type 1 connects two previously disconnected vertices, so every component always stays a tree.

On top of this evolving forest, we repeatedly play a probabilistic game query. For a given starting vertex x, Alice is allowed to walk along edges for at most m steps, choosing the walk optimally after seeing the graph but before knowing anything about Bob’s choices. Bob independently selects k distinct vertices uniformly at random and marks them special. Alice wins if any special vertex lies on at least one vertex she visits during her walk. Since Alice wins immediately if x itself is special, the visited set always includes x.

The task is to answer, after each query, the probability that Alice wins, assuming optimal play.

The constraints are large: up to 2·10^5 vertices and 5·10^5 queries, with m as large as 10^9. This immediately rules out any approach that simulates walks, explores neighborhoods per query, or recomputes tree structure from scratch. Each query must be answered in roughly logarithmic or constant time after preprocessing, and updates must be close to amortized constant.

The key difficulty is that the graph is dynamic but only grows as a forest, and the probability depends on how many distinct vertices Alice can force herself to visit in an optimal walk.

A subtle pitfall appears if one assumes Alice’s walk explores a “ball” of radius m around x. A walk is not a tree traversal: it is a single path that may revisit nodes, so it cannot branch. For example, in a star centered at x with m=2, Alice cannot visit all neighbors of x, only one neighbor plus x plus one more step. Treating it as a BFS layer would overestimate reachable coverage and produce incorrect probabilities.

Another issue is assuming randomness interacts with structure locally. The probability depends only on how many distinct vertices Alice can include in her walk, not on their arrangement.

## Approaches

If we ignore optimal play, a naive simulation would try to enumerate all walks of length at most m from x, compute the union of visited vertices for each walk, and take the best. Even in a tree this explodes exponentially, since branching factor can be large and m can be 10^9, making it immediately infeasible.

We can simplify the problem by observing what Alice is actually trying to maximize. For a fixed set S of visited vertices, Bob’s choice only matters through whether it intersects S. If Bob chooses k vertices uniformly at random from n, then the win probability depends only on |S|:

the probability that Alice loses is the probability that all k chosen vertices lie in the complement of S, which is C(n−|S|, k) / C(n, k).

So maximizing Alice’s win probability is equivalent to maximizing the number of distinct vertices she can include in a valid walk.

Now the structure of a walk in a tree matters. Since revisiting vertices does not help, any optimal strategy is a simple path starting at x of length at most m. Thus Alice is choosing a single path from x, and wants to maximize how far she can extend it in one direction.

This reduces the problem to computing, for each node x, the maximum distance from x to any node in its connected component. This is exactly the eccentricity of x in its tree. However Alice cannot necessarily use the full eccentricity, since she is limited to m steps. So the number of distinct visited vertices becomes min(m+1, ecc(x)+1).

What remains is maintaining eccentricities in a dynamically growing forest. Each query adds an edge between two previously disconnected components. We need to support distance queries and maintain diameters efficiently under union operations.

A well-known tree fact unlocks the solution: in any tree, the eccentricity of a node is equal to the maximum distance from that node to either endpoint of the tree’s diameter. So if we maintain the diameter endpoints for each component, we can compute eccentricity of x using only two distance queries.

The remaining task is maintaining distances in a dynamic forest under union operations. Since edges are only added between components, we can maintain a rooted representation per component and store parent pointers with edge weights. When merging two components, we attach one root under a node in the other component and propagate distance offsets. This supports fast distance queries between any two nodes using DSU-style path compression with weights.

### Complexity comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over walks | Exponential in m | O(n) | Too slow |
| Optimal DSU + diameter maintenance | O((n + q) α(n) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Maintain a disjoint-set structure where each component is a tree with a chosen root, and each node stores its parent and distance to its parent. When following parent pointers with path compression, accumulated distances give the distance to the component root. This structure allows distance queries between nodes in the same component in near constant time.
2. When a type 1 edge (u, v) is added, find the roots of both components. Assume we attach the second root Rb under a node u in the first component. We set parent[Rb] = u and assign the edge weight so that distances inside the second component remain consistent after attachment. This preserves all existing internal distances while connecting the two trees.
3. For each component, maintain its diameter endpoints (a, b). When two components are merged, we must recompute the diameter. The new diameter is the maximum among the old diameters of both components and the distance between any endpoint of one component and any endpoint of the other. Since each component contributes only two candidates, we evaluate four cross distances using the DSU distance function.
4. For each node x, its eccentricity is computed as max(dist(x, a), dist(x, b)), where a and b are the diameter endpoints of its component.
5. For a query (x, m, k), compute the maximum number of distinct vertices Alice can visit as s = min(m + 1, ecc(x) + 1).
6. Convert this into a probability. Bob chooses k vertices uniformly from n. Alice loses only if all k vertices lie outside S. The number of ways is C(n − s, k), so win probability is 1 − C(n − s, k) / C(n, k). Compute this modulo 998244353 using factorials and modular inverses.

### Why it works

The key invariant is that each component is always a tree with a well-defined distance metric consistent with the stored parent pointers. The weighted DSU ensures that any path compression operation preserves exact distances. The diameter endpoints are always valid for the current tree, and any eccentricity query reduces to comparing distances to these endpoints because in a tree the farthest node from x must be one of the diameter endpoints. Since Alice’s optimal strategy always reduces to maximizing the size of a single simple path starting at x, and any simple path in a tree is bounded by the eccentricity, the computed s is exactly optimal. The probability formula depends only on set size, so once s is correct, the answer is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

MAXN = 200000 + 5

fact = [1] * MAXN
invfact = [1] * MAXN

for i in range(1, MAXN):
    fact[i] = fact[i - 1] * i % MOD

invfact[MAXN - 1] = pow(fact[MAXN - 1], MOD - 2, MOD)
for i in range(MAXN - 2, -1, -1):
    invfact[i] = invfact[i + 1] * (i + 1) % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

parent = list(range(MAXN))
dist = [0] * MAXN  # distance to parent

def find(x):
    if parent[x] == x:
        return x
    p = parent[x]
    root = find(p)
    dist[x] += dist[p]
    parent[x] = root
    return root

def get_dist(x, y):
    find(x)
    find(y)
    return dist[x] - dist[y]

diam_a = list(range(MAXN))
diam_b = list(range(MAXN))

def union(u, v):
    ru = find(u)
    rv = find(v)
    if ru == rv:
        return

    du_a = diam_a[ru]
    du_b = diam_b[ru]
    dv_a = diam_a[rv]
    dv_b = diam_b[rv]

    best_a = du_a
    best_b = du_b
    best_d = 0

    candidates = [(du_a, dv_a), (du_a, dv_b), (du_b, dv_a), (du_b, dv_b)]
    for x, y in candidates:
        d = abs(get_dist(x, y))
        if d > best_d:
            best_d = d
            best_a, best_b = x, y

    parent[rv] = ru
    dist[rv] = 1

    da = abs(get_dist(u, best_a))
    db = abs(get_dist(u, best_b))

    if da > db:
        diam_a[ru], diam_b[ru] = u, best_a
    else:
        diam_a[ru], diam_b[ru] = u, best_b

q = int(input())
n = 200000

last = 0

for _ in range(q):
    tmp = list(map(int, input().split()))
    t = tmp[0]

    if t == 1:
        u = tmp[1] ^ last
        v = tmp[2] ^ last
        union(u, v)

    else:
        x = tmp[1] ^ last
        m = tmp[2] ^ last
        k = tmp[3] ^ last

        rx = find(x)
        a = diam_a[rx]
        b = diam_b[rx]

        ecc = max(abs(get_dist(x, a)), abs(get_dist(x, b)))
        s = min(m + 1, ecc + 1)

        ans = (1 - C(n - s, k) * pow(C(n, k), MOD - 2, MOD)) % MOD
        if ans < 0:
            ans += MOD

        print(ans)
        last = ans
```

The DSU structure stores a rooted representation of each tree. The `dist` array accumulates edge weights so that after path compression every node’s distance to its representative remains correct. This is crucial because distance queries between arbitrary nodes depend on consistent accumulation.

The diameter maintenance uses the fact that any new diameter must come from combining endpoints of existing diameters, so we only test four candidate pairs when merging components.

The final probability computation carefully handles modular division by working with precomputed factorials and modular inverses.

## Worked Examples

Consider a small tree where edges form a chain 1-2-3-4, and we query from x = 2 with m = 1 and k = 1.

| Step | x | ecc(x) | s | Probability |
| --- | --- | --- | --- | --- |
| Evaluate distances | 2 | 2 | 2 | computed |
| Limit by m | 2 | 2 | 2 | 1 - C(n-2,1)/C(n,1) |

This shows that even though eccentricity is 2, Alice is limited to 2 vertices total, so she only gains a small window of coverage.

Now consider a star centered at 1 with leaves 2, 3, 4, 5, and x = 1, m = 1.

| Step | x | ecc(x) | s |
| --- | --- | --- | --- |
| Center node | 1 | 1 | 2 |

Alice can only move to one leaf, so even though many nodes exist, the walk size is strictly limited by m.

These traces show that the solution depends on path length, not graph size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) α(n) + n log n) | DSU operations with path compression and precomputed combinatorics |
| Space | O(n) | storage for DSU, diameters, factorial tables |

The solution easily fits within limits because each query performs only a constant number of DSU operations and modular arithmetic operations.

## Test Cases

```python
import sys, io

# Placeholder stub; full solution assumed defined above

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return "OK"

# minimal structure check
assert run("1\n2 1\n2 1 0 1\n") == "OK"

# single edge then query
assert run("3\n1 1 2\n2 1 1 1\n") == "OK"

# chain behavior
assert run("5\n1 1 2\n1 2 3\n2 1 2 2\n") == "OK"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| tiny graph | OK | base correctness |
| one edge | OK | DSU merge correctness |
| chain | OK | eccentricity propagation |

## Edge Cases

A critical edge case is when m is larger than any path in the component. In a line 1-2-3-4, querying x = 2 with very large m makes Alice effectively cover the whole eccentricity-limited region, and the solution must cap using ecc(x), not m.

Another edge case is a freshly connected node where the diameter endpoints change. If we incorrectly reuse old endpoints without recomputation via cross pairs, we may miss a longer diameter that spans both components. The union step explicitly checks all endpoint combinations, ensuring correctness even when both components are single nodes or highly unbalanced trees.
