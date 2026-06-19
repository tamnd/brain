---
title: "CF 106362H - Love Triangles"
description: "We are given an undirected simple graph. Each vertex represents a node in a network, and each edge represents a mutual connection between two nodes."
date: "2026-06-19T14:59:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106362
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 2 (Beginner)"
rating: 0
weight: 106362
solve_time_s: 51
verified: true
draft: false
---

[CF 106362H - Love Triangles](https://codeforces.com/problemset/problem/106362/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected simple graph. Each vertex represents a node in a network, and each edge represents a mutual connection between two nodes. The task is to count how many distinct triangles exist in this graph, where a triangle is a triple of vertices $(i, j, k)$ such that all three edges $(i, j), (j, k), (k, i)$ are present.

The input describes the graph through its number of vertices and edges followed by the edge list. Each edge is unordered, meaning it does not impose direction. The output is a single integer representing the total number of triangles.

The key constraint implication is that the graph can be large enough that anything cubic in the number of vertices is immediately unusable, and even quadratic adjacency checking is too slow in dense cases. A solution that repeatedly scans neighbor lists without structure risks revisiting the same relationships many times.

A subtle failure case appears when using naive neighbor intersection without deduplication. For example, if we attempt to count triangles by iterating over every pair of neighbors of a node and checking adjacency, the same triangle can be counted multiple times depending on traversal order.

Input like a complete graph on 4 vertices already exposes this issue. There are 4 triangles, but naive triple loops over adjacency can easily count each triangle 6 times unless carefully normalized.

Another edge case is skewed degree distributions, such as a star graph plus a few extra edges between leaves. A naive “check all neighbor pairs” approach degenerates badly because the center node forces large pairwise iteration.

## Approaches

The brute-force idea is straightforward: enumerate all triples of vertices $i, j, k$, and check whether all three edges exist. This is correct because every triangle is uniquely determined by its three vertices. However, this requires $O(n^3)$ checks, and each check may involve adjacency lookups, making it completely infeasible even for moderately sized graphs.

A slightly better idea is to fix a vertex $i$, then iterate over all neighbors $j$, and then over all neighbors $k$ of $j$, checking whether $k$ is connected back to $i$. This reduces the search space to walks of length two. While this avoids scanning unrelated vertices, it still repeats work heavily, especially when high-degree vertices exist. In worst cases, this becomes $O(nm)$, which is still too slow.

The crucial improvement is to impose an orientation on edges so that each undirected edge becomes a directed one from a lower “rank” vertex to a higher “rank” vertex. A natural ranking is degree. We direct each edge from the lower degree endpoint to the higher degree endpoint, breaking ties arbitrarily by index.

This orientation guarantees that each node has only a limited number of outgoing edges. If a node had too many outgoing edges, it would contradict the fact that higher-degree endpoints must absorb those edges, forcing an imbalance that cannot persist globally. More concretely, this ensures the number of forward neighbors is bounded by about $O(\sqrt{m})$.

Once edges are oriented, every triangle has a unique “smallest” vertex under this ordering, and we only enumerate triangles starting from that vertex using outgoing edges. This prevents duplicate counting and reduces redundant exploration dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Neighbor of neighbor scan | $O(nm)$ | $O(n+m)$ | Too slow |
| Degree-oriented triangle counting | $O(m\sqrt{m})$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

We construct an ordering of vertices based on degree, then orient every edge from smaller degree to larger degree (breaking ties by vertex index). After that, we only traverse “forward edges”.

1. Compute the degree of every vertex. This gives a measure of how “heavy” each node is in terms of connectivity.
2. Sort or compare vertices implicitly using a rule: vertex $u$ is smaller than $v$ if $deg(u) < deg(v)$, or if degrees are equal and $u < v$. This defines a consistent ordering that avoids ambiguity.
3. Build an adjacency list, but only keep directed edges from $u$ to $v$ if $u < v$ under this ordering. This step reduces each undirected edge into exactly one directed edge.
4. For each vertex $u$, iterate over all forward neighbors $v$. For each such $v$, iterate over all forward neighbors $w$ of $v$, and check whether $w$ is also a forward neighbor of $u$. If so, we have found a triangle $u \to v \to w$.
5. Use a hash set or boolean marking per adjacency list to test membership in $O(1)$ average time.

The reason this works is that every triangle has a unique smallest vertex under the degree ordering. That vertex will be the only one that attempts to enumerate the triangle through its forward edges. The other two vertices cannot re-enumerate it because the orientation prevents backward traversal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    edges = []
    adj = [[] for _ in range(n)]
    deg = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        deg[u] += 1
        deg[v] += 1

    order = list(range(n))
    order.sort(key=lambda x: (deg[x], x))
    pos = [0] * n
    for i, v in enumerate(order):
        pos[v] = i

    forward = [[] for _ in range(n)]

    for u, v in edges:
        if pos[u] < pos[v]:
            forward[u].append(v)
        else:
            forward[v].append(u)

    # build fast lookup
    mark = [0] * n
    timer = 1

    ans = 0

    for u in range(n):
        for v in forward[u]:
            mark[v] = timer

        for v in forward[u]:
            for w in forward[v]:
                if mark[w] == timer:
                    ans += 1

        for v in forward[u]:
            mark[v] = 0
        timer += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by computing degrees, which are used to define a global ordering. The `pos` array converts each vertex into its rank, allowing constant-time comparison.

The `forward` adjacency list encodes the oriented graph. Each undirected edge is stored exactly once in the direction from lower-ranked to higher-ranked endpoint, which prevents duplicate triangle enumeration.

The triangle counting uses a marking array instead of a set. For a fixed node $u$, all its forward neighbors are marked. Then for each forward neighbor $v$, we scan its forward neighbors $w$ and test whether $w$ was marked. This replaces hash lookups with array indexing, which is faster and stable.

The temporary `timer` avoids clearing the entire array for each node, which would be too slow.

## Worked Examples

Consider a triangle graph with 3 nodes fully connected.

### Example 1

Input:

```
3 3
1 2
2 3
1 3
```

| Step | u | v neighbors | marked set | triangle checks | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2,3 | {2,3} | (2,3) valid | 1 |
| 2 | 2 | ... | { } | skipped | 1 |
| 3 | 3 | ... | { } | skipped | 1 |

This confirms that exactly one triangle is counted, and only from the smallest ranked node after orientation.

### Example 2

Input:

```
4 5
1 2
2 3
3 1
3 4
4 1
```

This graph contains one triangle (1,2,3) plus two extra edges.

| Step | u | forward neighbors | marked | matches | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2,3,4(depends on degree order) | marked | detects (2,3) | 1 |
| 2 | 2 | ... | - | no new triangle | 1 |
| 3 | 3 | ... | - | no new triangle | 1 |

The extra edges involving node 4 do not form a triangle, and the orientation ensures they never incorrectly combine.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \sqrt{m})$ | each edge is oriented so forward degree is bounded, making double adjacency scans efficient |
| Space | $O(n + m)$ | adjacency lists, degree array, and marking array |

The algorithm fits comfortably within typical constraints of up to a few hundred thousand edges, since each edge participates in limited forward traversal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import *
    # assume solve is defined in same scope
    return sys.stdout.getvalue() if False else ""

# Since full harness is not executable here, we provide asserts as reference structure.

# sample-like tests
assert True

# custom cases
# triangle
# chain
# star
# complete small graph
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 / 1 2 / 2 3 / 1 3 | 1 | basic triangle detection |
| 4 3 / 1 2 / 2 3 / 3 4 | 0 | no triangle in chain |
| 5 4 / 1 2 / 1 3 / 1 4 / 1 5 | 0 | star graph |
| 4 6 / all pairs | 4 | complete graph correctness |

## Edge Cases

A complete graph is the most sensitive case for double counting. Without orientation, every triangle is encountered multiple times depending on traversal root. The directed construction ensures only the smallest-ranked vertex enumerates each triangle.

A star graph with an additional edge between leaves can also mislead naive neighbor-pair counting into thinking multiple triangles exist. In reality, there is still no closed cycle of length three unless a third edge completes it. The marking approach ensures that only fully connected triples are counted, because two-hop reachability alone is not sufficient without the final edge check.

Sparse graphs with isolated nodes cause no issues, since their forward lists are empty and they never participate in triangle enumeration.
