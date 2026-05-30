---
title: "CF 1948G - MST with Matching"
description: "We are given a connected undirected weighted graph with at most 20 vertices. We must choose a spanning tree. The cost of that tree has two parts. The first part is standard, the sum of the chosen edge weights. The second part depends on the structure of the tree."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dsu", "graph-matchings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1948
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 163 (Rated for Div. 2)"
rating: 3100
weight: 1948
solve_time_s: 79
verified: true
draft: false
---

[CF 1948G - MST with Matching](https://codeforces.com/problemset/problem/1948/G)

**Rating:** 3100  
**Tags:** bitmasks, brute force, dsu, graph matchings, trees  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected undirected weighted graph with at most 20 vertices. We must choose a spanning tree. The cost of that tree has two parts.

The first part is standard, the sum of the chosen edge weights.

The second part depends on the structure of the tree. For the chosen spanning tree, we compute its maximum matching size, meaning the largest number of pairwise vertex-disjoint edges that can be selected from the tree. If the matching size is $k$, we pay an additional $k \cdot c$.

Our goal is to find the spanning tree with minimum total cost.

The graph is small in terms of vertices, $n \le 20$, but potentially dense because every pair of vertices may have an edge. A spanning tree has $n-1$ edges, but the number of possible spanning trees is enormous. Even for complete graphs, Cayley's formula gives $n^{n-2}$ spanning trees. For $n=20$, that is already around $2.6 \times 10^{23}$, completely impossible to enumerate.

The small value of $n$ strongly suggests that the solution should use bitmasks. A complexity around $O(2^n \cdot \text{poly}(n))$ is realistic because $2^{20}\approx 10^6$. Something like $O(2^n n^2)$ is roughly $4\times 10^8$ primitive operations in the worst theoretical count, but with very small constants and careful implementation it becomes acceptable in a 6 second limit. Anything involving enumeration of all trees or all matchings inside all trees is hopeless.

The dangerous part of the problem is the matching term. A naive idea would be to generate candidate spanning trees and compute their maximum matchings. The matching size depends on the whole tree structure, so it is not obvious how to optimize it together with MST construction.

There are several easy-to-miss situations.

Consider a path on four vertices:

```
1 - 2 - 3 - 4
```

The maximum matching size is 2 because we can take edges $(1,2)$ and $(3,4)$.

Input:

```
4 100
0 1 0 0
1 0 1 0
0 1 0 1
0 0 1 0
```

A solution that only minimizes edge weights would choose this tree and obtain edge sum $3$, but the real cost is $3+2\cdot100=203$.

Another subtle case is a star:

```
    2
    |
3 - 1 - 4
```

The maximum matching size is only 1 because every edge touches the center.

Input:

```
4 100
0 1 1 1
1 0 0 0
1 0 0 0
1 0 0 0
```

The tree weight is 3 and the matching penalty is only $100$, so total cost is 103. A solution that assumes "more edges around a vertex means larger matching" would be completely wrong.

The most important structural trap is that maximum matching size in a tree is not a local property. Different trees with the same edge weight sum may have different matching penalties. The optimization must handle both terms simultaneously.

## Approaches

The brute force idea is straightforward. Enumerate every spanning tree of the graph, compute its edge-weight sum, compute its maximum matching size, and keep the minimum answer.

This works because the objective is defined directly on a spanning tree. If we could examine every tree, correctness would be immediate.

The problem is the number of spanning trees. In a complete graph with 20 vertices there are

$$20^{18}$$

different spanning trees. Even checking one million trees per second would not make a dent in that search space.

So we need to understand the matching term more deeply.

The key observation comes from a classical theorem.

Every tree is bipartite.

For bipartite graphs,

$$\text{maximum matching}
=
\text{minimum vertex cover}.$$

This is Kőnig's theorem.

Instead of thinking about matchings, think about vertex covers.

Suppose the maximum matching size of the final tree is $k$. Then the tree has a vertex cover of size $k$.

Let that vertex cover be $S$.

Since every edge of the tree must be covered, every tree edge must have at least one endpoint inside $S$.

That means the tree uses only edges whose endpoints are not both outside $S$.

This completely changes the problem.

Fix some subset $S$. Assume $S$ is going to be a vertex cover of the final tree.

Then every allowed tree edge must satisfy:

$$u\in S
\quad\text{or}\quad
v\in S.$$

In other words, edges between two vertices outside $S$ are forbidden.

Among all spanning trees using only such edges, we simply want the minimum-weight one. That is just an MST problem on the restricted graph.

If that restricted graph is disconnected, then no spanning tree exists for this choice of $S$.

If the restricted graph is connected, the cheapest spanning tree compatible with $S$ is exactly its MST.

Its total cost becomes

$$\text{MST weight} + |S|\cdot c.$$

Why is this sufficient?

Because if a tree has maximum matching size $k$, then it has some vertex cover of size $k$. When we enumerate that cover, the tree becomes feasible in the corresponding restricted graph. The MST of that restricted graph can only be cheaper than that tree. Thus considering every subset $S$ never misses the optimum.

Now the problem becomes:

Enumerate every subset $S$, build the graph containing only edges touching $S$, compute its MST weight, and minimize

$$\text{MST weight}+|S|c.$$

Since $n\le 20$, there are $2^n$ subsets. For each subset we can run Prim's algorithm in $O(n^2)$.

That yields $O(2^n n^2)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over spanning trees | Exponential in number of trees | Huge | Too slow |
| Enumerate vertex covers + MST | $O(2^n n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the graph and replace every missing edge with an infinite value.
2. Enumerate every bitmask $mask$ from $0$ to $2^n-1$.
3. Interpret the set bits of $mask$ as a candidate vertex cover $S$.
4. Construct the implicit restricted graph where an edge $(u,v)$ is allowed only if at least one endpoint belongs to $S$.

An edge whose endpoints are both outside $S$ cannot appear in a tree covered by $S$.
5. Run Prim's algorithm on this restricted graph.

While relaxing edges, ignore every edge whose two endpoints are both outside $S$.
6. If Prim cannot reach all vertices, the restricted graph is disconnected.

In that case this subset $S$ cannot produce a spanning tree, so discard it.
7. Otherwise obtain the MST weight $W$.
8. Compute

$$W + c \cdot \text{popcount}(mask).$$

1. Minimize the answer over all masks.

### Why it works

For any spanning tree $T$, let $k$ be its maximum matching size.

Since every tree is bipartite, Kőnig's theorem gives a vertex cover $S$ of size $k$.

Every edge of $T$ has at least one endpoint in $S$, so $T$ is entirely contained inside the restricted graph defined by $S$.

The MST of that restricted graph has weight at most the weight of $T$, because $T$ is one valid spanning tree of the same graph.

Hence for this particular subset $S$,

$$\text{MST}(S)+|S|c
\le
\text{weight}(T)+kc.$$

Thus the optimal tree's cost is at least one value considered by our enumeration.

Conversely, for every subset $S$, any spanning tree of the restricted graph has all edges covered by $S$. Therefore $S$ is a vertex cover of that tree, so its maximum matching size is at most $|S|$. The cost we compute,

$$\text{MST}(S)+|S|c,$$

is achievable by the MST itself and never underestimates the true objective.

The two directions together show that the minimum value over all subsets is exactly the answer.

The reduction from matching to vertex cover is the crucial bridge.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 18

def prim(mask, n, g):
    dist = [INF] * n
    used = [False] * n
    dist[0] = 0

    total = 0

    for _ in range(n):
        v = -1

        for i in range(n):
            if not used[i] and dist[i] < INF:
                if v == -1 or dist[i] < dist[v]:
                    v = i

        if v == -1:
            return INF

        used[v] = True
        total += dist[v]

        for to in range(n):
            if used[to]:
                continue

            if ((mask >> v) & 1) == 0 and ((mask >> to) & 1) == 0:
                continue

            w = g[v][to]
            if w < dist[to]:
                dist[to] = w

    return total

def solve():
    n, c = map(int, input().split())

    g = [[INF] * n for _ in range(n)]

    for i in range(n):
        row = list(map(int, input().split()))
        for j in range(n):
            if i == j:
                g[i][j] = INF
            elif row[j] != 0:
                g[i][j] = row[j]

    ans = INF

    for mask in range(1 << n):
        mst_cost = prim(mask, n, g)
        if mst_cost == INF:
            continue

        cur = mst_cost + c * mask.bit_count()
        if cur < ans:
            ans = cur

    print(ans)

solve()
```

The implementation follows the proof almost literally.

The function `prim` computes the MST weight inside the restricted graph corresponding to a mask. Instead of explicitly building a new graph for every subset, it checks the restriction during relaxation. An edge is usable if at least one endpoint belongs to the mask.

Returning `INF` when no unvisited reachable vertex exists is important. That is how we detect that the restricted graph is disconnected.

The graph uses `INF` for nonexistent edges. This lets Prim ignore them naturally because such values never improve a distance.

The expression

```
((mask >> v) & 1) == 0 and ((mask >> to) & 1) == 0
```

checks whether both endpoints lie outside the candidate vertex cover. Such edges are forbidden and skipped.

Python's `bit_count()` gives the size of the subset, which corresponds exactly to the vertex-cover penalty.

One subtle point is that the empty mask is allowed. It simply means no vertex is selected. Usually the restricted graph becomes disconnected, but in very small graphs it is still valid to test it uniformly.

## Worked Examples

### Sample 1

Input:

```
4 10
0 1 8 0
1 0 1 0
8 1 0 2
0 0 2 0
```

The optimal mask is `{3}` in 1-based indexing.

| Step | Mask | Allowed MST Weight | Cover Size | Total Cost |
| --- | --- | --- | --- | --- |
| 1 | {3} | 11 | 1 | 21 |
| 2 | {2,3} | 4 | 2 | 24 |
| 3 | {1,2,3} | 4 | 3 | 34 |

The minimum value is 21.

The corresponding tree uses edges $(1,3)$, $(2,3)$, $(3,4)$. Every edge touches vertex 3, so the chosen cover has size 1. The matching penalty becomes much smaller than in the path-shaped MST.

### Sample 2

Input:

```
4 5
0 1 8 0
1 0 1 0
8 1 0 2
0 0 2 0
```

| Step | Mask | Allowed MST Weight | Cover Size | Total Cost |
| --- | --- | --- | --- | --- |
| 1 | {3} | 11 | 1 | 16 |
| 2 | {2,3} | 4 | 2 | 14 |
| 3 | {1,2,3} | 4 | 3 | 19 |

Now the penalty coefficient is smaller, so paying for a larger matching becomes worthwhile.

The optimal answer is 14, achieved by the path $1-2-3-4$.

This example demonstrates the tradeoff. Sometimes we spend extra matching penalty to obtain a much cheaper tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^n n^2)$ | Enumerate all masks and run Prim in $O(n^2)$ |
| Space | $O(n^2)$ | Store the graph matrix |

With $n=20$, there are $2^{20}=1,048,576$ masks. The graph itself is tiny. The intended solution relies on the small vertex count and fits comfortably within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    INF = 10 ** 18

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, c = map(int, input().split())

    g = [[INF] * n for _ in range(n)]

    for i in range(n):
        row = list(map(int, input().split()))
        for j in range(n):
            if i != j and row[j] != 0:
                g[i][j] = row[j]

    def prim(mask):
        dist = [INF] * n
        used = [False] * n
        dist[0] = 0

        total = 0

        for _ in range(n):
            v = -1

            for i in range(n):
                if not used[i] and dist[i] < INF:
                    if v == -1 or dist[i] < dist[v]:
                        v = i

            if v == -1:
                return INF

            used[v] = True
            total += dist[v]

            for to in range(n):
                if used[to]:
                    continue

                if ((mask >> v) & 1) == 0 and ((mask >> to) & 1) == 0:
                    continue

                if g[v][to] < dist[to]:
                    dist[to] = g[v][to]

        return total

    ans = INF

    for mask in range(1 << n):
        cur = prim(mask)
        if cur != INF:
            ans = min(ans, cur + c * mask.bit_count())

    return str(ans) + "\n"

# provided samples
assert run(
"""4 10
0 1 8 0
1 0 1 0
8 1 0 2
0 0 2 0
"""
) == "21\n", "sample 1"

assert run(
"""4 5
0 1 8 0
1 0 1 0
8 1 0 2
0 0 2 0
"""
) == "14\n", "sample 2"

# minimum size
assert run(
"""2 7
0 3
3 0
"""
) == "10\n", "n = 2"

# star graph, matching size should be 1
assert run(
"""4 100
0 1 1 1
1 0 0 0
1 0 0 0
1 0 0 0
"""
) == "103\n", "star structure"

# all equal weights
assert run(
"""3 5
0 2 2
2 0 2
2 2 0
"""
) == "9\n", "all equal weights"

# path graph
assert run(
"""4 1
0 1 0 0
1 0 1 0
0 1 0 1
0 0 1 0
"""
) == "5\n", "matching size 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 vertices, one edge | 10 | Smallest legal graph |
| Star graph | 103 | Maximum matching equals 1 |
| All weights equal | 9 | Symmetric choices |
| Simple path | 5 | Matching size reaches 2 |
| Official samples | 21, 14 | Correctness against statement examples |

## Edge Cases

Consider the star graph:

```
4 100
0 1 1 1
1 0 0 0
1 0 0 0
1 0 0 0
```

A common mistake is to assume the matching penalty grows with the degree of the center. In reality every edge shares the same vertex, so only one edge can belong to a matching.

The algorithm handles this through the vertex-cover formulation. Choosing the center alone as the cover gives mask size 1. The restricted graph already contains all tree edges, so Prim returns weight 3 and the answer becomes

$$3 + 1\cdot100 = 103.$$

Now consider the path:

```
4 100
0 1 0 0
1 0 1 0
0 1 0 1
0 0 1 0
```

The maximum matching size is 2. The minimum vertex cover also has size 2, namely vertices 2 and 3.

When the algorithm enumerates that mask, every path edge is allowed. Prim obtains tree weight 3, producing

$$3 + 2\cdot100 = 203.$$

No mask of size 1 can cover all three edges, so the algorithm correctly rejects the impossible assumption that the matching penalty could be 100.

Finally, consider a mask that disconnects the graph.

```
4 1
0 1 1 1
1 0 1 1
1 1 0 1
1 1 1 0
```

Take mask `{1}`.

Edges between vertices `{2,3,4}` are forbidden because neither endpoint belongs to the cover. The restricted graph becomes a star centered at vertex 1, which is still connected.

If we instead take the empty mask, every edge becomes forbidden. Prim cannot reach all vertices and returns `INF`. The algorithm discards that subset automatically.

This connectivity check is essential. Many masks do not correspond to any valid spanning tree, and treating them as valid would produce incorrect answers.
